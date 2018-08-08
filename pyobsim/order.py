CENTS_PER_DOLLAR = 100

class Order(object):
    def __init__(self, oid, owner, ticker, otype, price, qty):
        if int(oid) < 0:
            raise ValueError()

        if str(otype) != "BID" and str(otype) != "ASK":
            raise ValueError()

        if round(float(price), 2) <= 0:
            raise ValueError()

        if int(qty) <= 0:
            raise ValueError()
        
        self.__oid = int(oid)
        self.__owner = owner
        self.__ticker = str(ticker)
        self.__otype = str(otype)
        self.__price = round(float(price), 2)
        self.__qty = int(qty)

    @property
    def oid(self):
        return self.__oid

    @oid.setter
    def oid(self, oid):
        self.__oid = oid

    @property
    def owner(self):
        return self.__owner

    @owner.setter
    def owner(self, owner):
        self.__owner = str(owner)

    @property
    def ticker(self):
        return self.__ticker

    @ticker.setter
    def ticker(self, ticker):
        self.__ticker = str(ticker)

    @property
    def otype(self):
        return self.__otype

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
        return "{0}: {1} for {2} @ ${3} by {4}".format(self.ticker, self.otype,
                                                       self.qty, self.price,
                                                       self.owner)

    def __repr__(self):
        s = "ID: " + str(self.oid) + "\n"
        s += "Owner: " + self.owner + "\n"
        s += "Ticker: " + self.ticker + "\n"
        s += "Type: " + self.otype + "\n"
        s += "Price: $" + str(self.price) + "\n"
        s += "Quantity: " + str(self.qty) + "\n"

        return s

