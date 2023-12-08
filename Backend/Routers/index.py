from flask import Flask
from flask import Blueprint

app = Flask(__name__)

auth_route = Blueprint("auth", __name__)
story_route = Blueprint("story", __name__)
user_route = Blueprint("user", __name__)
comment_route = Blueprint("comment", __name__)

@auth_route.route("/")
def auth():
    # Your auth route logic here
    return "Auth Route"

@story_route.route("/")
def story():
    # Your story route logic here
    return "Story Route"

@user_route.route("/")
def user():
    # Your user route logic here
    return "User Route"

@comment_route.route("/")
def comment():
    # Your comment route logic here
    return "Comment Route"

app.register_blueprint(auth_route, url_prefix="/auth")
app.register_blueprint(story_route, url_prefix="/story")
app.register_blueprint(user_route, url_prefix="/user")
app.register_blueprint(comment_route, url_prefix="/comment")

if __name__ == "__main__":
    app.run(debug=True)
