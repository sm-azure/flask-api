from database import db

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
