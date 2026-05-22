import os

from dotenv import load_dotenv
from flask import Flask, render_template, url_for, redirect, request
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from db import db
from forms import CommentForm
from models import Post, Comment, User

from views.posts_views import PostUpdateView, PostsView, PostAddView ,PostDetailView, PostDeleteView, CommentAddView
from views.users_views import UsersView, AddUserView, DeleteUserView, UpdateUserView

app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')


def get_database_uri():
    database_uri = os.getenv('DATABASE_URL')
    if not database_uri:
        return 'sqlite:///flask_app.db'

    if database_uri.startswith(('postgresql://', 'postgres://')):
        try:
            engine = create_engine(database_uri, pool_pre_ping=True)
            with engine.connect():
                pass
            return database_uri
        except OperationalError:
            print('PostgreSQL is unavailable; falling back to sqlite:///flask_app.db')
            return 'sqlite:///flask_app.db'

    return database_uri


app.config['SQLALCHEMY_DATABASE_URI'] = get_database_uri()
db.init_app(app)

posts_view = PostsView.as_view('home')
app.add_url_rule('/', view_func=posts_view, methods=['GET'])

users_list_view = UsersView.as_view('users_list')
app.add_url_rule('/users', view_func=users_list_view, methods=['GET'])

users_add_view = AddUserView.as_view('add_user')
app.add_url_rule('/add-user', view_func=users_add_view, methods=['GET', 'POST'])

users_delete_view = DeleteUserView.as_view('delete_user')
app.add_url_rule('/delete-user/<int:id>', view_func=users_delete_view, methods=['POST'])


users_update_view = UpdateUserView.as_view('update_user')
app.add_url_rule('/update-user/<int:id>', view_func=users_update_view, methods=['GET', 'POST'])

add_posts_view = PostAddView.as_view('add_post')
app.add_url_rule('/add-post', view_func=add_posts_view, methods=['GET', 'POST']);


post_detail_view = PostDetailView.as_view('post_detail')
app.add_url_rule('/post/<int:id>', view_func=post_detail_view, methods=['GET']);


post_update_view = PostUpdateView.as_view('update_post')
app.add_url_rule('/post/<int:id>/update', view_func=post_update_view, methods=['GET', 'POST']);


post_delete_view = PostDeleteView.as_view('delete_post')
app.add_url_rule('/post/<int:id>/delete', view_func=post_delete_view, methods=['POST']);

comment_add_view = CommentAddView.as_view('add_comment')
app.add_url_rule('/post/<int:id>/add-comment', view_func=comment_add_view, methods=['POST']);



@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')


@app.route('/user/<username>', methods=['GET'])
def user(username):
    print(type(username))
    return f"Hello, {username}!"


@app.route('/user/<username>/<int:age>', methods=['GET'])
def user_info(username, age):
    print(type(username))
    print(type(age))
    return f"Hello, {username}! You are {age} years old."


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)