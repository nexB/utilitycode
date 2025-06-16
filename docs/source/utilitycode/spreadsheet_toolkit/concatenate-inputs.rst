.. _concatenate-inputs:

====================
Concatenate CSV/XLSX
====================

|div-page-outline|

.. contents:: :local:
    :depth: 7



Usage
======

.. code-block::

    Usage: concat [OPTIONS]

      Concatenate the input CSV/XLSX files and write to a new CSV/XLSX (-o) file.
      Multiple '-i' options are supported.

    Options:
      --csv                  Output as CSV format (Default: XLSX format)
      -ws, --worksheet TEXT  Define the name of the worksheet to work on for the
                            XLSX input.
      -i, --input FILE       Path to the input file.
      -o, --output OUTPUT    Path to the concatenated output file.
      -h, --help             Show this message and exit.

Example
========

.. code-block::

   concat -i /project/scans/license.csv -i /project/scans/copyright.xlsx -o
   /project/scans/license_copyright.xlsx
