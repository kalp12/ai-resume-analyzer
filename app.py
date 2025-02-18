from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from
from utils.file_handler import process_resume_file
from utils.nlp_processor import analyze_resume_mistral,analyze_resume_gemma
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
# Initialize Swagger
swagger = Swagger(app)

@app.route('/greet', methods=['get'])
@swag_from('swag/greet.yml')  # Link the Swagger YAML file
def greet_user():
    name = request.args.get('name')
    
    if name:
        return jsonify({"message": f"Hi, Good morning {name}!"})
    else:
        return jsonify({"error": "Name parameter is missing"}), 400
    
@app.route("/upload_check_file", methods=["POST"])
@swag_from("swag/upload_check_file.yml")  # Ensure correct path to `upload.yml`
def upload_check_file():
    """ Upload Resume """
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    filename = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filename)

    return jsonify({"message": "File uploaded", "filename": file.filename})


@app.route("/upload_resume", methods=["POST"])
@swag_from("swag/upload_resume.yml")  # Ensure correct path to the YAML file
def upload_resume():
    """ Upload and analyze a resume """
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    extracted_text, links , filename = process_resume_file(file, app.config["UPLOAD_FOLDER"])

    if extracted_text is None:
        return jsonify({"error": "Unsupported file format"}), 400

    # analysis = analyze_resume_gemma(extracted_text,links)

    return jsonify({
        "filename": filename,
        "links": links,
        "extracted_text": extracted_text,
        
    })
# v"skills": analysis["skills"],
#         "experience": analysis["experience"],
#         "job_titles": analysis["job_titles"]

if __name__ == '__main__':
    app.run(debug=True)
