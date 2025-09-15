# vector_store.py
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from config import CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL

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
    """Create vector store with in-memory database"""
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    
    # Use in-memory database - NO persist_directory parameter
    vector_store = Chroma.from_documents(
        documents=docs, 
        embedding=embeddings
        # REMOVED: persist_directory parameter entirely
    )
    return vector_store
