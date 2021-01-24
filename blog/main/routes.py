from flask import render_template, request, Blueprint
from blog.models import Post


main = Blueprint("main", __name__)


@main.route("/")
def home():
    page = request.args.get("page", 1, type=int)
    posts = Post.objects().order_by("-date_posted").paginate(
        page=page, per_page=2)
    number = 1
    return render_template("home.html",
                           posts=posts,
                           number=number)


@main.route("/about")
def about():
    return render_template("about.html", title="About Page")
