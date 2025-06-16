.. _npm-package-analyzer:

==========================
NPM Packages Analyzer
==========================

|div-page-outline|

.. contents:: :local:
    :depth: 7



Usage
=====

.. code-block::

  Usage: npm_package_analyzer [OPTIONS] INPUT OUTPUT

    Get the package information from 'https://registry.npmjs.org/' with the purl
    field in the input file. The input can be generated from Scancode Toolkit
    (JSON/CSV) or custom (CSV/XLSX). The output has to be either .csv or .xlsx

  Options:
    --scancode      Indicate the input file is generated from scancode_toolkit.
    --download DIR  Path to a directory where the package should be downloaded
                    to.
    --csv           Output as CSV format (Default: XLSX format)
    -h, --help      Show this message and exit.

Example
=======

.. code-block::

   npm_package_analyzer --csv --scancode ~/path/to/scancode-package_scan.json ~/path/to/out.csv

Notes
=====
This utilities queries the npmjs API using the `name` and `version` values
extracted from the `purl` field from the input. It then uses scancode to perform
an NPM package scan and then output the package scan information into a csv or
xlsx file.
