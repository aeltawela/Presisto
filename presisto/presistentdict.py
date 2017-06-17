from collections import MutableMapping
from hashlib import md5
from pickle import dumps, loads
from os import path, remove, listdir

_path = './temp/'


class PersistentDict(MutableMapping):
    """A dictionary that applies an arbitrary key-altering
       function before accessing the keys"""

    def __init__(self, *args, **kwargs):
        self.update(dict(*args, **kwargs))  # use the free update to set keys

    def __contains__(self, key):
        _key = self.__keytransform__(key)
        if path.isfile(_path + _key):
            return True

        return False

    def __getitem__(self, key):
        _key = self.__keytransform__(key)
        return loads(self.__read__(_key))

    def __setitem__(self, key, value):
        _key = self.__keytransform__(key)
        _value = self.__valuetransform__(value)
        self.__store__(_key, _value)

    def __delitem__(self, key):
        _key = self.__keytransform__(key)
        self.__remove__(_key)

    def __iter__(self):
        return iter(listdir(_path))

    def __len__(self):
        return len(listdir(_path))

    @staticmethod
    def __keytransform__(key):
        return md5(repr(key).encode()).hexdigest()

    @staticmethod
    def __valuetransform__(value):
        return dumps(value)

    @staticmethod
    def __store__(key, value):
        try:
            with open(_path + key, 'wb') as file:
                file.write(value)
        except Exception as e:
            raise CannotWriteDictFile("Can't write dictionary file") from e

    @staticmethod
    def __read__(key):
        try:
            with open(_path + key, 'rb') as file:
                value = file.read()
                return value
        except Exception as e:
            raise CannotReadDictFile("Can't read dictionary file") from e

    @staticmethod
    def __remove__(key):
        try:
            remove(_path + key)
        except Exception as e:
            raise CannotRemoveDictFile("Can't remove dictionary file") from e


class CannotReadDictFile(Exception):
    pass


class CannotWriteDictFile(Exception):
    pass


class CannotRemoveDictFile(Exception):
    pass
