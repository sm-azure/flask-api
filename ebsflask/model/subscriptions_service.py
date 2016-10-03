from database import db

class SubscriptionSubService(db.Model):
    __tablename__ = 'subscription_subservice'
    subscription_id = db.Column(db.Integer, primary_key=True)
    sub_service_id = db.Column(db.Integer,
        db.ForeignKey('sub_service_descriptions.sub_service_id')
        , nullable=False)
    account_id = db.Column(db.String(80),
        db.ForeignKey('managed_account.account_id'), nullable=False)
    is_operational = db.Column(db.Boolean)
    service_start_date = db.Column(db.Date)
    service_stop_date = db.Column(db.Date)
    total_users =db.Column(db.Integer)

    def __init__(self, sub_service_id, account_id, is_operational,
        service_start_date, service_stop_date, total_users):
        self.sub_service_id = sub_service_id
        self.account_id = account_id
        self.is_operational = is_operational
        self.service_start_date = service_start_date
        self.service_stop_date = service_stop_date
        self.total_users = total_users

    def __repr__(self):
        return "<SubscriptionSubService {0} {1} {2}".format(
            self.sub_service_id, self.account_id, self.total_users
        )
