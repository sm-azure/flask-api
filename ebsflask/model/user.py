from database import db

from config import SECRET_KEY
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, index = True)
    password_hash = db.Column(db.String(128))
    # flask-login field
    authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, email):
        self.email = email

    def hash_password(self, password):
        print password
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        print password
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration = 600):
        s = Serializer(SECRET_KEY, expires_in = expiration)
        return s.dumps({ 'id': self.id })

    def __repr__(self):
        return '<User %r>' % self.email

    # flask-login methods
    def is_active(self):
        return True # all users are active

    def get_id(self):
        return self.email # """Return the email address to satisfy Flask-Login's requirements."""

    def is_authenticated(self):
        return self.authenticated #"""Return True if the user is authenticated."""

    def is_anonymous(self):
        return False #"""False, as anonymous users aren't supported."""

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user
