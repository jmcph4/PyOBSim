# PyOBSim - the Python Order Book Simulator #
---

PyOBSim is a Python module facilitating market simulation by implementing an order book and other utilities. PyOBSim aims to make testing of trading algorithms clean and simple.

Running simulations is straightforward: simply provide an order flow and fire away:

    from pyobsim import *
    
    # build our participants
    alice = participant.Participant("Alice", 100, 0)    # $100, no units
    bob = participant.Participant("Bob", 0, 120)        # $0, 120 units
    
    sim = simulation.Simulation("My Simulation", [], [alice, bob])
    sim.load("order_flow.csv") # load our order flow from CSV file
    sim.run()
    print(sim)

This gives us our summary:

    Simulation 
	    My Simulation
    ---
    Statement of Accounts
    Alice: $100.0 with 0 units
    Bob: $0.0 with 120 units
    ---
    Market as at present
	     'GOOG'

If we want to inspect the book for `GOOG`:

    print(sim.books["GOOG"])

We get:

    Book for GOOG
    Spread is $0.5
    ===
    Ask
    Price		Quantity
    --------------------------------------------------------------------------------
    $1.0		100	|
    			    |$0.5		10
    --------------------------------------------------------------------------------
    			     Price		Quantity
    			     Bid    

## Development ##
---

PyOBSim uses [uv](https://docs.astral.sh/uv/) for dependency management,
packaging, and running tasks. With `uv` installed, set up the project with:

    uv sync

This creates a virtual environment and installs PyOBSim along with its
development dependencies (`ruff`). Common tasks:

    uv run python -m unittest tests/test_*.py   # run the test suite
    uv run ruff check                           # lint the codebase
    uv build                                    # build the sdist and wheel
