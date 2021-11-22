from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LikeForm, LoginForm, RegistrationForm
from app.models import User, Like


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
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
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
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/users/")
def show_users():
    users = User.query.all()
    if users == None:
        flash('Error fetching users')
    else:
        return render_template('users.html', title='Users', users=users)
    return render_template('base.html', title='Home')


@app.route("/likes/")
def likes():
    likes = Like.query.filter(
        Like.liker_id == current_user.id)
    return render_template('likes.html', likes=likes)


@app.route("/platonic", methods=["GET", "POST"])
@login_required
def add_platonic_likes():
    form = LikeForm()
    likes = Like.query.filter(
        Like.liker_id == current_user.id).filter(Like.is_platonic == False)
    users = User.query.filter(User.username != current_user.username).all()

    form.choices.choices = [(u.id, u.username) for u in users]

    if request.method == 'POST' and form.validate_on_submit():
        for id in form.choices.data:
            l = Like.query.filter(Like.liker_id == current_user.id).filter(
                Like.liked_id == id).first()
            if l and l.is_romantic:
                l.is_platonic = True
            else:
                l = Like(liker_id=current_user.id,
                         liked_id=id, is_platonic=True)
                db.session.add(l)
            db.session.commit()
        return redirect(url_for('likes'))
    else:
        form.choices.data = [(u.id, u.username, u.country) for u in users]
        return render_template('addLikes.html', title='Platonic', form=form)


@app.route("/romantic", methods=["GET", "POST"])
@login_required
def add_romantic_likes():
    form = LikeForm()
    likes = Like.query.filter(
        Like.liker_id == current_user.id).filter(Like.is_romantic == False)
    users = User.query.filter(User.username != current_user.username).all()
    form.choices.choices = [(u.id, u.username) for u in users]

    if request.method == 'POST' and form.validate_on_submit():
        accepted = []
        for id in form.choices.data:
            l = Like.query.filter(Like.liker_id == current_user.id).filter(
                Like.liked_id == id).first()
            if l and l.is_platonic:
                l.is_romantic = True
            else:
                l = Like(liker_id=current_user.id,
                         liked_id=id, is_romantic=True)
                db.session.add(l)
            db.session.commit()
        return redirect(url_for('likes'))
    else:
        form.choices.data = [(u.id, u.username, u.country) for u in users]
        return render_template('addLikes.html', title='Romantic', form=form)
