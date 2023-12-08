import os
from flask import Flask

app = Flask(__name__)

def delete_image_file(delete_image):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(root_dir, f"public/storyImages/{delete_image}")

    try:
        os.remove(file_path)
        print("File deleted successfully")
    except OSError as e:
        print(f"Error deleting file: {e}")

if __name__ == "__main__":
    app.run(debug=True)
