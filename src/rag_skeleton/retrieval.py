# src/rag_skeleton/retrieval.py
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

class DocumentRetriever:
    """
    Retrieves documents from the ChromaDB vector database using an embedding model.
    """

    def __init__(self, vectordb_path="vectordb", embedding_model_name="Alibaba-NLP/gte-large-en-v1.5"):
        """
        Initializes the DocumentRetriever with the path to the ChromaDB database and an embedding model.

        Parameters:
        - vectordb_path: str, path to the vector database directory. Default is "vectordb".
        - embedding_model_name: str, embedding model name for generating query embeddings.
        """
        self.vectordb_path = vectordb_path
        self.embedding = HuggingFaceEmbeddings(model_name=embedding_model_name, model_kwargs={"trust_remote_code":True})   # https://github.com/langchain-ai/langchain/issues/6080#issuecomment-1963311548
        self.vector_store = Chroma(persist_directory=self.vectordb_path, embedding_function=self.embedding)

    def get_retriever(self, search_type="similarity", search_kwargs={"k": 5}):
        """
        Returns a retriever instance for retrieving similar documents.

        Parameters:
        - search_type: str, type of search (Can be "similarity", "mmr", or "similarity_score_threshold"). Default is "similarity".
        - search_kwargs: dict, additional search parameters. Default is None.

        Returns:
        - retriever: a retriever instance for document retrieval.
        """
        return self.vector_store.as_retriever(search_type=search_type, search_kwargs=search_kwargs)
