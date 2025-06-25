import os
import json
import hashlib
import time
from typing import Any, Dict, Optional
from web3 import Web3
from eth_account.messages import encode_defunct


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
        private_key: Optional[str] = None,
        storage_dir: str = "./blockchain_storage",
    ):
        """
        Initialize the blockchain tracer.

        Args:
            provider_url: URL of the blockchain provider (e.g., Infura, Alchemy). Optional.
            private_key: Private key for signing transactions (optional)
            storage_dir: Directory to store files (models, data, etc.)
        """
        self._blockchain_data = {}
        if provider_url:
            self.web3 = Web3(Web3.HTTPProvider(provider_url))
        else:
            self.web3 = None
        self.private_key = private_key
        self.account = (
            self.web3.eth.account.from_key(private_key) if (self.web3 and private_key) else None
        )

        # Set up storage directory
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

    def compute_hash(self, data: Any) -> str:
        """
        Compute a hash of the provided data.

        Args:
            data: Any data that can be serialized to JSON or a file path

        Returns:
            str: SHA-256 hash of the data
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
        self,
        file_paths: Optional[Dict[str, str]] = None,
        **kwargs
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
                self._blockchain_data['file_hashes'][key] = {
                    'path': path,
                    'hash': self.compute_hash(path)
                }

        return self._blockchain_data

    def write_to_blockchain(self, only_write_hash = False) -> Dict[str, Any]:
        """
        Write the current data to the blockchain.
        Must call update_data first to set the data to write.

        Returns:
            Dict containing transaction details and data hash
        """
        if not hasattr(self, '_blockchain_data'):
            raise ValueError("No data to write. Call update_data first.")

        if not self.account:
            raise ValueError("Private key required for recording data")

        # Prepare the data package
        if only_write_hash:
            data_hash = self.compute_hash(self._blockchain_data)
            data_package = data_hash
        else:
            data_package = self._blockchain_data

        # Sign the data package
        message = encode_defunct(text=json.dumps(data_package, sort_keys=True))
        signed_message = self.web3.eth.account.sign_message(
            message, private_key=self.private_key
        )

        # Store the data package on the blockchain by sending a transaction with the data in the input field
        serialized_data = json.dumps(data_package)

        # Create transaction
        tx = {
            "from": self.account.address,
            "to": self.account.address,  # Send to self
            "value": 0,
            "gas": 100000,  # Adjust as needed
            "gasPrice": self.web3.eth.gas_price,
            "nonce": self.web3.eth.get_transaction_count(self.account.address),
            "data": self.web3.to_hex(text=serialized_data),
        }

        # Sign and send transaction
        signed_tx = self.account.sign_transaction(tx)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)

        # Wait for transaction receipt
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)

        # Save data locally for easier retrieval
        local_file_path = os.path.join(self.storage_dir, f"{data_hash}.json")
        with open(local_file_path, "w") as f:
            json.dump(
                {
                    "data_package": data_package,
                    "signature": signed_message.signature.hex(),
                    "tx_hash": tx_hash.hex(),
                    "block_number": tx_receipt.blockNumber,
                    "block_timestamp": self.web3.eth.get_block(
                        tx_receipt.blockNumber
                    ).timestamp,
                },
                f,
            )

        result = {
            "success": tx_receipt.status == 1,
            "data_hash": data_hash,
            "data_package": data_package,
            "signature": signed_message.signature.hex(),
            "signed_by": self.account.address,
            "transaction_hash": tx_hash.hex(),
            "block_number": tx_receipt.blockNumber,
        }

        # Store the transaction hash in the blockchain data
        self._blockchain_data['transaction_hash'] = result['transaction_hash']

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
        receipt = self.web3.eth.get_transaction_receipt(tx_hash)

        # Try to decode the data
        data = {}
        if tx.input and tx.input != "0x":
            try:
                # Remove '0x' prefix and decode
                hex_data = tx.input[2:]
                decoded_data = bytes.fromhex(hex_data).decode("utf-8")
                data = json.loads(decoded_data)
            except (UnicodeDecodeError, json.JSONDecodeError):
                data = {"raw": tx.input}

        # Get block timestamp
        block_timestamp = self.web3.eth.get_block(tx.blockNumber).timestamp

        # Try to get local file data if it exists
        local_data = None
        if data.get("hash"):
            local_file_path = os.path.join(self.storage_dir, f"{data['hash']}.json")
            if os.path.exists(local_file_path):
                with open(local_file_path, "r") as f:
                    local_data = json.load(f)

        return {
            "transaction": {
                "hash": tx_hash,
                "block_number": tx.blockNumber,
                "block_timestamp": block_timestamp,
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
            "local_data": local_data
        }

    def get_data(self) -> dict:
        """
        Return a copy of the current blockchain data being traced.
        Returns None if no data has been initialized yet.
        """
        if hasattr(self, '_blockchain_data') and self._blockchain_data is not None:
            return self._blockchain_data.copy()
        return None



# Ver:
#  - reproducibility score
# opcion: se comparte un diccionario con  el cual se evalua en la blockchain si tiene 
# la metadata correcta, para luego usarla.
# de todas formas se [podria guardar el diccionario en la blockchain, 
# y solo compartir un hash para buscar el diccionario

# each affirmation done by computation must have available code that justifies.

# escribo en blockchain. mando. tendo hash.
# otro dia hago lo mismo. tengo otro hash.
# guardar en cada tx el hash de la tx anterior para seguir linea temporal.
# puede quedar automatizado por dentro, sin que el usuario que usa el paquete lo vea.
# a todo esto se puede hacer un getter que lea todas las tx y las imprima, para visualizar todo lo guardado
# a lo largo del tiempo

# como saber cual es la secuencia de escritura de un estudio? por los hashes y que siempre a las tx las haga el mismo address.
# en versiones futuras se puede ver que la escritura este permitida a varias personas, pero no es tema de ahora.

# si se quiere dar un unico hash, se puede utilizar el hash de la ultima tx.
# luego con operaciones de lectura a la blockchain se puede ver todo el historial de txs de un experimento.


# creo que esto ultimo responde esto:
# un hash final obtenido de todos los datos?
# linkear pasos secuenciales con hashes?

# el usuario que escribe en blockchain debe dar una lista de hashes? o hacer todo invocando una unica vez al metodo 'trace'?

# se pueden subir hashes de cualquier dato. imagenes, datasets, etc. si uno los almacena offchain, luego es cuestion de hashearlos para verificar
#  que el hash guardado es el relacionado con estos datos.

# datos que no se quieran publicos, se puede guardar solo el hash en blockchain, aunque no garantiza la persistencia.
# se puede ver que hay hoy en dia en el ecosistema para resolver esto.

#que agregar para rep de ML.
# ver standard ONNX. guardar hash de ONNX
# hash del codigo
# IPFS
# mostrarle al usuario que tiene que guardar para pasarle la data a un 3ro y que lo pueda reproducir
