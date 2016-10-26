# PyOBSim - the Python Order Book Simulator#
---

PyOBSim is a Python module facilitating market simulation by implementing an order book and other utilities. PyOBSim aims to make testing of trading algorithms clean and simple.

To get started:

    $ git clone https://github.com/jmcph4/pyobsim.git
    $ cd pyobsim
    $ vi test.py
    $ cat test.py
    from pyobsim import *

    b = book.Book("Mangoes", {"Alice": {"balance": 150,
                                "volume": 0},
                          "Bob": {"balance": 0,
                                  "volume": 100}})

    init_bid = b.add(order.Order(0, "Alice", "Mangoes", "BID", 1.00, 100))
    print(repr(b))

    b.add(order.Order(0, "Bob", "Mangoes", "ASK", 1.50, 100))
    print(repr(b))

    b.cancel(init_bid) #cancel first bid (at $1.00)
    print(repr(b))

    # match Bob's ask price
    b.add(order.Order(0, "Alice", "Mangoes", "BID", 1.50, 100))
    print(repr(b))

    print(b.LTP) # last traded price for mangoes
    print(b.participants) # market participants' accounts

