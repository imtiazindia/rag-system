# main.py
import streamlit as st
import os
import tempfile
from file_processor import extract_text_from_files, get_supported_files
from vector_store import split_text, create_vector_store
from qa_system import setup_qa_chain
from config import SUPPORTED_EXTENSIONS, LLM_MODEL

# Set page configuration
st.set_page_config(
    page_title="AI Document Assistant",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = None
if 'processed_files' not in st.session_state:
    st.session_state.processed_files = []

def main():
    # Header
    st.title("🤖 AI Document Assistant")
    st.markdown(f"**Using AI Model:** {LLM_MODEL}")
    st.markdown("---")
    
    # Sidebar for file upload
    with st.sidebar:
        st.header("📁 Document Management")
        
        # Option 1: Upload files
        st.subheader("Upload Files")
        uploaded_files = st.file_uploader(
            "Choose files",
            type=[ext.replace('.', '') for ext in SUPPORTED_EXTENSIONS],
            accept_multiple_files=True
        )
        
        # Option 2: Select folder
        st.subheader("Or Select Folder")
        folder_path = st.text_input("Folder path", r"C:\Users\Admin\my_pdfs")
        process_folder = st.button("Process Folder")
    
    # Main content area
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.header("⚙️ Processing")
        
        files_to_process = []
        
        # Handle uploaded files
        if uploaded_files:
            # Save uploaded files to temporary directory
            temp_dir = tempfile.mkdtemp()
            for uploaded_file in uploaded_files:
                file_path = os.path.join(temp_dir, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                files_to_process.append(file_path)
            
            st.success(f"📄 {len(uploaded_files)} file(s) ready for processing")
        
        # Handle folder processing
        if process_folder and folder_path:
            if os.path.exists(folder_path):
                files_to_process = get_supported_files(folder_path)
                st.success(f"📁 Found {len(files_to_process)} file(s) in folder")
            else:
                st.error("❌ Folder path does not exist")
        
        # Process files button
        if files_to_process:
            if st.button("🚀 Process Documents", type="primary"):
                with st.spinner("Processing documents..."):
                    try:
                        # Extract text
                        text = extract_text_from_files(files_to_process)
                        
                        if not text.strip():
                            st.error("❌ No extractable text found in files")
                            return
                        
                        # Split into chunks
                        docs = split_text(text)
                        
                        # Create vector store
                        st.session_state.vector_store = create_vector_store(docs)
                        st.session_state.processed_files = [os.path.basename(f) for f in files_to_process]
                        
                        st.success(f"✅ Processed {len(files_to_process)} file(s), created {len(docs)} chunks")
                        
                    except Exception as e:
                        st.error(f"❌ Error processing files: {str(e)}")
    
    with col2:
        st.header("💬 Ask Questions")
        
        # Show processed files
        if st.session_state.processed_files:
            st.markdown("**Processed Files:**")
            for file in st.session_state.processed_files:
                st.markdown(f"- {file}")
            st.markdown("---")
        
        # Question input
        question = st.text_input(
            "Enter your question:",
            placeholder="What would you like to know about your documents?"
        )
        
        # Ask button
        if question and st.session_state.vector_store:
            if st.button("🔍 Get Answer", type="primary"):
                with st.spinner("Thinking..."):
                    try:
                        qa_chain = setup_qa_chain(st.session_state.vector_store)
                        result = qa_chain.invoke({"query": question})
                        
                        # Display answer
                        st.subheader("📘 Answer:")
                        st.write(result["result"])
                        
                        # Display sources (collapsible)
                        with st.expander("🔍 View Source Documents"):
                            for i, doc in enumerate(result["source_documents"]):
                                st.markdown(f"**Source {i+1}:**")
                                st.text(doc.page_content[:500] + "..." if len(doc.page_content) > 500 else doc.page_content)
                                st.markdown("---")
                                
                    except Exception as e:
                        st.error(f"❌ Error getting answer: {str(e)}")
        elif question and not st.session_state.vector_store:
            st.warning("⚠️ Please process documents first before asking questions")
        
        # Clear button
        if st.session_state.vector_store:
            if st.button("🗑️ Clear Documents", type="secondary"):
                st.session_state.vector_store = None
                st.session_state.processed_files = []
                st.success("✅ Documents cleared. You can process new ones.")

# Footer
st.markdown("---")
st.markdown("*Built with Streamlit, LangChain, and Ollama*")

if __name__ == "__main__":
    main()