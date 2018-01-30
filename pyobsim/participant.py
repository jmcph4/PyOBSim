class Participant(object):
    def __init__(self, name, balance, volume):
        self._name = str(name)

        if balance <0 or volume < 0:
            raise ValueError()
        
        self._balance = float(balance)
        self._volume = int(volume)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, balance):
        self._balance = balance

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, volume):
        self._volume = volume

    def __repr__(self):
        s = self.name + ": $" + str(self.balance) + " with " + str(self.volume) + " units" 

        return s
