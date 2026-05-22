from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class CommentForm(FlaskForm):
    content = StringField('Content', validators=[DataRequired()], render_kw={"placeholder": "Enter your comment here", "class": "input-field"})
    submit = SubmitField('Submit', render_kw={"class": "submit-btn"})