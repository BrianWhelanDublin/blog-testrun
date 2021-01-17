from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import (DataRequired, Length,
                                Email, EqualTo, ValidationError)
from flask_login import current_user
from blog.models import User


class RegistrationForm(FlaskForm):
    username = StringField("Username",
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email",
                        validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password",
                                     validators=[DataRequired(),
                                                 EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.objects(
            username=username.data).first()
        if user is not None:
            raise ValidationError("Username already used!")

    def validate_email(self, email):
        user = User.objects(
            email=email.data).first()
        if user is not None:
            raise ValidationError("Email already used!")


class LoginForm(FlaskForm):
    email = StringField("Email",
                        validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
    username = StringField("Username",
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email",
                        validators=[DataRequired(), Email()])
    picture = FileField("Update Profile Picture",
                        validators=[FileAllowed(["jpg", "png"])])

    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.objects(
                username=username.data).first()
            if user is not None:
                raise ValidationError("Username already used!")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.objects(
                email=email.data).first()
            if user is not None:
                raise ValidationError("Email already used!")
            