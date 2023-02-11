from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    if test_config:
        print("HERE")
        app.config.from_object('config.TestingConfig')
        # from models import setup_test_db
        # setup_test_db(app)
        # db.app = app
        db.init_app(app)

        # db.app = app
        # db.init_app(app)
    else:
        app.config.from_object('config.Config')
        # from models import setup_db
        db.init_app(app)
        migrate.init_app(app, db)

    with app.app_context():
        from . import routes
        app.register_blueprint(routes.api)
        return app
