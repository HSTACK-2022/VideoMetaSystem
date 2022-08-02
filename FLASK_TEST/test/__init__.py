from venv import create
from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text

from . import config
from . import models

def create_app():
    app = Flask(__name__)
    api = Api(app)

    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:hstackdbadmin@localhost/hstackDB"
    models.db.init_app(app)

    # Blueprint
    from .views import upload_views
    app.register_blueprint(upload_views.bp)

    return app

if __name__ == '__main__':
    app.run()