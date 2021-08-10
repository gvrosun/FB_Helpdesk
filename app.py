from myfb_helpdesk import app, db
from myfb_helpdesk.forms import LoginForm, RegistrationForm
from myfb_helpdesk.models import User
from flask import render_template, redirect, url_for, flash, session, request
from flask_login import login_user, login_required, logout_user, current_user
import requests
import json


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('login'):
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password):
            flash('Success')
            session['login'] = True
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Failed')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('login'):
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.submit.data:
        check_email = form.check_email(form.email)
        if check_email:
            user = User(
                email=form.email.data,
                password=form.password.data
            )
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('register_success')
            session['login'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Email already exists')
    return render_template('register.html', form=form)


@app.route('/fb_login')
def fb_login():
    render_template('fb_login.html')


@app.route('/fb_signup')
def fb_register():
    render_template('fb_login.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    session['login'] = False
    return redirect(url_for('login'))


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    verify_token = "12345"
    if 'hub.mode' in request.args:
        mode = request.args.get('hob.mode')
        print(mode)
    if 'hub.verify_token' in request.args:
        token = request.args.get('hub.verify_token')
        print(token)
    if 'hub.challenge' in request.args:
        challenge = request.args.get('hub.challenge')
        print(challenge)
    if 'hub.mode' in request.args and 'hub.verify_token' in request.args:
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')

        if mode == 'subscribe' and token == verify_token:
            print('WEBHOOK VERIFIED')
            challenge = request.args.get('hub.challenge')
            return challenge, 200
        else:
            return 'ERROR', 403

    return "something", 200


if __name__ == '__main__':
    app.run(debug=True)
