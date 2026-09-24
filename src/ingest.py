import os
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

def process_and_store_docs():
    file_path = "data/tech_manual.txt"
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} File not found!")
        return

    print("1. Loading Document...")
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    
    documents = [Document(page_content=text, metadata={"source": file_path})]

    print("2. Splitting Document into Small Chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Total Chunks Created: {len(chunks)}")

    print("3. Generating Vector Embeddings & Saving to ChromaDB...")
    db = Chroma.from_documents(
        documents=chunks,
        persist_directory="vector_db"
    )
    print("SUCCESS: Vector Database Created Successfully in 'vector_db/' directory!")

if __name__ == "__main__":
    process_and_store_docs()