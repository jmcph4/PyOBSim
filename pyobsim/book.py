from . import order
from . import side

class InsufficientVolume(Exception):
    pass

class PriceOutOfRange(Exception):
    pass

class Book(object):
    def __init__(self, name, participants):
        self._name = str(name)
        self._participants = dict(participants)

        self._bids = side.Side("BID")
        self._asks = side.Side("ASK")

        self._LTP = 0

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = str(name)

    @property
    def participants(self):
        return self._participants

    @property
    def bids(self):
        return self._bids

    @property
    def asks(self):
        return self._asks

    @property
    def top(self):
        return (self.bids.best, self.asks.best)

    @property
    def spread(self):
        return round(abs(self.top[0] - self.top[1]), 2)

    @property
    def depth(self):
        return (self.bids.depth, self.asks.depth)

    @property
    def volume(self):
        return (self.bids.volume, self.asks.volume)

    @property
    def LTP(self):
        return self._LTP

    def crossed(self):
        if self.bids.best >= self.asks.best:
            return True
        else:
            return False

    def _match(self, side, order):
        if side.stype == "BID":
            if order.price <= side.best:
                good_price = True
            else:
                good_price = False
        elif side.stype == "ASK":
            if order.price >= side.best:
                good_price = True
            else:
                good_price = False
            
        if good_price:
            if order.qty <= side.volume:
                # we can match
                for price in side.prices:
                    p = price
                    
                    matched = False
            
                    while not matched:
                        level = side.get(p)

                        for o in level:
                            if order.qty < o.qty:
                                self.execute(order)
                                self.execute(o, amt=order.qty)
                                matched = True
                                break
                            elif order.qty == o.qty:
                                self.execute(order)
                                self.execute(o)
                                matched = True
                                break
                            else:
                                self.execute(order, amt=o.qty)
                                self.execute(o)

                    # if we've matched, break out of price loop
                    if matched:
                        break
            else:
                # insufficient volume
                raise InsufficientVolume()
        else:
            # price out of range
            raise PriceOutOfRange()

    def _payout(self, side, order, amt=None):
        if side.stype == "BID":
            k = -1
        elif side.stype == "ASK":
            k = 1

        if amt:
            self.participants[order.owner] += k * order.price * amt
        else:
            self.participants[order.owner] += k * order.price * order.qty

    def add(self, order):
        if order.otype == "BID":
            try:
                self._match(self.asks, order)
            except InsufficientVolume:
                oid = self.volume[0] + self.volume[1] + 1
                order.oid = oid
                
                self.bids.put(order)
            except PriceOutOfRange:
                oid = self.volume[0] + self.volume[1] + 1
                order.oid = oid
                
                self.bids.put(order)
        elif order.otype == "ASK":
            try:
                self._match(self.bids, order)
            except InsufficientVolume:
                oid = self.volume[0] + self.volume[1] + 1
                order.oid = oid
                
                self.asks.put(order)
                
                return oid
            except PriceOutOfRange:
                oid = self.volume[0] + self.volume[1] + 1
                order.oid = oid
                
                self.asks.put(order)
                
                return oid

    def execute(self, order, amt=None):
        if amt:
            if order.otype == "BID":
                self._payout(self.bids, order, amt)
                order.qty -= amt
            elif order.otype == "ASK":
                self._payout(self.asks, order, amt)
                order.qty -= amt
        else:
            if order.otype == "BID":
                self._payout(self.bids, order)
                self.bids.remove(order.oid)
            elif order.otype == "ASK":
                self._payout(self.asks, order)
                self.asks.remove(order.oid)

        self._LTP = order.price

    def cancel(self, oid):
        self.bids.remove(oid)
        self.asks.remove(oid)

    def add_participant(self, participant):
        if len(tuple(participant)) == 2:
            self.participants[tuple(participant)[0]] = tuple(participant)[1]
        else:
            raise ValueError()

    def __str__(self):
        return "{0} with depth ({1}, {2})".format(self.name,
                                                       self.depth[0],
                                                       self.depth[1])

    def __repr__(self):
        s = "Book for " + self.name + "\n"
        s += "Spread is $" + str(self.spread) + "\n===\n"
        s += "Ask\n"
        s += "Price\t\tQuantity\n"
        s += "-" * 80 + "\n"

        for price in self.asks.prices:
            level = self.asks.get(price)

            for order in level:
                s += "${0}\t\t{1}\t|\n".format(order.price, order.qty)

        for price in self.bids.prices:
            level = self.bids.get(price)

            for order in level:
                s += "\t\t\t|${0}\t\t{1}\n".format(order.price, order.qty)

        s += "-" * 80 + "\n"
        s += "\t\t\tPrice\t\tQuantity\n"
        s += "\t\t\tBid\n"

        return s


