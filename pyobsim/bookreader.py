from copy import deepcopy
import pickle


class BookReader(object):
    def __init__(self, data):
        self.__data = deepcopy(data)

    @property
    def book(self):
        return deepcopy(self.__deserialise())

    def __deserialise(self):
        return pickle.loads(self.__data)
