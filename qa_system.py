# qa_system.py
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA
from config import LLM_MODEL, SEARCH_KWARGS

def setup_qa_chain(vector_store):
    """Set up the question-answering system"""
    llm = OllamaLLM(model=LLM_MODEL)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs=SEARCH_KWARGS),
        return_source_documents=True
    )
    return qa_chain
