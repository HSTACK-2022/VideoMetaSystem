# Api calls
from flask import jsonify
from flask import request
from flask import current_app as app # app.config 사용을 위함
from flask_restx import Resource, Namespace
from werkzeug.utils import secure_filename

from . import extractMetadata


Upload = Namespace('Upload')

@Upload.route('')
class ExtractMetadata(Resource):
    def post(self):
        fileTitle = request.form.get('title')
        print(fileTitle)
        filePresenter = request.form.get("presenter")
        print(filePresenter)
        uploadURL = request.form.get('uploadURL')
        print(uploadURL)
        
        totalDic = extractMetadata.extract(fileTitle, filePresenter, uploadURL)
        return jsonify(totalDic)