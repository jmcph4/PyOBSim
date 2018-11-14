import unittest

from pyobsim.errors import *
from pyobsim.book import Book
from pyobsim.side import Side
from pyobsim.participant import Participant
from pyobsim.order import Order

class TestBook(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.default_name = ""
        cls.default_participants = []

        cls.sample_name = "WOW"
        cls.sample_participants = [Participant(1, "John", 10000, 10),
                Participant(2, "Jane", 50000, 1200)]

    def test___init___normal(self):
        # assemble custom parameters
        params = {"PartialExecution": True,
                "AllowShorting": True,
                "AllowLending": False
                }
        
        actual_book = Book(self.sample_name, self.sample_participants, params)
       
        # check name and participants are correct
        self.assertEqual(actual_book.name, self.sample_name)
        self.assertEqual(actual_book.participants, self.sample_participants)
        
        # check parameters are correct
        for param_name, param_val in params.items():
            self.assertEqual(actual_book.get_param(param_name), param_val)

    def test___init___no_participants(self):
        actual_book = Book(self.sample_name, [])

        self.assertEqual(actual_book.name, self.sample_name)

    def test_add_normal(self):
        actual_book = Book(self.sample_name, self.sample_participants)

        test_order = Order(1, self.sample_participants[0], self.sample_name,
                "BID", 12.00, 150)

        actual_book.add(test_order)

        expected_bids = Side("BID")
        expected_bids.put(test_order)

        expected_asks = Side("ASK")

        self.assertEqual(actual_book.bids, expected_bids)
        self.assertEqual(actual_book.asks, expected_asks)
        self.assertEqual(actual_book.LTP, 0)

    def test_add_insufficient_funds(self):
        actual_book = Book(self.sample_name, self.sample_participants)

        test_order = Order(1, self.sample_participants[0], self.sample_name,
                "BID", 1000.00, 800)

        with self.assertRaises(InsufficientFundsError):
            actual_book.add(test_order)

    def test_add_no_cross(self):
        actual_book = Book(self.sample_name, self.sample_participants)

        test_orders = [Order(1, self.sample_participants[0], self.sample_name,
            "BID", 22.00, 3),
            Order(2, self.sample_participants[1], self.sample_name,
                "ASK", 100.00, 2)]

        # add order to book
        for order in test_orders:
            actual_book.add(order)

        expected_bids = Side("BID")
        expected_bids.put(test_orders[0])

        expected_asks = Side("ASK")
        expected_asks.put(test_orders[1])

        self.assertFalse(actual_book.crossed())
        self.assertEqual(actual_book.LTP, 0)
        self.assertEqual(actual_book.bids, expected_bids)
        self.assertEqual(actual_book.asks, expected_asks)

    def test_add_cross(self):
        actual_book = Book(self.sample_name, self.sample_participants)

        test_orders = [Order(1, self.sample_participants[0], self.sample_name,
            "BID", 22.00, 3),
            Order(2, self.sample_participants[1], self.sample_name,
                "ASK", 20.00, 3)]

        # add order to book
        for order in test_orders:
            actual_book.add(order)

        # expected Side objects
        expected_bids = Side("BID")
        expected_asks = Side("ASK")

        self.assertFalse(actual_book.crossed())
        self.assertEqual(actual_book.LTP, test_orders[0].price)
        self.assertEqual(actual_book.bids, expected_bids)
        self.assertEqual(actual_book.asks, expected_asks)

    def test_add_exact_match(self):
        actual_book = Book(self.sample_name, self.sample_participants)

        test_orders = [Order(1, self.sample_participants[0], self.sample_name,
            "BID", 22.00, 3),
            Order(2, self.sample_participants[1], self.sample_name,
                "ASK", 22.00, 3)]

        # add order to book
        for order in test_orders:
            actual_book.add(order)

        # expected Side objects
        expected_bids = Side("BID")
        expected_asks = Side("ASK")

        self.assertFalse(actual_book.crossed())
        self.assertEqual(actual_book.LTP, test_orders[0].price)
        self.assertEqual(actual_book.LTP, test_orders[1].price)
        self.assertEqual(actual_book.bids, expected_bids)
        self.assertEqual(actual_book.asks, expected_asks)

