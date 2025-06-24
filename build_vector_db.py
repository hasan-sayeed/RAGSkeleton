# build_vector_db.py

import os
import shutil
from langchain_community.document_loaders import JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Clean up old DB if it exists
DB_DIR = "vectordb"
if os.path.exists(DB_DIR):
    shutil.rmtree(DB_DIR)
    print("🧹 Deleted old vector DB at", DB_DIR)

# Load transcript segments
loader = JSONLoader(
    file_path="../../transcripts_lectures_large/transcripts.json",  # adjust path as needed
    jq_schema=".segments[]",
    text_content=False
)
docs = loader.load()
print(f"📄 Loaded {len(docs)} transcript segments")

# Chunk the text
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
splits = splitter.split_documents(docs)

# Embed & save
embedding_fn = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
Chroma.from_documents(splits, embedding=embedding_fn, persist_directory=DB_DIR).persist()
print("✅ Vector DB built and saved to", DB_DIR)
