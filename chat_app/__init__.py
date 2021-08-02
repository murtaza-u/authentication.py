from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ujieveiThae1fa3fuchiec2keighahe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com' # check your email provider info
app.config['MAIL_USE_TLS'] = 587 # check your email provider info. Usually 587 is what most providers use
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '' # email-id
app.config['MAIL_PASSWORD'] = '' # password

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'You must be logged in'
login_manager.login_message_category = 'info'

db = SQLAlchemy(app)
mail = Mail(app)
bcrypt = Bcrypt(app)


def run():
    from chat_app.auth import auth
    from chat_app.user import user

    import chat_app.auth.routes
    import chat_app.user.routes

    app.register_blueprint(auth)
    app.register_blueprint(user)

    app.run(debug=True)
