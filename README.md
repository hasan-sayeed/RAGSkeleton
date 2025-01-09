[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)
[![ReadTheDocs](https://readthedocs.org/projects/rag_skeleton/badge/?version=latest)](https://ragskeleton.readthedocs.io/en/latest/)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/hasan-sayeed/RAGSkeleton/blob/master/notebooks/RAGSkeleton_Tutorial.ipynb)
[![GitHub issues](https://img.shields.io/github/issues/hasan-sayeed/RAGSkeleton)](https://github.com/hasan-sayeed/RAGSkeleton/issues)
[![GitHub Discussions](https://img.shields.io/github/discussions/hasan-sayeed/RAGSkeleton)](https://github.com/hasan-sayeed/RAGSkeleton/discussions)
[![Last Committed](https://img.shields.io/github/last-commit/hasan-sayeed/RAGSkeleton)](https://github.com/hasan-sayeed/RAGSkeleton/commits/main/)
<!-- These are examples of badges you might also want to add to your README. Update the URLs accordingly.
[![Built Status](https://api.cirrus-ci.com/github/<USER>/rag_skeleton.svg?branch=main)](https://cirrus-ci.com/github/<USER>/rag_skeleton)
[![ReadTheDocs](https://readthedocs.org/projects/rag_skeleton/badge/?version=latest)](https://rag_skeleton.readthedocs.io/en/stable/)
[![Coveralls](https://img.shields.io/coveralls/github/<USER>/rag_skeleton/main.svg)](https://coveralls.io/r/<USER>/rag_skeleton)
[![PyPI-Server](https://img.shields.io/pypi/v/rag_skeleton.svg)](https://pypi.org/project/rag_skeleton/)
[![Conda-Forge](https://img.shields.io/conda/vn/conda-forge/rag_skeleton.svg)](https://anaconda.org/conda-forge/rag_skeleton)
[![Monthly Downloads](https://pepy.tech/badge/rag_skeleton/month)](https://pepy.tech/project/rag_skeleton)
[![Twitter](https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter)](https://twitter.com/rag_skeleton)
-->

# RAGSkeleton

![RAGSkeleton-logo](docs/_static/RAGSkeleton-logo.png)

*Figure: Schematic of a Retrieval-Augmented Generation (RAG) system. Adapted from [Elevating Your Retrieval Game: Insights from Real-world Deployments](https://blog.ml6.eu/elevating-your-retrieval-game-insights-from-real-world-deployments-84ccfcbe6422).*

**RAGSkeleton**: A foundational, modular framework for building customizable Retrieval-Augmented Generation (RAG) systems across any domain.

This project was originally developed as a Retrieval-Augmented Generation (RAG) system for materials science literature. However, it can be easily adapted for any domain with minimal modifications, making it a flexible RAG skeleton architecture. Users can adjust the system prompt to tailor responses to any field, making this setup a versatile foundation for a RAG system.

With this skeleton, users can seamlessly swap out different components—such as the embedding model, vector database, or LLM for response generation—with their preferred options, and quickly build a RAG system suited to their data and needs. This architecture significantly reduces the time and effort required to create a custom RAG system.

## Tutorials

To help you get started with **RAGSkeleton**, we’ve prepared a quick interactive Google Colab tutorial:

- [Google Colab Tutorial: Getting Started with RAGSkeleton](https://colab.research.google.com/github/hasan-sayeed/RAGSkeleton/blob/master/notebooks/RAGSkeleton_Tutorial.ipynb)

In this tutorial, you’ll learn how to:
1. Parse and index PDF files into a vector database.
2. Use a Retrieval-Augmented Generation (RAG) pipeline to query the documents.
3. Ask questions interactively and get responses grounded in your documents, with links to the source documents.

The tutorial runs on Google Colab, requiring no setup beyond logging into Hugging Face and uploading your data to Google Drive.

## Installation via pip

This section is recommended for users who want a quick setup for running RAGSkeleton with minimal configuration from their own machine.

### 1. Installation

- **Create a Conda Environment**

   To ensure compatibility, first set up a new conda environment:

   ```bash
   conda create -n rag_skeleton python=3.10
   conda activate rag_skeleton
   ```

- **Install via pip**

   Install RAGSkeleton and its dependencies using pip:

   ```bash
   pip install rag_skeleton
   ```

### 2. Login to Hugging Face 

RAGSkeleton relies on Hugging Face for both the embedding model and the generative language model. Log in to Hugging Face from the terminal to access the necessary models:

```bash
huggingface-cli login
```

Enter your Hugging Face access token when prompted. You can obtain an API token by signing up at [Hugging Face] and navigating to your account settings.

**Note:** Some models, like Meta LLaMA, may require additional permission from the owner on Hugging Face. To use these models, request access through the model's Hugging Face page, and you’ll be notified when access is granted.

### 3. Run the RAG System

Run RAGSkeleton with:

```bash
rag_skeleton --data_path /path/to/your/pdf/folder --load_mode local --model_name "meta-llama/Llama-3.2-3B-Instruct"
```

- `--data_path`: Path to a directory of PDF files for creating a vector database. If omitted, the system will use the existing knowledge base (if available) or prompt you to provide a path. If you want to ground your RAG on a different set of documents, simply provide the new directory path here, and the system will create a fresh knowledge base.

- `--load_mode`: Specify `local` to use a model hosted on your system, or `api` to use Hugging Face's API. `local` mode is suitable if you have the necessary computational resources, while `api` mode is useful if you prefer not to host the model locally or lack the computational resources.

- `--model_name`: Name of the language model to use. Default is "meta-llama/Llama-3.2-3B-Instruct". Any model available on Hugging Face can be specified here, allowing you to choose models best suited to your requirements.

- `--api_token`: Required if using the Hugging Face API (`--load_mode` api).

**Note:** With the API, you can opt for larger models that might otherwise be challenging to run locally. However, keep in mind that the Hugging Face Free API has a model size limit of 10GB. If you need to use larger models, consider a paid API plan or explore model optimization techniques.

### Usage

When you start RAGSkeleton, you’ll be welcomed by a chatbot interface where you can ask questions. The system will retrieve relevant information from the knowledge base and generate responses grounded in the PDF documents you provided.

To exit, type `exit`.


## Running the RAG System from Source

For developers and contributors who want to work with the source code or customize the setup.

### 1. Clone the Repository

First, clone the repository and navigate to the project root directory:

```bash
git clone https://github.com/hasan-sayeed/RAGSkeleton.git
cd RAGSkeleton
```

### 2. Set Up the Environment

- Create a Conda Environment:

   ```bash
   conda env create -f environment.yml
   conda activate rag_skeleton
   ```

- Login to Hugging Face

   Similar to the pip installation, login to Hugging Face:

   ```bash
   huggingface-cli login
   ```

- **Optional Setup for Git Hooks:**

   - Install pre-commit git hooks with:

      ```bash
      pre-commit install
      ```

   - This configuration can be modified in .pre-commit-config.yaml.
   - Install nbstripout to automatically remove notebook output cells in committed files:

      ```bash
      nbstripout --install --attributes notebooks/.gitattributes
      ```

### 3. Run the RAG System

To run the RAG system directly from the source, use the -m flag with Python to specify the module path. This will invoke the __main__.py entry point, which manages command-line arguments and initiates the chatbot.

```bash
python -m src.rag_skeleton --data_path /path/to/your/pdf/folder --load_mode local --model_name "meta-llama/Llama-3.2-3B-Instruct"
```

- `--data_path`: Path to a directory of PDF files for creating a vector database. If omitted, the system will use the existing knowledge base (if available) or prompt you to provide a path. If you want to ground your RAG on a different set of documents, simply provide the new directory path here, and the system will create a fresh knowledge base.

- `--load_mode`: Specify `local` to use a model hosted on your system, or `api` to use Hugging Face's API. `local` mode is suitable if you have the necessary computational resources, while `api` mode is useful if you prefer not to host the model locally or lack the computational resources.

- `--model_name`: Name of the language model to use. Default is "meta-llama/Llama-3.2-3B-Instruct". Any model available on Hugging Face can be specified here, allowing you to choose models best suited to your requirements.

- `--api_token`: Required if using the Hugging Face API (`--load_mode` api).

**Note:** With the API, you can opt for larger models that might otherwise be challenging to run locally. However, keep in mind that the Hugging Face Free API has a model size limit of 10GB. If you need to use larger models, consider a paid API plan or explore model optimization techniques.

### Usage

When you start RAGSkeleton, you’ll be welcomed by a chatbot interface where you can ask questions. The system will retrieve relevant information from the knowledge base and generate responses grounded in the PDF documents you provided.

To exit, type `exit`.


## Documentation

Full documentation is available on [Read the Docs](https://ragskeleton.readthedocs.io/en/latest/).

## Dependency Management & Reproducibility

1. Always keep your abstract (unpinned) dependencies updated in `environment.yml` and eventually
   in `setup.cfg` if you want to ship and install your package via `pip` later on.
2. Create concrete dependencies as `environment.lock.yml` for the exact reproduction of your
   environment with:
   ```bash
   conda env export -n rag_skeleton -f environment.lock.yml
   ```
   For multi-OS development, consider using `--no-builds` during the export.
3. Update your current environment with respect to a new `environment.lock.yml` using:
   ```bash
   conda env update -f environment.lock.yml --prune
   ```
## Project Organization

```
├── AUTHORS.md              <- List of developers and maintainers.
├── CHANGELOG.md            <- Changelog to keep track of new features and fixes.
├── CONTRIBUTING.md         <- Guidelines for contributing to this project.
├── Dockerfile              <- Build a docker container with `docker build .`.
├── LICENSE.txt             <- License as chosen on the command-line.
├── README.md               <- The top-level README for developers.
├── configs                 <- Directory for configurations of model & application.
├── data
│   ├── external            <- Data from third party sources.
│   ├── interim             <- Intermediate data that has been transformed.
│   ├── processed           <- The final, canonical data sets for modeling.
│   └── raw                 <- The original, immutable data dump.
├── docs                    <- Directory for Sphinx documentation in rst or md.
├── environment.yml         <- The conda environment file for reproducibility.
├── models                  <- Trained and serialized models, model predictions,
│                              or model summaries.
├── notebooks               <- Jupyter notebooks. Naming convention is a number (for
│                              ordering), the creator's initials and a description,
│                              e.g. `1.0-fw-initial-data-exploration`.
├── pyproject.toml          <- Build configuration. Don't change! Use `pip install -e .`
│                              to install for development or to build `tox -e build`.
├── references              <- Data dictionaries, manuals, and all other materials.
├── reports                 <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures             <- Generated plots and figures for reports.
├── scripts                 <- Analysis and production scripts which import the
│                              actual PYTHON_PKG, e.g. train_model.
├── setup.cfg               <- Declarative configuration of your project.
├── setup.py                <- [DEPRECATED] Use `python setup.py develop` to install for
│                              development or `python setup.py bdist_wheel` to build.
├── src
│   └── rag_skeleton        <- Actual Python package where the main functionality goes.
├── tests                   <- Unit tests which can be run with `pytest`.
├── .coveragerc             <- Configuration for coverage reports of unit tests.
├── .isort.cfg              <- Configuration for git hook that sorts imports.
└── .pre-commit-config.yaml <- Configuration of pre-commit git hooks.
```

## 🚀 Planned Features

The following enhancements are coming soon to RAGSkeleton:

- [ ] **Evaluate RAG Performance with Ragas Metrics** – Enable users to assess the quality of generated responses using standard RAG evaluation metrics from [Ragas](https://github.com/explodinggradients/ragas).
- [ ] **Conceptual Understanding Score (Materials Science Specific)** – A domain-specific metric to assess how well the RAG system understands key concepts in materials science.
- [ ] **Cross-Disciplinary Score (Materials Science Specific)** – A custom metric designed to evaluate the model’s ability to connect materials science concepts with insights from other scientific disciplines.

Stay tuned! If you have suggestions or feature requests, feel free to open a discussion or issue on [GitHub](https://github.com/hasan-sayeed/RAGSkeleton/issues).

## Feedback

Any questions, comments, or suggestions are welcome! This project is a flexible foundation for RAG-based applications, and we’re open to improvements that can make it even more useful across various domains.

<!-- pyscaffold-notes -->

## Note

This project has been set up using [PyScaffold] 4.6 and the [dsproject extension] 0.7.2.

[MTEB leaderboard]: https://huggingface.co/spaces/mteb/leaderboard
[Hugging Face]: https://huggingface.co/
[conda]: https://docs.conda.io/
[pre-commit]: https://pre-commit.com/
[Jupyter]: https://jupyter.org/
[nbstripout]: https://github.com/kynan/nbstripout
[Google style]: http://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings
[PyScaffold]: https://pyscaffold.org/
[dsproject extension]: https://github.com/pyscaffold/pyscaffoldext-dsproject