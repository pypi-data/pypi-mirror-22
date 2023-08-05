googlefinance.client
====================

googlefinance.client is a python client library for google finance api

Installation
------------

::

    $ pip install googlefinance.client

Usage
-----

.. code:: python

    import googlefinance.client as gfc

    # Dow Jones
    param = {
        'q': ".DJI", # Stock symbol (ex: "AAPL")
        'i': "86400", # Interval size in seconds ("86400" = 1 day intervals)
        'x': "INDEXDJX", # Stock exchange symbol on which stock is traded (ex: "NASD")
        'p': "1Y" # Period (Ex: "1Y" = 1 year)
    }
    # get price data (return pandas dataframe)
    df = gfc.get_price_data(param)
    print(df)
    #                          Open      High       Low     Close     Volume
    # 2016-05-17 05:00:00  17531.76   17755.8  17531.76  17710.71   88436105
    # 2016-05-18 05:00:00  17701.46  17701.46  17469.92  17529.98  103253947
    # 2016-05-19 05:00:00  17501.28  17636.22  17418.21  17526.62   79038923
    # 2016-05-20 05:00:00  17514.16  17514.16  17331.07   17435.4   95531058
    # 2016-05-21 05:00:00  17437.32  17571.75  17437.32  17500.94  111992332
    # ...                       ...       ...       ...       ...        ...

    params = [
        # Dow Jones
        {
            'q': ".DJI",
            'x': "INDEXDJX",
        },
        # NYSE COMPOSITE (DJ)
        {
            'q': "NYA",
            'x': "INDEXNYSEGIS",
        },
        # S&P 500
        {
            'q': ".INX",
            'x': "INDEXSP",
        }
    ]
    period = "1Y"
    # get closing price data (return pandas dataframe)
    df = gfc.get_closing_data(params, period)
    print(df)
    #                 .DJI         NYA     .INX
    # 2016-05-17  17710.71  10332.4261  2066.66
    # 2016-05-18  17529.98  10257.6102  2047.21
    # 2016-05-19  17526.62  10239.6501  2047.63
    # 2016-05-20  17435.40  10192.5015  2040.04
    # 2016-05-21  17500.94  10250.4961  2052.32
    # ...              ...         ...      ...

Contributing
------------

1. Fork it
2. Create your feature branch (``git checkout -b my-new-feature``)
3. Commit your changes (``git commit -am 'Add some feature'``)
4. Push to the branch (``git push origin my-new-feature``)
5. Create new Pull Request
