# src/rag_skeleton/generation.py
import torch
from langchain_huggingface import HuggingFacePipeline
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from langchain_huggingface import HuggingFaceEndpoint

class TextGenerator:
    """
    Generates text responses using a specified LLM model.

    """

    def __init__(self, model_name="meta-llama/Llama-3.2-3B-Instruct", device=None, load_mode="local", api_token=None):
        """
        Initializes the TextGenerator with a model name, device setting, and load mode.

        Parameters:

            - model_name: str, HuggingFace model ID.

            - device: int or str, device to run the model on (e.g., "cuda" for GPU, -1 or "cpu" for CPU).

            - load_mode: str, whether to load the model locally or from the Hugging Face API ("local" or "api").

            - api_token: str, Hugging Face API token, required if load_mode is "api".

        """
        self.model_name = model_name
        self.load_mode = load_mode
        self.api_token = api_token
        self.device = device if device is not None else ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.tokenizer = None

    def load_model(self):
        """
        Loads the LLM model and tokenizer and sets up the text generation pipeline.

        If `load_mode` is set to "api", it uses the Hugging Face API to load the model 
        and requires an API token. If `load_mode` is "local", it loads the model and tokenizer 
        locally from the Hugging Face repository.

        Raises:
            ValueError: If `load_mode` is "api" and `api_token` is not provided.
        
        Configurations:

            - For both "api" and "local" modes, specific parameters such as `temperature`, 
              `do_sample`, `repetition_penalty`, and `max_new_tokens` are set to control 
              text generation behavior.
            
            - For the local model, the `eos_token_id` parameter is set to stop generation at 
              specified tokens, ensuring response clarity.

        """
        if self.load_mode == "api":
            if not self.api_token:
                raise ValueError("Hugging Face API token is required for 'api' load mode.")
            # Use HuggingFaceEndpoint for loading the model via API
            self.llm = HuggingFaceEndpoint(
                endpoint_url=f"https://api-inference.huggingface.co/models/{self.model_name}",
                huggingfacehub_api_token=self.api_token,
                task="text-generation", 
                temperature=0.3,
                do_sample=True,
                repetition_penalty=1.1,
                return_full_text=False,
                max_new_tokens=1000
            )
        else:
            # Load the model and tokenizer locally
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name).to(self.device)
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

            # Set pad_token_id to eos_token_id to avoid warnings
            if self.tokenizer.pad_token_id is None:
                self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
            if self.model.config.pad_token_id is None:
                self.model.config.pad_token_id = self.tokenizer.eos_token_id
            
            # Define terminators for stopping generation at end of response
            terminators = [
                self.tokenizer.eos_token_id,
                self.tokenizer.convert_tokens_to_ids("<|eot_id|>")
            ]

            # Set up the text generation pipeline
            text_generation_pipeline = pipeline(
                model=self.model,
                tokenizer=self.tokenizer,
                task="text-generation",
                device=self.device,
                temperature=0.3,
                do_sample=True,
                repetition_penalty=1.1,
                return_full_text=False,
                max_new_tokens=1000,
                eos_token_id=terminators
            )

            # Wrap the pipeline for LangChain compatibility
            self.llm = HuggingFacePipeline(pipeline=text_generation_pipeline)
