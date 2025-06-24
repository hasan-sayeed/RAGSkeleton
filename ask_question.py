# ask_question.py

import time
from langchain.chains import RetrievalQAWithSourcesChain
from langchain_ollama import Ollama
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate

# Load vector DB
embedding_fn = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectordb = Chroma(persist_directory="vectordb", embedding_function=embedding_fn)
retriever = vectordb.as_retriever(search_kwargs={"k": 4})

# Load LLM
llm = Ollama(model="phi3:mini")

# Optional: prompt template
prompt_template = PromptTemplate.from_template("""
Use the following transcript excerpts to answer the question. Provide specific, concise answers. Add clickable YouTube timestamp links if possible.

{context}

Question: {question}
Answer:""")

# Run retrieval + LLM
qa = RetrievalQAWithSourcesChain.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt_template}
)

# Ask question
question = "What's the difference between ionic and covalent bonding?"
start = time.time()
result = qa.invoke({"question": question})
end = time.time()

# Format answer and clickable links
print("\n💬 Answer:\n", result["answer"])

if "source_documents" in result:
    print("\n📚 Sources:")
    for doc in result["source_documents"]:
        metadata = doc.metadata
        url = metadata.get("url", "")
        start = metadata.get("start", "")
        end_time = metadata.get("end", "")
        if url and start:
            ts = int(float(start))
            link = f"https://www.youtube.com/watch?v={url}&t={ts}s"
            print(f" - [{url} @ {ts}s]({link})")

print(f"\n⏱️ Response time: {end - start:.2f} seconds")
