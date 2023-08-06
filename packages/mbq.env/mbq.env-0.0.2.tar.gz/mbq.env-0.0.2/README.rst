mbq.env: protect the environment
===================================

.. image:: https://img.shields.io/pypi/v/mbq.env.svg
    :target: https://pypi.python.org/pypi/mbq.env

.. image:: https://img.shields.io/pypi/l/mbq.env.svg
    :target: https://pypi.python.org/pypi/mbq.env

.. image:: https://img.shields.io/pypi/pyversions/mbq.env.svg
    :target: https://pypi.python.org/pypi/mbq.env

.. image:: https://img.shields.io/travis/managedbyq/mbq.env/master.svg
    :target: https://travis-ci.org/managedbyq/mbq.env

Installation
------------

.. code-block:: bash

    $ pip install mbq.env
    🚀✨

Guaranteed fresh.


Getting started
---------------

.. code-block:: bash

    $ env
    ...
    MY_VAR=bacon
    MY_INT_VAR=123
    MY_BOOL_VAR=1
    MY_CSV_VAR=a,b,c
    MY_TOKEN_VAR=a b c
    MY_KEY_VAR=-----BEGIN CERTIFICATE-----...-----END CERTIFICATE-----
    ...

.. code-block:: python

    In [1]: from mbq import env

    In [2]: env.get('MY_VAR', default='BACON')
    Out[2]: 'bacon'

    In [3]: env.get_int('MY_INT_VAR', default=12)
    Out[3]: 123

    In [4]: env.get_bool('MY_BOOL_VAR', default=False)
    Out[4]: True

    In [5]: env.get_csv('MY_CSV_VAR', default=['abc', '123'])
    Out[5]: ['a', 'b', 'c']

    In [6]: env.get_tokens('MY_TOKEN_VAR', default=['abc', '123'])
    Out[6]: ['a', 'b', 'c']

    In [7]: env.get_key('CERTIFICATE', 'MY_KEY_VAR')
    Out[7]: '-----BEGIN CERTIFICATE-----\n...\n-----END CERTIFICATE-----'
