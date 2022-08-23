# coding: utf-8
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class AuthGroup(db.Model):
    __tablename__ = 'auth_group'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)



class AuthGroupPermission(db.Model):
    __tablename__ = 'auth_group_permissions'
    __table_args__ = (
        db.Index('auth_group_permissions_group_id_permission_id_0cd325b0_uniq', 'group_id', 'permission_id'),
    )

    id = db.Column(db.BigInteger, primary_key=True)
    group_id = db.Column(db.ForeignKey('auth_group.id'), nullable=False)
    permission_id = db.Column(db.ForeignKey('auth_permission.id'), nullable=False, index=True)

    group = db.relationship('AuthGroup', primaryjoin='AuthGroupPermission.group_id == AuthGroup.id', backref='auth_group_permissions')
    permission = db.relationship('AuthPermission', primaryjoin='AuthGroupPermission.permission_id == AuthPermission.id', backref='auth_group_permissions')



class AuthPermission(db.Model):
    __tablename__ = 'auth_permission'
    __table_args__ = (
        db.Index('auth_permission_content_type_id_codename_01ab375a_uniq', 'content_type_id', 'codename'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    content_type_id = db.Column(db.ForeignKey('django_content_type.id'), nullable=False)
    codename = db.Column(db.String(100), nullable=False)

    content_type = db.relationship('DjangoContentType', primaryjoin='AuthPermission.content_type_id == DjangoContentType.id', backref='auth_permissions')



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
        db.Index('auth_user_groups_user_id_group_id_94350c0c_uniq', 'user_id', 'group_id'),
    )

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.ForeignKey('auth_user.id'), nullable=False)
    group_id = db.Column(db.ForeignKey('auth_group.id'), nullable=False, index=True)

    group = db.relationship('AuthGroup', primaryjoin='AuthUserGroup.group_id == AuthGroup.id', backref='auth_user_groups')
    user = db.relationship('AuthUser', primaryjoin='AuthUserGroup.user_id == AuthUser.id', backref='auth_user_groups')



class AuthUserUserPermission(db.Model):
    __tablename__ = 'auth_user_user_permissions'
    __table_args__ = (
        db.Index('auth_user_user_permissions_user_id_permission_id_14a6b632_uniq', 'user_id', 'permission_id'),
    )

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.ForeignKey('auth_user.id'), nullable=False)
    permission_id = db.Column(db.ForeignKey('auth_permission.id'), nullable=False, index=True)

    permission = db.relationship('AuthPermission', primaryjoin='AuthUserUserPermission.permission_id == AuthPermission.id', backref='auth_user_user_permissions')
    user = db.relationship('AuthUser', primaryjoin='AuthUserUserPermission.user_id == AuthUser.id', backref='auth_user_user_permissions')



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
    author_id = db.Column(db.ForeignKey('auth_user.id'), nullable=False, index=True)
    category_id = db.Column(db.ForeignKey('core_category.id'), index=True)

    author = db.relationship('AuthUser', primaryjoin='CorePost.author_id == AuthUser.id', backref='core_posts')
    category = db.relationship('CoreCategory', primaryjoin='CorePost.category_id == CoreCategory.id', backref='core_posts')



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
    content_type_id = db.Column(db.ForeignKey('django_content_type.id'), index=True)
    user_id = db.Column(db.ForeignKey('auth_user.id'), nullable=False, index=True)

    content_type = db.relationship('DjangoContentType', primaryjoin='DjangoAdminLog.content_type_id == DjangoContentType.id', backref='django_admin_logs')
    user = db.relationship('AuthUser', primaryjoin='DjangoAdminLog.user_id == AuthUser.id', backref='django_admin_logs')



class DjangoContentType(db.Model):
    __tablename__ = 'django_content_type'
    __table_args__ = (
        db.Index('django_content_type_app_label_model_76bd3d3b_uniq', 'app_label', 'model'),
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



class KeywordSearch(db.Model):
    __tablename__ = 'keyword_search'

    kKeyword = db.Column(db.String(50), primary_key=True)
    cnt = db.Column(db.Integer, nullable=False)



class Keyword(db.Model):
    __tablename__ = 'keywords'

    id = db.Column(db.ForeignKey('videopath.id'), primary_key=True, nullable=False)
    keyword = db.Column(db.String(10), primary_key=True, nullable=False)
    expose = db.Column(db.Integer, server_default=db.FetchedValue())
    sysdef = db.Column(db.Integer, server_default=db.FetchedValue())

    videopath = db.relationship('Videopath', primaryjoin='Keyword.id == Videopath.id', backref='keywords')



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



class Timestamp(db.Model):
    __tablename__ = 'timestamp'

    id = db.Column(db.ForeignKey('videopath.id'), primary_key=True, nullable=False)
    time = db.Column(db.String(50), primary_key=True, nullable=False)
    subtitle = db.Column(db.String(100))
    expose = db.Column(db.Integer, server_default=db.FetchedValue())
    sysdef = db.Column(db.Integer, server_default=db.FetchedValue())

    videopath = db.relationship('Videopath', primaryjoin='Timestamp.id == Videopath.id', backref='timestamps')



class TitleSearch(db.Model):
    __tablename__ = 'title_search'

    tiKeyword = db.Column(db.String(50), primary_key=True)
    cnt = db.Column(db.Integer, nullable=False)



class TotalSearch(db.Model):
    __tablename__ = 'total_search'

    tKeyword = db.Column(db.String(50), primary_key=True)
    cnt = db.Column(db.Integer, nullable=False)



class Videopath(db.Model):
    __tablename__ = 'videopath'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    videoAddr = db.Column(db.String(200))
    audioAddr = db.Column(db.String(100))
    textAddr = db.Column(db.String(100))
    imageAddr = db.Column(db.String(100))
    extracted = db.Column(db.Integer, server_default=db.FetchedValue())


class Metadatum(Videopath):
    __tablename__ = 'metadata'

    id = db.Column(db.ForeignKey('videopath.id'), primary_key=True)
    title = db.Column(db.String(50))
    presenter = db.Column(db.String(50))
    category = db.Column(db.String(20))
    narrative = db.Column(db.String(30))
    method = db.Column(db.String(10))
    videoLength = db.Column(db.Time)
    videoFrame = db.Column(db.String(10))
    videoType = db.Column(db.String(5))
    videoSize = db.Column(db.String(10))
    uploadDate = db.Column(db.Date)
    voiceManRate = db.Column(db.Float)
    voiceWomanRate = db.Column(db.Float)
