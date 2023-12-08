from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt()

def validate_user_input(email, password):
    return email and password

def compare_password(password, hashed_password):
    return bcrypt.check_password_hash(hashed_password, password)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if validate_user_input(email, password):
        # Assume hashed_password is retrieved from the database based on the email
        hashed_password = get_hashed_password_from_database(email)

        if hashed_password and compare_password(password, hashed_password):
            return jsonify({'message': 'Login successful'})
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    else:
        return jsonify({'message': 'Invalid input'}), 400

def get_hashed_password_from_database(email):
    # Replace this with your database query to retrieve hashed password based on email
    # For simplicity, a hardcoded example is provided
    hashed_passwords = {'user@example.com': '$2b$12$abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJK'}
    return hashed_passwords.get(email)

if __name__ == '__main__':
    app.run(debug=True)
