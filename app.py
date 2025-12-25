from flask import Flask, request, send_from_directory
import subprocess, os

app = Flask(__name__)

UPLOAD_FOLDER = "/tmp/uploads"
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
        [
            "cppcheck",
            "--enable=all",
            "--suppress=missingIncludeSystem",
            filepath
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    return result.stderr or "No issues found."

app.run(host="0.0.0.0", port=5000)
