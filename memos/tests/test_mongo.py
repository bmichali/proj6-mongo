import arrow
import nose  # Testing framework
from pymongo import MongoClient
import config

CONFIG = config.configuration()
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.WARNING)
log = logging.getLogger(__name__)

MONGO_CLIENT_URL = "mongodb://{}:{}@{}:{}/{}".format(
    CONFIG.DB_USER,
    CONFIG.DB_USER_PW,
    CONFIG.DB_HOST,
    CONFIG.DB_PORT,
    CONFIG.DB)

try:
    dbclient = MongoClient(MONGO_CLIENT_URL)
    db = getattr(dbclient, CONFIG.DB)
    collection = db.dated

except:
    print("Failure opening database.  Is Mongo running? Correct password?")
    sys.exit(1)


def test_add():
    records = []
    counter = 0
    collection.insert({"type": "test_memo", "token": 1})
    collection.insert({"type": "test_memo", "token": 2})


    assert 2 == collection.count()

def test_del():
    collection.delete_one({"token": 2})
    assert collection.count() == 1

test_add()
test_del()
