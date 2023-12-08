from flask import Flask, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
from Helpers.Libraries.imageUpload import image_upload  # Assuming image_upload is the equivalent library in Python

from Middlewares.Authorization.auth import get_access_to_route
from Controllers.story import add_story, get_all_stories, detail_story, like_story, edit_story, delete_story, edit_story_page
from Middlewares.database.databaseErrorhandler import check_story_exist, check_user_and_story_exist

app = Flask(__name__)

# Configure image uploads
photos = UploadSet("photos", IMAGES)
app.config["UPLOADED_PHOTOS_DEST"] = "path/to/uploaded/images"
configure_uploads(app, photos)

@app.route("/addstory", methods=["POST"])
@get_access_to_route
def add_story_route():
    if "image" in request.files:
        image = request.files["image"]
        image_upload(image)  # Assuming image_upload function handles image upload
    return add_story()

@app.route("/<slug>", methods=["POST"])
@check_story_exist
def detail_story_route(slug):
    return detail_story(slug)

@app.route("/<slug>/like", methods=["POST"])
@get_access_to_route
@check_story_exist
def like_story_route(slug):
    return like_story(slug)

@app.route("/editStory/<slug>", methods=["GET"])
@get_access_to_route
@check_story_exist
@check_user_and_story_exist
def edit_story_page_route(slug):
    return edit_story_page(slug)

@app.route("/<slug>/edit", methods=["PUT"])
@get_access_to_route
@check_story_exist
@check_user_and_story_exist
def edit_story_route(slug):
    if "image" in request.files:
        image = request.files["image"]
        image_upload(image)  # Assuming image_upload function handles image upload
    return edit_story(slug)

@app.route("/<slug>/delete", methods=["DELETE"])
@get_access_to_route
@check_story_exist
@check_user_and_story_exist
def delete_story_route(slug):
    return delete_story(slug)

@app.route("/getAllStories", methods=["GET"])
def get_all_stories_route():
    return get_all_stories()

if __name__ == "__main__":
    app.run(debug=True)
