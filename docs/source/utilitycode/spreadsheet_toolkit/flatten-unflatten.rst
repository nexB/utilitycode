.. _flatten-unflatten:

=================
Flatten Unflatten
=================

|div-page-outline|

.. contents:: :local:
    :depth: 7


Flatten
========

Usage
-----

.. code-block::

    Usage: flatten [OPTIONS] INPUT OUTPUT

      Flatten the input CSV/XLSX based on the provided key.

    Options:
      --csv          Output as CSV format (Default: XLSX format)
      -k, --key key  Key to be flatten.  [required]
      -h, --help     Show this message and exit.

Example
-------

.. code-block::

   flatten -k about_resource /project/boms/input.csv /project/boms/output.csv --csv

Notes
-----

The key (-k) is required to tell the utility which key to be flatten.

``input.csv``

.. list-table::
   :widths: 35 30 35
   :header-rows: 1

   * - about_resource
     - name
     - license
   * - /project/test.c
     - test.c
     - apache-2.0
   * - /project/test.c
     - test.c
     - public-domain

``output.csv``

.. list-table::
   :widths: 35 30 35
   :header-rows: 1

   * - about_resource
     - name
     - license
   * - /project/test.c
     - test.c
     - | apache-2.0
       | public-domain

Unflatten
==========

.. _usage-1:

Usage
-----

.. code-block::

    Usage: unflatten [OPTIONS] INPUT OUTPUT

      Unflatten the input CSV/XLSX based on the provided key.

    Options:
      --csv          Output as CSV format (Default: XLSX format)
      -k, --key key  Key to be unflatten.  [required]
      -h, --help     Show this message and exit.

.. _example-1:

Example
-------

.. code-block::

   unflatten -k license /project/boms/input.csv /project/boms/output.csv --csv

.. _notes-1:

Notes
------

The key (-k) is required to tell the utility which key to unflatten.

``input.csv``

.. list-table::
   :widths: 35 30 35
   :header-rows: 1

   * - about_resource
     - name
     - license
   * - /project/test.c
     - test.c
     - | apache-2.0
       | public-domain

``output.csv``

.. list-table::
   :widths: 35 30 35
   :header-rows: 1

   * - about_resource
     - name
     - license
   * - /project/test.c
     - test.c
     - apache-2.0
   * - /project/test.c
     - test.c
     - public-domain
