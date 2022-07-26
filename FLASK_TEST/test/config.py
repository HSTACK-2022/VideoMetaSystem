import os

BASE_DIR = os.path.dirname(__file__)

db = {
    'user' : 'root',
    'password' : 'hstackdbadmin',
    'host' : 'localhost',
    'port' : 3306,
    'database' : 'hstackDB_TEST'
}

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"