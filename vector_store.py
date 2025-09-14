# vector_store.py
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from config import CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL, VECTOR_STORE_PATH

def split_text(text):
    """Split text into manageable chunks"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return [Document(page_content=chunk) for chunk in chunks]

def create_vector_store(docs):
    """Create or update vector store with documents"""
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vector_store = Chroma.from_documents(docs, embeddings, persist_directory=VECTOR_STORE_PATH)
    return vector_store

def load_vector_store():
    """Load existing vector store"""
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return Chroma(persist_directory=VECTOR_STORE_PATH, embedding_function=embeddings)
