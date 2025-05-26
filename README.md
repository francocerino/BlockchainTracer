# BlockchainTracer
Python package to trace sensitive information and process flows on the blockchain.

Leverages the blockchain’s inherent properties —immutability, transparency, availability, and traceability— to record and audit sequential steps in any process. Ideal for applications requiring verifiable records of actions or sensitive data trails.

Save sequential steps of anything.

## Implementation

A single multipurpose Python class.

## Multipurpose

 - Improve reproducibility of Machine Learning models. There is a 'reproducibility crysis'. (THIS IS THE MAIN IDEA)
 - Upload hashes of big data files. 
 - Trace NGO donations.
 - Improve supply chain traceability.
 - Save important data of scientific studies.
 - Proof of authorship. Trace results with an address and a timestamp.
 - Any text.
 - What you want.

## Roadmap

### Stage 1

 1. Read saved and related bibliography to clarify the needed things for ML reproducibility.

    - [A Survey of Data Provenance in e-Science](https://sci-hub.se/10.1145/1084805.1084812)
    - [Ensuring Trustworthy Neural Network Training via Blockchain](https://par.nsf.gov/servlets/purl/10464202)
    - [Towards Enabling Trusted Artificial Intelligence via Blockchain](https://www.researchgate.net/publication/332642472_Towards_Enabling_Trusted_Artificial_Intelligence_via_Blockchain)
    - [BlockFlow: Trust in Scientific Provenance Data](https://sol.sbc.org.br/index.php/bresci/article/view/10033/9915)
    - [ProML: A Decentralised Platform for Provenance Management of Machine Learning Software Systems](https://arxiv.org/pdf/2206.10110)
    - [Blockchain Based Provenance Sharing of Scientific Workflows](https://sci-hub.se/10.1109/BigData.2018.8622237)
    - [Improving Reproducibility in Machine Learning Research (2021)](https://www.jmlr.org/papers/volume22/20-303/20-303.pdf)
    - [Reproducibility in Machine Learning-Driven Research (2023)](https://arxiv.org/pdf/2307.10320)
    - [Leakage and the reproducibility crisis in machine learning-based science (2023)](https://www.cell.com/patterns/pdf/S2666-3899(23)00159-9.pdf)
    - [reforms: Reporting Standards for Machine Learning Based Science (2023)](https://arxiv.org/pdf/2308.07832)
    - [Traceability for Trustworthy AI: A Review of Models and Tools (2021)](https://www.mdpi.com/2504-2289/5/2/20). Comparison of some existing frameworks for ML reproducibility.
    - [Reproducibility in PyTorch](https://pytorch.org/docs/stable/notes/randomness.html)
    - [Advancing Research Reproducibility in Machine Learning through Blockchain Technology (2024)](https://informatica.vu.lt/journal/INFORMATICA/article/1330/info). Shows a review of works related to ML reproducibility with Blockchain.
    - [Promoting Distributed Trust in Machine Learning and Computational Simulation via a Blockchain Network](https://arxiv.org/pdf/1810.11126)
    - [Blockchain analytics and Artificial Intelligence](https://www.researchgate.net/profile/Qi-Zhang-126/publication/331241223_Blockchain_Analytics_and_Artificial_Intelligence/links/5c79ee12299bf1268d30af9e/Blockchain-Analytics-and-Artificial-Intelligence.pdf)
    - [Automatically Tracking Metadata and
Provenance of Machine Learning Experiments](https://assets.amazon.science/2f/39/4b32cf354e4c993b439d88258597/automatically-tracking-metadata-and-provenance-of-machine-learning-experiments.pdf) Comments an approach for scikit-learn Pipelines and other libraries.
    - [Reproducibility in Machine Learning-based Research: Overview, Barriers and Drivers (2024)](https://arxiv.org/html/2406.14325v1)
    - [Model Cards for Model Reporting](https://arxiv.org/pdf/1810.03993), [Model Cards applied to known models](https://iapp.org/news/a/5-things-to-know-about-ai-model-cards). Each model card could be accompanied with Datasheets, Nutrition Labels, Data Statements, or Factsheets, describing datasets that the model was trained and evaluated on.
    - [Practices for reproducibility](https://koustuvsinha.com/practices_for_reproducibility/)

 2. **Specifying differentiators of this work**.
     A solution that has simultaneously:
    - Traceability of ML models in EVM Blockchains with a Python API. Python is the most used language in ML, and EVM the most used for smart contracts.
    - Open source code.
    - Following standards of previous studies for ML reproducibility. Is a good idea more focus on narrative for reproducibility?
    - Ability to trace other processes in general. But focused in ML reproducibility.
    - Trace computer environment where the ML model was trained.
    - Use Arweave or IPFS for large data, storing its hash in the EVM blockchain.
  
 4. Fine-tune the case of ML. Requirements for good reproducibility.
    - The NeurIPS 2019 ML reproducibility checklist ([Improving Reproducibility in Machine Learning Research](https://www.jmlr.org/papers/volume22/20-303/20-303.pdf)).
    - JSON data structure with every configuration of the ML pipeline (hardware, environment, preprocesses, hyperparameters, seeds, metrics, package versions, etc). Also HDF5? [Traceability for Trustworthy AI: A Review of Models and Tools (2021)](https://www.mdpi.com/2504-2289/5/2/20)
    - Model info sheet of [Leakage and the reproducibility crisis in machine learning-based science (2023)](https://www.cell.com/patterns/pdf/S2666-3899(23)00159-9.pdf)
    - Standarized enviroment. Docker is always needed? [Leakage and the reproducibility crisis in machine learning-based science (2023)](https://www.cell.com/patterns/pdf/S2666-3899(23)00159-9.pdf)
    - Checklist of [reforms: Reporting Standards for Machine Learning Based Science (2023)](https://arxiv.org/pdf/2308.07832).
    - Minimal Description Profile: [Traceability for Trustworthy AI: A Review of Models and Tools (2021)](https://www.mdpi.com/2504-2289/5/2/20).
    - [Model Cards for Model Reporting](https://arxiv.org/pdf/1810.03993)
      
      [Continue list, reading remaining items from 1.]

 5. Give the user things needed to reproduce models.
 6. Ensure the code is easy to use and works well. 
    - Python code to facilitate technical people, not necessarily in blockchain.
    - Integration with EVM blockchains (the most used and highly decentralized).

### Stage 2

 6. Solve what to do with code and binaries.
 7. Integration with IPFS or Arweave for large data.
 
 ### Stage 3

 8. Frontend for scalability (usable by non-technical persons).
 9. Smart contract to decentralice the code used.
 10. Extend to other public blockchains.
 11. Extend to private blockchains. 
 12. Display option to trace data with a new address.
