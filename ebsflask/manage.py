from application import create_app, db
#from model.database import db

#db.metadata.create_all(db.engine)

db.create_all(app=create_app())
