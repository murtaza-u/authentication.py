from flask import render_template, url_for, flash, redirect
from flask_login import login_required, current_user

from auth_app import db, bcrypt
from auth_app.user import user
from auth_app.user.forms import ChangeEmailForm, ChangePasswordForm, UpdateProfilePictureForm
from auth_app.user.utils import save_picture


@user.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    change_email_form = ChangeEmailForm()
    change_password_form = ChangePasswordForm()
    update_profile_picture_form = UpdateProfilePictureForm()

    if change_email_form.validate_on_submit():
        current_user.email = change_email_form.email.data
        db.session.commit()
        flash("Email changed successfully", "success")
    elif change_password_form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, change_password_form.old_password.data):
            new_hashed_password = bcrypt.generate_password_hash(change_password_form.new_password.data)
            current_user.password = new_hashed_password
            db.session.commit()
            flash("Password changed successfully", "success")
            return redirect(url_for('auth.logout'))
        else:
            flash("Invalid Password", "danger")
    elif update_profile_picture_form.validate_on_submit():
        profile_picture = save_picture(update_profile_picture_form.picture.data)
        current_user.profile_picture = profile_picture
        db.session.commit()
        flash("Profile Picture Updated!", "success")

    profile_picture = url_for('static', filename='profile_pictures/' + current_user.profile_picture)

    return render_template(
            'account.html',
            title='account',
            profile_picture=profile_picture,
            change_email_form=change_email_form,
            change_password_form=change_password_form,
            update_profile_picture_form=update_profile_picture_form
        )
