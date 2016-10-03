from database import db

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
