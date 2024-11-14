# src/rag_skeleton/run.py
import os
import shutil
from pathlib import Path
from rag_skeleton.rag import RAGPipeline
from rag_skeleton.data_processing import DataProcessor

# Define a default vectordb path within the package directory
default_vdb_dir = Path(__file__).resolve().parent / "data" / "vectordb"
default_vdb_dir.mkdir(parents=True, exist_ok=True)

def main(data_path=None, load_mode="local", model_name="meta-llama/Llama-3.2-3B-Instruct", 
         api_token=None, vectordb_path=default_vdb_dir):
    """
    Initializes the RAG pipeline, ensuring the vector database is available or created.
    
    Parameters:

    - data_path (str): Optional path to a directory of PDF files to process and build a new vector database.

    - load_mode (str): Specifies whether to load the model locally or via Hugging Face API. Options are 'local' (default) or 'api'.

    - model_name (str): The name of the language model to use for generation. Default is 'meta-llama/Llama-3.2-3B-Instruct'.

    - api_token (str, optional): Hugging Face API token, required if `load_mode` is set to 'api'.
    
    - vectordb_path (Path, optional): Path to store the vector database. Defaults to package directory.
    
    """
    
    # Convert vectordb_path to a string, as required by ChromaDB
    vectordb_path = str(vectordb_path)  
    data_path = Path(data_path) if data_path else None

    # Determine if we need to create a new vector database
    if data_path:
        # If a new data path is provided or vectordb_path exists but is empty, clear and recreate the database
        if os.path.exists(vectordb_path) and any(Path(vectordb_path).iterdir()):
            print("A new document path is provided. Clearing the existing knowledge base to create a fresh one.")
            shutil.rmtree(vectordb_path)  # Remove the existing vectordb directory

        print(f"Processing new documents from: {data_path}")
        process_data = DataProcessor(data_path=data_path, vectordb_path=vectordb_path)
        process_data.process_and_create_db()
    elif not os.path.exists(vectordb_path) or not any(Path(vectordb_path).iterdir()):
        print("No knowledge base found. Please provide a directory of PDF files to create a custom, searchable knowledge base for grounding responses.")
        data_path = input("Please enter the path to your directory of PDF files here: ").strip()
        process_data = DataProcessor(data_path=data_path, vectordb_path=vectordb_path)
        process_data.process_and_create_db()
    else:
        print("Knowledge base found. Proceeding with responses grounded in this existing knowledge base.")

    # Initialize the RAG pipeline
    rag_pipeline = RAGPipeline(
        vectordb_path=vectordb_path,
        model_name=model_name,
        load_mode=load_mode,
        api_token=api_token
    )
    rag_pipeline.setup_pipeline()

    print("Welcome to the RAG chatbot. Type 'exit' to quit.")
    while True:
        question = input("Ask your question: ")
        if question.lower() == "exit":
            print("Exiting the chatbot. Goodbye!")
            break
        response = rag_pipeline.get_response(question)
        print("Answer:", response)
        print("\n\n")
