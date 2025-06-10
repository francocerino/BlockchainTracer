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

# First update with initial research data
print("\nUpdating with initial research data...")
current_data = tracer.update_data(
    data={
        "title": "Blockchain in ML: A Survey",
        "authors": ["John Doe"]
    },
    data_type="research",
    metadata={"institution": "Example University"}
)
print("Current data state:")
print(json.dumps(current_data, indent=2))

# Later, update with more authors and keywords
print("\nUpdating with additional authors and keywords...")
current_data = tracer.update_data(
    data={
        "title": "Blockchain in ML: A Survey",
        "authors": ["John Doe", "Jane Smith"],
        "keywords": ["blockchain", "machine learning", "reproducibility"]
    },
    metadata={"institution": "Example University", "department": "Computer Science"}
)
print("Current data state:")
print(json.dumps(current_data, indent=2))

# Finally, write to blockchain
general_result = tracer.write_to_blockchain()
print(f"\nGeneral data traced. Transaction hash: {general_result['transaction_hash']}\n")

# Example 2: Using the specialized MLTracer
print("Example 2: Using MLTracer for ML experiments")
ml_tracer = MLTracer(
    provider_url=os.getenv('ETH_NETWORK_URL'),
    private_key=os.getenv('ETH_PRIVATE_KEY'),
    storage_dir="./ml_storage"
)

# Initial model configuration
print("\nStep 1: Setting up initial model configuration...")
model_config = {
    'framework': 'pytorch',
    'architecture': 'resnet18',
    'hyperparameters': {
        'learning_rate': 0.001,
        'batch_size': 32,
        'epochs': 10
    }
}

# Update with initial configuration
current_experiment = ml_tracer.update_experiment(
    model_config=model_config,
    additional_info={'stage': 'initialization'}
)
print("Current experiment state:")
print(json.dumps(current_experiment, indent=2))

# Save a mock model file
mock_model_path = 'mock_model.json'
with open(mock_model_path, 'w') as f:
    json.dump(model_config, f)

# Update with model file
print("\nStep 2: Adding model file...")
current_experiment = ml_tracer.update_experiment(
    model_path=mock_model_path
)
print("Current experiment state (showing file hashes):")
print(json.dumps(current_experiment.get('file_hashes', {}), indent=2))

# Update with dataset information
print("\nStep 3: Adding dataset information...")
dataset_info = {
    'name': 'CIFAR-10',
    'num_classes': 10,
    'train_samples': 50000,
    'test_samples': 10000,
    'input_shape': [3, 32, 32]
}
current_experiment = ml_tracer.update_experiment(
    additional_info={
        'stage': 'data_preparation',
        'dataset_info': dataset_info
    }
)

# Update with initial training metrics
print("\nStep 4: Adding initial training metrics...")
current_experiment = ml_tracer.update_experiment(
    metrics={
        'accuracy': 0.85,
        'precision': 0.84,
        'recall': 0.83,
    }
)
print("Current experiment state (metrics):")
print(json.dumps(current_experiment.get('metrics', {}), indent=2))

# Final update with improved metrics after tuning
print("\nStep 5: Updating with final metrics and reviewing complete state...")
current_experiment = ml_tracer.update_experiment(
    metrics={
        'accuracy': 0.92,
        'precision': 0.91,
        'recall': 0.90,
        'f1_score': 0.905
    },
    additional_info={
        'stage': 'completed',
        'dataset_info': dataset_info,
        'notes': 'Final results after hyperparameter tuning'
    }
)

print("\nFinal experiment state before writing to blockchain:")
print("1. Model Configuration:")
print(json.dumps(current_experiment.get('model_config', {}), indent=2))
print("\n2. Metrics:")
print(json.dumps(current_experiment.get('metrics', {}), indent=2))
print("\n3. Additional Info:")
print(json.dumps(current_experiment.get('additional_info', {}), indent=2))
print("\n4. File Hashes:")
print(json.dumps(current_experiment.get('file_hashes', {}), indent=2))

# Write final state to blockchain
ml_result = ml_tracer.trace_experiment()
print(f"\nML experiment traced. Transaction hash: {ml_result['transaction_hash']}")

# Retrieve and display the final experiment data
experiment = ml_tracer.get_experiment(ml_result['transaction_hash'])
print("\nRetrieved experiment data from blockchain:")
print(f"Model architecture: {experiment['experiment_data']['model_config']['architecture']}")
print(f"Final accuracy: {experiment['experiment_data']['metrics']['accuracy']}")
print(f"Stage: {experiment['experiment_data']['additional_info']['stage']}")
print(f"Block number: {experiment['blockchain_info']['block_number']}")

# Clean up
os.remove(mock_model_path)
print("\nExample completed. Check the storage directories for local copies of the traced data.")

# Example 3: Recovering data using transaction hashes
print("\nExample 3: Recovering previously traced data")
print("Note: Only provider URL is needed for reading data (no private key required)")

# Create new tracer instances for reading only (no private key needed)
readonly_tracer = BlockchainTracer(
    provider_url=os.getenv('ETH_NETWORK_URL'),
    storage_dir="./blockchain_storage"  # Optional: only needed if you want to access local files
)

readonly_ml_tracer = MLTracer(
    provider_url=os.getenv('ETH_NETWORK_URL'),
    storage_dir="./ml_storage"  # Optional: only needed if you want to access local files
)

# Recover general research data
print("\nRecovering general research data...")
research_data = readonly_tracer.get_transaction_details(general_result['transaction_hash'])
print("Retrieved research data:")
print(f"Title: {research_data['transaction']['data']['data'].get('title')}")
print(f"Authors: {research_data['transaction']['data']['data'].get('authors')}")
print(f"Keywords: {research_data['transaction']['data']['data'].get('keywords')}")
print(f"Recorded at block: {research_data['transaction']['block_number']}")

# Recover ML experiment data
print("\nRecovering ML experiment data...")
experiment_data = readonly_ml_tracer.get_experiment(ml_result['transaction_hash'])
print("Retrieved experiment data:")
print("\n1. Model Details:")
print(f"- Framework: {experiment_data['experiment_data']['model_config']['framework']}")
print(f"- Architecture: {experiment_data['experiment_data']['model_config']['architecture']}")
print(f"- Learning Rate: {experiment_data['experiment_data']['model_config']['hyperparameters']['learning_rate']}")

print("\n2. Performance Metrics:")
metrics = experiment_data['experiment_data']['metrics']
for metric, value in metrics.items():
    print(f"- {metric}: {value}")

print("\n3. Dataset Information:")
dataset = experiment_data['experiment_data']['additional_info']['dataset_info']
print(f"- Dataset: {dataset['name']}")
print(f"- Classes: {dataset['num_classes']}")
print(f"- Training samples: {dataset['train_samples']}")

print("\n4. Blockchain Information:")
print(f"- Transaction Hash: {experiment_data['blockchain_info']['transaction_hash']}")
print(f"- Block Number: {experiment_data['blockchain_info']['block_number']}")
print(f"- Timestamp: {experiment_data['blockchain_info']['timestamp']}")

# If there are file hashes, show how to verify them
if experiment_data['experiment_data'].get('file_hashes'):
    print("\n5. File References:")
    for file_type, file_info in experiment_data['experiment_data']['file_hashes'].items():
        print(f"- {file_type}:")
        print(f"  Original path: {file_info['path']}")
        print(f"  Hash: {file_info['hash']}")

print("\nNote: As demonstrated, you can read any traced data with just:")
print("1. The transaction hash")
print("2. A blockchain provider URL (e.g., Infura, Alchemy)")
print("No private key or special permissions needed for reading data!") 