from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'

db=SQLAlchemy(app)

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
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
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
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user

class VPNTunnel(db.Model):
    __tablename__ = 'vpn_tunnels'
    tunnel_id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.String(80), db.ForeignKey('managed_account.account_id'), nullable=False)
    fits_ticket = db.Column(db.String(80))
    firewall_ticket = db.Column(db.String(80))
    firewall_date = db.Column(db.DateTime)
    vpn_id = db.Column(db.String(80))
    ciso = db.Column(db.String(80))

    def __init__(self, account_id, fits_ticket, firewall_ticket,
                    firewall_date,vpn_id, ciso):
        self.account_id = account_id
        self.fits_ticket = fits_ticket
        self.firewall_ticket = firewall_ticket
        self.firewall_date = firewall_date
        self.vpn_id = vpn_id
        self.ciso = ciso

    def __repr__(self):
        #return '<VPNTunnel %r, %r ,%r >' % self.tunnel_id, self.account_id, self.ciso
        return "<VPNTunnel {0}, {1} ,{2}>".format(self.tunnel_id, self.account_id, self.ciso)

class ManagedAccount(db.Model):
    __tablename__ = 'managed_account'
    account_id = db.Column(db.String(80), primary_key=True, unique=True)
    fits_order_id = db.Column(db.String(80))
    org_id = db.Column(db.String(80))
    cost_center = db.Column(db.String(80))
    cloud_vendor  = db.Column(db.String(80))
    is_operational = db.Column(db.Boolean)
    service_start_date = db.Column(db.Date)
    service_stop_date = db.Column(db.Date)
    is_productive = db.Column(db.Boolean)
    is_aws_enterprise_support_enabled = db.Column(db.Boolean)

    def __init__(self, account_id, fits_order_id, org_id, cost_center,
        cloud_vendor, is_operational, service_start_date,
        service_stop_date, is_productive, is_aws_enterprise_support_enabled  ):
        self.account_id = account_id
        self.fits_order_id = fits_order_id
        self.org_id = org_id
        self.cost_center = cost_center
        self.cloud_vendor = cloud_vendor
        self.is_operational = is_operational
        self.service_start_date = service_start_date
        self.service_stop_date = service_stop_date
        self.is_productive = is_productive
        self.is_aws_enterprise_support_enabled = is_aws_enterprise_support_enabled


    def __repr__(self):
        #return ''<MCA %r, %r ,%r >' % self.account_id, self.cloud_vendor, self.service_start_date
        return "<MCA {0} {1} {2}>".format(self.account_id, self.cloud_vendor, self.service_start_date)
