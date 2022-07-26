import os

BASE_DIR = os.path.dirname(__file__)

db = {
    'user' : 'root',
    'password' : '1891265',
    'host' : 'localhost',
    'port' : 3306,
    'database' : 'hstackdb'
}

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"