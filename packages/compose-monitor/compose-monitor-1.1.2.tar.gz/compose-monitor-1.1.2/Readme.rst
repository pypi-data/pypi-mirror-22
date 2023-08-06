|language| |license|

===============
compose-monitor
===============

Description
~~~~~~~~~~~

This utility is designed for monitoring and updating of the services in the specified docker-compose.yml file.

Installation
~~~~~~~~~~~~

``python setup.py install``

or

``pip install -e .``

or

``pip install compose-monitor``

How to use
~~~~~~~~~~

Run it with the directory with ``docker-compose.yml`` file path: ``compose-monitor -c .``

Also checkout list of `arguments`_

arguments
^^^^^^^^^

* ``-c, --config`` - Run with config
* ``-o, --options`` - Additional options for the project
* ``-l, --log`` - Redirect logging to file

.. |language| image:: https://img.shields.io/badge/language-python-blue.svg
.. |license| image:: https://img.shields.io/badge/license-Apache%202-blue.svg
