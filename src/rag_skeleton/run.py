# src/rag_skeleton/run.py
import argparse
from rag import RAGPipeline

def main(load_mode="local", model_name="meta-llama/Llama-3.2-3B-Instruct", api_token=None):
    """
    Initializes the RAG pipeline and starts an interactive chatbot session.

    Parameters:
    - load_mode (str): Specifies whether to load the model locally or via Hugging Face API.
                       Options are 'local' (default) or 'api'.
    - model_name (str): The name of the language model to use for generation.
                        Default is 'meta-llama/Llama-3.2-3B-Instruct'.
    - api_token (str, optional): Hugging Face API token, required if `load_mode` is set to 'api'.
                                 Default is None.
    
    This function initializes the RAG pipeline with the specified configuration and starts
    an interactive loop where the user can ask questions and receive responses based on
    retrieved document context.
    """
    vectordb_path = "vectordb"  # Path to the existing ChromaDB vector database

    # Initialize the RAG pipeline with the vector database, model name, load mode, and API token
    rag_pipeline = RAGPipeline(
        vectordb_path=vectordb_path,
        model_name=model_name,
        load_mode=load_mode,
        api_token=api_token
    )
    rag_pipeline.setup_pipeline()

    print("Welcome to the RAG chatbot. Type 'exit' to quit.")
    
    # Interactive chat loop
    while True:
        question = input("Ask your question: ")
        if question.lower() == "exit":
            print("Exiting the chatbot. Goodbye!")
            break
        response = rag_pipeline.get_response(question)
        print("Answer:", response)
        print("\n\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the RAG chatbot with custom settings.")
    parser.add_argument("--load_mode", type=str, default="local", choices=["local", "api"], 
                        help="Set to 'local' to load model locally, or 'api' to use Hugging Face API.")
    parser.add_argument("--model_name", type=str, default="meta-llama/Llama-3.2-3B-Instruct", 
                        help="Specify the model name. Default is 'meta-llama/Llama-3.2-3B-Instruct'.")
    parser.add_argument("--api_token", type=str, default=None, 
                        help="Hugging Face API token, required if load_mode is 'api'.")

    args = parser.parse_args()

    main(load_mode=args.load_mode, model_name=args.model_name, api_token=args.api_token)
