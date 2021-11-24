from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app
from app.models import User
from app.db import db
from .forms import LikeForm, LoginForm, RegistrationForm


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.get_user_by_username(form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        # used to redirect user to the page they wanted to view
        # before they were prompted with the login form
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    country=form.country.data)
        user.set_password(form.password.data)
        db.register(user)
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/users/")
def show_users():
    users = db.get_all_other_users(current_user)
    if users == None:
        flash('Error fetching users')
    else:
        return render_template('users.html', title='Users', users=users)
    return render_template('base.html', title='Home')


@app.route("/likes_and_loves_sent/")
def likes_and_loves_sent():
    likes = db.get_likes_sent(current_user)
    loves = db.get_loves_sent(current_user)
    return render_template('likesAndLoves.html', title='Sent', likes=likes, loves=loves)


@app.route("/likes_and_loves_received/")
def likes_and_loves_received():
    likes = db.get_likes_received(current_user)
    loves = db.get_loves_received(current_user)
    return render_template('likesAndLoves.html', title='Received', likes=likes, loves=loves)


@app.route("/like", methods=["GET", "POST"])
@login_required
def like():
    form = LikeForm()
    users_not_liked = db.get_users_not_liked(current_user)
    for u in users_not_liked:
        print(f'User not liked: {u}')

    form.choices.choices = [(u.id, u.username) for u in users_not_liked]

    if request.method == 'POST' and form.validate_on_submit():
        for id in form.choices.data:
            db.like(current_user, id)
        return redirect(url_for('likes_and_loves_sent'))
    else:
        form.choices.data = [(u.id, u.username, u.country)
                             for u in users_not_liked]
        return render_template('likeAndLove.html', title='Add Platonic Likes', form=form)


@app.route("/love", methods=["GET", "POST"])
@login_required
def love():
    form = LikeForm()
    users_not_loved = db.get_users_not_loved(current_user)
    form.choices.choices = [(u.id, u.username) for u in users_not_loved]

    if request.method == 'POST' and form.validate_on_submit():
        for id in form.choices.data:
            db.love(current_user, id)
        return redirect(url_for('likes_and_loves_sent'))
    else:
        form.choices.data = [(u.id, u.username, u.country)
                             for u in users_not_loved]
        return render_template('likeAndLove.html', title='Add Romantic Likes', form=form)


@app.route("/unlike", methods=["GET", "POST"])
@login_required
def unlike():
    form = LikeForm()
    users_liked = db.get_likes_sent(current_user)
    form.choices.choices = [(u.id, u.username) for u in users_liked]

    if request.method == 'POST' and form.validate_on_submit():
        for id in form.choices.data:
            db.unlike(current_user, id)
        return redirect(url_for('likes_and_loves_sent'))
    else:
        form.choices.data = [(u.id, u.username, u.country)
                             for u in users_liked]
        return render_template('likeAndLove.html', title='Remove Platonic Likes', form=form)


@app.route("/unlove", methods=["GET", "POST"])
@login_required
def unlove():
    form = LikeForm()
    users_loved = db.get_loves_sent(current_user)
    form.choices.choices = [(u.id, u.username) for u in users_loved]

    if request.method == 'POST' and form.validate_on_submit():
        for id in form.choices.data:
            db.unlove(current_user, id)
        return redirect(url_for('likes_and_loves_sent'))
    else:
        form.choices.data = [(u.id, u.username, u.country)
                             for u in users_loved]
        return render_template('likeAndLove.html', title='Remove Platonic Likes', form=form)
