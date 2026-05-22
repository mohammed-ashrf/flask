import os

from dotenv import load_dotenv
from flask import Flask, render_template, url_for, redirect, request
from db import db
from forms import CommentForm
from models import Post, Comment

app = Flask(__name__)
load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
db.init_app(app)

@app.route('/', methods=['GET'])
def home():
    posts = Post.query.all()
    form = CommentForm()
    return render_template('home.html', posts=posts, form=form)

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

users = [
    {"id":1,"name":"ali","age":20},
    {"id":2,"name":"ahmed","age":30},
]

@app.route('/users', methods=['GET'])
def users_list():
    return render_template('users.html', users=users)


@app.route('/add-user/<name>/<int:age>', methods=['GET', 'POST'])
@app.route('/add-user', methods=['GET', 'POST'])
def add_user(name=None, age=None):
    if request.method == 'POST':
        if not name or not age:
            name = request.form['name']
            age = int(request.form['age'])
        user = {"id": len(users) + 1, "name": name, "age": age}
        users.append(user)
        return redirect(url_for('users_list'))
    return render_template('addUser.html')

@app.route('/delete-user/<int:id>', methods=['GET', 'POST'])
def delete_user(id):
    global users
    users = [user for user in users if user['id'] != id]
    return redirect(url_for('users_list'))


@app.route('/update-user/<int:id>/edit/<name>/<int:age>', methods=['GET', 'POST'])
@app.route('/update-user/<int:id>', methods=['GET', 'POST'])
def update_user(id, name=None, age=None):
    if request.method == 'POST':
        if name is None or age is None:
            name = request.form['name']
            age = int(request.form['age'])
        if id > len(users) or id <= 0:
            return "User not found"
        for user in users:
            if user['id'] == id:
                user['name'] = name
                user['age'] = age
                return redirect(url_for('users_list'))
    return render_template('updateUser.html', user=users[id - 1])


@app.route('/add-post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        auther = request.form['auther']
        post = Post(title=title, content=content, auther=auther)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('addPost.html')


@app.route('/post/<int:id>', methods=['GET'])
def post_detail(id):
    post = Post.query.get_or_404(id)
    return render_template('postDetails.html', post=post)

@app.route('/post/<int:id>/update', methods=['POST'])
def update_post(id):
    post = Post.query.get_or_404(id)
    post.title = request.form['title']
    post.content = request.form['content']
    post.auther = request.form['auther']
    db.session.commit()
    return redirect(url_for('post_detail', id=post.id))


@app.route('/post/<int:id>/delete', methods=['POST'])
def delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/post/<int:id>/add-comment', methods=['POST'])
def add_comment(id):
    post= Post.query.get_or_404(id)
    content = request.form['content']
    comment= Comment(content=content, post=post)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)