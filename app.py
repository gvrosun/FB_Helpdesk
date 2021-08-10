from myfb_helpdesk import app, db
from myfb_helpdesk.forms import LoginForm, RegistrationForm
from myfb_helpdesk.models import User
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from myfb_helpdesk.oauth import blueprint


# Blueprint
app.register_blueprint(blueprint, url_prefix="/login")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password):
            flash('Success')
            login_user(user)
            redirect(url_for('dashboard'))
        else:
            flash('Failed')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        check_username = form.check_username(form.username)
        check_email = form.check_email(form.email)
        if check_username and check_email:
            user = User(
                email=form.email.data,
                username=form.username.data,
                password=form.password.data
            )
            db.session.add(user)
            db.session.commit()
            flash('register_success')
        redirect(url_for('dashboard'))
    return render_template('register.html', form=form)


@app.route('/fb_login')
def fb_login():
    render_template('fb_login.html')


@app.route('/fb_signup')
def fb_register():
    render_template('fb_login.html')


@login_required
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
