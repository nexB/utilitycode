.. _json2xlsx:

============
JSON to XLSX
============

|div-page-outline|

.. contents:: :local:
    :depth: 7



Usage
=====

.. code-block::

  Usage: json2xlsx [OPTIONS] INPUT OUTPUT

    Convert a JSON file (list of directories) to a XLSX output

  Options:
    -h, --help  Show this message and exit.

Example
=======

.. code-block::

    json2xlsx ~/scans/inventory.json ~/output/inventory.xlsx


Notes
=====
The input JSON file has to be in a list of dictionaries format.
