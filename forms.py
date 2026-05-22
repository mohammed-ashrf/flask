from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, NumberRange


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()], render_kw={"placeholder": "Enter the post title", "class": "input-field"})
    content = TextAreaField('Content', validators=[DataRequired()], render_kw={"placeholder": "Enter the post content", "class": "input-field"})
    auther = StringField('Author', validators=[DataRequired()], render_kw={"placeholder": "Enter the author name", "class": "input-field"})
    submit = SubmitField('Submit', render_kw={"class": "submit-btn"})


class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Enter the user name", "class": "input-field"})
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=0)], render_kw={"placeholder": "Enter the age", "class": "input-field"})
    submit = SubmitField('Submit', render_kw={"class": "submit-btn"})


class DeleteForm(FlaskForm):
    submit = SubmitField('Delete', render_kw={"class": "delete-btn"})

class CommentForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()], render_kw={"placeholder": "Enter your comment here", "class": "input-field"})
    submit = SubmitField('Submit', render_kw={"class": "submit-btn"})