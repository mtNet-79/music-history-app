
# from os.path import join, dirname
# from dotenv import load_dotenv
# from logging import StreamHandler
# from sys import stdout
# import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

def create_app(test_config=None):
    # from flaskr import routes
    # app.register_blueprint(routes.main)
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.Config')
    # app.config.from_pyfile('config.py')
    
    # Load the file specified by the APP_CONFIG_FILE environment variable
    # Variables defined here will override those in the default configuration
    # app.config.from_envvar('APP_CONFIG_FILE')
    from models import setup_db
    setup_db(app)
    
    return app

    # with app.app_context():
    #     from . import routes
    #     app.register_blueprint(routes.main)
    #     return app

# dotenv_path = join(dirname(__file__), '../.env')
# load_dotenv(dotenv_path)

# db = SQLAlchemy()

# def create_app():
#     from api.kittens import kittens_api
#     from views.index import index_view

#     app = Flask(__name__)
#     app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#     app.register_blueprint(kittens_api.blueprint, url_prefix='/api')
#     app.register_blueprint(index_view)

#     db.init_app(app)

#     handler = StreamHandler(stdout)
#     app.logger.addHandler(handler)
#     return app