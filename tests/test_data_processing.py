# tests/test_data_processing.py
import pytest
import os
from unittest.mock import patch, MagicMock
from rag_skeleton.data_processing import DataProcessor
from langchain.schema import Document


@pytest.fixture
def data_processor():
    """Fixture for DataProcessor with a test path."""
    return DataProcessor(vectordb_path="test_vectordb", data_path="test_data")


@patch("rag_skeleton.data_processing.PyMuPDFLoader")
def test_load_documents(mock_loader, data_processor):
    """Test the load_documents method."""
    # Mocking file loading
    mock_doc = MagicMock()
    mock_loader.return_value.load.return_value = [mock_doc]

    # Creating fake files
    os.makedirs("test_data", exist_ok=True)
    with open("test_data/test1.pdf", "w") as f:
        f.write("fake content")

    try:
        docs = data_processor.load_documents()
        assert len(docs) == 1  # Check if one document was loaded
    finally:
        # Cleanup
        os.remove("test_data/test1.pdf")
        os.rmdir("test_data")


def test_split_documents(data_processor):
    """Test the split_documents method."""
    mock_docs = [Document(page_content="Some long text to split", metadata={})]
    chunks = data_processor.split_documents(mock_docs, chunk_size=10, chunk_overlap=2)
    assert len(chunks) > 0  # Ensure the documents are split into chunks
    assert all(isinstance(chunk, Document) for chunk in chunks)  # Ensure output is a list of Document objects


@patch("rag_skeleton.data_processing.Chroma")
def test_create_vector_db(mock_chroma, data_processor):
    """Test the create_vector_db method."""
    mock_docs = [{"page_content": "Some text"}]
    data_processor.create_vector_db(mock_docs)
    mock_chroma.from_documents.assert_called_once()  # Ensure Chroma is called