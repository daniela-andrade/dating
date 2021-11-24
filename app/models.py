from app import login
from app.db.setup import Base
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


liker_liked = Table(
    'like',
    Base.metadata,
    Column('liker_id', Integer, ForeignKey('user.id')),
    Column('liked_id', Integer, ForeignKey('user.id')),
)

lover_loved = Table(
    'love',
    Base.metadata,
    Column('lover_id', Integer, ForeignKey('user.id')),
    Column('loved_id', Integer, ForeignKey('user.id')),
)


class User(UserMixin, Base):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    email = Column(String(120), index=True, unique=True)
    country = Column(String(64))
    password_hash = Column(String(128))
    likes_sent = relationship(
        'User',
        secondary=liker_liked,
        primaryjoin=(liker_liked.c.liker_id == id),
        secondaryjoin=(liker_liked.c.liked_id == id),
        backref=backref('likes_received', lazy='dynamic'),
        lazy='dynamic'
    )
    loves_sent = relationship(
        'User',
        secondary=lover_loved,
        primaryjoin=(lover_loved.c.lover_id == id),
        secondaryjoin=(lover_loved.c.loved_id == id),
        backref=backref('loves_received', lazy='dynamic'),
        lazy='dynamic'
    )

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def like(self, user):
        self.likes_sent.append(user)

    def unlike(self, user):
        self.likes_sent.remove(user)

    def love(self, user):
        self.loves_sent.append(user)

    def unlove(self, user):
        self.loves_sent.remove(user)


@ login.user_loader
def load_user(id):
    return User.query.get(int(id))
