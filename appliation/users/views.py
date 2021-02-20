from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import current_user, login_required, login_user, logout_user
from application import login_manager
from application.users.forms import LoginForm, RegistrationForm, RequestForm, ResetPasswordForm, ProfileForm
from application.Model import User, Insert_Data
from application import bcrypt
from datetime import timedelta
from application.users.helper import send_reset_email, get_and_save_picture
from application import db
#                             Creating BluePrint of User Package
users = Blueprint('users', __name__)

login_manager.login_view = 'users.login'
login_manager.login_message = 'Sorry!! You must Login to access this page'
login_manager.login_message_category = 'info'
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@users.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.email.data).first()
        result = bcrypt.check_password_hash(user.user_password, form.password.data)
        if result is not True:
            flash(f"{form.email.data} Something Wrong !!!", "danger")
            # return redirect(url_for('login'))
            return redirect(request.url)
        else:
            login_user(user, remember=form.rememberMe.data, duration=timedelta(minutes=10), fresh=True)
            flash(f"{form.email.data} welcome to Home!!! ", "success")
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
    return render_template("login.html", title="Login", form=form)

@users.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Saving and getting name for picture
        picture_name = get_and_save_picture(form.picture.data)
        # Generating Hash Password
        hash_password = bcrypt.generate_password_hash(form.password.data)
        Insert_Data(form.userName.data, form.email. data, hash_password, picture_name)
        flash(f"{form.userName.data} with {form.email.data} Added successfully !!! ", "success")
        return redirect(url_for('users.login'))

    return render_template("register.html", title="Register", form=form)

@users.route('/logout')
@login_required
def logout():
    form = LoginForm()
    logout_user()
    return render_template('login.html', title="Login", form=form)

@users.route("/reset_password", methods=["POST", "GET"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent to reset password', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Request', form=form)

@users.route("/reset_password/<token>", methods=["POST","GET"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('This token is invalid !!! ', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user.user_password = hashed_password
        db.session.commit()
        flash("Password has been updated , You are now able to Login", "info")
        # return redirect(url_for('login'))
        return redirect(url_for('users.login'))

    return render_template('reset_token.html', title='Reset Password', form=form)
@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = ProfileForm()
    if form.validate_on_submit():
        image_name = get_and_save_picture(form.picture.data)
        current_user.user_name = form.userName.data
        current_user.user_email = form.email.data
        current_user.user_image = image_name
        db.session.commit()
        flash("Profile has been updated", 'success')
    return render_template('account.html', title='Profile', form=form)