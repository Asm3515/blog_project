from flask import Flask, request, jsonify

app = Flask(__name__)

def is_token_included(req):
    return (
        req.headers.get('Authorization') and req.headers.get('Authorization').startswith('Bearer')
    )

def get_access_token_from_header(req):
    authorization = req.headers.get('Authorization')
    access_token = authorization.split(' ')[1]
    return access_token

def send_token(user, status_code, res):
    token = user.generate_jwt_from_user()  # Assuming you have a method like generate_jwt_from_user in your User class
    return jsonify(success=True, token=token), status_code

@app.route('/example', methods=['POST'])
def example_route():
    if not is_token_included(request):
        return jsonify(success=False, error='Token not included'), 401

    access_token = get_access_token_from_header(request)

    user = User()  # Replace with actual user instance

    return send_token(user, 200, jsonify())

if __name__ == '__main__':
    app.run(debug=True)
