import csv

from copy import deepcopy

from .order import Order
from .side import Side
from .book import Book
from .participant import Participant

class Simulation(object):
    def __init__(self, name, orders, participants):
        self._name = str(name)
        self._orders = list(orders)
        self._participants = deepcopy(participants)

        self._books = {}

        tickers = []

        for order in self.orders:
            if order.ticker not in tickers:
                tickers.append(order.ticker)

        for ticker in tickers:
            self.add_book(Book(ticker, self.participants))

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = str(name)

    @property
    def orders(self):
        return self._orders

    @property
    def participants(self):
        return self._participants

    @property
    def books(self):
        return self._books

    @property
    def num_orders(self):
        return len(self.orders)

    @property
    def num_participants(self):
        return len(self.participants)

    def add_order(self, order):
        self.orders.append(order)

    def add_book(self, book):
        self._books[book.name] = book

    def load(self, filepath):
        with open(filepath, "r") as orders_file:
            csv_orders = csv.reader(orders_file, delimiter=",")

            for row in csv_orders:
                if len(row) == 6:
                    self.add_order(Order(row[0], row[1], row[2], row[3], row[4], row[5]))

        for o in self.orders:
            self.add_book(Book(o.ticker, self.participants))

    def run(self, steps=None):
        if steps:
            for order in self.orders:
                if i == steps:
                    break
                self.books[order.ticker].add(order)

            return i
        else:
            for order in self.orders:
                self.books[order.ticker].add(order)

            print("{0} participants traded {1} orders".format(self.num_participants,
                                                              self.num_orders))

            return self.num_orders

    def __repr__(self):
        s = "Simulation \n\t" + self.name + "\n---\n"
        s += "Statement of Accounts\n"

        for participant in self._participants:
            s += str(participant) + "\n"
            
        s += "---\n"
        s += "Market as at present\n"

        for book in self.books:
            s += "\t" + str(repr(book))
            s += "\n"

        return s
        
