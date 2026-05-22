from flask import Flask, jsonify, request
from flask_cors import CORS
from db import db
from models import User, Post, Comment
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

load_dotenv()

app = Flask(__name__)
CORS(app)

def get_database_uri():
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        return 'sqlite:///blog.db'
    if database_url.startswith('postgresql://') or database_url.startswith('postgres://'):
        try:
            engine = create_engine(database_url)
            with engine.connect():
                pass
            return database_url
        except OperationalError:
            print("PostgreSQL is unavailable; falling back to SQLite.")
            return 'sqlite:///blog.db'
    return database_url

def load_config(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = get_database_uri()
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

load_config(app)

db.init_app(app)

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Welcome to the Blog API'})

@app.route('/posts', methods=['GET'])
def posts():
    posts = Post.query.all()
    return jsonify([{
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'author': post.author.username,
        'comments': [{
            'id': comment.id,
            'content': comment.content,
            'author': User.query.get(comment.user_id).username
        } for comment in post.comments]
    } for post in posts
    ])

@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    post = Post(title=data['title'], content=data['content'], author=user)
    db.session.add(post)
    db.session.commit()
    return jsonify({'message': 'Post created successfully', 'post_id': post.id}), 201

@app.route('/posts/<int:post_id>/comments', methods=['POST'])
def create_comment(post_id):
    data = request.get_json()
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    comment = Comment(content=data['content'], post=post, author=user)
    db.session.add(comment)
    db.session.commit()
    return jsonify({'message': 'Comment added successfully', 'comment_id': comment.id}), 201

@app.route('/posts/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    return jsonify([{
        'id': comment.id,
        'content': comment.content,
        'author': User.query.get(comment.user_id).username
    } for comment in post.comments])


@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    return jsonify({
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'author': post.author.username,
        'comments': [{
            'id': comment.id,
            'content': comment.content,
            'author': User.query.get(comment.user_id).username
        } for comment in post.comments]
    })

@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    data = request.get_json()
    post.title = data['title']
    post.content = data['content']
    db.session.commit()
    return jsonify({'message': 'Post updated successfully'})

@app.route('/posts/<int:post_id>/comments/<int:comment_id>', methods=['PUT'])
def update_comment(post_id, comment_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    comment = Comment.query.get(comment_id)
    if not comment or comment.post_id != post_id:
        return jsonify({'error': 'Comment not found'}), 404
    data = request.get_json()
    comment.content = data['content']
    db.session.commit()
    return jsonify({'message': 'Comment updated successfully'})

@app.route('/posts/<int:post_id>', methods=['PATCH'])
def patch_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    data = request.get_json()
    if 'title' in data:
        post.title = data['title']
    if 'content' in data:
        post.content = data['content']
    db.session.commit()
    return jsonify({'message': 'Post updated successfully'})

@app.route('/posts/<int:post_id>/comments/<int:comment_id>', methods=['PATCH'])
def patch_comment(post_id, comment_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    comment = Comment.query.get(comment_id)
    if not comment or comment.post_id != post_id:
        return jsonify({'error': 'Comment not found'}), 404
    data = request.get_json()
    if 'content' in data:
        comment.content = data['content']
    db.session.commit()
    return jsonify({'message': 'Comment updated successfully'})


@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted successfully'}), 200

@app.route('/posts/<int:post_id>/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(post_id, comment_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    comment = Comment.query.get(comment_id)
    if not comment or comment.post_id != post_id:
        return jsonify({'error': 'Comment not found'}), 404
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message': 'Comment deleted successfully'}), 200

# user routes
@app.route('/users', methods=['GET'])
def users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'posts': [{
            'id': post.id,
            'title': post.title,
            'content': post.content
        } for post in user.posts]
    } for user in users])


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    user = User(username=data['username'], email=data['email'], password=data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully', 'user_id': user.id}), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'posts': [{
            'id': post.id,
            'title': post.title,
            'content': post.content
        } for post in user.posts]
    })

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    data = request.get_json()
    user.username = data['username']
    user.email = data['email']
    user.password = data['password']
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

@app.route('/users/<int:user_id>', methods=['PATCH'])
def patch_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    data = request.get_json()
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.password = data['password']
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200

def create_app():
    with app.app_context():
        db.create_all()
    return app

create_app()

if __name__ == '__main__':
    app.run(debug=True)