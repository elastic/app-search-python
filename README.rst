=========================================
Python Client for Swiftype App Search API
=========================================

About
=====

A Python client for interacting with Swiftype App Search API.

For more information, go to our official documentation page:
https://swiftype.com/documentation/app-search/

Installation
============
Swiftype App Search Client can be installed with
`pip <http://pypi.python.org/pypi/pip>`_::

    $ python -m pip install swiftype_app_search

You can also download the project source and run::

    $ python setup.py install

Running Tests
============

    $ python setup.py test

Dependencies
============
Swiftype App Search supports Python 2.7 and Python 3.3+. It depends on requests and PyJWT.

Usage
========

Instantiating a client
----------------------

.. code-block:: python

    >>> from swiftype_app_search import Client
    >>> account_host_key = 'host-c5s2mj'
    >>> api_key = 'api-mu75psc5egt9ppzuycnc2mc3'
    >>> client = Client(account_host_key, api_key)

Index document
--------------

.. code-block:: python

    >>> engine_name = 'favorite-videos'
    >>> document = {
          'id': 'INscMGmhmX4',
          'url': 'https://www.youtube.com/watch?v=INscMGmhmX4',
          'title': 'The Original Grumpy Cat',
          'body': 'A wonderful video of a magnificent cat.'
        }
    >>> client.index_document(engine_name, document)
    {'id': 'INscMGmhmX4'}

Index documents
---------------

.. code-block:: python

    >>> engine_name = 'favorite-videos'
    >>> documents = [
        {
          'id': 'INscMGmhmX4',
          'url': 'https://www.youtube.com/watch?v=INscMGmhmX4',
          'title': 'The Original Grumpy Cat',
          'body': 'A wonderful video of a magnificent cat.'
        },
        {
          'id': 'JNDFojsd02',
          'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
          'title': 'Another Grumpy Cat',
          'body': 'A great video of another cool cat.'
        }
    ]

    >>> client.index_documents(engine_name, documents)
    [{'id': 'INscMGmhmX4', 'errors': []}, {'id': 'JNDFojsd02', 'errors': []}]

Get Documents
-------------

.. code-block:: python

    >>> engine_name = 'favorite-videos'
    >>> client.get_documents(engine_name, ['INscMGmhmX4'])
    [{'id': 'INscMGmhmX4','url': 'https://www.youtube.com/watch?v=INscMGmhmX4','title': 'The Original Grumpy Cat','body': 'A wonderful video of a magnificent cat.'}]


Destroy Documents
-----------------

.. code-block:: python

    >>> engine_name = 'favorite-videos'
    >>> client.destroy_documents(engine_name, ['INscMGmhmX4'])
    [{'id': 'INscMGmhmX4','result': True}]

List Engines
------------

.. code-block:: python

    >>> client.list_engines(current=1, size=20)
    {
        'meta': {
            'page': {
            'current': 1,
            'total_pages': 1,
            'total_results': 2,
            'size': 20
            }
        },
        'results': [{'name': 'favorite-videos'}, {'name': 'another-engine'}]
    }

Get an Engine
-------------

.. code-block:: python

    >>> client.get_engine('favorite-videos')
    {'name': 'favorite-videos'}

Create an Engine
----------------

.. code-block:: python

    >>> client.create_engine('favorite-videos')
    {'name': 'favorite-videos'}

Destroy an Engine
-----------------

.. code-block:: python

    >>> client.destroy_engine('favorite-videos')
    {'deleted': True}

Search
------

.. code-block:: python

    >>> client.search('favorite-videos', 'grumpy cat', {})
    {'meta': {'page': {'current': 1, 'total_pages': 1, 'total_results': 2, 'size': 10}, ...}, 'results': [...]}

Create a Signed Search Key
--------------------------
Creating a search key that will only search over the body field.

.. code-block:: python

    >>> api_key = 'api-mu75psc5egt9ppzuycnc2mc3'
    >>> api_key_name = 'my-api-token'
    >>> signed_search_key = Client.create_signed_search_key(api_key, api_key_name, {'search_fields': { 'body': {}}})
    >>> client = Client(account_host_key, signed_search_key)
