from myfb_helpdesk import app, db
from myfb_helpdesk.forms import LoginForm, RegistrationForm
from myfb_helpdesk.models import User
from flask import render_template, redirect, url_for, flash, session, request
from flask_login import login_user, login_required, logout_user, current_user
from flask_dance.contrib.facebook import facebook
import requests
import json


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('login'):
        return redirect(url_for('fb_login'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password):
            flash('Success')
            session['login'] = True
            login_user(user)
            return redirect(url_for('fb_login'))
        else:
            flash('Failed')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('login'):
        return redirect(url_for('fb_login'))
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
            return redirect(url_for('fb_login'))
        else:
            flash('Email already exists')
    return render_template('register.html', form=form)


@app.route('/fb_login')
def fb_login():
    user = User.query.filter_by(email=current_user.email).first()
    if not facebook.authorized:
        return redirect(url_for("facebook.login"))
    else:
        if user.fb_id:
            redirect(url_for('dashboard'))

    resp = facebook.get("/me")
    assert resp.ok, resp.text
    user.name = resp.json()["name"]
    user.fb_id = resp.json()["id"]
    db.session.commit()
    return render_template('dashboard.html')


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
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
