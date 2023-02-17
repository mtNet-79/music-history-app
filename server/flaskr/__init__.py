
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    if test_config:
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
        migrate.init_app(app, db, compare_type=True)

    with app.app_context():
        if test_config:
            db.create_all()
        from .routes import api
        app.register_blueprint(api)

        return app
        
# from .models.performer import Performer
# from .models.recording import Recording
# from .models.tables import (contemporaries, composer_performer, 
# composer_style, performer_style, composer_title, performer_title)
# from .models.style import Style
# from .models.period import Period
# from .models.composition import Composition
# from .models.composer import Composer
