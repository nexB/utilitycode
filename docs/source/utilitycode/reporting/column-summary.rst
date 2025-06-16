.. _csum:

==============
Column Summary
==============

|div-page-outline|

.. contents:: :local:
    :depth: 7



Usage
=====

.. code-block::

   Usage: csum [OPTIONS] LOCATION DESTINATION

   This script creates a "Summarized Count" column, tracking the occurrence
   of values within the defined column(s).

   Options:
   -c, --columns TEXT  Specify the column name you wish to summarize on.
                        [required]
   --help              Show this message and exit.

Example 1
=========

.. code-block::

   csum -c "Component" ~/path/to/BOM.xlsx ~/path/to/output.xlsx


``BOM.xlsx``

.. list-table::
   :widths: 30 20 30
   :header-rows: 1

   * - about_resource
     - Component
     - license_expression
   * - /project/test.c
     - test
     - apache-2.0
   * - /project/test.java
     - test
     - public-domain
   * - /project/hello.h
     - hello
     - public-domain
   * - /project/test.h
     - test
     - apache-2.0

``output.xlsx``

.. list-table::
   :widths: 30 30 20 30
   :header-rows: 1

   * - Summarized Count
     - about_resource
     - Component
     - license_expression
   * - 3
     - /project/test.h
     - test
     - apache-2.0
   * - 1
     - /project/hello.h
     - hello
     - public-domain


Example 2
=========

.. code-block::

   csum -c "Component" -c "license_expression" ~/path/to/BOM.xlsx ~/path/to/output.xlsx

``BOM.xlsx``

.. list-table::
   :widths: 30 20 30
   :header-rows: 1

   * - about_resource
     - Component
     - license_expression
   * - /project/test.c
     - test
     - apache-2.0
   * - /project/test.java
     - test
     - public-domain
   * - /project/hello.h
     - hello
     - public-domain
   * - /project/test.h
     - test
     - apache-2.0

``output.xlsx``

.. list-table::
   :widths: 30 30 20 30
   :header-rows: 1

   * - Summarized Count
     - about_resource
     - Component
     - license_expression
   * - 2
     - /project/test.h
     - test
     - apache-2.0
   * - 1
     - /project/test.java
     - test
     - public-domain
   * - 1
     - /project/hello.h
     - hello
     - public-domain
