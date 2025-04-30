import os
import json
import hashlib
import time
from typing import Any, Dict, Optional
from web3 import Web3
from eth_account.messages import encode_defunct

# Ver:
#  - reproducibility score
# opcion: se comparte un diccionario con  el cual se evalua en la blockchain si tiene 
# la metadata correcta, para luego usarla.
# de todas formas se [podria guardar el diccionario en la blockchain, 
# y solo compartir un hash para buscar el diccionario



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
# ver standard ONNX
# hash del codigo
# IPFS


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
        provider_url: str,
        private_key: Optional[str] = None,
        storage_dir: str = "./blockchain_storage",
    ):
        """
        Initialize the blockchain tracer.

        Args:
            provider_url: URL of the blockchain provider (e.g., Infura, Alchemy)
            private_key: Private key for signing transactions (optional)
            storage_dir: Directory to store files (models, data, etc.)
        """
        self.web3 = Web3(Web3.HTTPProvider(provider_url))
        self.private_key = private_key
        self.account = (
            self.web3.eth.account.from_key(private_key) if private_key else None
        )

        # Set up storage directory
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

    def compute_hash(self, data: Any) -> str:
        """
        Compute a hash of the provided data.

        Args:
            data: Any data that can be serialized to JSON

        Returns:
            str: SHA-256 hash of the data
        """
        if isinstance(data, bytes):
            return hashlib.sha256(data).hexdigest()
        else:
            serialized = json.dumps(data, sort_keys=True)
            return hashlib.sha256(serialized.encode()).hexdigest()

    def trace(
        self, data: Any, data_type: str, metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Record data on the blockchain with a specific type.

        Args:
            data: The data to record (will be hashed)
            data_type: Type of data (e.g., 'ml_model', 'scientific_study', 'donation', 'green_h2')
            metadata: Additional metadata about the data

        Returns:
            Dict containing transaction details and data hash
        """
        if not self.account:
            raise ValueError("Private key required for recording data")

        # Prepare the data package
        timestamp = int(time.time())
        data_hash = self.compute_hash(data)

        data_package = {
            "hash": data_hash,
            "type": data_type,
            "timestamp": timestamp,
            "metadata": metadata or {},
            "recorder": self.account.address,
        }

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

        return {
            "success": tx_receipt.status == 1,
            "data_hash": data_hash,
            "data_package": data_package,
            "signature": signed_message.signature.hex(),
            "signed_by": self.account.address,
            "transaction_hash": tx_hash.hex(),
            "block_number": tx_receipt.blockNumber,
        }

    def verify_data(
        self, original_data: Any, blockchain_record: Dict[str, Any]
    ) -> bool:
        """
        Verify that data matches what was recorded on the blockchain.

        Args:
            original_data: The original data to verify
            blockchain_record: The record returned from trace

        Returns:
            bool: True if the data matches the blockchain record
        """
        computed_hash = self.compute_hash(original_data)
        return computed_hash == blockchain_record.get("data_hash")

    # Retrieve a record by tx hash from blockchain.
    def get_transaction_details(self, tx_hash: str) -> Dict[str, Any]:
        """
        Get details of a transaction by its hash.

        Args:
            tx_hash: Transaction hash

        Returns:
            Dict containing transaction details
        """
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

        return {
            "transaction": {
                "hash": tx_hash,
                "block_number": tx.blockNumber,
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

    def retrieve_record_by_hash(self, data_hash: str) -> Dict[str, Any]:
        """
        Retrieve a record by its data hash from local storage.

        Args:
            data_hash: The hash of the data to retrieve

        Returns:
            Dict containing the record details
        """
        local_file_path = os.path.join(self.storage_dir, f"{data_hash}.json")
        if not os.path.exists(local_file_path):
            raise FileNotFoundError(f"No record found for hash {data_hash}")

        with open(local_file_path, "r") as f:
            record = json.load(f)

        # Verify the record on the blockchain
        tx_hash = record.get("tx_hash")
        if tx_hash:
            tx_details = self.get_transaction_details(tx_hash)
            record["blockchain_verification"] = {
                "verified": tx_details["receipt"]["status"] == 1,
                "block_number": tx_details["transaction"]["block_number"],
                "timestamp": self.web3.eth.get_block(
                    tx_details["transaction"]["block_number"]
                ).timestamp,
            }

        return record

