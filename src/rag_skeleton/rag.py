# src/rag_skeleton/rag.py
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from rag_skeleton.retrieval import DocumentRetriever
from rag_skeleton.generation import TextGenerator


class RAGPipeline:
    """
    Combines document retrieval and text generation to create a Retrieval-Augmented Generation (RAG) pipeline
    with conversation history.
    """

    def __init__(
            self, 
            vectordb_path="vectordb", 
            embedding_model_name="Alibaba-NLP/gte-large-en-v1.5",
            model_name="meta-llama/Llama-3.2-3B-Instruct", 
            load_mode="local", 
            api_token=None,
            use_history=True, 
            max_history=4
    ):
        """
        Initializes the RAGPipeline with retrieval and generation components.

        Parameters:

        - vectordb_path: str, path to the ChromaDB vector database directory.

        - embedding_model_name: str, name of the embedding model used for query embeddings.

        - model_name: str, LLM model name for generation.

        - load_mode: str, whether to load the model locally or from the Hugging Face API ("local" or "api").

        - api_token: str, Hugging Face API token, required if load_mode is "api".

        - use_history: bool, whether to keep track of conversation history.

        - max_history: int, maximum number of recent question-answer pairs to remember (default: 4).

        """
        
        self.use_history = use_history
        self.max_history = max_history  # Limit the history length

        # Set up document retriever
        self.retriever = DocumentRetriever(vectordb_path=vectordb_path, embedding_model_name=embedding_model_name)
        
        # Initialize the text generator
        self.generator = TextGenerator(model_name=model_name, load_mode=load_mode, api_token=api_token)
        self.generator.load_model()  # Load model here once to avoid reloading

        # Initialize conversation history
        self.history = []  # List to store past exchanges (questions and responses)

        print("RAG Pipeline is ready for queries.")

    def format_docs_with_history(self, docs):
        """
        Formats retrieved documents and conversation history for the prompt context.

        Parameters:

        - docs: list of documents retrieved for the query.

        Returns:

        - tuple: (str, list) - formatted document text with history, and list of sources.

        """
        doc_text = "\n\n".join(doc.page_content for doc in docs)
        sources = [doc.metadata.get('source', 'Unknown source') for doc in docs]
        
        # Format conversation history if available. Include conversation history only if enabled
        if self.use_history and self.history:
            history_text = "\n".join([f"user: {q}\nassistant: {a}" for q, a in self.history])
            doc_text += f"\n\nConversation history:\n{history_text}"

        return doc_text, sources

    def setup_pipeline(self):
        """
        Sets up the full RAG pipeline with retrieval, prompt formatting, and text generation.

        This method configures the RAG pipeline by:

            - Defining the prompt template that guides the language model on how to respond to user queries.

            - Initializing the `PromptTemplate` with the defined format to structure the question, context, and conversation history.

            - Setting up the `rag_chain` pipeline, which includes:

                - Document retrieval: Retrieves relevant documents based on the user’s query.

                - Context formatting: Incorporates retrieved documents and conversation history.

                - Language model invocation: Passes the formatted prompt to the language model for generating a response.
                
                - Output parsing: Structures the final output format for the response.

        Raises:

            ValueError: If any pipeline component is misconfigured.

        The final `rag_chain` processes queries end-to-end, combining retrieval and generation.
        
        """
        
        # Define the prompt template with memory format
        prompt_template = """
        <|start_header_id|>system<|end_header_id|>
        You are a knowledgeable assistant specializing in materials science. Answer each question directly and concisely, providing only the necessary information in a straightforward manner, using only the provided context and conversation history. Do NOT reference the question or instructions in the prompt.
        If you lack sufficient information, respond with "I do not know". Don't fabricate answers.
        <|eot_id|>
        <|start_header_id|>user<|end_header_id|>
        Context: {context}
        Question: {question}<|eot_id|>
        <|start_header_id|>assistant<|end_header_id|>
        """

        # Initialize prompt template
        self.prompt = PromptTemplate.from_template(prompt_template)
        
        # Set up the chain as a modular pipeline
        self.rag_chain = (
            {"context": self.retriever.get_retriever() | self.format_docs_with_history, "question": RunnablePassthrough()}
            | self.prompt
            | self.generator.llm
            | StrOutputParser()
        )

    def preview_prompt(self, question):
        """
        Returns the prompt that will be passed to the LLM without invoking the generation step.

        Parameters:

        - question: str, the question to be previewed.

        Returns:

        - str: The formatted prompt with history and context.

        """
        # Retrieve documents and format them with history
        docs = self.retriever.get_retriever().invoke(question)
        context, _ = self.format_docs_with_history(docs)  # Only need context for preview

        # Format the full prompt
        prompt_text = self.prompt.format(question=question, context=context)
        return prompt_text

    def get_response(self, question):
        """
        Fetches a response to the user's query using the RAG pipeline, including conversation history.

        Parameters:

        - question: str, the question to be answered.

        Returns:

        - str: The generated response with sources for reference.

        """
        if not hasattr(self, 'rag_chain'):
            raise ValueError("RAG pipeline is not set up. Call setup_pipeline() first.")
        
        # Retrieve documents and format them with history
        docs = self.retriever.get_retriever().invoke(question)
        _, sources = self.format_docs_with_history(docs)
        
        # Generate response
        response = self.rag_chain.invoke(question)
        
        # Add current question and response to history
        # Record history only if enabled
        if self.use_history:
            self.history.append((question, response))
        
        # Update history **only if it's not already added**
        if self.use_history:
            if len(self.history) == 0 or self.history[-1] != (question, response):
                self.history.append((question, response))

            # Keep only the last `max_history` pairs
            self.history = self.history[-self.max_history:]

        # Deduplicate sources
        unique_sources = list(set(sources))
        
        # Format sources text
        sources_text = "For further reference, look at:\n" + "\n".join(f"- {src}" for src in unique_sources)
        
        # Return response with sources
        return f"{response}\n\n{sources_text}"
