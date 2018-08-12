from copy import deepcopy

from .order import Order
from .side import Side
from .errors import InsufficientFundsError, InsufficientVolumeError, \
    PriceOutOfRangeError, NoPriceError, ParticipantAlreadyExistsError, \
    NoSuchParameterError


class Book(object):
    def __init__(self, name, participants, params=None):
        self.__name = str(name)
        self.__participants = {}

        # build participants dictionary from list
        for participant in participants:
            self.__participants[participant.id] = participant

        if params is not None:
            self.__params = deepcopy(params)
        else:
            self.__params = {}

            # initialise default parameters
            self.__params["PartialExecution"] = True
            self.__params["AllowShorting"] = False
            self.__params["AllowLending"] = False

        self.__bids = Side("BID")
        self.__asks = Side("ASK")

        self.__LTP = 0

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = str(name)

    @property
    def participants(self):
        return deepcopy(self.__participants)

    @property
    def bids(self):
        return self.__bids

    @property
    def asks(self):
        return self.__asks

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
        return self.__LTP

    def set_param(self, name, value):
        if name not in self.__params.keys():
            raise NoSuchParameterError()

        self.__params[name] = value

    def get_param(self, name):
        if name not in self.__params.keys():
            raise NoSuchParameterError()

        return self.__params[name]

    def add_participant(self, participant):
        if participant.id in self.__participants.keys():
            raise ParticipantAlreadyExistsError()

        self.__participants[participant.id] = participant

    def crossed(self):
        if self.bids.best >= self.asks.best:
            return True
        else:
            return False

    def __match(self, counter_side, order):
        matched = False  # order starts unmatched

        crossed = False

        # determine if this order will cross the book
        if order.type == "BID":
            crossed = order.price >= counter_side.best
        elif order.type == "ASK":
            crossed = order.price <= counter_side.best

        if counter_side.volume > 0 and crossed and \
                (order.qty <= counter_side.volume or \
                 self.__params["PartialExecution"]) :
            while not matched and len(counter_side.prices) > 0:
                for counter_price in counter_side.prices:
                    level = counter_side.get(counter_price)

                    for counter_order in level:
                        actual_qty = None
                        actual_counter_qty = None

                        if order.qty < counter_order.qty:
                            actual_counter_qty = order.qty

                            # mark order as matched and terminate
                            matched = True
                        elif order.qty == counter_order.qty:
                            # mark order as matched and terminate
                            matched = True
                        else: # partial execution
                            actual_price = counter_order.qty

                        self.__execute(order, price=counter_order.price, amt=actual_qty)
                        self.__execute(counter_order, price=counter_order.price, amt=actual_counter_qty)

                    if matched: # done, so terminate
                        break

        return matched

    def __payout(self, side, order, price=None, amt=None):
        if not price:
            actual_price = order.price
        else:
            actual_price = price

        if side.type == "BID":
            if amt:
                self.__participants[order.owner.id].balance -= actual_price * amt
                self.__participants[order.owner.id].volume += amt
            else:
                self.__participants[order.owner.id].balance -= actual_price * order.qty
                self.__participants[order.owner.id].volume += order.qty
        elif side.type == "ASK":
            if amt:
                self.__participants[order.owner.id].balance += actual_price * amt
                self.__participants[order.owner.id].volume -= amt
            else:
                self.__participants[order.owner.id].balance += actual_price * order.qty
                self.__participants[order.owner.id].volume -= order.qty

    def add(self, order):
        if order.type == "BID":
            if order.price * order.qty <= \
                    self.__participants[order.owner.id].balance \
                    or self.__params["AllowLending"]:
                matched = self.__match(self.asks, order)

                # order could not be matched at this time
                if not matched:
                    self.__bids.put(order)
            else:
                raise InsufficientFundsError()
        elif order.type == "ASK":
            if order.qty <= self.__participants[order.owner.id].volume \
                    or self.__params["AllowShorting"]:
                matched = self.__match(self.bids, order)

                # order could not be matched at this time
                if not matched:
                    self.__asks.put(order)
            else:
                raise InsufficientFundsError()

    def __execute(self, order, price=None, amt=None):
        if amt:
            if order.type == "BID":
                self.__payout(self.__bids, order, price, amt)
                order.qty -= amt
            elif order.type == "ASK":
                self.__payout(self.__asks, order, price, amt)
                order.qty -= amt
        else:
            if order.type == "BID":
                self.__payout(self.__bids, order, price, amt)
                self.__bids.remove(order.id)
            elif order.type == "ASK":
                self.__payout(self.__asks, order, price, amt)
                self.__asks.remove(order.id)

        self.__LTP = order.price

    def cancel(self, id):
        self.__bids.remove(id)
        self.__asks.remove(id)

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


