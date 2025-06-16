.. _normalize_license_expression:

============================
Normalize License Expression
============================

|div-page-outline|

.. contents:: :local:
    :depth: 7



Usage
=====

.. code-block::

  Usage: normalize_license_expression [OPTIONS] INPUT OUTPUT

    Read the license_expression field from the input XLSX and perfrom
    deduplication and then write to the output

  Options:
    -h, --help  Show this message and exit.

Example
=======

.. code-block::

   normalize_license_expression ~/path/to/input.xlsx ~/path/to/out.xlsx


Notes
=====
This utilities requires both input and output be XLSX format. In addition,
it requires the input has the 'license_expression' field
