from flask import Flask, request, jsonify
from flask_cors import CORS
import pdfplumber
import os
import docx
from werkzeug.utils import secure_filename
from flasgger import Swagger

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

app = Flask(__name__)
swagger = Swagger(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()

def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text.strip()

@app.route("/", methods=["GET"])
def home():
    """
    Resume Analyzer API Home
    ---
    responses:
      200:
        description: API is running successfully
    """
    return jsonify({"message": "Resume Analyzer API is running!"})

@app.route("/upload", methods=["POST"])
def upload_resume():
    """
    Upload a resume file (PDF or DOCX) and extract text.
    ---
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: The resume file to upload (PDF or DOCX).
    responses:
      200:
        description: Successfully extracted text from the resume
        schema:
          type: object
          properties:
            filename:
              type: string
              description: The uploaded filename
            extracted_text:
              type: string
              description: Extracted text from the resume
      400:
        description: Bad request (invalid file or missing file)
    """
    if "file" not in request.files:
        return jsonify({"error": "No file part in request"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        file_extension = filename.rsplit(".", 1)[1].lower()
        if file_extension == "pdf":
            extracted_text = extract_text_from_pdf(file_path)
        elif file_extension == "docx":
            extracted_text = extract_text_from_docx(file_path)
        else:
            return jsonify({"error": "Unsupported file format"}), 400

        return jsonify({"filename": filename, "extracted_text": extracted_text})

    return jsonify({"error": "Invalid file type"}), 400

if __name__ == "__main__":
    app.run(debug=True)