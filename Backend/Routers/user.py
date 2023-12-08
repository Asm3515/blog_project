from flask import Flask, request
from flask import Blueprint
from .Helpers.Libraries.imageUpload import imageUpload
from .Controllers.user import profile, editProfile, changePassword, addStoryToReadList, readListPage
from .Middlewares.Authorization.auth import getAccessToRoute

router = Blueprint("router", __name__)

@router.route("/profile", methods=["GET"])
@getAccessToRoute
def get_profile():
    return profile()

@router.route("/editProfile", methods=["POST"])
@getAccessToRoute
def edit_profile():
    if "photo" in request.files:
        photo = request.files["photo"]
    else:
        photo = None
    return editProfile(photo)

@router.route("/changePassword", methods=["PUT"])
@getAccessToRoute
def change_password():
    return changePassword()

@router.route("/<slug>/addStoryToReadList", methods=["POST"])
@getAccessToRoute
def add_story_to_read_list(slug):
    return addStoryToReadList(slug)

@router.route("/readList", methods=["GET"])
@getAccessToRoute
def read_list_page():
    return readListPage()

# Assuming you have created a Flask app instance elsewhere
app = Flask(__name__)
app.register_blueprint(router, url_prefix="/api/user")

# Alternatively, you can create the app and register the blueprint in one file
app = Flask(__name__)
app.register_blueprint(router, url_prefix="/api/user")

# Then run the app
if __name__ == "__main__":
    app.run()
