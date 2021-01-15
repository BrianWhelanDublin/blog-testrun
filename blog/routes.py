from flask import (render_template, url_for,
                   flash, redirect, request)
from blog import app, bcrypt
import secrets
import os
import cloudinary.uploader
import cloudinary.api
from blog.forms import (RegistrationForm, LoginForm,
                        UpdateAccountForm)
from blog.models import User, Post
from flask_login import (login_user, current_user,
                         logout_user, login_required)


posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
def home():
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About Page")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.validate_on_submit():
            user = User(username=form.username.data,
                        email=form.email.data)
            user.set_password(form.password.data)
            user.save()
            flash("User registered! Please Log in", "success")
        return redirect(url_for("login"))
    return render_template("register.html",
                           title="Register",
                           form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(
            email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            flash("Logged in sucsessfuly", "success")
            return redirect(next_page) if next_page \
                else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password',
                  'danger')
    return render_template("login.html",
                           title="Login",
                           form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


def save_picture(form_picture):
    response = cloudinary.uploader.upload(form_picture)
    print(response)
    url_start = "https://res.cloudinary.com/dmgevdb7w/"
    image_sizing = "image/upload/w_200,h_200,c_fill,g_face/"
    version = response["version"]
    public_id = response["public_id"]
    image_format = response["format"]

    return f"{url_start}{image_sizing}v{version}/{public_id}.{image_format}"


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_url = save_picture(form.picture.data)
            current_user.image_file = picture_url
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.save()
        flash("your account has been updated!", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("account.html",
                           title="Account",
                           form=form)
