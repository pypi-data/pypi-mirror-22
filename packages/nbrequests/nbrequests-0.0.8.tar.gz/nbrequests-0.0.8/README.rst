nbrequests: Display Python Requests in Notebook
===============================================

Pretty printing the requests/responses from `python requests <http://requests.readthedocs.io>`_. Check out the `example notebook <https://nbviewer.jupyter.org/github/kristianperkins/nbrequests/blob/master/example_nbrequests.ipynb>`_ for usage.

Install
-------

::

    pip install nbrequests


Usage
-----

Make a request using the python `requests` module and run `display_request()`.  e.g.

    r = requests.get('http://httpbin.org/get')
    display_request(r)

