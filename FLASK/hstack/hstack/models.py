# coding: utf-8
from .config import DB as db


class BackgroundTask(db.Model):
    __tablename__ = 'background_task'
    __table_args__ = (
        db.CheckConstraint('(`creator_object_id` >= 0)'),
    )

    id = db.Column(db.BigInteger, primary_key=True)
    task_name = db.Column(db.String(190), nullable=False, index=True)
    task_params = db.Column(db.String, nullable=False)
    task_hash = db.Column(db.String(40), nullable=False, index=True)
    verbose_name = db.Column(db.String(255))
    priority = db.Column(db.Integer, nullable=False, index=True)
    run_at = db.Column(db.DateTime, nullable=False, index=True)
    repeat = db.Column(db.BigInteger, nullable=False)
    repeat_until = db.Column(db.DateTime)
    queue = db.Column(db.String(190), index=True)
    attempts = db.Column(db.Integer, nullable=False, index=True)
    failed_at = db.Column(db.DateTime, index=True)
    last_error = db.Column(db.String, nullable=False)
    locked_by = db.Column(db.String(64), index=True)
    locked_at = db.Column(db.DateTime, index=True)
    creator_object_id = db.Column(db.Integer)
    creator_content_type_id = db.Column(db.ForeignKey('django_content_type.id'), index=True)

    creator_content_type = db.relationship('DjangoContentType', primaryjoin='BackgroundTask.creator_content_type_id == DjangoContentType.id', backref='background_tasks')

class BackgroundTaskCompletedtask(db.Model):
    __tablename__ = 'background_task_completedtask'
    __table_args__ = (
        db.CheckConstraint('(`creator_object_id` >= 0)'),
    )

    id = db.Column(db.BigInteger, primary_key=True)
    task_name = db.Column(db.String(190), nullable=False, index=True)
    task_params = db.Column(db.String, nullable=False)
    task_hash = db.Column(db.String(40), nullable=False, index=True)
    verbose_name = db.Column(db.String(255))
    priority = db.Column(db.Integer, nullable=False, index=True)
    run_at = db.Column(db.DateTime, nullable=False, index=True)
    repeat = db.Column(db.BigInteger, nullable=False)
    repeat_until = db.Column(db.DateTime)
    queue = db.Column(db.String(190), index=True)
    attempts = db.Column(db.Integer, nullable=False, index=True)
    failed_at = db.Column(db.DateTime, index=True)
    last_error = db.Column(db.String, nullable=False)
    locked_by = db.Column(db.String(64), index=True)
    locked_at = db.Column(db.DateTime, index=True)
    creator_object_id = db.Column(db.Integer)
    creator_content_type_id = db.Column(db.ForeignKey('django_content_type.id'), index=True)

    creator_content_type = db.relationship('DjangoContentType', primaryjoin='BackgroundTaskCompletedtask.creator_content_type_id == DjangoContentType.id', backref='background_task_completedtasks')





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




class KeywordSearch(db.Model):
    __tablename__ = 'keyword_search'

    kKeyword = db.Column(db.String(50), primary_key=True)
    cnt = db.Column(db.Integer, nullable=False)


class PresenterSearch(db.Model):
    __tablename__ = 'presenter_search'

    pKeyword = db.Column(db.String(50), primary_key=True)
    cnt = db.Column(db.Integer, nullable=False)


class ScriptSearch(db.Model):
    __tablename__ = 'script_search'

    id = db.Column(db.ForeignKey('videopath.id'), primary_key=True, nullable=False)
    sKeyword = db.Column(db.String(50), primary_key=True, nullable=False)
    cnt = db.Column(db.Integer, nullable=False)

    videopath = db.relationship('Videopath', primaryjoin='ScriptSearch.id == Videopath.id', backref='script_searches')



class TitleSearch(db.Model):
    __tablename__ = 'title_search'

    tiKeyword = db.Column(db.String(50), primary_key=True)
    cnt = db.Column(db.Integer, nullable=False)



class TotalSearch(db.Model):
    __tablename__ = 'total_search'

    tKeyword = db.Column(db.String(50), primary_key=True)
    cnt = db.Column(db.Integer, nullable=False)