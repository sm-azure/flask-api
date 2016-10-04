from flask import Flask

from model.database import db
from routes.views import apis
from routes.views2 import posts
from utils.security import login_manager

from logging.handlers import RotatingFileHandler
import logging

def create_app():

    # app and db initialization
    app = Flask(__name__)
    app.config.from_object('config')
    db.init_app(app)

    # login manager
    login_manager.init_app(app)

    # setup logging
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s' '[in %(pathname)s:%(lineno)d]')
    #handler = RotatingFileHandler('/home/vagrant/opt/python/log/application.log', maxBytes=1024,backupCount=5)
    handler = RotatingFileHandler('/opt/python/log/application.log', maxBytes=1024,backupCount=5)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)

    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)

    app.logger.error("Blah blah")

    # register the blueprints after login manager
    app.register_blueprint(apis)
    app.register_blueprint(posts)

    return app

# ebs requires application to be made available by default
application = create_app()

if __name__ == '__main__':
    application.debug = True
    #application.run(host='0.0.0.0', port=3000)
    application.run()
