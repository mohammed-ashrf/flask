from flask.views import MethodView

from flask import render_template, request, redirect, url_for
from models import Post, Comment
from forms import CommentForm, DeleteForm, PostForm
from db import db

class PostsView(MethodView):
    def get(self):
        posts = Post.query.all()
        comment_form = CommentForm()
        delete_form = DeleteForm()
        return render_template('home.html', posts=posts, comment_form=comment_form, delete_form=delete_form)
    
class PostAddView(MethodView):
    def get(self):
        form = PostForm()
        return render_template('addPost.html', form=form)

    def post(self):
        form = PostForm()
        if form.validate_on_submit():
            post = Post(title=form.title.data, content=form.content.data, auther=form.auther.data)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('home'))
        return render_template('addPost.html', form=form)
    
class PostDetailView(MethodView):
    def get(self, id):
        post = Post.query.get_or_404(id)
        comment_form = CommentForm()
        delete_form = DeleteForm()
        return render_template('postDetails.html', post=post, comment_form=comment_form, delete_form=delete_form)
    
class PostUpdateView(MethodView):
    def get(self, id):
        post = Post.query.get_or_404(id)
        form = PostForm(obj=post)
        return render_template('updatePost.html', post=post, form=form)

    def post(self, id):
        post = Post.query.get_or_404(id)
        form = PostForm()
        if form.validate_on_submit():
            post.title = form.title.data
            post.content = form.content.data
            post.auther = form.auther.data
            db.session.commit()
            return redirect(url_for('post_detail', id=post.id))
        return render_template('updatePost.html', post=post, form=form)
    
class PostDeleteView(MethodView):
    def post(self, id):
        post = Post.query.get_or_404(id)
        form = DeleteForm()
        if form.validate_on_submit():
            db.session.delete(post)
            db.session.commit()
        return redirect(url_for('home'))

class CommentAddView(MethodView):
    def post(self, id):
        post= Post.query.get_or_404(id)
        form = CommentForm()
        if form.validate_on_submit():
            comment= Comment(content=form.content.data, post=post)
            db.session.add(comment)
            db.session.commit()
        return redirect(request.referrer or url_for('home'))