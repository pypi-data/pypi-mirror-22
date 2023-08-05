Introduction
============
.. image:: https://travis-ci.org/sp4x/kombu-stomp.svg?branch=master
   :target: https://travis-ci.org/sp4x/kombu-stomp
.. image:: https://coveralls.io/repos/github/sp4x/kombu-stomp/badge.svg?branch=master
   :target: https://coveralls.io/github/sp4x/kombu-stomp?branch=master


This is project is an effort for adding STOMP protocol support to Kombu, mostly
Celery oriented. You can find documentation at `Read the docs`_.

Limitations
-----------
Currently we offer very limited support:

* ActiveMQ is the only one broker supported.

* We support only STOMP 1.0 protocol.

* No PyPy, Jython support.

* There is no transport options support but the host, port and credentials.

* There is no support for timeout when consuming queues.

.. _`Read the docs`: http://kombu-stomp.readthedocs.org/en/latest/
