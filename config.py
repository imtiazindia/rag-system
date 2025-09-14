# config.py
SUPPORTED_EXTENSIONS = ['.pdf', '.docx', '.txt']
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100
VECTOR_STORE_PATH = "./pdf_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
#LLM_MODEL = "llama2"
LLM_MODEL = "mistral"
SEARCH_KWARGS = {"k": 3}  # Number of chunks to retrieve
