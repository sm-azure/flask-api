from flask import Flask

from model.database import db
from routes.views import apis
from routes.views2 import posts

def create_app():
    application = Flask(__name__)
    application.config.from_object('config')
    db.init_app(application)
    # register the blueprints
    application.register_blueprint(apis)
    application.register_blueprint(posts)
    return application

if __name__ == '__main__':
    #application.debug = True
    create_app().run(host='0.0.0.0', port=3000)
    #application.run()
