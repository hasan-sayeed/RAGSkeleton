# tests/test_retrieval.py
from unittest.mock import patch
from rag_skeleton.retrieval import DocumentRetriever


@patch("rag_skeleton.retrieval.Chroma")
def test_get_retriever(mock_chroma):
    """Test the get_retriever method."""
    DocumentRetriever().get_retriever()
    assert mock_chroma.return_value.as_retriever.called  # Check if retriever was created