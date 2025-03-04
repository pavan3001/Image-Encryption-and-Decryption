from flask import Flask, render_template_string, request, send_from_directory
from encryption import encrypt_image, decrypt_image
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'original'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'encrypted'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'decrypted'), exist_ok=True)

CSS_STYLE = """
<style>
    body { font-family: Arial, sans-serif; background-color: #1e1e1e; color: white; text-align: center; padding: 20px; }
    .container { display: flex; justify-content: center; gap: 20px; }
    .box { width: 300px; background: #333; padding: 20px; border-radius: 10px; text-align: center; }
    h1 { color: #ffcc00; }
    button { background-color: #ff5733; color: white; border: none; padding: 10px 20px; cursor: pointer; border-radius: 5px; }
    button:hover { background-color: #c70039; }
    input { padding: 10px; width: 90%; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; }
</style>
"""

@app.route('/')
def index():
    return render_template_string(f"""
        {CSS_STYLE}
        <h1>Image Encryption & Decryption</h1>
        <div class="container">
            <div class="box">
                <h2>Encrypt</h2>
                <button onclick="window.location.href='/encrypt'">Go to Encrypt</button>
            </div>
            <div class="box">
                <h2>Decrypt</h2>
                <button onclick="window.location.href='/decrypt'">Go to Decrypt</button>
            </div>
        </div>
    """)

@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt():
    if request.method == 'POST':
        file = request.files['image']
        if file:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'original', file.filename)
            file.save(image_path)
            encrypted_path, key = encrypt_image(image_path)
            encrypted_file_name = os.path.basename(encrypted_path)
            return render_template_string(f"""
                {CSS_STYLE}
                <div class="box">
                    <h1>Encrypted Image</h1>
                    <p>Encryption Key: {key}</p>
                    <button onclick="window.location.href='/'">Home</button>
                </div>
            """)
    return render_template_string(f"""
        {CSS_STYLE}
        <div class="box">
            <h1>Encrypt an Image</h1>
            <form method="post" enctype="multipart/form-data">
                <input type="file" name="image" required>
                <button type="submit">Encrypt</button>
            </form>
        </div>
    """)

@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt():
    if request.method == 'POST':
        file = request.files['encrypted_image']
        key = request.form['key']
        if file and key:
            encrypted_path = os.path.join(app.config['UPLOAD_FOLDER'], 'encrypted', file.filename)
            file.save(encrypted_path)
            decrypted_path = decrypt_image(encrypted_path, key)
            decrypted_file_name = os.path.basename(decrypted_path)
            return render_template_string(f"""
                {CSS_STYLE}
                <div class="box">
                    <h1>Decrypted Image</h1>
                    <button onclick="window.location.href='/'">Home</button>
                </div>
            """)
    return render_template_string(f"""
        {CSS_STYLE}
        <div class="box">
            <h1>Decrypt an Image</h1>
            <form method="post" enctype="multipart/form-data">
                <input type="file" name="encrypted_image" required>
                <input type="text" name="key" placeholder="Enter Encryption Key" required>
                <button type="submit">Decrypt</button>
            </form>
        </div>
    """)

@app.route('/download/<path:filename>')
def download_file(filename):
    folder = ''
    if 'original' in filename:
        folder = 'original'
    elif 'encrypted' in filename:
        folder = 'encrypted'
    elif 'decrypted' in filename:
        folder = 'decrypted'
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], folder), filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
