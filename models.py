from flask_login import UserMixin
from app import db


class User(db.Model, UserMixin):
    """This will create the user object
    portion of our database and hold the users.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)

    def __repr__(self):
        return "<Person %r>" % self.username


class Entry(db.Model):
    """This will create our entry object portion,
    which will be stored in our database.
    """

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(40), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(1500), nullable=False)
    timestamp = db.Column(db.String(100))

    def __repr__(self):
        return "User: %s posted: %s, and titled it ' %s ', at " "the time of %s" % (
            self.user,
            self.content,
            self.title,
            self.timestamp,
        )
