from collections import MutableMapping
from hashlib import md5
from os import path, remove, listdir, mkdir
from pathlib import Path
from pickle import dumps, loads

_path = './.data/'


class PersistentDict(MutableMapping):
    """A dictionary that applies an arbitrary key-altering
       function before accessing the keys"""

    def __init__(self, data_dir=None):
        self.data_dir = Path(data_dir or './.data/').as_posix() + '/'

        try:
            mkdir(self.data_dir)
        except FileExistsError as e:
            pass

    def __contains__(self, key):
        _key = self.__keytransform__(key)
        if path.isfile(self.data_dir + _key):
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
        # to be supported
        # return iter(listdir(self.data_dir))
        return iter([])

    def __len__(self):
        return len(listdir(self.data_dir))

    @staticmethod
    def __keytransform__(key):
        return md5(repr(key).encode()).hexdigest()

    @staticmethod
    def __valuetransform__(value):
        return dumps(value)

    def __store__(self, key, value):
        try:
            with open(self.data_dir + key, 'wb') as file:
                file.write(value)
        except Exception as e:
            raise CannotWriteDictFile("Can't write dictionary file") from e

    def __read__(self, key):
        try:
            with open(self.data_dir + key, 'rb') as file:
                value = file.read()
                return value
        except Exception as e:
            raise KeyError from e

    def __remove__(self, key):
        try:
            remove(self.data_dir + key)
        except Exception as e:
            raise CannotRemoveDictFile("Can't remove dictionary file") from e


class CannotReadDictFile(Exception):
    pass


class CannotWriteDictFile(Exception):
    pass


class CannotRemoveDictFile(Exception):
    pass
