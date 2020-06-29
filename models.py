from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(50),
                           nullable=False,
                           unique=True)

    last_name = db.Column(db.String(50),
                          nullable=False)

    image_url = db.Column(
        db.String(200), nullable=False, default='https://via.placeholder.com/200')

    posts = db.relationship("Post", backref="user",
                            cascade="all, delete-orphan")

    def __repr__(self):
        """Show info about user."""

        u = self
        return f"<User id={u.id} name={u.first_name} {u.last_name}>"


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False,
                           default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
