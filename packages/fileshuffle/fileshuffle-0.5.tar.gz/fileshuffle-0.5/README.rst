fileshuffle.py
**************

.. image:: https://img.shields.io/pypi/status/fileshuffle.svg
    :target: https://github.com/sashgorokhov/fileshuffle

.. image:: https://img.shields.io/pypi/pyversions/fileshuffle.svg
    :target: https://pypi.python.org/pypi/fileshuffle

.. image:: https://badge.fury.io/py/fileshuffle.svg
    :target: https://badge.fury.io/py/fileshuffle

.. image:: https://img.shields.io/github/license/sashgorokhov/fileshuffle.svg
    :target: https://raw.githubusercontent.com/sashgorokhov/fileshuffle/master/LICENSE

Shuffle files

Installation
------------

Python3.5 is required.

.. code-block:: shell

    pip install fileshuffle

Usage
-----

.. code-block:: shell

    usage: fileshuffle.py [-h] --destination DESTINATION [--recurse]
                          [--no-shuffle] [--order_prefix ORDER_PREFIX]
                          [--order_prefix_regexp ORDER_PREFIX_REGEXP]
                          source

    Shuffle files

    positional arguments:
      source                Source directory

    optional arguments:
      -h, --help            show this help message and exit
      --destination DESTINATION
                            Destination directory. Will be cleared if exists and
                            created if not
      --recurse, -R         Search files in source directory recursively
      --no-shuffle          Do not shuffle gathered files
      --order_prefix ORDER_PREFIX
      --order_prefix_regexp ORDER_PREFIX_REGEXP
                            Used to detect existing order prefixes and remove them
