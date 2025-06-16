.. _filter:

==========
BOM Filter
==========

|div-page-outline|

.. contents:: :local:
    :depth: 7



Usage
======

.. code-block::

   Usage: bom_filter [OPTIONS] INPUT OUTPUT

     Filtering the input with the provided option(s).

   Options:
     --include "key=string [or] key=string..."
                                     Include the rows which the string exist in
                                     the key value.
     --exclude "key=string [or] key=string..."
                                     Exclude the rows which the string exist in
                                     the key value.
     --startswith "key=string [or] key=string..."
                                     Include the rows which the key value starts
                                     with the string.
     --endswith "key=string [or] key=string..."
                                     Include the rows which the key value ends
                                     with the string.
     --equals "key=string [or] key=string..."
                                     Include the rows which the string equals
                                     with the key value.
     -h, --help                      Show this message and exit.

Examples
=========

Example Input
-------------

``input.csv``

.. list-table::
   :widths: 25 15 25
   :header-rows: 1

   * - about_resource
     - name
     - license
   * - /project/test.c
     - test.c
     - apache-2.0
   * - /project/test.java
     - test.java
     - public-domain
   * - /project/hello.h
     - hello.h
     - public-domain

Example Command 1
-----------------

.. code-block::

   bom_filter --include "about_resource=test" input.csv output.csv

``output.csv``

.. list-table::
   :widths: 25 15 25
   :header-rows: 1

   * - about_resource
     - name
     - license
   * - /project/test.c
     - test.c
     - apache-2.0
   * - /project/test.java
     - test.java
     - public-domain

Example Command 2
-----------------

.. code-block::

   bom_filter --exclude "about_resource=test" input.csv output.csv

``output.csv``

.. list-table::
   :widths: 25 15 25
   :header-rows: 1

   * - about_resource
     - name
     - license
   * - /project/hello.h
     - hello.h
     - public-domain

Example Command 3
-----------------

.. code-block::

   bom_filter --startswith "license=p" input.csv output.csv

``output.csv``

.. list-table::
   :widths: 25 15 25
   :header-rows: 1

   * - about_resource
     - name
     - license
   * - /project/test.java
     - test.java
     - public-domain
   * - /project/hello.h
     - hello.h
     - public-domain

Example Command 4
-----------------

.. code-block::

   bom_filter --endswith "about_resource=.c or name=.h" input.csv output.csv

``output.csv``

.. list-table::
   :widths: 25 15 25
   :header-rows: 1

   * - about_resource
     - name
     - license
   * - /project/test.c
     - test.c
     - apache-2.0
   * - /project/hello.h
     - hello.h
     - public-domain

Example Command 5
-----------------

.. code-block::

   bom_filter --equals "license=public-domain" --endswith "about_resource=.h" input.csv output.csv

``output.csv``

.. list-table::
   :widths: 25 15 25
   :header-rows: 1

   * - about_resource
     - name
     - license
   * - /project/hello.h
     - hello.h
     - public-domain

Notes
=====

.. raw:: html

    <style> .option01 {color:#e74c3c; font-weight:normal; font-style: italic;}
    </style>

.. role:: option01

The *OR* condition is defined in the option expression.

The *AND* condition is defined when multiple options are used.

- i.e., in the last example, it means license equals public-domain **AND**
  about_resource ends with .h

Unfortunately, the *OR* condition can only work with one condition.

- For instance, about_resource :option01:`endswith` .h **OR** about_resource
  :option01:`endswith` .java **OR** about_resource :option01:`endswith` .h

- The tool cannot process different *OR* conditions, e.g., it cannot process
  about_resource :option01:`endswith` .h **OR** license :option01:`startswith`
  public

If multiple *OR* options are needed, the user can run the filter multiple times
to create multiple outputs and then use the ``concat`` command (see
:ref:`concatenate-inputs`) to combine the output.
