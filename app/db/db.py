from flask_login import current_user
from app.db.setup import session
from app.models import User


def get_users_not_liked(user):
    users = get_all_other_users(user)
    users_liked = get_likes_sent(user)
    return [u for u in users if u not in users_liked]


def get_users_not_loved(user):
    users = get_all_other_users(user)
    users_loved = get_loves_sent(user)
    return [u for u in users if u not in users_loved]


def get_all_other_users(user):
    return User.query.filter(user.id != User.id).all()


def get_user_by_id(user_id):
    return User.query.filter(User.id == user_id).first()


def get_user_by_username(username):
    return User.query.filter_by(username=username).first()


def get_likes_sent(user):
    return user.likes_sent


def get_loves_sent(user):
    return user.loves_sent


def get_likes_received(user):
    return user.likes_received


def get_loves_received(user):
    return user.loves_received


def like(user, id):
    liked_user = get_user_by_id(id)
    user.like(liked_user)
    session.commit()


def love(user, id):
    loved_user = get_user_by_id(id)
    user.love(loved_user)
    session.commit()


def unlike(user, id):
    unliked_user = get_user_by_id(id)
    user.unlike(unliked_user)
    session.commit()


def unlove(user, id):
    unloved_user = get_user_by_id(id)
    user.unlove(unloved_user)
    session.commit()


def register(user):
    session.add(user)
    session.commit()
