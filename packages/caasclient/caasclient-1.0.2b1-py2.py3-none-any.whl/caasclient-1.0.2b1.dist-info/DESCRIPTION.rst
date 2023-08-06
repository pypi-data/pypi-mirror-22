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
    source python-caasclient/bin/activate
    pip install python-caasclient

Manual Installation::

	git clone https://github.com/rogeryu27/python-caasclient.git
	cd python-caasclient
	python setup.py install

Usage
-----

Query for all ready containers [in a custom namespace]:

.. code:: python

	from caasclient import client as caas_client

	container_list = caas_client.Client(<caas url>).containers.list()

Create a self-defined image:

.. code:: python

	import os

	from caasclient import client as caas_client

	image = caas_client.Client(<caas url>).images.create_by_dockerfile(os.open('path/to/dockerfile','w+'))

Requirements
------------

* Python 2.7
* requests



