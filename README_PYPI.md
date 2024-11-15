# RAGSkeleton

A foundational, modular framework for building customizable Retrieval-Augmented Generation (RAG) systems across any domain.

## Installation via pip

This section is recommended for users who want a quick setup for running RAGSkeleton with minimal configuration.

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


## Documentation

Full documentation is available on [Read the Docs](https://ragskeleton.readthedocs.io/en/latest/).