from blockchaintracer import BlockchainTracer, MLTracer
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Example 1: Using the general-purpose BlockchainTracer
print("Example 1: Using BlockchainTracer for general data")
tracer = BlockchainTracer(
    provider_url=os.getenv('ETH_NETWORK_URL'),
    private_key=os.getenv('ETH_PRIVATE_KEY'),
    storage_dir="./blockchain_storage"
)

# Trace some general data
general_data = {
    "type": "research_paper",
    "title": "Blockchain in ML: A Survey",
    "authors": ["John Doe", "Jane Smith"],
    "keywords": ["blockchain", "machine learning", "reproducibility"]
}

general_result = tracer.trace(
    data=general_data,
    data_type="research",
    metadata={"institution": "Example University"}
)

print(f"General data traced. Transaction hash: {general_result['transaction_hash']}\n")

# Example 2: Using the specialized MLTracer
print("Example 2: Using MLTracer for ML experiments")
ml_tracer = MLTracer(
    provider_url=os.getenv('ETH_NETWORK_URL'),
    private_key=os.getenv('ETH_PRIVATE_KEY'),
    storage_dir="./ml_storage"
)

# Prepare ML experiment data
model_config = {
    'framework': 'pytorch',
    'architecture': 'resnet18',
    'hyperparameters': {
        'learning_rate': 0.001,
        'batch_size': 32,
        'epochs': 10
    }
}

# Save a mock model file
mock_model_path = 'mock_model.json'
with open(mock_model_path, 'w') as f:
    json.dump(model_config, f)

# Dataset information
dataset_info = {
    'name': 'CIFAR-10',
    'num_classes': 10,
    'train_samples': 50000,
    'test_samples': 10000,
    'input_shape': [3, 32, 32]
}

# Metrics
metrics = {
    'accuracy': 0.92,
    'precision': 0.91,
    'recall': 0.90,
    'f1_score': 0.905
}

# Trace the ML experiment
ml_result = ml_tracer.trace_experiment(
    model_config=model_config,
    model_path=mock_model_path,
    dataset_info=dataset_info,
    metrics=metrics,
    additional_info={'notes': 'Image classification experiment'}
)

print(f"ML experiment traced. Transaction hash: {ml_result['transaction_hash']}")

# Verify the experiment
verification = ml_tracer.verify_experiment(
    original_data={
        'model_config': model_config,
        'dataset_info': dataset_info,
        'metrics': metrics
    },
    tx_hash=ml_result['transaction_hash']
)

print("\nVerification result:", verification['is_valid'])

# Clean up
os.remove(mock_model_path)
print("\nExample completed. Check the storage directories for local copies of the traced data.") 