from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    category = SelectField("Category")
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Post")


class CommentForm(FlaskForm):
    comment = TextAreaField("Add Comment", validators=[DataRequired()])
    submit = SubmitField("Comment")
