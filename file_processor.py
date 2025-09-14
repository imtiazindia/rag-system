# file_processor.py
import PyPDF2
import os
import docx
from langchain.schema import Document
from config import SUPPORTED_EXTENSIONS

def extract_text_from_file(file_path):
    """Extract text from a single file based on its extension"""
    file_extension = os.path.splitext(file_path)[1].lower()
    
    try:
        if file_extension == '.pdf':
            return extract_text_from_pdf(file_path)
        elif file_extension == '.docx':
            return extract_text_from_docx(file_path)
        elif file_extension == '.txt':
            return extract_text_from_txt(file_path)
        else:
            print(f"⚠️  Unsupported file type: {file_extension}")
            return ""
    except Exception as e:
        print(f"❌ Error processing {os.path.basename(file_path)}: {e}")
        return ""

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    print(f"📖 Reading PDF: {os.path.basename(pdf_path)}...")
    
    if os.path.getsize(pdf_path) == 0:
        print(f"⚠️  Empty PDF file: {os.path.basename(pdf_path)}")
        return ""
    
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            if len(reader.pages) == 0:
                print(f"⚠️  PDF has no pages: {os.path.basename(pdf_path)}")
                return ""
            
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
            return text
    except Exception as e:
        print(f"❌ Failed to read PDF {os.path.basename(pdf_path)}: {e}")
        return ""

def extract_text_from_docx(docx_path):
    """Extract text from Word document"""
    print(f"📖 Reading Word: {os.path.basename(docx_path)}...")
    
    if os.path.getsize(docx_path) == 0:
        print(f"⚠️  Empty Word file: {os.path.basename(docx_path)}")
        return ""
    
    try:
        doc = docx.Document(docx_path)
        text = ""
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text += paragraph.text + "\n\n"
        return text
    except Exception as e:
        print(f"❌ Failed to read Word document {os.path.basename(docx_path)}: {e}")
        return ""

def extract_text_from_txt(txt_path):
    """Extract text from text file with encoding detection"""
    print(f"📖 Reading Text: {os.path.basename(txt_path)}...")
    
    if os.path.getsize(txt_path) == 0:
        print(f"⚠️  Empty text file: {os.path.basename(txt_path)}")
        return ""
    
    encodings = ['utf-8', 'utf-16', 'latin-1', 'cp1252', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            with open(txt_path, 'r', encoding=encoding) as file:
                content = file.read()
                if content.strip():
                    return content
                else:
                    print(f"⚠️  Empty text content: {os.path.basename(txt_path)}")
                    return ""
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"⚠️  Error reading {txt_path} with {encoding}: {e}")
            continue
    
    print(f"❌ Failed to read text file {os.path.basename(txt_path)} with any encoding")
    return ""

def extract_text_from_files(file_paths):
    """Extract text from multiple files with error handling"""
    all_text = ""
    successful_files = 0
    
    for file_path in file_paths:
        file_text = extract_text_from_file(file_path)
        if file_text and file_text.strip():
            all_text += file_text + "\n\n"
            successful_files += 1
        else:
            print(f"⚠️  Skipping {os.path.basename(file_path)} (no extractable content)")
    
    print(f"✅ Successfully processed {successful_files} out of {len(file_paths)} files")
    return all_text

def get_supported_files(folder_path):
    """Get all supported files from a folder"""
    file_paths = []
    for f in os.listdir(folder_path):
        file_path = os.path.join(folder_path, f)
        if os.path.isfile(file_path):
            file_extension = os.path.splitext(f)[1].lower()
            if file_extension in SUPPORTED_EXTENSIONS:
                file_paths.append(file_path)
    return file_paths
