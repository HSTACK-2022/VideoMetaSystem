import os
import platform

from flask_sqlalchemy import SQLAlchemy

OS = platform.system()
BASE_DIR = os.path.dirname(__file__)
UPLOAD_FILE_DIR = os.path.join('.', 'media', 'Uploaded')
UPLOAD_LOG_DIR = os.path.join('.', 'logs')

STT_API_KEY = {
    "2d40b072-37f1-4317-9899-33e0b3f5fb90",
    "80ff5736-f813-4686-aca6-472739d8ebe0",
    "25833dd1-e685-4f13-adc6-c85341d1bac5",
    "40c498a8-7d33-4909-9b60-427b3d0ccf8b", 
    "0913ccd7-0cd1-4455-8b60-7940aa54f7be"
}

db = {
    'user' : 'root',
    'password' : 'csedbadmin',
    'host' : 'localhost',
    'port' : 3306,
    'database' : 'hstackdb'
}

DB = SQLAlchemy()

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"
