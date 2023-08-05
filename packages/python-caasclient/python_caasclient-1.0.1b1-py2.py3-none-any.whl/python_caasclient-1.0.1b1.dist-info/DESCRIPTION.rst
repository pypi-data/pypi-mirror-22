python-caasclient
=================

Python client for CAAS

*To be filled: Brief Introduction*

Features
--------

* HTTP interface using requests
* Python native quering for CAAS API objects

Installation
------------
Using pip::

	pip install python-caasclient

A virtualenvwrapper is recommended::

	virtualenv python-caasclient
	pip install python-caasclient

Manual Installation::

	git clone https://github.com/rogeryu27/python-caasclient.git
	cd python-caasclient
	python setup.py install

Usage
-----

Query for all ready containers [in a custom namespace]:

.. code:: python

	from python_caasclient import client

	container_list = client(<caas url>).containers.list()

Create a self-defined image:

.. code:: python

	import os

	from python_caasclient import client

	image = client(<caas url>).image.create_by_dockerfile(os.open('path/to/dockerfile','w+'))

Requirements
------------

* Python 2.7
* requests



