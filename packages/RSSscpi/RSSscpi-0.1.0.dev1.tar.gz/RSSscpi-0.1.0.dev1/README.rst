========================================================
RSSscpi - Instrument (VNA) control in a pythonic fashion
========================================================

.. start-badges

.. list-table::
    :stub-columns: 1

    * - tests
      - |travis| |codecov|

.. |travis| image:: https://travis-ci.org/luksan/RSSscpi.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/luksan/RSSscpi

.. |codecov| image:: https://codecov.io/github/luksan/RSSscpi/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/luksan/RSSscpi

.. end-badges

The purpose of this Python library is to provide a nice way of writing measurement instrument remote control programs
in Python. This is acheived mainly by converting all SCPI commands to equivalent Python classes, so that no text strings
with SCPI commands have to be entered by the programmer. This will hopefully reduce bugs in the code, and increase
programmer productivity.

Main features
-------------
* Complete SCPI command class heirarchy; automatically generated from extracted command lists
* Each SCPI command class has a docstring with links to the relevant online manual page
* py.test regression testsuite
* Helper classes to wrap the more unveildly SCPI commands

To use this library you need pyvisa, and a suitable VISA backend.

See ``examples/`` for inspirational usage.

Please report bugs to lukas.sandstrom@rohde-schwarz.com, or at https://github.com/luksan/RSSscpi
