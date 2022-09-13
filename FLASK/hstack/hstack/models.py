# coding: utf-8
from .config import DB as db


class Keyword(db.Model):
    __tablename__ = 'keywords'

    id = db.Column(db.ForeignKey('videopath.id'),
                   primary_key=True, nullable=False)
    keyword = db.Column(db.String(10), primary_key=True, nullable=False)
    expose = db.Column(db.Integer, server_default=db.FetchedValue())
    sysdef = db.Column(db.Integer, server_default=db.FetchedValue())
    percent = db.Column(db.Float, nullable=False, default=0)

    videopath = db.relationship(
        'Videopath', primaryjoin='Keyword.id == Videopath.id', backref='keywords')


class Timestamp(db.Model):
    __tablename__ = 'timestamp'

    id = db.Column(db.ForeignKey('videopath.id'),
                   primary_key=True, nullable=False)
    time = db.Column(db.String(10), primary_key=True, nullable=False)
    subtitle = db.Column(db.String(100))
    expose = db.Column(db.Integer, server_default=db.FetchedValue())
    sysdef = db.Column(db.Integer, server_default=db.FetchedValue())

    videopath = db.relationship(
        'Videopath', primaryjoin='Timestamp.id == Videopath.id', backref='timestamps')


class Videopath(db.Model):
    __tablename__ = 'videopath'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    videoAddr = db.Column(db.String(200))
    audioAddr = db.Column(db.String(200))
    textAddr = db.Column(db.String(200))
    imageAddr = db.Column(db.String(200))
    extracted = db.Column(db.Integer)
    password = db.Column(db.String(10), nullable=True, default=None)


class Metadatum(db.Model):
    __tablename__ = 'metadata'
    __table_args__ = (
        db.CheckConstraint(
            "(`presentation` in (_utf8mb3'Dynamic',_utf8mb3'Static')"),
        db.CheckConstraint(
            "(`narrative` in (_utf8mb3'description',_utf8mb3'application',_utf8mb3'description/application'))")
    )

    id = db.Column(db.ForeignKey('videopath.id'),
                   primary_key=True, nullable=False)
    title = db.Column(db.String(50), nullable=False)
    presenter = db.Column(db.String(50))
    category = db.Column(db.String(20))
    category_percent = db.Column(db.String(30))
    narrative = db.Column(db.String(30))
    presentation = db.Column(db.String(10))
    videoLength = db.Column(db.String(10))
    videoFrame = db.Column(db.String(10))
    videoType = db.Column(db.String(5))
    videoSize = db.Column(db.String(10))
    uploadDate = db.Column(db.Date)
    voiceManRate = db.Column(db.Float)
    voiceWomanRate = db.Column(db.Float)

    category_percent = db.Column(db.String(30))

    videopath = db.relationship(
        'Videopath', primaryjoin='Metadatum.id == Videopath.id', backref='metadata')


class PresenterSearch(db.Model):
    __tablename__ = 'presenter_search'

    pKeyword = db.Column(db.String(50), primary_key=True)
    cnt = db.Column(db.Integer, nullable=False)

    def __init__(self, pKeyword, cnt, **kwargs):
        self.pKeyword = pKeyword
        self.cnt = cnt

    def __repr__(self):
        return f"<PresenterSearch('{self.pKeyword}', '{self.cnt}')>"


class KeywordSearch(db.Model):
    __tablename__ = 'keyword_search'

    kKeyword = db.Column(db.String(50), primary_key=True)
    cnt = db.Column(db.Integer, nullable=False)

    def __init__(self, kKeyword, cnt, **kwargs):
        self.kKeyword = kKeyword
        self.cnt = cnt

    def __repr__(self):
        return f"<KeywordSearch('{self.kKeyword}', '{self.cnt}')>"


class TitleSearch(db.Model):
    __tablename__ = 'title_search'

    tiKeyword = db.Column(db.String(50), primary_key=True)
    cnt = db.Column(db.Integer, nullable=False)

    def __init__(self, tiKeyword, cnt, **kwargs):
        self.tiKeyword = tiKeyword
        self.cnt = cnt

    def __repr__(self):
        return f"<TitleSearch('{self.tiKeyword}', '{self.cnt}')>"


class TotalSearch(db.Model):
    __tablename__ = 'total_search'

    tKeyword = db.Column(db.String(50), primary_key=True)
    cnt = db.Column(db.Integer, nullable=False)

    def __init__(self, tKeyword, cnt, **kwargs):
        self.tKeyword = tKeyword
        self.cnt = cnt

    def __repr__(self):
        return f"<TotalKeyword('{self.tKeyword}', '{self.cnt}')>"


class UploadTime(db.Model):
    __tablename__ = 'upload_time'

    id = db.Column(db.ForeignKey('videopath.id'),
                   primary_key=True, nullable=False)
    time = db.Column(db.Float)
    size = db.Column(db.Float)

    def __init__(self, id, time, size, **kwargs):
        self.id = id
        self.time = time
        self.size = size

    def __repr__(self):
        return f"<UpoladTime('{self.id}', '{self.time}', '{self.size}')>"
