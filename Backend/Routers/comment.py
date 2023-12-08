from flask import Flask, request
from Middlewares.Authorization.auth import getAccessToRoute
from Controllers.comment import (
    addNewCommentToStory,
    getAllCommentByStory,
    commentLike,
    getCommentLikeStatus
)
from Middlewares.database.databaseErrorhandler import checkStoryExist

app = Flask(__name__)

@app.route("/<slug>/addComment", methods=["POST"])
def add_comment(slug):
    return addNewCommentToStory(slug)

@app.route("/<slug>/getAllComment", methods=["GET"])
def get_all_comment(slug):
    return getAllCommentByStory(slug)

@app.route("/<comment_id>/like", methods=["POST"])
def like_comment(comment_id):
    return commentLike(comment_id)

@app.route("/<comment_id>/getCommentLikeStatus", methods=["POST"])
def get_comment_like_status(comment_id):
    return getCommentLikeStatus(comment_id)

if __name__ == "__main__":
    app.run(debug=True)
