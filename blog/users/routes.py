from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from blog import bcrypt
from blog.models import User, Post
from blog.users.forms import (RegistrationForm, LoginForm,
                              UpdateAccountForm)
from blog.users.utils import save_picture

users = Blueprint('users', __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.validate_on_submit():
            user = User(username=form.username.data,
                        email=form.email.data)
            user.set_password(form.password.data)
            user.save()
            flash("User registered! Please Log in", "success")
        return redirect(url_for("users.login"))
    return render_template("register.html",
                           title="Register",
                           form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
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
                else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password',
                  'danger')
    return render_template("login.html",
                           title="Login",
                           form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@users.route("/account", methods=["GET", "POST"])
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
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("account.html",
                           title="Account",
                           form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.objects(username=username).first_or_404()
    posts = Post.objects(author=user.id).order_by("-date_posted").paginate(
        page=page, per_page=2)
    return render_template("user_posts.html",
                           posts=posts,
                           user=user)
