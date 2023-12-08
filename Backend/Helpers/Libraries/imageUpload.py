import os
from flask import Flask, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

def allowed_file(filename):
    allowed_extensions = {'jpg', 'jpeg', 'png', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']

    if file.filename == '':
        return "No selected file", 400

    if file and allowed_file(file.filename):
        root_dir = os.path.dirname(os.path.abspath(__file__))
        if file.fieldname == "photo":
            upload_folder = os.path.join(root_dir, "static/userPhotos")
        else:
            upload_folder = os.path.join(root_dir, "static/storyImages")

        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        if file.fieldname == "photo":
            filename = "photo_user_" + str(request.form.get('user_id')) + secure_filename(file.filename)
            saved_path = os.path.join(upload_folder, filename)
            file.save(saved_path)
            return "File uploaded successfully: " + filename
        else:
            filename = "image_" + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + secure_filename(file.filename)
            saved_path = os.path.join(upload_folder, filename)
            file.save(saved_path)
            return "File uploaded successfully: " + filename

    else:
        return "Invalid file type", 400

if __name__ == '__main__':
    app.run(debug=True)
