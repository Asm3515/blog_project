from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'your_database_name',
    'host': 'your_database_host',
    'port': 27017,
    'username': 'your_database_username',
    'password': 'your_database_password'
}

db = MongoEngine(app)

class Story(db.Document):
    # Define your Story model fields here
    slug = db.StringField()
    comments = db.ListField(db.ReferenceField('Comment'))
    commentCount = db.IntField()

class Comment(db.Document):
    # Define your Comment model fields here
    story = db.ReferenceField('Story')
    content = db.StringField()
    author = db.ReferenceField('User')
    star = db.IntField()
    likes = db.ListField(db.ReferenceField('User'))
    likeCount = db.IntField()

class User(db.Document):
    # Define your User model fields here
    username = db.StringField()
    photo = db.StringField()

# Define your routes

@app.route('/add_new_comment_to_story/<slug>', methods=['POST'])
def add_new_comment_to_story(slug):
    data = request.json
    story = Story.objects(slug=slug).first()

    comment = Comment(
        story=story,
        content=data['content'],
        author=User.objects(id=request.user.id).first(),
        star=data['star']
    ).save()

    story.comments.append(comment)
    story.commentCount = len(story.comments)
    story.save()

    return jsonify({'success': True, 'data': comment.to_json()}), 200

@app.route('/get_all_comment_by_story/<slug>', methods=['GET'])
def get_all_comment_by_story(slug):
    story = Story.objects(slug=slug).first()
    comments = Comment.objects(story=story).order_by('-createdAt').all()

    return jsonify({'success': True, 'count': story.commentCount, 'data': [comment.to_json() for comment in comments]}), 200

@app.route('/comment_like/<comment_id>', methods=['POST'])
def comment_like(comment_id):
    data = request.json
    comment = Comment.objects(id=comment_id).first()

    if data['activeUser']['_id'] not in comment.likes:
        comment.likes.append(data['activeUser']['_id'])
        comment.likeCount = len(comment.likes)
        comment.save()
    else:
        comment.likes.remove(data['activeUser']['_id'])
        comment.likeCount = len(comment.likes)
        comment.save()

    like_status = data['activeUser']['_id'] in comment.likes

    return jsonify({'success': True, 'data': comment.to_json(), 'likeStatus': like_status}), 200

@app.route('/get_comment_like_status/<comment_id>', methods=['POST'])
def get_comment_like_status(comment_id):
    data = request.json
    comment = Comment.objects(id=comment_id).first()
    like_status = data['activeUser']['_id'] in comment.likes

    return jsonify({'success': True, 'likeStatus': like_status}), 200

if __name__ == '__main__':
    app.run(debug=True)
