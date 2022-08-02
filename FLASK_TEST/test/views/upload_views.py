from flask import Blueprint
from flask import jsonify
from flask import Flask, Request
from flask import current_app as app # app.config 사용을 위함
from flask_restx import Resource, Api

from test import extractMetadata

# 상수 설정
api = Api(app)
bp = Blueprint('main', __name__, url_prefix='/')

#@bp.route('/')
#def home():
#    return render_template('home.html')

@api.route('/upload')
class ExtractMetadata(Resource):
    def post(self):
        totalDic = extractMetadata.extract("title", "presenter", ".\\media\\Uploaded\\algo\\algo.mp4")
        return jsonify(totalDic)