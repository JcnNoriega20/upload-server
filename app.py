from flask import Flask, request, jsonify
import base64
import requests

app = Flask(__name__)

# ===============================
# ⚠️ EDITA ESTO CON TU TOKEN Y USUARIO
# ===============================
GITHUB_TOKEN = "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"
GITHUB_REPO = "JcnNoriega20/fotos-accesos"
# ===============================


@app.route("/upload", methods=["POST"])
def upload():
    try:
        image_base64 = request.form.get("image")
        filename = request.form.get("filename")

        if not image_base64 or not filename:
            return jsonify({"status": "error", "message": "Faltan parámetros"}), 400

        # Decodificar la imagen Base64
        image_bytes = base64.b64decode(image_base64)

        # Subir archivo a GitHub
        api_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{filename}"

        payload = {
            "message": f"Upload {filename}",
            "content": base64.b64encode(image_bytes).decode("utf-8")
        }

        headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Content-Type": "application/json"
        }

        response = requests.put(api_url, json=payload, headers=headers)

        if response.status_code in [200, 201]:
            return jsonify({"status": "success", "file": filename}), 200

        else:
            return jsonify({
                "status": "error",
                "github_response": response.text
            }), 400

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/", methods=["GET"])
def home():
    return "Servidor activo para recibir fotos Base64 de la ESP32-CAM", 200
