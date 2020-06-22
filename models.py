from flask_sqlalchemy import SQLAlchemy

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

    image_url = db.Column(db.String(200))

    def __repr__(self):
        """Show info about user."""

        u = self
        return f"<User id={u.id} name={u.first_name} {u.last_name}>"
