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

records = []
counter = 0


def test_add(records, counter):
    collection.insert({"type": "test_memo", "date": "test_now", "token": counter})
    for record in collection.find({"type": "test_memo"}):
        records.append(
            {"date": arrow.get(record['date']).to('local').isoformat(),
             "token": counter})
        counter += 1

    assert len(records) == collection.count()


def test_del(records, counter):
    for record in records:
        collection.delete_one({"token": counter})
        counter -= 1
        assert collection.count() == counter

test_add(records, counter)
test_del(records, counter)