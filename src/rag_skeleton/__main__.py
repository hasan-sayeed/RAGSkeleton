# src/rag_skeleton/__main__.py
"""
Entry point for the rag_skeleton package.

This module handles argument parsing and initializes the main function 
of the RAG chatbot. It is invoked when the package is run as a script 
or through the console entry point.

Example:
    To run the RAG chatbot with specified arguments:

        $ rag_skeleton --data_path /path/to/docs --load_mode api --model_name "model-name" --api_token <your-api-token>
        
"""

import argparse
from rag_skeleton.run import main

def entry():
    
    parser = argparse.ArgumentParser(description="Run the RAG chatbot with custom settings.")
    parser.add_argument("--data_path", type=str, default=None, help="Optional path to a directory of PDF files for creating a new vector database.")
    parser.add_argument("--load_mode", type=str, default="local", choices=["local", "api"], help="Set to 'local' to load model locally, or 'api' to use Hugging Face API.")
    parser.add_argument("--model_name", type=str, default="meta-llama/Llama-3.2-3B-Instruct", help="Specify the model name.")
    parser.add_argument("--api_token", type=str, default=None, help="Hugging Face API token, required if load_mode is 'api'.")

    args = parser.parse_args()
    
    main(**vars(args))  # Pass parsed arguments to main

if __name__ == "__main__":
    entry()