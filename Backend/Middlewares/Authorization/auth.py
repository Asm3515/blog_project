from flask import Flask, request, jsonify
import jwt
from Models.user import User  # Assuming you have a user module
from Helpers.auth.token_helpers import is_token_included, get_access_token_from_header
from Helpers.error.custom_error import CustomError
from functools import wraps

app = Flask(__name__)

def get_access_to_route(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        jwt_secret_key = "your_jwt_secret_key"  # Replace with your actual JWT secret key

        if not is_token_included(request):
            return jsonify({"error": "You are not authorized to access this route"}), 401

        access_token = get_access_token_from_header(request)

        try:
            decoded = jwt.decode(access_token, jwt_secret_key)
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        user = User.query.get(decoded["id"])

        if not user:
            return jsonify({"error": "You are not authorized to access this route"}), 401

        request.user = user

        return route_function(*args, **kwargs)

    return wrapper

@app.route('/protected-route', methods=['GET'])
@get_access_to_route
def protected_route():
    return jsonify({"message": "You have access to this route", "user_id": request.user.id})

if __name__ == '__main__':
    app.run(debug=True)
