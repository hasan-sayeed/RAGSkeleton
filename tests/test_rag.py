# tests/test_rag.py
from unittest.mock import patch
from rag_skeleton.rag import RAGPipeline
from langchain.schema import Document
from langchain_core.runnables.base import RunnableSequence


@patch("rag_skeleton.rag.DocumentRetriever")
@patch("rag_skeleton.rag.TextGenerator")
@patch.object(RunnableSequence, "invoke", return_value="Test response")
def test_rag_pipeline(mock_runnable_invoke, mock_generator_class, mock_retriever_class):
    """Test the RAG pipeline's integration."""
    # Mock retriever behavior
    mock_retriever = mock_retriever_class.return_value.get_retriever.return_value
    mock_retriever.invoke.return_value = [
        Document(page_content="Relevant content", metadata={"source": "Test Source"})
    ]

    # Mock generator behavior
    mock_generator = mock_generator_class.return_value
    mock_generator.llm.invoke.return_value = "Test response"

    # Create RAGPipeline instance with mocked classes
    rag_pipeline = RAGPipeline()
    rag_pipeline.setup_pipeline()

    # Call the method
    response = rag_pipeline.get_response("Test question")

    # Assert the main response and metadata
    assert "Test response" in response, "The RAG pipeline did not return the expected main response."
    assert "For further reference, look at:\n- Test Source" in response, "The RAG pipeline did not include the expected metadata."
