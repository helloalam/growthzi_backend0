from flask import Flask, request, jsonify, url_for
from werkzeug.utils import secure_filename
from datetime import datetime,timezone
from flask import send_from_directory;
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# api for image upload

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

def require_user_context():
    def decorator(f):
        def wrapped(*args, **kwargs):
            return f(*args, **kwargs)
        return wrapped
    return decorator

@app.route("/upload", methods=["POST"])
@require_user_context()
def upload_file():
    if "image" not in request.files or "image_id" not in request.form:
        print("[ERROR] Invalid upload request: Missing image or image_id")
        return jsonify({"error": "Invalid request"}), 400

    file = request.files["image"]
    image_id = request.form["image_id"]

    if file.filename == "":
        print(f"[ERROR] No file selected for image_id: {image_id}")
        return jsonify({"error": "No file selected"}), 400

    filename = secure_filename(f"{image_id}_{file.filename}")
    save_path = os.path.join(UPLOAD_FOLDER, filename)

    try:
        file.save(save_path)
        file_url = request.url_root.rstrip('/') + url_for('uploaded_file', filename=filename)
        print(f"[SUCCESS] Image uploaded: {file_url}")
        return jsonify({
            "url": file_url,
            "image_id": image_id,
            "local_path": save_path,
            "uploaded_at": datetime.now(timezone.utc).isoformat()
        }), 200

    except Exception as e:
        print(f"[ERROR] Upload failed: {str(e)}")
        return jsonify({"error": f"Upload failed: {str(e)}"}), 500

@app.route("/update-section", methods=["POST"])
def log_edit():
    try:
        data = request.get_json()
        print("FRONTEND EDIT DETECTED")
        print(f"Component: {data.get('component')}")
        print(f"Field: {data.get('field')}")
        print("New Value:", data.get('value'))
        print("-" * 50)
        return jsonify({"message": "Edit logged successfully"}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
