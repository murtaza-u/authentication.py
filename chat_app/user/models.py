from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin

from chat_app import db, app, login_manager


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    profile_picture = db.Column(db.String(20), default='default.png')
    message = db.relationship('Message', backref='sender', lazy=True)

    def __repr__(self):
        return f"User({self.username}, {self.email})"

    def get_reset_token(self, expiry_period=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiry_period)
        token = s.dumps({'user_id': self.id}).decode('utf-8')
        return token

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
