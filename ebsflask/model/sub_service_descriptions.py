from database import db

class SubServiceDescriptions(db.Model):
    __tablename__ = 'sub_service_descriptions'
    sub_service_id = db.Column(db.Integer, primary_key=True)
    sub_service_name = db.Column(db.String(80), unique= True)
    sub_service_unit_cost = db.Column(db.Float)
    is_sub_service_per_user = db.Column(db.Boolean)

    def __init__(self, sub_service_name, sub_service_unit_cost,
        is_sub_service_per_user):
        self.sub_service_name = sub_service_name
        self.sub_service_unit_cost = sub_service_unit_cost
        self.is_sub_service_per_user = is_sub_service_per_user

    def __repr__(self):
        return "<SSD {0} {1} {2}>".format(self.sub_service_name,
        self.sub_service_unit_cost, self.is_sub_service_per_user)
