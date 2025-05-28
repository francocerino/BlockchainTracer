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
                    'file_hashes': {},
                    'metrics': {},
                    'additional_info': {}
                }

            if model_config:
                self._current_experiment['model_config'] = model_config

            # Hash large files
            if model_path:
                self._current_experiment['file_hashes']['model'] = {
                    'path': model_path,
                    'hash': self.compute_hash(model_path)
                }

            if dataset_path:
                self._current_experiment['file_hashes']['dataset'] = {
                    'path': dataset_path,
                    'hash': self.compute_hash(dataset_path)
                }

            if metrics:
                self._current_experiment['metrics'] = metrics
            if additional_info:
                self._current_experiment['additional_info'] = additional_info

        return self._current_experiment

    def write_to_blockchain(self) -> Dict[str, Any]:
        """
        Write the current experiment data to the blockchain.
        Large file data is represented by their hashes, while configuration and metrics
        are written directly.

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

        # Prepare blockchain data
        blockchain_data = {
            'system_info': self._current_experiment['system_info'],
            'model_config': self._current_experiment['model_config'],
            'metrics': self._current_experiment['metrics'],
            'additional_info': self._current_experiment['additional_info'],
            'file_references': {
                file_type: {
                    'hash': file_info['hash'],
                    'original_path': file_info['path']
                }
                for file_type, file_info in self._current_experiment.get('file_hashes', {}).items()
            }
        }

        # Use the base class trace method
        result = self.trace(
            data=blockchain_data,
            data_type='ml_experiment',
            metadata={
                'framework': self._current_experiment.get('model_config', {}).get('framework', 'unknown'),
                'experiment_sequence': len(self._experiment_history)
            }
        )

        # Store the transaction hash in the current experiment
        self._current_experiment['transaction_hash'] = result['transaction_hash']

        return result

    def trace_experiment(self, 
                        model_config: Dict[str, Any],
                        model_path: str,
                        dataset_info: Dict[str, Any],
                        metrics: Dict[str, float],
                        additional_info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Trace an ML experiment by recording its configuration and results on the blockchain.
        
        Args:
            model_config: Model configuration including hyperparameters
            model_path: Path to the saved model file
            dataset_info: Information about the dataset used
            metrics: Model performance metrics
            additional_info: Any additional information to record
            
        Returns:
            Dict containing transaction details and data hash
        """
        # Prepare the experiment data
        experiment_data = {
            'system_info': self._get_system_info(),
            'model_config': model_config,
            'model_hash': self.compute_hash(model_path),
            'dataset_info': dataset_info,
            'metrics': metrics
        }
        
        if additional_info:
            experiment_data.update(additional_info)

        # Use the base class trace method with ML-specific type
        return self.trace(
            data=experiment_data,
            data_type='ml_experiment',
            metadata={
                'model_path': model_path,
                'framework': model_config.get('framework', 'unknown')
            }
        )

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

    def get_experiment(self, tx_hash: str) -> Dict[str, Any]:
        """
        Retrieve an ML experiment record by its transaction hash.
        
        Args:
            tx_hash: Transaction hash of the recorded experiment
            
        Returns:
            Dict containing the experiment information
        """
        return self.get_transaction_details(tx_hash) 