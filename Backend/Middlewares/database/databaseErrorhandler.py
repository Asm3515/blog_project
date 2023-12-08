from flask import Flask, request, jsonify
from functools import wraps
from helpers.error.custom_error import CustomError
from models.story import Story

app = Flask(__name__)

def async_error_wrapper(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            return result
        except CustomError as e:
            return jsonify({"error": str(e), "status_code": e.status_code}), e.status_code
    return wrapper

@app.route('/check_story_exist/<slug>', methods=['GET'])
@async_error_wrapper
async def check_story_exist(slug):
    story = await Story.findOne({"slug": slug})
    if not story:
        raise CustomError("There is no such story with that slug", 400)
    return jsonify({"message": "Story exists"}), 200

@app.route('/check_user_and_story_exist/<slug>', methods=['GET'])
@async_error_wrapper
async def check_user_and_story_exist(slug):
    story = await Story.findOne({"slug": slug, "author": request.user})
    if not story:
        raise CustomError("There is no story with that slug associated with the user", 400)
    return jsonify({"message": "Story and user exist"}), 200

if __name__ == '__main__':
    app.run(debug=True)
