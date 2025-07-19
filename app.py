from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
