from .order import Order
from .side import Side
from .errors import InsufficientFundsError, InsufficientVolumeError, PriceOutOfRangeError, NoPriceError

class Book(object):
    def __init__(self, name, participants):
        self._name = str(name)
        self._participants = dict(participants)

        self._bids = Side("BID")
        self._asks = Side("ASK")

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

    def add_participant(self, name, balance, volume):
        if int(balance) < 0 or int(volume) < 0:
            raise ValueError()
        
        self.participants[name] = {"balance": int(balance),
                                   "volume": int(volume)}

    def crossed(self):
        if self.bids.best >= self.asks.best:
            return True
        else:
            return False

    def _match(self, counter_side, order):
        if counter_side.stype == "BID":
            if order.price <= counter_side.best:
                good_price = True
            else:
                good_price = False
        elif counter_side.stype == "ASK":
            if order.price >= counter_side.best:
                good_price = True
            else:
                good_price = False
            
        if good_price:
            if order.qty <= counter_side.volume:
                # we can match
                for price in counter_side.prices:
                    matched = False
            
                    while not matched:
                        try:
                            level = counter_side.get(price)
                        except NoPriceError:
                            break

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

                    # exhausted this price level
                    if len(level) == 0:
                        break
            else:
                # insufficient volume
                raise InsufficientVolumeError()
        else:
            # price out of range
            raise PriceOutOfRangeError()

    def _payout(self, side, order, amt=None):
        if side.stype == "BID":
            if amt:
                self.participants[order.owner]["balance"] -= order.price * amt
                self.participants[order.owner]["volume"] += amt
            else:
                self.participants[order.owner]["balance"] -= order.price * order.qty
                self.participants[order.owner]["volume"] += order.qty
        elif side.stype == "ASK":
            if amt:
                self.participants[order.owner]["balance"] += order.price * amt
                self.participants[order.owner]["volume"] -= amt
            else:
                self.participants[order.owner]["balance"] += order.price * order.qty
                self.participants[order.owner]["volume"] -= order.qty

    def add(self, order):
        if order.otype == "BID":
            if order.price * order.qty <= self.participants[order.owner]["balance"]:
                try:
                    self._match(self.asks, order)
                except InsufficientVolumeError:
                    oid = self.volume[0] + self.volume[1] + 1
                    order.oid = oid
                
                    self.bids.put(order)

                    return oid
                except PriceOutOfRangeError:
                    oid = self.volume[0] + self.volume[1] + 1
                    order.oid = oid
                
                    self.bids.put(order)

                    return oid
            else:
                raise InsufficientFundsError()
        elif order.otype == "ASK":
            if order.qty <= self.participants[order.owner]["volume"]:
                try:
                    self._match(self.bids, order)
                except InsufficientVolumeError:
                    oid = self.volume[0] + self.volume[1] + 1
                    order.oid = oid
                
                    self.asks.put(order)
                
                    return oid
                except PriceOutOfRangeError:
                    oid = self.volume[0] + self.volume[1] + 1
                    order.oid = oid
                
                    self.asks.put(order)
                
                    return oid
            else:
                raise InsufficientFundsError()

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
            level_qty = 0

            for order in level:
                level_qty += order.qty

            s += "${0}\t\t{1}\t|\n".format(price, level_qty)

        for price in self.bids.prices:
            level = self.bids.get(price)
            level_qty = 0

            for order in level:
                level_qty += order.qty

            s += "\t\t\t|${0}\t\t{1}\n".format(price, level_qty)

        s += "-" * 80 + "\n"
        s += "\t\t\tPrice\t\tQuantity\n"
        s += "\t\t\tBid\n"

        return s


