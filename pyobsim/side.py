from .errors import NoPriceError


class Side(object):
    def __init__(self, type):
        if str(type) != "BID" and str(type) != "ASK":
            raise ValueError()

        self.__type = str(type)

        self.__data = {}
        self.__prices = []

    @property
    def type(self):
        return self.__type

    @property
    def prices(self):
        return self.__prices

    @property
    def depth(self):
        return len(self.prices)

    @property
    def best(self):
        if len(self.prices) > 0:
            return self.prices[0]
        else:
            return 0

    @property
    def volume(self):
        vol = 0

        for price in self.prices:
            level = self.get(price)

            for order in level:
                vol += order.qty

        return vol

    def get(self, price):
        if price not in self.prices:
            raise NoPriceError()

        return self.__data[price]

    def put(self, order):
        # add price level if it doesn't already exist
        if order.price not in self.prices:
            self.__add_price(order.price)

        self.__data[order.price].append(order)

    def remove(self, id):
        for price in self.prices:
            level = self.get(price)

            # traverse price level, searching for order with the required id
            for order in level:
                if order.id == id:
                    level.remove(order)

                # prune price level if now empty
                if len(level) == 0:
                    self.__data.pop(price)
                    self.__prices.remove(price)

                break

    def num_orders(self):
        n = 0

        for price in self.prices:
            level = self.get(price)

            n += len(level)

        return n

    def __eq__(self, o):
        if isinstance(o, Side):
            if self.type == o.type and self.prices == o.prices:
                for price in self.prices:
                    if self.get(price) != o.get(price):
                        return False

                return True
            else:
                return False
        else:
            return False

    def __add_price(self, price):
        self.prices.append(price)
        self.__sort_prices()
        self.__data[price] = []

    def __sort_prices(self):
        if self.type == "BID":
            self.prices.sort(reverse=True)
        elif self.type == "ASK":
            self.prices.sort()

    def __str__(self):
        s = self.type + " side with " + str(self.num_orders()) + " orders "
        s += "across " + str(self.depth) + " price levels"

        return s

    def __repr__(self):
        s = self.type + "s\n"

        for price in self.prices:
            level = self.get(price)

            for order in level:
                s += str(order)
                s += "\n"

        return s
