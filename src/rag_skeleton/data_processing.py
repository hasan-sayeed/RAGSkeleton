# src/rag_skeleton/data_processing.py
import os
import gc
import torch
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

class DataProcessor:
    """
    Handles loading, processing, and creating vector databases for documents.
    """

    def __init__(self, vectordb_path, data_path="data/raw", embedding_model="Alibaba-NLP/gte-large-en-v1.5"):
        """
        Initialize the DataProcessor with default values. 

        Parameters:
        
        - data_path: str, path to the directory containing raw PDF files. Default is "data/raw".

        - vectordb_path: str, path to the directory where the vector database will be stored. Default is "vectordb".
                         
        - embedding_model: str, the embedding model to be used for vectorization. Default is "Alibaba-NLP/gte-large-en-v1.5".

        Note:
        These are the default values. We suggest models from the MTEB leaderboard
        (https://huggingface.co/spaces/mteb/leaderboard) based on the `Retrieval Average` score
        and `Memory Usage`. Balancing retrieval quality and available resources is recommended
        to optimize both accuracy and efficiency in your specific environment.
        """
        self.data_path = data_path
        self.vectordb_path = vectordb_path
        self.embedding = HuggingFaceEmbeddings(model_name=embedding_model, model_kwargs={"trust_remote_code":True})   # https://github.com/langchain-ai/langchain/issues/6080#issuecomment-1963311548
        self.vector_store = None

    def load_documents(self, enrich_metadata=False):
        """
        Loads PDF documents from the specified data path and optionally enriches metadata.

        Parameters:

        - enrich_metadata (bool): If True, add metadata to each document (e.g., name and year).

        Returns:

        - list: List of loaded documents with optional metadata.

        """
        docs = []
        for file in os.listdir(self.data_path):
            if file.endswith(".pdf"):
                file_path = os.path.join(self.data_path, file)
                loader = PyMuPDFLoader(file_path)
                loaded_docs = loader.load()
                
                # Enrich metadata if the flag is set
                if enrich_metadata:
                    for doc in loaded_docs:
                        doc.metadata["name"] = os.path.splitext(file)[0]  # Get file name without extension
                        doc.metadata["year"] = 2024  # Set year as 2024 for now

                docs.extend(loaded_docs)

        print(f"Loaded {len(docs)} documents.")
        return docs

    def split_documents(self, docs, chunk_size=1500, chunk_overlap=100):
        """
        Splits documents into chunks for vectorization.

        Parameters:

        - docs: list, documents to split.

        - chunk_size: int, size of each chunk. Default is 1500.

        - chunk_overlap: int, overlap between chunks. Default is 100.

        Returns:

        - list: List of document chunks.

        """
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        return splitter.split_documents(docs)

    def create_vector_db(self, docs):
        """
        Creates and stores the vector database in ChromaDB.

        Parameters:

        - docs: list, document chunks to vectorize and store.

        """
        if not os.path.exists(self.vectordb_path):
            os.makedirs(self.vectordb_path)
        
        self.vector_store = Chroma.from_documents(
            documents=docs,
            embedding=self.embedding,
            persist_directory=self.vectordb_path
        )

        print(f"Knowledge base created and saved in directory: {self.vectordb_path}")

    def process_and_create_db(self):
        """Main method to load, split, and create vectorDB."""
        docs = self.load_documents()
        splits = self.split_documents(docs)
        self.create_vector_db(splits)
