from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from billingmodel import db
from billingmodel import User, ManagedAccount, VPNTunnel

import datetime

app= Flask(__name__)

admin = User('admin', 'admin@example.com')
guest = User('guest', 'guest@example.com')
start_date = datetime.datetime.strptime('15-5-2015', '%d-%m-%Y').date()
end_date = datetime.datetime.max.date()
mca  = ManagedAccount('2384768234554', '','ARE243', '12384665234', 'AWS' ,
        True, start_date, end_date, True, False)

tunnel1 = VPNTunnel('238476823455', '1234', '2222', start_date, 'vpn1', 'Mr. CISO')


User.query.delete()
ManagedAccount.query.delete()
VPNTunnel.query.delete()

db.session.add(mca)
db.session.add(tunnel1)
db.session.add(admin)
db.session.add(guest)
db.session.commit()


users = User.query.all()
print users
mcas = ManagedAccount.query.all()
print mcas
print VPNTunnel.query.all()
