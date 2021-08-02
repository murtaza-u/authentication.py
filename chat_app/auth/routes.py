from flask import render_template, flash, redirect, url_for, request
from flask_login import logout_user, current_user, login_user

from chat_app import db, bcrypt
from chat_app.auth import auth
from chat_app.auth.utils import send_reset_email
from chat_app.auth.forms import RegistrationForm, LoginForm, ResetRequestForm, ResetPasswordForm
from chat_app.user.models import User


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user.account'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Account created!", "success")
        return redirect(url_for('user.account'))

    return render_template('register.html', title='Register', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.account'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Login in successful", "success")
            next_page = request.args.get('next')
            return redirect(url_for('user.account'))
        else:
            flash("Invalid credentials. Please check your email and password", "danger")

    return render_template('login.html', title='Login', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('user.account'))
    else:
        form = ResetRequestForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            send_reset_email(user) if user else flash("No such account exists. Please check your email", "info")

        return render_template('reset_request.html', form=form)


@auth.route('/reset_password/<string:token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('user.account'))
    else:
        user = User.verify_reset_token(token)
        if user:
            form = ResetPasswordForm()
            if form.validate_on_submit():
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                user.password = hashed_password
                db.session.commit()
                flash("Password has been reset", "success")
                return redirect(url_for('auth.login'))
        else:
            flash("Invalid or expired token", 'danger')
            return redirect(url_for('auth.reset_request'))

        return render_template('reset_password.html', form=form)
