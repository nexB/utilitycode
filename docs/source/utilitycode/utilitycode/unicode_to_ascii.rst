.. _unicode_to_ascii:

==============
Detect Unicode
==============

|div-page-outline|

.. contents:: :local:
    :depth: 7



Usage
=====

.. code-block::

  Usage: unicode_to_ascii [OPTIONS] INPUT OUTPUT

    Detect if the input (CSV/XLSX) contains any unicode Mark an "x" in a
    "Unicode Detected" column and proposed correction in the output.

  Options:
    --worksheet name  The worksheet name from the INPUT. (Default: the "active"
                      worksheet)
    -h, --help        Show this message and exit.

Example
=======

.. code-block::

    unicode_to_ascii ~/project/input.xlsx ~/project/output.xlsx --worksheet BOM


Notes
=====
If unicode string is detected, a "Unicode Detected" column will be created
with an "x" along with the proposed correction value columns.

On the other hand, if no unicode is detected, nothing will be generated.

Example
=======

``input.xlsx``

.. list-table::
   :widths: 35 35
   :header-rows: 1

   * - field1
     - field2
   * - /project/test.c
     - Copyright © abc

``output.xlsx``

.. list-table::
   :widths: 35 35 35 35
   :header-rows: 1

   * - field1
     - field2
     - Unicode Detected
     - Ignored Unicode - field2
   * - /project/test.c
     - Copyright © abc
     - x
     - Copyright  abc
