from flask import Flask, request
from Controllers import auth

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register():
    return auth.register(request)

@app.route('/login', methods=['POST'])
def login():
    return auth.login(request)

@app.route('/forgotpassword', methods=['POST'])
def forgotpassword():
    return auth.forgotpassword(request)

@app.route('/resetpassword', methods=['PUT'])
def resetpassword():
    return auth.resetpassword(request)

@app.route('/private', methods=['GET'])
def get_private_data():
    if auth.get_access_to_route(request):
        return auth.get_private_data(request)
    else:
        return 'Unauthorized', 403

if __name__ == '__main__':
    app.run(debug=True)