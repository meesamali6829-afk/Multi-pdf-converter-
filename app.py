import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from groq import Groq
from pypdf import PdfReader

app = Flask(__name__, template_folder='templates')
CORS(app)

# 🔥 70B Model for Extreme Speed
client = Groq(api_key="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")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ai_refine', methods=['POST'])
def ai_refine():
    try:
        data = request.json
        prompt = data.get('text', '')
        # AI formatting for professional look
        res = client.chat.completions.create(
            messages=[{"role": "system", "content": "Format this content into a professional, structured document. Use headings if needed."}],
            model="llama3-70b-8192"
        )
        return jsonify({"refined": res.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/pdf_to_text', methods=['POST'])
def pdf_to_text():
    try:
        file = request.files['file']
        reader = PdfReader(file)
        text = "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
        # Cleaning OCR errors with AI
        clean = client.chat.completions.create(
            messages=[{"role": "system", "content": "Fix all OCR and spelling errors in this text."}, {"role": "user", "content": text}],
            model="llama3-70b-8192"
        )
        return jsonify({"text": clean.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": "AI Extraction Failed"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
