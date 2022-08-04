from flask import Flask
from flask_restx import Api

from . import main


def create_app():
    app = Flask(__name__)
    api = Api(app)

    app.config.from_pyfile('config.py')

    # Namespace
    api.add_namespace(main.Upload, '/upload')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()