from flask import url_for
from flask import request
from flask import redirect
from flask import Blueprint
from flask import render_template
from flask import send_from_directory

from hstack import models
from hstack import searchAll

# from sqlalchemy import SQLAlchemy
from hstack.models import TotalSearch
import os
import re
import platform
import datetime #로그파일 시간

from flask_sqlalchemy import SQLAlchemy
from hstack import countSearch

db = SQLAlchemy()


OS = platform.system()
bp = Blueprint('manage', __name__, url_prefix='/')


@bp.route('/manage/', methods=['GET', 'POST'])
def manage():
    text = countSearch.total_search
    print("^^^^^^66K6DW;LDFKG")
    print(text)

    return render_template('data.html')