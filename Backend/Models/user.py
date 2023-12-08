from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from flask_mongoengine import MongoEngine
import datetime
import os
import hashlib
import secrets

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'your_database_name',
    'host': 'your_mongodb_connection_string'
}
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
app.config['BCRYPT_LOG_ROUNDS'] = 10

db = MongoEngine(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

class User(db.Document):
    username = db.StringField(required=True)
    photo = db.StringField(default="user.png")
    email = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)
    role = db.StringField(default="user", choices=["user", "admin"])
    readList = db.ListField(db.ReferenceField('Story'))
    readListLength = db.IntField(default=0)
    resetPasswordToken = db.StringField()
    resetPasswordExpire = db.DateTimeField()

    def generate_jwt(self):
        payload = {
            'id': str(self.id),
            'username': self.username,
            'email': self.email
        }
        token = create_access_token(identity=payload)
        return token

    def get_reset_password_token(self):
        random_hex_string = secrets.token_hex(20)
        reset_password_token = hashlib.sha256(random_hex_string.encode('utf-8')).hexdigest()
        self.resetPasswordToken = reset_password_token
        self.resetPasswordExpire = datetime.datetime.utcnow() + datetime.timedelta(days=1)
        return reset_password_token

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password
    )
    new_user.save()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.objects(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = user.generate_jwt()
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(debug=True)
