from flask import Flask, request, jsonify
import fitz  # PyMuPDF

app = Flask(__name__)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    try:
        pdf_document = fitz.open(pdf_path)
        full_text = ""
        
        # Extract text from all pages of the PDF
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)  # Load each page
            full_text += page.get_text("text")  # Extract text in plain text format
        
        pdf_document.close()
        return full_text  # Return full text from all pages
    except Exception as e:
        return str(e)

# API route to handle PDF upload and text extraction
@app.route("/extract_text", methods=["POST"])
def extract_text():
    try:
        # Check if a file was uploaded
        if "pdf_file" not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files["pdf_file"]
        
        # Save the uploaded file temporarily
        file_path = f"uploads/{file.filename}"
        file.save(file_path)

        # Extract text from the uploaded PDF
        extracted_text = extract_text_from_pdf(file_path)
        
        return jsonify({"extracted_text": extracted_text})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
