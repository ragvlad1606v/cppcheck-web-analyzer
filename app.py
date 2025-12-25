from flask import Flask, send_from_directory, request
import subprocess, os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED = (".c", ".cpp", ".h")

@app.route("/")
def home():
    return send_from_directory("templates", "index.html")

@app.route("/scan", methods=["POST"])
def scan():
    file = request.files.get("file")

    if not file or not file.filename.endswith(ALLOWED):
        return "Only C / C++ files are allowed."

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    result = subprocess.run(
        ["cppcheck", "--enable=all", filepath],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    return result.stderr

app.run(host="0.0.0.0", port=5000)
