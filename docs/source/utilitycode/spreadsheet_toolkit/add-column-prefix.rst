.. _add-column-prefix:

=================
Add Column Prefix
=================

|div-page-outline|

.. contents:: :local:
    :depth: 7



Usage
=====

.. code-block::

    Usage: add_column_prefix [OPTIONS] INPUT OUTPUT

      Take the input CSV/XLSX, add a defined prefix to all columns and write to
      the output CSV/XLSX.

    Options:
      --csv          Output as CSV format (Default: XLSX format)
      -k, --key key  Prefix to be added to all column names.
      -h, --help     Show this message and exit.

Examples
========

.. code-block::

   add_column_prefix -k test_ ~/BOM/input.xlsx ~/BOM/output.xlsx


Notes
=====

Sample
------

``input.xlsx``

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - resource
     - license
   * - /project/test.c
     - apache-2.0


``output.xlsx``

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - test_resource
     - test_license
   * - /project/test.c
     - apache-2.0
