import os
import pdfplumber
import docx
import fitz  # PyMuPDF
from docx import Document
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {"pdf", "docx"}

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"
    return text.strip()

def extract_text_from_docx(docx_path):
    """Extract text from a DOCX file."""
    doc = docx.Document(docx_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text.strip()

def process_resume_file(file, upload_folder):
    """Handles file saving and text extraction."""
    if file.filename == "" or not allowed_file(file.filename):
        return None, None

    filename = secure_filename(file.filename)
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)

    file_extension = filename.rsplit(".", 1)[1].lower()
    
    if file_extension == "pdf":
        extracted_text = extract_text_from_pdf(file_path)
        links = extract_links_from_pdf(file_path)
    elif file_extension == "docx":
        print("DOCX file detected")
        extracted_text = extract_text_from_docx(file_path)
        links = extract_links_from_docx(file_path)
        print(links)
    else:
        return None, None

    return extracted_text, links, filename

def extract_links_from_pdf(pdf_path):
    links = []
    doc = fitz.open(pdf_path)

    for page in doc:
        for link in page.get_links():
            if "uri" in link:  # Extract only actual links
                links.append(link["uri"])

    return links

def extract_links_from_docx(docx_path):
    doc = Document(docx_path)
    links = []
    
    # Extract hyperlinks from the document
    for rel in doc.part.rels.values():
        if "hyperlink" in rel.reltype:
            links.append(rel.target_ref)
    
    return links
