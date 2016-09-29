from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db=SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, index = True)
    password_hash = db.Column(db.String(128))

    def __init__(self, email):
        self.email = email

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, pasword):
        return pwd_context.verify(password, self.password_hash)

    def __repr__(self):
        return '<User %r>' % self.email

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
