from typing import Dict, Any, Optional
import platform
import importlib.metadata

# import docker
from datetime import datetime
from huggingface_hub import DatasetCardData, ModelCardData
import json

from blockchain_tracer import BlockchainTracer


class MLTracer(BlockchainTracer):
    """
    A specialized blockchain tracer for ML model experiments.
    Inherits from the base BlockchainTracer class to leverage its core functionality
    while adding ML-specific features.
    """

    def __init__(
        self,
        provider_url: Optional[str] = None,
        storage_dir: str = "./ml_tracer_storage",
    ):
        """
        Initialize the MLTracer with optional blockchain provider and storage directory.
        Sets up experiment tracking and card field introspection.
        Args:
            provider_url: Blockchain provider URL (optional)
            storage_dir: Directory to store files (models, data, etc.)
        Note:
            The private key is loaded exclusively from the BLOCKCHAIN_PRIVATE_KEY environment variable via the base class for security reasons.
        """
        super().__init__(provider_url, storage_dir)
        # self._blockchain_data = {} # check: heredado?
        self._experiment_history = []
        self._model_card_fields = self._get_card_fields(ModelCardData)
        self._data_card_fields = self._get_card_fields(DatasetCardData)
        self._model_card = None
        self._data_card = None

        self._blockchain_data["system_info"] = self._get_system_info()
        # self.update_model_card()  # Initialize _model_card and experiment state
        # self.update_data_card()   # Initialize _data_card and experiment state

    def _get_system_info(self) -> Dict[str, Any]:
        """
        Collect system information: OS, Python version, and all installed package versions.
        Used for experiment reproducibility and traceability.
        """
        system_info = {
            "os": platform.platform(),
            "python_version": platform.python_version(),
            "packages": {
                dist.metadata["Name"]: dist.version
                for dist in importlib.metadata.distributions()
            },
            "timestamp": int(datetime.now().timestamp()),
        }  # check: es mejor un requirements.txt?

        try:
            docker_client = docker.from_env()
            system_info["docker"] = {
                "version": docker_client.version(),
                "info": docker_client.info(),
            }
        except:
            # system_info['docker'] = None
            pass
        return system_info

    def _get_card_fields(self, card_class) -> Dict[str, Any]:
        """
        Introspect a Hugging Face card class to extract all public fields and their descriptions.
        Returns a dictionary mapping field names to descriptions.
        """
        card_instance = card_class()

        # Get all attributes that are not private or special methods
        fields = {}
        for attr_name in dir(card_instance):
            # Skip private attributes and methods
            if not attr_name.startswith("_") and not callable(
                getattr(card_instance, attr_name)
            ):
                # Get the attribute value
                attr_value = getattr(card_instance, attr_name)

                # Get the type hint if available
                type_hint = getattr(card_instance.__class__, "__annotations__", {}).get(
                    attr_name, type(attr_value).__name__
                )

                # Create a description based on the field name and type
                description = f"{attr_name.replace('_', ' ').title()} ({type_hint})"

                fields[attr_name] = description

        return fields

    @property
    def get_model_card(self) -> Optional[ModelCardData]:
        """
        Get the current Hugging Face ModelCardData object for this experiment.
        """
        return self._model_card

    @property
    def get_data_card(self) -> Optional[DatasetCardData]:
        """
        Get the current Hugging Face DatasetCardData object for this experiment.
        """
        return self._data_card

    @property
    def model_card_fields(self) -> Dict[str, str]:
        """
        Get all available model card fields and their descriptions.
        """
        return self._model_card_fields

    @property
    def data_card_fields(self) -> Dict[str, str]:
        """
        Get all available data card fields and their descriptions.
        """
        return self._data_card_fields

    def _update_card(self, card_obj, card_type, card_fields, kwargs):
        """
        Shared logic for updating either a model card or data card.
        Updates the card object, blockchain data, and returns a summary dict including all traced data.
        """
        for key, value in kwargs.items():
            setattr(card_obj, key, value)

        card_to_dict = {card_type: card_obj.to_dict()}

        self.update_data(**card_to_dict)

        """
        fields_status = {
            'filled': {k: v for k, v in card_obj.to_dict().items()},
            'available': {k: v for k, v in card_fields.items() if k not in card_obj.to_dict()},
            'descriptions': card_fields
        }
        
        print( {
            "fields_filled": list(fields_status['filled'].keys()),
            "fields_available": list(fields_status['available'].keys()),
            "experiment_data": self._blockchain_data.copy()
        })
        """

        return card_obj

    def update_model_card(self, **kwargs) -> dict:
        """
        Update or create the model card for this experiment.
        Accepts keyword arguments for model card fields.
        Returns a summary dict of the update.
        """
        if self._model_card is None:
            self._model_card = ModelCardData()
        if kwargs:
            card_obj = self._update_card(
                self._model_card, "model_card", self._model_card_fields, kwargs
            )
            self._model_card = card_obj
        else:
            raise ValueError("No keyword arguments provided to model card.")

        return self._blockchain_data.copy()

    def update_data_card(self, **kwargs) -> dict:
        """
        Update or create the data card for this experiment.
        Accepts keyword arguments for data card fields.
        Returns a summary dict of the update.
        """
        if self._data_card is None:
            self._data_card = DatasetCardData()

        if kwargs:
            card_obj = self._update_card(
                self._data_card,
                "data_card",
                self._data_card_fields,
                kwargs,
            )
            self._data_card = card_obj
        else:
            raise ValueError("No keyword arguments provided to data card.")

        return self._blockchain_data.copy()

    def trace_experiment(self) -> Dict[str, Any]:
        """
        Write the current experiment data (including model/data cards) to the blockchain.
        Returns transaction details and data hash.
        """
        if self._blockchain_data is None:
            raise ValueError(
                "No experiment data to write. Create or update a card first."
            )

        # Add to experiment history
        self._experiment_history.append(self._blockchain_data.copy())

        # If there are previous experiments, link them
        if len(self._experiment_history) > 1:
            previous_tx = self._experiment_history[-2].get("transaction_hash")
            if previous_tx:
                self._blockchain_data["previous_transaction"] = previous_tx

        # Write to blockchain using base class method
        result = super().write_to_blockchain()

        # Store the transaction hash in the experiment data
        self._blockchain_data["transaction_hash"] = result["transaction_hash"]

        return result

    def get_experiment(self, tx_hash: str) -> Dict[str, Any]:
        """
        Retrieve an ML experiment record by its transaction hash.

        Args:
            tx_hash: Transaction hash of the recorded experiment

        Returns:
            Dict containing the experiment information including blockchain data and local file data
        """
        tx_details = self.get_transaction_details(tx_hash)

        # Extract experiment data from transaction data
        if tx_details.get("local_data"):
            # If we have local data, use it for complete experiment info
            return {
                "experiment_data": tx_details["transaction"]["data"].get("data", {}),
                "metadata": tx_details["transaction"]["data"].get("metadata", {}),
                "file_references": tx_details["transaction"]["data"].get(
                    "file_references", {}
                ),
                "blockchain_info": {
                    "transaction_hash": tx_hash,
                    "block_number": tx_details["transaction"]["block_number"],
                    "timestamp": tx_details["transaction"]["block_timestamp"],
                    "recorder": tx_details["transaction"]["from"],
                },
                "local_data": tx_details["local_data"],
            }
        else:
            # If no local data, return just the blockchain data
            return {
                "experiment_data": tx_details["transaction"]["data"].get("data", {}),
                "metadata": tx_details["transaction"]["data"].get("metadata", {}),
                "blockchain_info": {
                    "transaction_hash": tx_hash,
                    "block_number": tx_details["transaction"]["block_number"],
                    "timestamp": tx_details["transaction"]["block_timestamp"],
                    "recorder": tx_details["transaction"]["from"],
                },
            }
