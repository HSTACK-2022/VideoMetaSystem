from django.db import models

# Create your models here.
class Document(models.Model):
    title = models.CharField(max_length = 200)
    uploadedFile = models.FileField(upload_to = "Uploaded/Video")
    dateTimeOfUpload = models.DateTimeField(auto_now = True)

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

class Videopath(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=50)
    videoaddr = models.CharField(db_column='videoAddr', max_length=100, blank=True, null=True)  # Field name made lowercase.
    audioaddr = models.CharField(db_column='audioAddr', max_length=100, blank=True, null=True)  # Field name made lowercase.
    textaddr = models.CharField(db_column='textAddr', max_length=100, blank=True, null=True)  # Field name made lowercase. 
    imageaddr = models.CharField(db_column='imageAddr', max_length=100, blank=True, null=True)  # Field name made lowercase. 

    class Meta:
        managed = False
        db_table = 'videopath'    

class Keywords(models.Model):
    id = models.ForeignKey(Videopath, db_column='id', primary_key=True, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=10)
    expose = models.IntegerField(default=True)
    sysdef = models.IntegerField(default=True)

    class Meta:
        managed = False
        db_table = 'keywords'
        unique_together = (('id', 'keyword'),)

class Timestamp(models.Model):
    id = models.ForeignKey(Videopath, db_column='id', primary_key=True, on_delete=models.CASCADE)
    time = models.TimeField()
    subtitle = models.CharField(max_length=100, blank=True, null=True)
    expose = models.IntegerField(default=True)
    sysdef = models.IntegerField(default=True)

    class Meta:
        managed = False
        db_table = 'timestamp'
        unique_together = (('id', 'time'),)

class Metadata(models.Model):
    id = models.ForeignKey(Videopath, db_column='id', primary_key=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    presenter = models.CharField(max_length=50, blank=True, null=True)
    topic = models.CharField(max_length=20, blank=True, null=True)
    narrative = models.CharField(max_length=30, blank=True, null=True)
    method = models.CharField(max_length=10, blank=True, null=True)   
    videolength = models.TimeField(db_column='videoLength', blank=True, null=True)  # Field name made lowercase.
    videoframe = models.CharField(db_column='videoFrame', max_length=10, blank=True, null=True)  # Field name made lowercase.
    videotype = models.CharField(db_column='videoType', max_length=5, blank=True, null=True)  # Field name made lowercase.  
    videosize = models.CharField(db_column='videoSize', max_length=10, blank=True, null=True)  # Field name made lowercase. 
    uploaddate = models.DateField(db_column='uploadDate', blank=True, null=True)  # Field name made lowercase.
    voicenum = models.IntegerField(db_column='voiceNum', blank=True, null=True)  # Field name made lowercase.
    voicemanrate = models.FloatField(db_column='voiceManRate', blank=True, null=True)  # Field name made lowercase.
    voicewomanrate = models.FloatField(db_column='voiceWomanRate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'metadata'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CoreDocument(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200)
    uploadedfile = models.CharField(db_column='uploadedFile', max_length=100)  # Field name made lowercase.
    datetimeofupload = models.DateTimeField(db_column='dateTimeOfUpload')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'core_document'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'