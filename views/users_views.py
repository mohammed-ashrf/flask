from flask.views import MethodView
from flask import render_template, redirect, url_for
from db import db
from models import User
from forms import DeleteForm, UserForm

class UsersView(MethodView):
    def get(self):
        users = User.query.order_by(User.id).all()
        delete_form = DeleteForm()
        return render_template('users.html', users=users, delete_form=delete_form)

class AddUserView(MethodView):
    def get(self):
        form = UserForm()
        return render_template('addUser.html', form=form)
    
    def post(self):
        form = UserForm()
        if form.validate_on_submit():
            user = User(name=form.name.data, age=form.age.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('users_list'))
        return render_template('addUser.html', form=form)
    

class DeleteUserView(MethodView):
    def post(self, id):
        user = User.query.get_or_404(id)
        form = DeleteForm()
        if form.validate_on_submit():
            db.session.delete(user)
            db.session.commit()
        return redirect(url_for('users_list'))
    
class UpdateUserView(MethodView):
    def get(self, id):
        user = User.query.get_or_404(id)
        form = UserForm(obj=user)
        return render_template('updateUser.html', user=user, form=form)
    
    def post(self, id):
        user = User.query.get_or_404(id)
        form = UserForm()
        if form.validate_on_submit():
            user.name = form.name.data
            user.age = form.age.data
            db.session.commit()
            return redirect(url_for('users_list'))
        return render_template('updateUser.html', user=user, form=form)