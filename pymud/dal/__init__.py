import logging

import pymongo
import pymongo.errors

from pymud import core

logger = logging.getLogger(__name__)
db = None


class ConnectionFailure(BaseException):
    pass


def connect():
    host = core.config.get('database', 'host')
    port = core.config.get('database', 'port')

    logger.info('Trying to connect to MongoDB instance at {0}:{1}'.format(host, port))
    client = pymongo.MongoClient('mongodb://{0}:{1}'.format(host, port))

    try:
        client.admin.command('ismaster')
    except pymongo.errors.ConnectionFailure as ex:
        raise ConnectionFailure(ex)

    logger.info('Connected to database')
    global db
    db = client['mud']
