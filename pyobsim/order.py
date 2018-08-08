CENTS_PER_DOLLAR = 100


class Order(object):
    def __init__(self, id, owner, ticker, type, price, qty):
        if int(id) < 0:
            raise ValueError()

        if round(float(price), 2) <= 0:
            raise ValueError()

        if int(qty) <= 0:
            raise ValueError()
        
        self.__id = id
        self.__owner = owner
        self.__ticker = str(ticker)
        self.__type = type
        self.__price = round(float(price), 2)
        self.__qty = int(qty)

    @property
    def id(self):
        return self.__id

    @property
    def owner(self):
        return self.__owner

    @owner.setter
    def owner(self, owner):
        self.__owner = owner

    @property
    def ticker(self):
        return self.__ticker

    @ticker.setter
    def ticker(self, ticker):
        self.__ticker = str(ticker)

    @property
    def type(self):
        return self.__type

    @property
    def price(self):
        return round(self.__price, 2)

    @price.setter
    def price(self, price):
        if round(float(price)) <= 0:
            raise ValueError()

        self.__price = round(float(price))

    @property
    def qty(self):
        return self.__qty

    @qty.setter
    def qty(self, qty):
        if int(qty) <= 0:
            raise ValueError()

        self.__qty = int(qty)

    def __str__(self):
        return "{0}: {1} for {2} @ ${3} by {4}".format(self.ticker, self.type,
                                                       self.qty, self.price,
                                                       self.owner)

    def __repr__(self):
        s = "ID: " + str(self.id) + "\n"
        s += "Owner: " + str(self.owner) + "\n"
        s += "Ticker: " + self.ticker + "\n"
        s += "Type: " + str(self.type) + "\n"
        s += "Price: $" + str(self.price) + "\n"
        s += "Quantity: " + str(self.qty) + "\n"

        return s

