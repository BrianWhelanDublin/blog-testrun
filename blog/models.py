from flask_mongoengine import BaseQuerySet
from datetime import datetime
from blog import db, bcrypt, login_manager
from flask_login import UserMixin


class User(db.Document, UserMixin):
    meta = {
        'collection': 'users',
        'queryset_class': BaseQuerySet
        }
    username = db.StringField(max_length=20, unique=True, required=True)
    email = db.StringField(max_length=120, unique=True, required=True)
    password = db.StringField(max_length=120)
    image_file = db.StringField(
        default="https://res.cloudinary.com/dmgevdb7w/image\
/upload/v1610563923/xymcofmhj3le6l9uh8qa.jpg")
    liked_posts = db.ListField(db.ReferenceField("Post"))

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(
            password).decode("utf8")


@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()


class Comment(db.DynamicDocument):
    comment = db.StringField(max_length=200, required=True)
    comment_author = db.ReferenceField(User)
    post = db.ReferenceField("Post")


class Categories(db.Document):
    meta = {
        'collection': 'categories',
        'queryset_class': BaseQuerySet
        }
    category_name = db.StringField(max_length=30)


class Post(db.Document):
    meta = {
        'allow_inheritance': True,
        'collection': 'posts',
        'queryset_class': BaseQuerySet
        }
    title = title = db.StringField(max_length=50)
    content = db.StringField()
    date_posted = db.DateTimeField(default=datetime.utcnow)
    author = db.ReferenceField(User)
    user_likes = db.ListField(db.ReferenceField(User))
    comments = db.ListField(db.ReferenceField(Comment))

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

