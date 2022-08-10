from venv import create
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text

from . import config
from . import models


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:hstackdbadmin@localhost/hstackDB_TEST"
    models.db.init_app(app)

    # Blueprint
    from .views import main_views
    app.register_blueprint(main_views.bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()