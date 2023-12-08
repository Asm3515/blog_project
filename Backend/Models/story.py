from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from slugify import slugify

app = Flask(__name__)
app.config['MONGO_URI'] = 'your_mongo_db_uri'
mongo = PyMongo(app)

@app.route('/stories', methods=['POST'])
def create_story():
    data = request.get_json()

    author = data.get('author')
    title = data.get('title')
    content = data.get('content')
    tags = data.get('tags')
    image = data.get('image', 'default.jpg')
    readtime = data.get('readtime', 3)

    slug = make_slug(title)

    story = {
        'author': author,
        'slug': slug,
        'title': title,
        'content': content,
        'tags': tags,
        'image': image,
        'readtime': readtime,
        'likes': [],
        'likeCount': 0,
        'comments': [],
        'commentCount': 0
    }

    inserted_story = mongo.db.stories.insert_one(story)

    return jsonify({'message': 'Story created successfully', 'story_id': str(inserted_story.inserted_id)}), 201

@app.route('/stories/<story_id>', methods=['DELETE'])
def delete_story(story_id):
    story = mongo.db.stories.find_one({'_id': ObjectId(story_id)})

    if story:
        mongo.db.stories.delete_one({'_id': ObjectId(story_id)})
        mongo.db.comments.delete_many({'story': ObjectId(story_id)})
        return jsonify({'message': 'Story deleted successfully'}), 200
    else:
        return jsonify({'message': 'Story not found'}), 404

def make_slug(title):
    return slugify(title, separator='-', lowercase=True)

if __name__ == '__main__':
    app.run(debug=True)
