# vector_store.py
from langchain_community.vectorstores import FAISS

def create_vector_store(docs):
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vector_store = FAISS.from_documents(docs, embeddings)
    return vector_store
