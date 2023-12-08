from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from Models.user import User  # Assuming you have a User model
from Helpers.error.custom_error import CustomError
from Helpers.auth.token_helpers import send_token
from Helpers.libraries.send_email import send_email
from Helpers.input.input_helpers import validate_user_input

app = Flask(__name__)

# Assume the implementation of the necessary functions and classes like async_error_wrapper, compare_password, etc.

@app.route('/private-data', methods=['GET'])
def get_private_data():
    # Assume req.user is set somewhere in your middleware
    user = getattr(request, 'user', None)

    if not user:
        return jsonify(success=False, message="Unauthorized"), 401

    return jsonify(success=True, message="You got access to the private data in this route", user=user), 200

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    hashed_password = generate_password_hash(password, method='sha256')

    new_user = User(username=username, email=email, password=hashed_password)
    new_user.save()

    return send_token(new_user, 201)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not validate_user_input(email, password):
        return jsonify(success=False, message="Please check your inputs"), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify(success=False, message="Invalid credentials"), 404

    return send_token(user, 200)

@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    # Implementation of forgot password logic

@app.route('/reset-password', methods=['POST'])
def reset_password():
    # Implementation of reset password logic

if __name__ == '__main__':
    app.run(debug=True)
