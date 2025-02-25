import os
from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Replace this with your generated key
SECRET_KEY = b'YOUR_GENERATED_KEY_HERE'
cipher = Fernet(SECRET_KEY)

def encrypt_file(file_path):
    """Encrypt a file using Fernet encryption."""
    with open(file_path, "rb") as file:
        encrypted_data = cipher.encrypt(file.read())

    encrypted_path = file_path + ".enc"
    with open(encrypted_path, "wb") as encrypted_file:
        encrypted_file.write(encrypted_data)

    return encrypted_path

def decrypt_file(file_path):
    """Decrypt a file using Fernet encryption."""
    with open(file_path, "rb") as encrypted_file:
        decrypted_data = cipher.decrypt(encrypted_file.read())

    original_path = file_path.replace(".enc", "_decrypted")
    with open(original_path, "wb") as decrypted_file:
        decrypted_file.write(decrypted_data)

    return original_path

@app.route("/", methods=["GET", "POST"])
def home():
    encrypted_file = None
    decrypted_file = None

    if request.method == "POST":
        file = request.files["file"]
        action = request.form.get("action")

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            if action == "encrypt":
                encrypted_file = encrypt_file(filepath)
            elif action == "decrypt":
                encrypted_file = decrypt_file(filepath)

    return render_template("index.html", encrypted_file=encrypted_file, decrypted_file=decrypted_file)

@app.route("/download/<filename>")
def download_file(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
