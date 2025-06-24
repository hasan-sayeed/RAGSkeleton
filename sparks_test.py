import os
import shutil
import json
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableMap

# Clean vector store directory
if os.path.exists("vectordb"):
    print("🧹 Deleted old vector DB at vectordb")
    shutil.rmtree("vectordb")

# Load transcripts
docs = []
for file in os.listdir("AskSparks/transcripts_lectures_large"):
    if not file.endswith(".json"):
        continue
    with open(os.path.join("AskSparks/transcripts_lectures_large", file), "r", encoding="utf-8") as f:
        data = json.load(f)
    for entry in data["segments"]:
        start = entry["start"]
        end = entry["end"]
        text = entry["text"].strip()
        if not text:
            continue
        yt_id = os.path.splitext(file)[0]
        metadata = {
            "source": f"https://www.youtube.com/watch?v={yt_id}&t={int(start)}s",
            "start": start,
            "end": end
        }
        docs.append(Document(page_content=text, metadata=metadata))

print(f"📄 Loaded {len(docs)} transcript segments")

# Split text
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
splits = splitter.split_documents(docs)

# Embed documents
embedding_fn = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectordb = Chroma.from_documents(splits, embedding=embedding_fn, persist_directory="vectordb")

# Load retriever
retriever = vectordb.as_retriever()

# Define prompt
template = """You are a helpful TA. Answer the question using the lecture transcript below.
If you use a transcript segment, include the clickable YouTube link.
Question: {question}
Transcript:
{context}
Answer:"""

prompt = PromptTemplate.from_template(template)
llm = OllamaLLM(model="phi3:mini")

# Define chain
def format_docs(docs):
    return "\n\n".join(
        f"{doc.page_content}\n🔗 {doc.metadata['source']}" for doc in docs
    )

rag_chain = RunnableMap({
    "context": retriever | format_docs,
    "question": RunnablePassthrough()
}) | prompt | llm

# Ask a sample question
question = "What's the difference between ionic and covalent bonding?"
print("💬 Answer:")
print(rag_chain.invoke(question))
