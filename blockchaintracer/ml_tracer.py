from typing import Dict, Any, Optional
import platform
import pkg_resources
import docker
from datetime import datetime
from huggingface_hub import DatasetCardData, ModelCardData
from .base import BlockchainTracer

class MLTracer(BlockchainTracer):
    """
    A specialized blockchain tracer for ML model experiments.
    Inherits from the base BlockchainTracer class to leverage its core functionality
    while adding ML-specific features.
    """

    def __init__(self, provider_url: str, private_key: Optional[str] = None, storage_dir: str = "./blockchain_storage"):
        super().__init__(provider_url, private_key, storage_dir)
        self._current_experiment = None
        self._experiment_history = []
        self._model_card = None
        self._data_card = None
        self._model_card_fields = self._get_card_fields(ModelCardData)
        self._data_card_fields = self._get_card_fields(DatasetCardData)

    def _get_system_info(self) -> Dict[str, Any]:
        """Get system information including OS, Python version, and package versions."""
        system_info = {
            'os': platform.platform(),
            'python_version': platform.python_version(),
            'packages': {
                pkg.key: pkg.version for pkg in pkg_resources.working_set
            }
        }
        
        try:
            docker_client = docker.from_env()
            system_info['docker'] = {
                'version': docker_client.version(),
                'info': docker_client.info()
            }
        except:
            system_info['docker'] = None
            
        return system_info

    def _get_card_fields(self, card_class) -> Dict[str, Any]:
        """
        Extract fields and their descriptions from a Hugging Face card class using introspection.
        """
        # Create an instance to get default values
        card_instance = card_class()
        
        # Get all attributes that are not private or special methods
        fields = {}
        for attr_name in dir(card_instance):
            # Skip private attributes and methods
            if not attr_name.startswith('_') and not callable(getattr(card_instance, attr_name)):
                # Get the attribute value
                attr_value = getattr(card_instance, attr_name)
                
                # Get the type hint if available
                type_hint = getattr(card_instance.__class__, '__annotations__', {}).get(attr_name, type(attr_value).__name__)
                
                # Create a description based on the field name and type
                description = f"{attr_name.replace('_', ' ').title()} ({type_hint})"
                
                fields[attr_name] = description
        
        return fields

    @property
    def model_card(self) -> Optional[ModelCardData]:
        """Get the current model card."""
        return self._model_card

    @property
    def data_card(self) -> Optional[DatasetCardData]:
        """Get the current data card."""
        return self._data_card

    @property
    def model_card_fields(self) -> Dict[str, str]:
        """Get all available model card fields with their descriptions."""
        return self._model_card_fields

    @property
    def data_card_fields(self) -> Dict[str, str]:
        """Get all available data card fields with their descriptions."""
        return self._data_card_fields

    def model_card(self, **kwargs) -> Dict[str, Any]:
        """
        Create or update a Model Card using Hugging Face's ModelCardData format.
        https://huggingface.co/docs/hub/model-cards
        """
        if self._model_card is None:
            self._model_card = ModelCardData()

        for key, value in kwargs.items():
            setattr(self._model_card, key, value)

        # Create visualization of fields
        fields_status = {
            'filled': {k: v for k, v in self._model_card.to_dict().items()},
            'available': {k: v for k, v in self._model_card_fields.items() if k not in self._model_card.to_dict()},
            'descriptions': self._model_card_fields
        }

        # Initialize experiment if needed
        if self._current_experiment is None:
            self._current_experiment = {
                'system_info': self._get_system_info(),
                'model_config': {},
                'metrics': {},
                'additional_info': {}
            }

        # Update experiment with model card
        self._current_experiment['model_card'] = self._model_card.to_dict()

        # Update the base class's data
        base_data = self.update_data(
            data=self._current_experiment,
            data_type='ml_experiment',
            metadata={
                'framework': self._current_experiment.get('model_config', {}).get('framework', 'unknown'),
                'experiment_sequence': len(self._experiment_history)
            }
        )

        # Update file hashes in current experiment
        self._current_experiment['file_hashes'] = base_data['file_hashes']

        return {
            "model_card": self._model_card.to_dict(),
            "system_info": self._get_system_info(),
            "timestamp": int(datetime.now().timestamp()),
            "fields_status": fields_status
        }

    def data_card(self, **kwargs) -> Dict[str, Any]:
        """
        Create or update a Data Card using Hugging Face's DatasetCardData format.
        https://huggingface.co/docs/hub/datasets-cards
        """
        if self._data_card is None:
            self._data_card = DatasetCardData()

        for key, value in kwargs.items():
            setattr(self._data_card, key, value)

        # Create visualization of fields
        fields_status = {
            'filled': {k: v for k, v in self._data_card.to_dict().items()},
            'available': {k: v for k, v in self._data_card_fields.items() if k not in self._data_card.to_dict()},
            'descriptions': self._data_card_fields
        }

        # Initialize experiment if needed
        if self._current_experiment is None:
            self._current_experiment = {
                'system_info': self._get_system_info(),
                'model_config': {},
                'metrics': {},
                'additional_info': {}
            }

        # Update experiment with data card
        self._current_experiment['data_card'] = self._data_card.to_dict()

        # Update the base class's data
        base_data = self.update_data(
            data=self._current_experiment,
            data_type='ml_experiment',
            metadata={
                'framework': self._current_experiment.get('model_config', {}).get('framework', 'unknown'),
                'experiment_sequence': len(self._experiment_history)
            }
        )

        # Update file hashes in current experiment
        self._current_experiment['file_hashes'] = base_data['file_hashes']

        return {
            "data_card": self._data_card.to_dict(),
            "system_info": self._get_system_info(),
            "timestamp": int(datetime.now().timestamp()),
            "fields_status": fields_status
        }

    def trace_experiment(self) -> Dict[str, Any]:
        """
        Write the current experiment data to the blockchain.
        Must have created or updated at least one card (model or data) first.

        Returns:
            Dict containing transaction details and data hash
        """
        if self._current_experiment is None:
            raise ValueError("No experiment data to write. Create or update a card first.")

        # Add to experiment history
        self._experiment_history.append(self._current_experiment.copy())

        # If there are previous experiments, link them
        if len(self._experiment_history) > 1:
            previous_tx = self._experiment_history[-2].get('transaction_hash')
            if previous_tx:
                self._current_experiment['previous_transaction'] = previous_tx

        # Write to blockchain using base class method
        result = super().write_to_blockchain()

        # Store the transaction hash in the experiment data
        self._current_experiment['transaction_hash'] = result['transaction_hash']

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
        if tx_details.get('local_data'):
            # If we have local data, use it for complete experiment info
            return {
                'experiment_data': tx_details['transaction']['data'].get('data', {}),
                'metadata': tx_details['transaction']['data'].get('metadata', {}),
                'file_references': tx_details['transaction']['data'].get('file_references', {}),
                'blockchain_info': {
                    'transaction_hash': tx_hash,
                    'block_number': tx_details['transaction']['block_number'],
                    'timestamp': tx_details['transaction']['block_timestamp'],
                    'recorder': tx_details['transaction']['from']
                },
                'local_data': tx_details['local_data']
            }
        else:
            # If no local data, return just the blockchain data
            return {
                'experiment_data': tx_details['transaction']['data'].get('data', {}),
                'metadata': tx_details['transaction']['data'].get('metadata', {}),
                'blockchain_info': {
                    'transaction_hash': tx_hash,
                    'block_number': tx_details['transaction']['block_number'],
                    'timestamp': tx_details['transaction']['block_timestamp'],
                    'recorder': tx_details['transaction']['from']
                }
            }

    def verify_experiment(self, 
                         original_data: Dict[str, Any], 
                         tx_hash: str) -> Dict[str, Any]:
        """
        Verify an ML experiment record on the blockchain.
        
        Args:
            original_data: The original experiment data to verify
            tx_hash: Transaction hash of the recorded experiment
            
        Returns:
            Dict containing verification results
        """
        # Get the blockchain record
        tx_details = self.get_transaction_details(tx_hash)
        
        # Verify the data matches
        is_valid = self.verify_data(original_data, tx_details)
        
        return {
            'is_valid': is_valid,
            'blockchain_record': tx_details,
            'verification_time': self.web3.eth.get_block('latest').timestamp
        } 