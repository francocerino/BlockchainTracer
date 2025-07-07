import os
import json
import hashlib
import time
from typing import Any, Dict, Optional
from web3 import Web3
from eth_account.messages import encode_defunct
import warnings


class BlockchainTracer:
    """
    A multipurpose blockchain tracer for recording and verifying sensitive information
    on EVM-compatible blockchains.

    Can be used for:
    - ML model reproducibility
    - Scientific studies
    - NGO donations
    - Green hydrogen traceability
    - Other traceability use cases
    """

    def __init__(
        self,
        provider_url: Optional[str] = None,
    ):
        """
        Initialize the blockchain tracer.

        Args:
            provider_url: URL of the blockchain provider (e.g., Infura, Alchemy). Optional.
        Note:
            The private key is loaded exclusively from the BLOCKCHAIN_PRIVATE_KEY environment variable for security reasons.
        """
        self._blockchain_data = {}
        self.web3 = None
        self.account = None
        self.__private_key = os.environ.get("BLOCKCHAIN_PRIVATE_KEY", None)
        if provider_url:
            self.web3 = Web3(Web3.HTTPProvider(provider_url))
            if self.__private_key:
                self.account = self.web3.eth.account.from_key(self.__private_key)
            else:
                warnings.warn(
                    "No private key provided. The tracer is in read-only mode.\n"
                    "For security, set the BLOCKCHAIN_PRIVATE_KEY environment variable in your shell before starting Jupyter or Python,\n"
                    "Never set your private key directly in a notebook."
                )  # or use a .env file with python-dotenv
        else:
            warnings.warn(
                "No provider_url specified. Blockchain operations (read/write) will not be available.\n"
                "Set the provider_url argument to connect to a blockchain node (e.g., Infura or Alchemy)."
            )

    def compute_hash(self, data: Any) -> str:
        """
        Compute a SHA-256 hash for the provided data.

        This function supports three main use cases:
        1. If `data` is a string and is a valid file path, it reads the file in chunks and computes the hash of its contents.
        2. If `data` is a bytes object, it computes the hash directly from those bytes.
        3. For any other type (e.g., dict, list, or string that is not a file path), it serializes the data to a JSON string
           (with sorted keys for consistency) and computes the hash of the resulting UTF-8 encoded string.

        This approach ensures generating a unique, reproducible hash for files, raw bytes, or structured data
        (like dicts or lists), which is useful for verifying data integrity or storing fingerprints on the blockchain.

        Args:
            data: The data to hash. Can be a file path (str), bytes, or any JSON-serializable object.

        Returns:
            str: The SHA-256 hash as a hexadecimal string.
        """
        if isinstance(data, str) and os.path.isfile(data):
            # If data is a file path, hash the file contents
            sha256_hash = hashlib.sha256()
            with open(data, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        elif isinstance(data, bytes):
            return hashlib.sha256(data).hexdigest()
        else:
            serialized = json.dumps(data, sort_keys=True)
            return hashlib.sha256(serialized.encode()).hexdigest()

    def update_data(
        self, file_paths: Optional[Dict[str, str]] = None, **kwargs
    ) -> Dict[str, Any]:
        """
        Update the current data that will be written to blockchain.
        This method allows accumulating data before writing it to the blockchain.

        Args:
            file_paths: Dictionary of file paths to hash, with keys as identifiers
            **kwargs: Arbitrary key-value pairs to add/update in the current data dict

        Returns:
            Dict containing the current data state
        """

        # Write all kwargs directly to the blockchain data dict
        for key, value in kwargs.items():
            self._blockchain_data[key] = value

        if file_paths:
            for key, path in file_paths.items():
                self._blockchain_data["file_hashes"][key] = {
                    #'path': path,
                    "hash": self.compute_hash(path)
                }

        return self._blockchain_data.copy()

    def write_to_blockchain(
        self,
        only_write_hash=False,
        save_locally=False,
        storage_dir: str = "./blockchain_storage",
    ) -> Dict[str, Any]:
        """
        Write the current data to the blockchain.
        Must call update_data first to set the data to write.

        Args:
            only_write_hash: If True, only the hash of the data is written to the blockchain.
            save_locally: If True, save the data package and signature locally.
            storage_dir: Optional directory to save local files.

        Returns:
            Dict containing transaction details and data hash
        """
        if self._blockchain_data is {}:
            raise ValueError("No data to write in blockchain.")

        if not self.account:
            raise ValueError("Private key required for recording data.")

        # Prepare the data package
        if only_write_hash:
            data_hash = self.compute_hash(self._blockchain_data)
            data_package = data_hash
        else:
            data_package = self._blockchain_data

        # Store the data package on the blockchain by sending a transaction with the data in the input field
        serialized_data = json.dumps(data_package)

        # Create transaction
        tx = {
            "from": self.account.address,
            "to": self.account.address,  # Send to self
            "value": 0,
            "gasPrice": self.web3.eth.gas_price,
            "nonce": self.web3.eth.get_transaction_count(self.account.address),
            "data": self.web3.to_hex(text=serialized_data),
            "chainId": self.web3.eth.chain_id,  # optional but recommended
        }
        default_gas = 100000  # initial guess of gas needed
        try:
            tx["gas"] = self.web3.eth.estimate_gas(tx)
        except Exception as e:
            warnings.warn(
                f"Gas estimation failed, using default gas = {default_gas}. Error: {e}"
            )
            tx["gas"] = default_gas

        try:
            # Sign and send transaction
            signed_tx = self.account.sign_transaction(tx)
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.raw_transaction)

            # Wait for transaction receipt
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        except Exception as e:
            raise RuntimeError(f"Transaction failed: {e}")

        ## Store the transaction hash in the blockchain data
        # self._blockchain_data['transaction_hash'] = tx_hash.hex()

        # Always compute the signature
        message = encode_defunct(text=json.dumps(data_package, sort_keys=True))
        signed_message = self.web3.eth.account.sign_message(
            message, private_key=self.__private_key
        )

        result = {
            "transaction_success": tx_receipt.status == 1,
            "data_package": data_package,
            "data_signature": signed_message.signature.hex(),
            "signed_by": self.account.address,
            "transaction_hash": tx_hash.hex(),
            "block_number": tx_receipt.blockNumber,
            "block_timestamp": self.web3.eth.get_block(
                tx_receipt.blockNumber
            ).timestamp,
            "tx_dict_to_sign": tx,
            "tx_receipt": tx_receipt,
        }

        if save_locally:
            # Use the provided storage_dir or default to self.storage_dir
            local_storage_dir = (
                storage_dir if storage_dir is not None else self.storage_dir
            )
            os.makedirs(local_storage_dir, exist_ok=True)
            local_file_path = os.path.join(local_storage_dir, f"{data_hash}.json")
            with open(local_file_path, "w") as f:
                json.dump(result, f)

        return result

    def get_transaction_details(self, tx_hash: str) -> Dict[str, Any]:
        """
        Get details of a transaction by its hash, including both blockchain data
        and local file data if available.

        Args:
            tx_hash: Transaction hash

        Returns:
            Dict containing transaction details and associated data
        """
        # Get blockchain transaction data
        tx = self.web3.eth.get_transaction(tx_hash)

        # Try to decode the data
        data = {}
        if tx.input and tx.input != "0x":
            try:
                hex_data = tx.input.hex()  # [2:]
                decoded_data = bytes.fromhex(hex_data).decode("utf-8")
                data = json.loads(decoded_data)
            except (UnicodeDecodeError, json.JSONDecodeError):
                # Try to show as UTF-8 string if possible
                try:
                    data = {"raw": bytes.fromhex(hex_data).decode("utf-8")}
                except Exception:
                    data = {"raw": tx.input}

        ## Try to get local file data if it exists
        # local_data = None
        # if data.get("hash"):
        #    local_file_path = os.path.join(self.storage_dir, f"{data['hash']}.json")
        #    if os.path.exists(local_file_path):
        #        with open(local_file_path, "r") as f:
        #            local_data = json.load(f)

        receipt = self.web3.eth.get_transaction_receipt(tx_hash)
        tx_data = {
            "transaction": {
                "hash": tx_hash,
                "block_number": tx.blockNumber,
                "block_timestamp": self.web3.eth.get_block(tx.blockNumber).timestamp,
                "from": tx["from"],
                "to": tx["to"],
                "value": self.web3.from_wei(tx.value, "ether"),
                "gas": tx.gas,
                "gas_price": self.web3.from_wei(tx.gasPrice, "gwei"),
                "data": data,
            },
            "receipt": {
                "status": receipt.status,
                "gas_used": receipt.gasUsed,
                "logs": [dict(log) for log in receipt.logs],
            },
        }

        return tx_data

    def get_data(self) -> dict:
        """
        Return a copy of the current blockchain data being traced.
        Returns None if no data has been initialized yet.
        """
        return self._blockchain_data.copy()
