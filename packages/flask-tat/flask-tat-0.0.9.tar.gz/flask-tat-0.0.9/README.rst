.. image:: https://travis-ci.org/cdumay/flask-tat.svg?branch=master
    :target: https://travis-ci.org/cdumay/flask-tat

=========
flask-tat
=========

OVH TAT client as Flask extension.

----------
Quickstart
----------

First, install flask-tat using
`pip <https://pip.pypa.io/en/stable/>`_::

    pip install flask-tat


Next, add a :code:`TATClient` instance to your code:

.. code-block:: python

    from flask import Flask
    from flask_tat import TATClient

    app = Flask(__name__)
    app.config.update(dict(
        TAT_URL="http://the.tat.server",
        TAT_USERNAME="username",
        TAT_PASSWORD="password,
        TAT_SSL_VERIFY=False
    ))

    tat_client = TATClient(app)

-------
License
-------

Apache License 2.0