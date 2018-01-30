from .order import Order

class NoPriceError(Exception):
    pass

class Side(object):
    def __init__(self, stype):
        if str(stype) != "BID" and str(stype) != "ASK":
            raise ValueError()

        self._stype = str(stype)

        self._data = {}
        self._prices = []

    @property
    def stype(self):
        return self._stype

    @property
    def prices(self):
        return self._prices

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

        return self._data[price]

    def put(self, order):
        # add price level if it doesn't already exist
        if order.price not in self.prices:
            self._add_price(order.price)

        self._data[order.price].append(order)

    def remove(self, oid):
        for price in self.prices:
            level = self.get(price)

            # traverse price level, searching for order with the required oid
            for order in level:
                if order.oid == oid:
                    level.remove(order)

                # prune price level if now empty
                if len(level) == 0:
                    self._data.pop(price)
                    self._prices.remove(price)

                break

    def num_orders(self):
        n = 0
        
        for price in self.prices:
            level = self.get(price)

            n += len(level)

        return n

    def _add_price(self, price):
        self.prices.append(price)
        self._sort_prices()
        self._data[price] = []

    def _sort_prices(self):
        if self.stype == "BID":
            self.prices.sort(reverse=True)
        elif self.stype == "ASK":
            self.prices.sort()

    def __str__(self):
        s = self.stype + " side with " + str(self.num_orders()) + " orders "
        s += "across " + str(self.depth) + " price levels"

        return s

    def __repr__(self):
        s = self.stype + "s\n"

        for price in self.prices:
            level = self.get(price)

            for order in level:
                s += str(order)
                s += "\n"

        return s
