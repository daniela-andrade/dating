from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    country = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    likes_sent = db.relationship("Like", foreign_keys='like.c.liker_id',
                                 backref='liker', lazy='dynamic')
    likes_received = db.relationship("Like", foreign_keys='like.c.liked_id',
                                     backref='liked', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Like(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    liker_id = db.Column(db.Integer, db.ForeignKey("user.id"), index=True)
    liked_id = db.Column(db.Integer, db.ForeignKey("user.id"), index=True)
    is_platonic = db.Column(db.Boolean, default=False)
    is_romantic = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Like: {} likes {}>'.format(self.liker_id, self.liked_id)
