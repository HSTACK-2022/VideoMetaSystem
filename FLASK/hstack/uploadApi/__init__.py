from flask import Flask
from flask_restx import Api

from . import extractMetadata


def create_app():
    app = Flask(__name__)
    api = Api(app)

    app.config.from_pyfile('config.py')

    # Namespace
    api.add_namespace(extractMetadata.Upload, '/upload')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port='8000', debug=True)