class Participant(object):
    def __init__(self, id, name, balance, volume):
        self.__id = id
        self.__name = str(name)

        if balance < 0 or volume < 0:
            raise ValueError()
        
        self.__balance = float(balance)
        self.__volume = int(volume)

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, balance):
        self.__balance = balance

    @property
    def volume(self):
        return self.__volume

    @volume.setter
    def volume(self, volume):
        self.__volume = volume

    def __eq__(self, o):
        return self.id == o.id and self.name == o.name and \
               self.balance == o.balance and self.volume == o.volume

    def __hash__(self):
        return self.__id

    def __repr__(self):
        s = self.name + ": $" + str(self.balance) + " with " + \
            str(self.volume) + " units"

        return s
