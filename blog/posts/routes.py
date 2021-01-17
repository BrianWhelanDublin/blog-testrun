from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
# from blog import db
from blog.models import Post
from blog.posts.forms import PostForm

posts = Blueprint("posts", __name__)


@posts.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data,
                    author=current_user.id)
        post.save()
        flash("Post has been created!", "success")
        return redirect(url_for("main.home"))
    return render_template("create_post.html",
                           title="New Post",
                           form=form,
                           legend="New Post")


@posts.route("/post/<post_id>")
def post(post_id):
    post = Post.objects().get_or_404(id=post_id)
    likes = len(post.user_likes)
    is_liked = False
    if current_user.is_authenticated and post.id in current_user.liked_posts:
        is_liked = True
    return render_template("post.html",
                           title=post.title,
                           post=post,
                           is_liked=is_liked,
                           likes=likes)


@posts.route("/liked/<post_id>", methods=["GET", "POST"])
@login_required
def liked_post(post_id):
    post = Post.objects().get_or_404(id=post_id)
    if post not in current_user.liked_posts:
        current_user.liked_posts.append(post.id)
        current_user.save()
        post.user_likes.append(current_user.id)
        post.save()
    flash("post liked")
    return redirect(url_for("posts.post", post_id=post.id))


@posts.route("/post/<post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.objects().get_or_404(id=post_id)
    if post.author.id != current_user.id:
        abort(403)
    form = PostForm()
    if form .validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.save()
        flash("Your post has been updated", "success")
        return redirect(url_for("posts.post", post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("create_post.html",
                           title="Update Post",
                           form=form,
                           legend="Update Post")


@posts.route("/post/<post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.objects().get_or_404(id=post_id)
    if post.author.id != current_user.id:
        abort(403)
    post.delete()
    flash("Post has been deleted", "success")
    return redirect(url_for("main.home"))