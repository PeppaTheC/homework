import json
import os
import pickle
import redis

from abc import ABC, abstractmethod
from pymongo import MongoClient

supported_protocols = {'pickle': pickle,
                       'json': json}


class Serializer:
    """Class by protocol name can serialize and deserialize objects

     Attributes:
         protocol_name: The name of executable protocol
         protocol: Packet of executable protocol
     """

    def __init__(self, protocol: str = None):
        """By given name assigned protocol packet"""
        self.protocol_name = protocol.lower()
        self.protocol = supported_protocols.get(self.protocol_name, 'json')

    def serialize(self, data):
        return self.protocol.dumps(data)

    def deserialize(self, data):
        return self.protocol.loads(data)

    def get_name(self):
        return self.protocol_name


def serializer_wrap(cls):
    """Wrapper for DB set and get data"""
    origin_set_data = cls.set_data
    origin_get_data = cls.get_data

    def set_data(self: cls = None, key=None, data=None, protocol=None):
        """Serialize data before set"""
        serializer = Serializer(protocol)
        data = serializer.serialize(data)
        origin_set_data(self, key, data, serializer)

    def get_data(self: cls = None, key=None, protocol=None):
        """Deserialize data after get"""
        serializer = Serializer(protocol)
        return serializer.deserialize(origin_get_data(self, key, serializer))

    cls.get_data = get_data
    cls.set_data = set_data
    return cls


class DB(ABC):
    """Meta class for DB"""

    def __init__(self, host='localhost', port=6379):
        self.host = host
        self.port = port

    @abstractmethod
    def set_data(self, key: str, data, protocol):
        pass

    @abstractmethod
    def get_data(self, key: str, protocol):
        pass


@serializer_wrap
class FileDB(DB):
    """File database"""

    def __init__(self, path='./', ):
        self.abs_path = os.path.abspath(path)
        super().__init__()

    def set_data(self, filename, data, protocol):
        """Write information to  the given filename"""
        mode = 'wb' if protocol.get_name() == 'pickle' else 'w'
        abs_name = self.abs_path + '/' + filename
        with open(abs_name, mode) as db_file:
            db_file.write(data)

    def get_data(self, filename, protocol):
        """Read information from the given filename"""
        mode = 'rb' if protocol.get_name() == 'pickle' else 'r'
        abs_name = self.abs_path + '/' + filename
        with open(abs_name, mode) as db_file:
            return db_file.read()


@serializer_wrap
class RedisDB(DB):
    """Redis database"""

    def __init__(self, host, port):
        super().__init__(host, port)
        self.db = redis.Redis(self.host, self.port)

    def set_data(self, key, data, protocol):
        self.db.set(key, data)

    def get_data(self, key, protocol: str):
        return self.db.get(key)


class MongoDB(DB):
    def __init__(self, host, port, name):
        super().__init__(host, port)
        client = MongoClient(self.host, self.port)
        self.db = client[name]

    def set_data(self, collection_name: str, data, protocol: str):
        collection = self.db[collection_name]
        collection.insert_one(data, True)

    def get_data(self, collection_name: str, protocol: str) -> list:
        data = []
        for row in self.db[collection_name].find():
            data.append(row)
        return data


supported_dbs = {'file': FileDB,
                 'redis': RedisDB,
                 'mongo': MongoDB,
                 }


def save(data, key: str, *args, protocol: str, db: str, place: dict, ):
    db = supported_dbs.get(db)(**place)
    db.set_data(key, data, protocol)


def get(key: str, *args, protocol: str, db: str, place: dict, ):
    db = supported_dbs.get(db)(**place)
    return db.get_data(key, protocol)


def test_file_db():
    a = {1: 2, 2: 3}
    config = {
        'protocol': 'pickle',
        'db': 'file',
        'place':
            {
                'path': './'
            },
    }
    save(a, 'text.txt', **config)
    print(get('text.txt', **config))


def test_redis_db():
    a = {3: 2, 1: 4}
    config = {
        'protocol': 'json',
        'db': 'redis',
        'place':
            {
                'host': 'localhost',
                'port': 6379
            },
    }

    save(a, 'redis-data', **config)
    print(get('redis-data', **config))


def test_mongo_db():
    a = {'73': 2, '23': 4}
    config = {
        'protocol': None,
        'db': 'mongo',
        'place':
            {
                'host': 'localhost',
                'port': 27017,
                'name': 'test-database'
            },
    }

    save(a, 'test-collection', **config)
    print(get('redis-data', **config))


if __name__ == '__main__':
    test_file_db()
    test_redis_db()
    test_mongo_db()
    pass
