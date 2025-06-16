.. _summarize:

=========
Summarize
=========

|div-page-outline|

.. contents:: :local:
    :depth: 7



Usage
=====

.. code-block::

  Usage: summarize [OPTIONS] INPUT OUTPUT

    Summarize the key data in the inputfrom file level to directory level.

  Options:
    --csv          Output as CSV format (Default: XLSX format)
    -k, --key key  Key to be summarized.  [required]
    -h, --help     Show this message and exit.

Example
=======

.. code-block::

   summarize -k license_expresion <input.csv> <output.xlsx>

input.csv
---------

.. list-table::
   :widths: 20 15 30
   :header-rows: 1

   * - Resource
     - name
     - license_expression
   * - /project/
     - project
     -
   * - /project/test1/
     - test1
     -
   * - /project/test1/test.c
     - test.c
     - apache-2.0
   * - /project/test1/test.c
     - test.c
     - public-domain
   * - /project/test2/
     - test2
     -
   * - /project/test2/test.c
     - test.c
     - mit

output.xlsx
-----------

+-----------------+-------------------------------+
| Resource        | summarized_license_expression |
+=================+===============================+
| /project/       | | apache-2.0                  |
|                 | | public-domain               |
|                 | | mit                         |
+-----------------+-------------------------------+
| /project/test1/ | | apache-2.0                  |
|                 | | public-domain               |
+-----------------+-------------------------------+
| /project/test2/ | mit                           |
+-----------------+-------------------------------+

Notes
======

Only the 'Resource' and the defined summarized key will be kept in the output.
