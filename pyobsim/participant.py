class Participant(object):
    def __init__(self, name, balance, volume):
        self._name = name
        self._balance = balance
        self._volume = volume

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def balance(self):
        return self._balance

    @balance.setter(self, balance):
        self._balance = balance

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, volume):
        self._volume = volume
