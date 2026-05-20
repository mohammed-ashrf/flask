from flask import Flask, render_template, url_for, redirect, request
app = Flask(__name__)
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

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

if __name__ == '__main__':
    app.run(debug=True)