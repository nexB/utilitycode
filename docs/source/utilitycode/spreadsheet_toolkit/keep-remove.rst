.. _keep-remove:

====================
Keep / Remove Column
====================

|div-page-outline|

.. contents:: :local:
    :depth: 7



keep_column
===========

Usage
-----

.. code-block::

    Usage: keep_column [OPTIONS] INPUT OUTPUT

      Take the input CSV/XLSX and keep the defined columns and write to the output
      CSV/XLSX

    Options:
      --csv          Output as CSV format (Default: XLSX format)
      -k, --key key  Column(s) to be kept.
      -h, --help     Show this message and exit.

Example
-------

.. code-block::

   keep_column -k Resource,license_expression /project/boms/input.csv
   /project/boms/output.csv --csv

input.csv
^^^^^^^^^

.. list-table::
   :widths: 20 15 30
   :header-rows: 1

   * - Resource
     - type
     - license_expression
   * - /tmp/test.c
     - file
     - mit

output.csv
^^^^^^^^^^

.. list-table::
   :widths: 20 30
   :header-rows: 1

   * - Resource
     - license_expression
   * - /tmp/test.c
     - mit

remove_column
=============

Usage
-----

.. code-block::

    Usage: remove_column [OPTIONS] INPUT OUTPUT

      Take the input CSV/XLSX and remove the defined columns and write to the
      output CSV/XLSX

    Options:
      --csv          Output as CSV format (Default: XLSX format)
      -k, --key key  Column(s) to be removed.
      -h, --help     Show this message and exit.

Example
-------

.. code-block::

   remove_column -k license_expression /project/boms/input.csv /project/boms/output-remove.xlsx

input.csv
^^^^^^^^^

.. list-table::
   :widths: 20 15 30
   :header-rows: 1

   * - Resource
     - type
     - license_expression
   * - /tmp/test.c
     - file
     - mit

output-remove.xlsx
^^^^^^^^^^^^^^^^^^

.. list-table::
   :widths: 20 15
   :header-rows: 1

   * - Resource
     - type
   * - /tmp/test.c
     - file

Notes
=====
Defined keys are separated by comma.

