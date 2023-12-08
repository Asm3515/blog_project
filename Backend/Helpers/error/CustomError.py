from flask import Flask, jsonify

class CustomError(Exception):

    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code

app = Flask(__name__)

@app.route('/')
def index():
    try:
        # Your Express.js code logic goes here
        # For example, if an error occurs, you can raise the CustomError
        raise CustomError("An error occurred", 500)
        
        return jsonify({"message": "Success"})
    except CustomError as e:
        return jsonify({"error": str(e)}), e.status_code
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
