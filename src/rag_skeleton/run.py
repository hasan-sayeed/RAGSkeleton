# # src/rag_skeleton/run.py
# import argparse
# from rag_skeleton.rag import RAGPipeline

# def main(load_mode="local", model_name="meta-llama/Llama-3.2-3B-Instruct", api_token=None):
#     """
#     Initializes the RAG pipeline and starts an interactive chatbot session.

#     Parameters:

#     - load_mode (str): Specifies whether to load the model locally or via Hugging Face API.
#                        Options are 'local' (default) or 'api'.

#     - model_name (str): The name of the language model to use for generation.
#                         Default is 'meta-llama/Llama-3.2-3B-Instruct'.

#     - api_token (str, optional): Hugging Face API token, required if `load_mode` is set to 'api'.
#                                  Default is None.
    
#     This function initializes the RAG pipeline with the specified configuration and starts
#     an interactive loop where the user can ask questions and receive responses based on
#     retrieved document context.

#     """
#     vectordb_path = "vectordb"  # Path to the existing ChromaDB vector database

#     # Initialize the RAG pipeline with the vector database, model name, load mode, and API token
#     rag_pipeline = RAGPipeline(
#         vectordb_path=vectordb_path,
#         model_name=model_name,
#         load_mode=load_mode,
#         api_token=api_token
#     )
#     rag_pipeline.setup_pipeline()

#     print("Welcome to the RAG chatbot. Type 'exit' to quit.")
    
#     # Interactive chat loop
#     while True:
#         question = input("Ask your question: ")
#         if question.lower() == "exit":
#             print("Exiting the chatbot. Goodbye!")
#             break
#         response = rag_pipeline.get_response(question)
#         print("Answer:", response)
#         print("\n\n")

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Run the RAG chatbot with custom settings.")
#     parser.add_argument("--load_mode", type=str, default="local", choices=["local", "api"], 
#                         help="Set to 'local' to load model locally, or 'api' to use Hugging Face API.")
#     parser.add_argument("--model_name", type=str, default="meta-llama/Llama-3.2-3B-Instruct", 
#                         help="Specify the model name. Default is 'meta-llama/Llama-3.2-3B-Instruct'.")
#     parser.add_argument("--api_token", type=str, default=None, 
#                         help="Hugging Face API token, required if load_mode is 'api'.")

#     args = parser.parse_args()

#     main(load_mode=args.load_mode, model_name=args.model_name, api_token=args.api_token)



import argparse
import os
import shutil
from rag_skeleton.rag import RAGPipeline
from rag_skeleton.data_processing import DataProcessor

def main(data_path=None, load_mode="local", model_name="meta-llama/Llama-3.2-3B-Instruct", api_token=None):
    """
    Initializes the RAG pipeline, ensuring the vector database is available or created.
    
    Parameters:
    - data_path (str): Optional path to a directory of PDF files to process and build a new vector database.

    - load_mode (str): Specifies whether to load the model locally or via Hugging Face API.
                       Options are 'local' (default) or 'api'.

    - model_name (str): The name of the language model to use for generation.
                        Default is 'meta-llama/Llama-3.2-3B-Instruct'.

    - api_token (str, optional): Hugging Face API token, required if `load_mode` is set to 'api'.
    """
    vectordb_path = "vectordb"  # Path to the vector database

    # Determine if we need to create a new vector database
    if data_path:
        # If a new data path is provided, delete the old vectordb if it exists
        if os.path.exists(vectordb_path):
            print("A new document path is provided. Clearing the existing knowledge base to create a fresh one.")
            shutil.rmtree(vectordb_path)  # Remove the existing vectordb directory
            
        print(f"Processing new documents from: {data_path}")
        # Process and create the vector database
        process_data = DataProcessor(data_path=data_path, vectordb_path=vectordb_path)
        process_data.process_and_create_db()
    elif not os.path.exists(vectordb_path):
        print("No knowledge base found. Please provide a directory of PDF files to create a custom, searchable knowledge base for grounding responses.")
        data_path = input("Please enter the path to your directory of PDF files: ").strip()
        
        # Process and create the vector database
        process_data = DataProcessor(data_path=data_path, vectordb_path=vectordb_path)
        process_data.process_and_create_db()
    else:
        print("Knowledge base found. Proceeding with responses grounded in this knowledge base.")

    # Initialize the RAG pipeline with the vector database and other parameters
    rag_pipeline = RAGPipeline(
        vectordb_path=vectordb_path,
        model_name=model_name,
        load_mode=load_mode,
        api_token=api_token
    )
    rag_pipeline.setup_pipeline()

    # Interactive chat loop
    print("Welcome to the RAG chatbot. Type 'exit' to quit.")
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
    parser.add_argument("--data_path", type=str, default=None,
                        help="Optional path to a directory of PDF files for creating a new vector database.")
    parser.add_argument("--load_mode", type=str, default="local", choices=["local", "api"], 
                        help="Set to 'local' to load model locally, or 'api' to use Hugging Face API.")
    parser.add_argument("--model_name", type=str, default="meta-llama/Llama-3.2-3B-Instruct", 
                        help="Specify the model name. Default is 'meta-llama/Llama-3.2-3B-Instruct'.")
    parser.add_argument("--api_token", type=str, default=None, 
                        help="Hugging Face API token, required if load_mode is 'api'.")

    args = parser.parse_args()

    main(data_path=args.data_path, load_mode=args.load_mode, model_name=args.model_name, api_token=args.api_token)
