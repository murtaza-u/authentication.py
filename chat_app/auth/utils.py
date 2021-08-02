from flask import url_for, flash
from flask_mail import Message

from chat_app import mail


def send_reset_email(user):
    token = user.get_reset_token()
    message = Message()
    message.subject = "Password Reset Request"
    message.sender = 'noreply@chat_app.org'
    message.recipients = [user.email]
    message.body = f'''To reset your password visit the following link:
        {url_for('auth.reset_password', token=token, _external=True)}
        '''
    mail.send(message)
    flash("An email is sent to your email account", "success")
