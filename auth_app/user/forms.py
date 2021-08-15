from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class ChangeEmailForm(FlaskForm):
    email = StringField('Email', validators=[
            DataRequired(),
            Email(),
            Length(min=2, max=120)
        ])

    submit = SubmitField('Change Email')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[
            DataRequired(),
            Length(min=8, max=120)
        ])

    new_password = PasswordField('New Password', validators=[
            DataRequired(),
            Length(min=8, max=120)
        ])

    new_confirm_password = PasswordField('Confirm New Password', validators=[
            DataRequired(),
            EqualTo('new_password'),
            Length(min=8, max=120)
        ])

    submit = SubmitField('Change Password')


class UpdateProfilePictureForm(FlaskForm):
    picture = FileField('', validators=[
            FileAllowed(['png', 'jpg', 'jpeg'])
        ])

    submit = SubmitField('Update')
