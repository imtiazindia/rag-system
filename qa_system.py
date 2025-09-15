# qa_system.py
import os
from langchain.llms import OpenAI  # ← Correct import
from langchain.chains import RetrievalQA
from config import LLM_MODEL

def setup_qa_chain(vector_store):
    llm = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"), 
        model_name=LLM_MODEL,
        temperature=0.1
    )
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True
    )
    return qa_chain
