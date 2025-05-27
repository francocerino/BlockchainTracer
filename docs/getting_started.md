# Getting Started with BlockchainTracer

This guide will walk you through all the steps needed to use BlockchainTracer, from setting up your Ethereum account to recording your first ML experiment.

## 1. Setting Up Your Ethereum Account

### 1.1 Create an Ethereum Wallet
1. Install MetaMask (recommended for beginners):
   - Visit [MetaMask](https://metamask.io/)
   - Install the browser extension
   - Create a new wallet and SAFELY STORE your seed phrase
   - Once created, click on your account to copy your address

2. Get your private key from MetaMask:
   - Click on the three dots menu
   - Go to "Account Details"
   - Click "Export Private Key"
   - Enter your password
   - Copy your private key (NEVER share this with anyone)

### 1.2 Get Test ETH
1. Choose a test network in MetaMask:
   - Click on "Ethereum Mainnet" dropdown
   - Select "Sepolia Test Network" (recommended) or "Goerli Test Network"

2. Get test ETH:
   - For Sepolia: Visit [Sepolia Faucet](https://sepoliafaucet.com/)
   - For Goerli: Visit [Goerli Faucet](https://goerlifaucet.com/)
   - Enter your wallet address
   - Receive test ETH (free)

### 1.3 Set Up Infura
1. Create an Infura account:
   - Visit [Infura](https://infura.io/)
   - Sign up for a free account
   - Create a new project
   - Select the same network you chose in MetaMask (Sepolia or Goerli)
   - Copy your project's endpoint URL (e.g., `https://sepolia.infura.io/v3/YOUR-PROJECT-ID`)

## 2. Installing BlockchainTracer

```bash
# Clone the repository
git clone https://github.com/fcerino/BlockchainTracer
cd BlockchainTracer

# Install the package
pip install -e .
```

## 3. Configuration

1. Create a `.env` file in your project root:
```bash
# Create .env file
touch .env

# Add your credentials (replace with your actual values)
echo "ETH_PRIVATE_KEY=your_private_key_here" >> .env
echo "ETH_NETWORK_URL=your_infura_endpoint_here" >> .env
```

⚠️ IMPORTANT:
- Never commit your `.env` file to version control
- Keep your private key secure and never share it
- Make sure your `.env` file is in `.gitignore`

## 4. Basic Usage

Here's a minimal example of how to use BlockchainTracer:

```python
from blockchaintracer import BlockchainTracer

# Initialize the tracer
tracer = BlockchainTracer()

# Prepare your experiment information
model_config = {
    'architecture': 'simple_neural_network',
    'layers': [
        {'type': 'dense', 'units': 64, 'activation': 'relu'},
        {'type': 'dense', 'units': 1, 'activation': 'sigmoid'}
    ],
    'optimizer': {'name': 'adam', 'learning_rate': 0.001}
}

dataset_info = {
    'name': 'my_dataset',
    'num_samples': 1000,
    'features': 20,
    'split': {'train': 0.8, 'test': 0.2}
}

metrics = {
    'accuracy': 0.85,
    'precision': 0.83,
    'f1_score': 0.84
}

# Record your experiment
tx_hash = tracer.trace_ml_experiment(
    model_config=model_config,
    model_path='path/to/your/saved/model',
    dataset_info=dataset_info,
    metrics=metrics,
    additional_info={'notes': 'First experiment'}
)

print(f"Experiment recorded with transaction hash: {tx_hash}")

# Later, verify your experiment
traced_data = tracer.verify_experiment(tx_hash)
```

## 5. Verifying Transactions

You can verify your transactions in two ways:

1. Using BlockchainTracer:
```python
traced_data = tracer.verify_experiment(tx_hash)
```

2. Using Etherscan:
   - For Sepolia: Visit [Sepolia Etherscan](https://sepolia.etherscan.io/) and paste your transaction hash
   - For Goerli: Visit [Goerli Etherscan](https://goerli.etherscan.io/) and paste your transaction hash

## 6. Best Practices

1. **Security**:
   - Never share your private key
   - Use test networks for development
   - Keep your `.env` file secure

2. **Data Management**:
   - Include all relevant information in your model_config
   - Document your dataset properly
   - Include meaningful metrics
   - Add descriptive notes in additional_info

3. **Cost Efficiency**:
   - Use test networks for development
   - Group related information together to minimize transactions
   - Monitor gas prices before sending transactions

## 7. Troubleshooting

Common issues and solutions:

1. **Transaction Failed**
   - Check your ETH balance
   - Verify network connectivity
   - Ensure gas price is sufficient

2. **Authentication Error**
   - Verify your private key is correct
   - Check your Infura endpoint URL
   - Ensure `.env` file is in the correct location
   - Confirm Infura project is active

3. **File Not Found**
   - Verify model file path is correct
   - Check file permissions
   - Ensure working directory is correct

## 8. Getting Help

- Check the [GitHub Issues](https://github.com/fcerino/BlockchainTracer/issues)
- Review the [README.md](../README.md)
- Contact the maintainers

## 9. Contributing

We welcome contributions! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

For major changes, please open an issue first to discuss what you would like to change. 