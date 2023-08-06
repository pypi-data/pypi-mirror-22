daftlistings
============

A web scraper that enables programmatic interaction with daft.ie. Tested on Python 2.7 and Python 3.5.2

Install
-------

::

    pip install daftlistings

Developing Locally
------------------

::

    git clone https://github.com/AnthonyBloomer/daftlistings.git
    cd daftlistings
    virtualenv env
    source env/bin/activate
    pip install -r requirements.txt

Examples
--------

Get the current properties for rent in Dublin that are between €1000 and
€1500 per month.

.. code:: python

    from daftlistings import Daft, CommercialType, SaleType, RentType

    d = Daft()

    listings = d.get_listings(
        county='Dublin City',
        area='Dublin 15',
        listing_type=RentType.APARTMENTS,
        min_price=1000,
        max_price=1500,
        sale_type='rent'
    )

    for listing in listings:
        print(listing.get_formalised_address())
        print(listing.get_daft_link())

Retrieve commercial office listings in Dublin.

.. code:: python

    listings = daft.get_listings(
        county='Dublin',
        listing_type=SaleType.COMMERCIAL,
        commercial_property_type=CommercialType.OFFICE
    )

    for listing in listings:
        print(listing.get_formalised_address())
        print(listing.get_daft_link())


Get the current sale agreed prices for properties in Dublin.

.. code:: python

    listings = d.get_listings(
        county='Dublin City',
        area='Dublin 15',
        listing_type=SaleType.PROPERTIES,
        sale_agreed=True,
        min_price=200000,
        max_price=250000
    )

    for listing in listings:
        print(listing.get_formalised_address())
        print(listing.get_daft_link())

Retrieve all properties for sale in Dublin 15.

.. code:: python


    from daftlistings import Daft

    d = Daft()
    offset = 0
    pages = True

    while pages:

        listings = d.get_listings(
            county='Dublin City',
            area='Dublin 15',
            offset=offset,
            listing_type=SaleType.PROPERTIES
        )

        if not listings:
            pages = False

        for listing in listings:
            print(listing.get_agent_url())
            print(listing.get_price())
            print(listing.get_formalised_address())
            print(listing.get_daft_link())
            print(' ')


        offset += 10


Full Documentation
------------------

https://anthonybloomer.github.io/daftlistings/
