# Copilot Instructions for `rag_system`

## Project Overview
This is a document-based Retrieval-Augmented Generation (RAG) system for question answering over local files. The architecture is modular, with clear separation of concerns:
- **File Processing** (`file_processor.py`): Extracts text from `.pdf`, `.docx`, and `.txt` files using format-specific logic. Handles errors and unsupported formats gracefully.
- **Vector Store** (`vector_store.py`): Splits extracted text into chunks, embeds them using HuggingFace models, and stores them in a persistent Chroma vector database.
- **QA System** (`qa_system.py`): Sets up a LangChain RetrievalQA pipeline using Ollama LLM for answering user queries based on retrieved document chunks.
- **Configuration** (`config.py`): Centralizes all tunable parameters (chunk size, embedding/LLM models, vector store path, retrieval settings).
- **Main Entrypoint** (`main.py`): Orchestrates the workflow: file discovery, text extraction, chunking, vectorization, and interactive Q&A loop.

## Key Patterns & Conventions
- **Supported File Types**: Only `.pdf`, `.docx`, and `.txt` (see `SUPPORTED_EXTENSIONS` in `config.py`).
- **Error Handling**: All file operations print clear error messages and continue processing other files.
- **Chunking**: Text is split using `RecursiveCharacterTextSplitter` with parameters from `config.py`.
- **Embeddings**: Uses HuggingFace model specified in `EMBEDDING_MODEL`.
- **Vector Store**: Chroma DB is persisted at `VECTOR_STORE_PATH`.
- **LLM**: Uses Ollama LLM (model name in `LLM_MODEL`).
- **Retrieval**: Number of chunks retrieved is set by `SEARCH_KWARGS`.
- **Interactive Loop**: Main script runs a CLI loop for user questions; type 'quit' to exit.

## Developer Workflows
- **Run the System**: Execute `main.py` directly. No build step required.
- **Add New File Types**: Extend `extract_text_from_file` in `file_processor.py` and update `SUPPORTED_EXTENSIONS`.
- **Change Embedding/LLM Models**: Update `EMBEDDING_MODEL` or `LLM_MODEL` in `config.py`.
- **Debugging**: Use print statements; errors are surfaced in CLI output.
- **Dependencies**: Requires `langchain`, `langchain_community`, `langchain_huggingface`, `langchain_ollama`, `PyPDF2`, `docx`, and `Chroma`.

## Integration Points
- **External Models**: HuggingFace for embeddings, Ollama for LLM.
- **Vector DB**: Chroma (local persistence).
- **LangChain**: Used for text splitting, document schema, and QA pipeline.

## Example Workflow
1. Place supported files in the target folder (default: `C:\Users\Admin\my_pdfs`).
2. Run `main.py`.
3. System extracts, chunks, embeds, and stores document data.
4. User interacts via CLI to ask questions about the documents.

## References
- See `file_processor.py` for file handling logic and error patterns.
- See `vector_store.py` for chunking and vector DB setup.
- See `qa_system.py` for QA pipeline configuration.
- See `config.py` for all tunable parameters.

---
**Feedback:** If any section is unclear or missing, please specify which part needs improvement or more detail.
