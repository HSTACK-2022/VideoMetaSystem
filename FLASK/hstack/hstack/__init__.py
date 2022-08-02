from venv import create
from flask import Flask
from flask_restx import Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text

from . import models


def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:hstackdbadmin@localhost/hstackDB"
    models.db.init_app(app)

    # Blueprint
    from .views import main_views
    from .views import search_views
    from .views import detail_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(search_views.bp)
    app.register_blueprint(detail_views.bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()