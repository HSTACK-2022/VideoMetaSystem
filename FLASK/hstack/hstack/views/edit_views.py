from flask import url_for
from flask import request
from flask import redirect
from flask import Blueprint
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

from hstack.config import DB
from hstack.models import Videopath
from hstack.models import Metadatum
from hstack.models import Keyword
from hstack.models import Timestamp
from sqlalchemy import and_

from hstack import makePPT

bp = Blueprint('edit', __name__, url_prefix='/')

def checkPW(pk, inputPW):
    res = dict()
    password = DB.session.query(Videopath).filter(Videopath.id == pk).first().password

    if password == None:
        res['isValid'] = True
    else:
        if (password == inputPW):
            res['isValid'] = True
        elif(inputPW == None):
            res['isValid'] = False
            res['errorMsg'] = ""
        else:
            res['isValid'] = False
            res['errorMsg'] = "잘못된 비밀번호입니다."

    return res


@bp.route('/detail/<int:pk>/edit', methods=['GET', 'POST'])
def editFile(pk):
    inputPW = request.form.get("password")
    check = checkPW(pk, inputPW)
    if check['isValid'] == False:
        return render_template('checkPW.html', pk = pk, error = check['errorMsg'])

    sysKEList = request.form.getlist("sysKEList")
    sysKCList = request.form.getlist("sysKCList")

    newUserKEList = request.form.getlist("newUserKEList")
    newUserKCList = request.form.getlist("newUserKCList")
    userKEList = request.form.getlist("userKEList")
    userKCList = request.form.getlist("userKCList")
        
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    print(sysKEList)
    print(sysKCList)
    print(userKEList)
    print(userKCList)
    print(newUserKEList)
    print(newUserKCList)
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

    
    # edit Keyword perc
    if (len(newUserKCList) != 0):
        sysKECount = len(DB.session.query(Keyword).filter(Keyword.id == pk).all())
        keywordCount = sysKECount + len(newUserKCList)
        percWeight = round(1/keywordCount, 3)           # for userdef Keywords
        sysWeight = round(sysKECount * percWeight, 3)   # for sysdef Keywords
        print(percWeight)

        for i in range(len(sysKEList)):
            oldPerc = DB.session.query(Keyword).filter(and_(Keyword.id == pk, Keyword.keyword.like(sysKCList[i]))).first().percent
            newPerc = round(oldPerc * sysWeight, 3)
            DB.session.query(Keyword).filter(and_(Keyword.id == pk, Keyword.keyword.like(sysKCList[i]))).update({"percent" : newPerc}, synchronize_session="fetch")
            DB.session.flush()
        for i in range(len(userKEList)):
            DB.session.query(Keyword).filter(and_(Keyword.id == pk, Keyword.keyword.like(userKCList[i]))).update({"percent" : percWeight}, synchronize_session="fetch")
            DB.session.flush()
        for i in range(len(newUserKCList)):
            k = Keyword(
                id = DB.session.query(Videopath).filter(Videopath.id == pk).first().id,
                keyword = newUserKCList[i],
                percent = percWeight,
                expose = newUserKEList[i],
                sysdef = 0
            )
            DB.session.add(k)
            DB.session.flush()

    for i in range(len(sysKEList)):
        DB.session.query(Keyword).filter(and_(Keyword.id == pk, Keyword.keyword.like(sysKCList[i]), Keyword.sysdef == 1)).update({"expose" : sysKEList[i]}, synchronize_session="fetch")
        DB.session.flush()
    for i in range(len(userKEList)):
        DB.session.query(Keyword).filter(and_(Keyword.id == pk, Keyword.keyword.like(userKCList[i]), Keyword.sysdef == 0)).update({"expose" : userKEList[i]}, synchronize_session="fetch")
        DB.session.flush()

    DB.session.commit()
    
    videoPath = DB.session.query(Videopath).filter(Videopath.id == pk).first().videoAddr 
    textPath = DB.session.query(Videopath).filter(Videopath.id == pk).first().textAddr

    try:
        with open(textPath, 'r', encoding='UTF-8-sig') as f:
            scripts = f.readlines()
    except FileNotFoundError as err:
        print(err)
        scripts = []

    # 이미지 받아오기
    pptImage = makePPT.getPPTImage(videoPath)

    return render_template('edit.html',
        pk = pk,
        pw = inputPW,
        videoaddr = videoPath,
        scripts = scripts,
        images = pptImage,
        keywords =  DB.session.query(Keyword).filter(and_(Keyword.id == pk, Keyword.sysdef == 1)).all(),
        userkeywords =  DB.session.query(Keyword).filter(and_(Keyword.id == pk, Keyword.sysdef == 0)).all(),
        metadatas = Metadatum.query.filter(Metadatum.id == pk).all(),
        timestamps =  Timestamp.query.filter(Timestamp.id == pk).all(),
    )