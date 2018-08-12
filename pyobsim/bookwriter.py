from copy import deepcopy
import pickle


class BookWriter(object):
    def __init__(self, book):
        self.__book = deepcopy(book)

    @property
    def data(self):
        return deepcopy(self.__serialise())

    def __serialise(self):
        return pickle.dumps(self.__book)
