from typing import Dict, Any, Optional
import platform
import pkg_resources
import docker
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

    def _get_system_info(self) -> Dict[str, Any]:
        """Get system information including OS, Python version, and package versions."""
        system_info = {
            'os': platform.platform(),
            'python_version': platform.python_version(),
            'packages': {
                pkg.key: pkg.version for pkg in pkg_resources.working_set
            }
        }
        
        # Add Docker info if available
        try:
            docker_client = docker.from_env()
            system_info['docker'] = {
                'version': docker_client.version(),
                'info': docker_client.info()
            }
        except:
            system_info['docker'] = None
            
        return system_info

    def update_experiment(self,
                         experiment_data: Optional[Dict[str, Any]] = None,
                         model_config: Optional[Dict[str, Any]] = None,
                         model_path: Optional[str] = None,
                         dataset_path: Optional[str] = None,
                         metrics: Optional[Dict[str, float]] = None,
                         additional_info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Update the current experiment data without writing to blockchain.
        Large files (models, datasets) will be hashed, while configuration and metrics
        will be written directly to the blockchain.

        Args:
            experiment_data: Complete experiment data dict to replace current data
            model_config: Model configuration including hyperparameters (written to blockchain)
            model_path: Path to the model file (will be hashed)
            dataset_path: Path to the dataset file or directory (will be hashed)
            metrics: Model performance metrics (written to blockchain)
            additional_info: Any additional information to record (written to blockchain)

        Returns:
            Dict containing the current experiment data
        """
        if experiment_data:
            self._current_experiment = experiment_data
        else:
            if self._current_experiment is None:
                self._current_experiment = {
                    'system_info': self._get_system_info(),
                    'model_config': {},
                    'metrics': {},
                    'additional_info': {}
                }

            if model_config:
                self._current_experiment['model_config'] = model_config

            if metrics:
                self._current_experiment['metrics'] = metrics
            if additional_info:
                self._current_experiment['additional_info'] = additional_info

        # Update the base class's data
        file_paths = {}
        if model_path:
            file_paths['model'] = model_path
        if dataset_path:
            file_paths['dataset'] = dataset_path

        # Use the base class's update_data method
        base_data = self.update_data(
            data=self._current_experiment,
            data_type='ml_experiment',
            metadata={
                'framework': self._current_experiment.get('model_config', {}).get('framework', 'unknown'),
                'experiment_sequence': len(self._experiment_history)
            },
            file_paths=file_paths
        )

        # Update file hashes in current experiment
        self._current_experiment['file_hashes'] = base_data['file_hashes']

        return self._current_experiment

    def trace_experiment(self) -> Dict[str, Any]:
        """
        Write the current experiment data to the blockchain.
        Must call update_experiment first to set the experiment data.

        Returns:
            Dict containing transaction details and data hash
        """
        if self._current_experiment is None:
            raise ValueError("No experiment data to write. Call update_experiment first.")

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