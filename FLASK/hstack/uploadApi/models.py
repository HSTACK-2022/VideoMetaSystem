# coding: utf-8
from .config import DB as db

class Keyword(db.Model):
    __tablename__ = 'keywords'

    id = db.Column(db.ForeignKey('videopath.id'), primary_key=True, nullable=False)
    keyword = db.Column(db.String(10), primary_key=True, nullable=False)
    expose = db.Column(db.Integer, nullable=False)
    sysdef = db.Column(db.Integer, server_default=db.FetchedValue())
    percent = db.Column(db.Float, nullable=False, default=0)

    videopath = db.relationship('Videopath', primaryjoin='Keyword.id == Videopath.id', backref='keywords')

class Timestamp(db.Model):
    __tablename__ = 'timestamp'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    time = db.Column(db.String(10), primary_key=True, nullable=False)
    subtitle = db.Column(db.String(100))
    expose = db.Column(db.Integer, nullable=False)
    sysdef = db.Column(db.Integer, server_default=db.FetchedValue())

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
        db.CheckConstraint("(`method` in (_utf8mb3'PPT',_utf8mb3'실습'))"),
        db.CheckConstraint("(`narrative` in (_utf8mb3'description',_utf8mb3'application',_utf8mb3'description/application'))")
    )

    id = db.Column(db.ForeignKey('videopath.id'), primary_key=True, nullable=False)
    title = db.Column(db.String(50), nullable=False)
    presenter = db.Column(db.String(50))
    category = db.Column(db.String(20))
    category_percent = db.Column(db.String(30))
    narrative = db.Column(db.String(30))
    method = db.Column(db.String(10))
    videoLength = db.Column(db.String(10))
    videoFrame = db.Column(db.String(10))
    videoType = db.Column(db.String(5))
    videoSize = db.Column(db.String(10))
    uploadDate = db.Column(db.Date)
    voiceManRate = db.Column(db.Float)
    voiceWomanRate = db.Column(db.Float)

    videopath = db.relationship('Videopath', primaryjoin='Metadatum.id == Videopath.id', backref='metadata')