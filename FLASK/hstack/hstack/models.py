# coding: utf-8
from turtle import update
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class AuthGroup(db.Model):
    __tablename__ = 'auth_group'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)


class AuthGroupPermission(db.Model):
    __tablename__ = 'auth_group_permissions'
    __table_args__ = (
        db.Index('auth_group_permissions_group_id_permission_id_0cd325b0_uniq',
                 'group_id', 'permission_id'),
    )

    id = db.Column(db.BigInteger, primary_key=True)
    group_id = db.Column(db.ForeignKey('auth_group.id'), nullable=False)
    permission_id = db.Column(db.ForeignKey(
        'auth_permission.id'), nullable=False, index=True)

    group = db.relationship(
        'AuthGroup', primaryjoin='AuthGroupPermission.group_id == AuthGroup.id', backref='auth_group_permissions')
    permission = db.relationship(
        'AuthPermission', primaryjoin='AuthGroupPermission.permission_id == AuthPermission.id', backref='auth_group_permissions')


class AuthPermission(db.Model):
    __tablename__ = 'auth_permission'
    __table_args__ = (
        db.Index('auth_permission_content_type_id_codename_01ab375a_uniq',
                 'content_type_id', 'codename'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    content_type_id = db.Column(db.ForeignKey(
        'django_content_type.id'), nullable=False)
    codename = db.Column(db.String(100), nullable=False)

    content_type = db.relationship(
        'DjangoContentType', primaryjoin='AuthPermission.content_type_id == DjangoContentType.id', backref='auth_permissions')


class AuthUser(db.Model):
    __tablename__ = 'auth_user'

    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(128), nullable=False)
    last_login = db.Column(db.DateTime)
    is_superuser = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(150), nullable=False, unique=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(254), nullable=False)
    is_staff = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Integer, nullable=False)
    date_joined = db.Column(db.DateTime, nullable=False)


class AuthUserGroup(db.Model):
    __tablename__ = 'auth_user_groups'
    __table_args__ = (
        db.Index('auth_user_groups_user_id_group_id_94350c0c_uniq',
                 'user_id', 'group_id'),
    )

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.ForeignKey('auth_user.id'), nullable=False)
    group_id = db.Column(db.ForeignKey('auth_group.id'),
                         nullable=False, index=True)

    group = db.relationship(
        'AuthGroup', primaryjoin='AuthUserGroup.group_id == AuthGroup.id', backref='auth_user_groups')
    user = db.relationship(
        'AuthUser', primaryjoin='AuthUserGroup.user_id == AuthUser.id', backref='auth_user_groups')


class AuthUserUserPermission(db.Model):
    __tablename__ = 'auth_user_user_permissions'
    __table_args__ = (
        db.Index('auth_user_user_permissions_user_id_permission_id_14a6b632_uniq',
                 'user_id', 'permission_id'),
    )

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.ForeignKey('auth_user.id'), nullable=False)
    permission_id = db.Column(db.ForeignKey(
        'auth_permission.id'), nullable=False, index=True)

    permission = db.relationship(
        'AuthPermission', primaryjoin='AuthUserUserPermission.permission_id == AuthPermission.id', backref='auth_user_user_permissions')
    user = db.relationship(
        'AuthUser', primaryjoin='AuthUserUserPermission.user_id == AuthUser.id', backref='auth_user_user_permissions')


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
    creator_content_type_id = db.Column(
        db.ForeignKey('django_content_type.id'), index=True)

    creator_content_type = db.relationship(
        'DjangoContentType', primaryjoin='BackgroundTask.creator_content_type_id == DjangoContentType.id', backref='background_tasks')


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
    creator_content_type_id = db.Column(
        db.ForeignKey('django_content_type.id'), index=True)

    creator_content_type = db.relationship(
        'DjangoContentType', primaryjoin='BackgroundTaskCompletedtask.creator_content_type_id == DjangoContentType.id', backref='background_task_completedtasks')


class CoreCategory(db.Model):
    __tablename__ = 'core_category'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    slug = db.Column(db.String(200), nullable=False, unique=True)


class CoreDocument(db.Model):
    __tablename__ = 'core_document'

    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    uploadedFile = db.Column(db.String(100), nullable=False)
    dateTimeOfUpload = db.Column(db.DateTime, nullable=False)


class CorePost(db.Model):
    __tablename__ = 'core_post'

    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    hook_text = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String, nullable=False)
    head_image = db.Column(db.String(100))
    head_video = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, nullable=False)
    update_at = db.Column(db.DateTime, nullable=False)
    author_id = db.Column(db.Integer, index=True)
    category_id = db.Column(db.ForeignKey('core_category.id'), index=True)

    category = db.relationship(
        'CoreCategory', primaryjoin='CorePost.category_id == CoreCategory.id', backref='core_posts')


class DjangoAdminLog(db.Model):
    __tablename__ = 'django_admin_log'
    __table_args__ = (
        db.CheckConstraint('(`action_flag` >= 0)'),
    )

    id = db.Column(db.Integer, primary_key=True)
    action_time = db.Column(db.DateTime, nullable=False)
    object_id = db.Column(db.String)
    object_repr = db.Column(db.String(200), nullable=False)
    action_flag = db.Column(db.SmallInteger, nullable=False)
    change_message = db.Column(db.String, nullable=False)
    content_type_id = db.Column(db.ForeignKey(
        'django_content_type.id'), index=True)
    user_id = db.Column(db.ForeignKey('auth_user.id'),
                        nullable=False, index=True)

    content_type = db.relationship(
        'DjangoContentType', primaryjoin='DjangoAdminLog.content_type_id == DjangoContentType.id', backref='django_admin_logs')
    user = db.relationship(
        'AuthUser', primaryjoin='DjangoAdminLog.user_id == AuthUser.id', backref='django_admin_logs')


class DjangoContentType(db.Model):
    __tablename__ = 'django_content_type'
    __table_args__ = (
        db.Index('django_content_type_app_label_model_76bd3d3b_uniq',
                 'app_label', 'model'),
    )

    id = db.Column(db.Integer, primary_key=True)
    app_label = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)


class DjangoMigration(db.Model):
    __tablename__ = 'django_migrations'

    id = db.Column(db.BigInteger, primary_key=True)
    app = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    applied = db.Column(db.DateTime, nullable=False)


class DjangoSession(db.Model):
    __tablename__ = 'django_session'

    session_key = db.Column(db.String(40), primary_key=True)
    session_data = db.Column(db.String, nullable=False)
    expire_date = db.Column(db.DateTime, nullable=False, index=True)


class Keyword(db.Model):
    __tablename__ = 'keywords'

    id = db.Column(db.ForeignKey('videopath.id'),
                   primary_key=True, nullable=False)
    keyword = db.Column(db.String(10), primary_key=True, nullable=False)
    expose = db.Column(db.Integer, nullable=False)
    sysdef = db.Column(db.Integer, server_default=db.FetchedValue())

    videopath = db.relationship(
        'Videopath', primaryjoin='Keyword.id == Videopath.id', backref='keywords')


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
    logAddr = db.Column(db.String(100))
    extracted = db.Column(db.Integer, server_default=db.FetchedValue())


class Metadatum(Videopath):
    __tablename__ = 'metadata'
    __table_args__ = (
        db.CheckConstraint("(`method` in (_utf8mb3'PPT',_utf8mb3'실습'))"),
        db.CheckConstraint(
            "(`narrative` in (_utf8mb3'description',_utf8mb3'application',_utf8mb3'description/application'))")
    )

    id = db.Column(db.ForeignKey('videopath.id'), primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    presenter = db.Column(db.String(50))
    category = db.Column(db.String(20))
    narrative = db.Column(db.String(30))
    method = db.Column(db.String(10))
    videoLength = db.Column(db.String(10))
    videoFrame = db.Column(db.String(10))
    videoType = db.Column(db.String(5))
    videoSize = db.Column(db.String(10))
    uploadDate = db.Column(db.Date)
    voiceManRate = db.Column(db.Float)
    voiceWomanRate = db.Column(db.Float)


class TotalSearch(db.Model):
    __tablename__ = 'total_search'

    tKeyword = db.Column(db.String(50), primary_key=True)
    cnt = db.Column(db.Integer, nullable=False)

    def __init__(self, tKeyword, cnt, **kwargs):
        self.tKeyword = tKeyword
        self.cnt = cnt

    def __repr__(self):
        return f"<TotalSearch('{self.tKeyword}', '{self.cnt}')>"


class TitleSearch(db.Model):
    __tablename__ = 'title_search'

    tiKeyword = db.Column(db.String(50), primary_key=True)
    cnt = db.Column(db.Integer, nullable=False)

    def __init__(self, tiKeyword, cnt, **kwargs):
        self.tiKeyword = tiKeyword
        self.cnt = cnt

    def __repr__(self):
        return f"<TitleSearch('{self.tiKeyword}', '{self.cnt}')>"


class KeywordSearch(db.Model):
    __tablename__ = 'keyword_search'

    kKeyword = db.Column(db.String(50), primary_key=True)
    cnt = db.Column(db.Integer, nullable=False)

    def __init__(self, kKeyword, cnt, **kwargs):
        self.kKeyword = kKeyword
        self.cnt = cnt

    def __repr__(self):
        return f"<KeywordSearch('{self.kKeyword}', '{self.cnt}')>"


class PresenterSearch(db.Model):
    __tablename__ = 'presenter_search'

    pKeyword = db.Column(db.String(50), primary_key=True)
    cnt = db.Column(db.Integer, nullable=False)

    def __init__(self, pKeyword, cnt, **kwargs):
        self.pKeyword = pKeyword
        self.cnt = cnt

    def __repr__(self):
        return f"<PresenterSearch('{self.pKeyword}', '{self.cnt}')>"


class ScriptSearch(db.Model):
    __tablename__ = 'script_search'

    id = db.Column(db.ForeignKey('videopath.id'),
                   primary_key=True, nullable=False)
    sKeyword = db.Column(db.String(50), primary_key=True, nullable=False)
    cnt = db.Column(db.Integer, nullable=False)

    videopath = db.relationship(
        'Videopath', primaryjoin='ScriptSearch.id == Videopath.id', backref='script_search')

    def __init__(self, id, sKeyword, cnt, **kwargs):
        self.id = id
        self.sKeyword = sKeyword
        self.cnt = cnt

    def __repr__(self):
        return f"<ScriptSearch('{self.sKeyword}','{self.pKeyword}', '{self.cnt}')>"
