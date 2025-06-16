.. _i2j:

===========
inv_to_json
===========

|div-page-outline|

.. contents:: :local:
    :depth: 7



Usage
=====

.. code-block::

    Usage: i2j [OPTIONS] INPUT_XLSX OUTPUT_LOCATION

    Convert an input XLSX (worksheet named "INVENTORY" and/or "INV-DETAILS") to
    a JSON output. The output will contains the component and package
    information such as name, path, version, license_expression etc.

    Options:
    -h, --help  Show this message and exit.

Example
=======

.. code-block::

    i2j ~/scans/inventory.xlsx ~/output/inventory.json
