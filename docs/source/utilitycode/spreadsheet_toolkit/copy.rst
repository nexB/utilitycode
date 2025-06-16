.. _copy:

====
Copy
====

|div-page-outline|

.. contents:: :local:
    :depth: 7



Usage
=====

.. code-block::

   Usage: copy_resource [OPTIONS] INPUT Project_Location OUTPUT

   Copy/Zip the resource paths listed in the input from the project_loc to the
   output location.

   Options:
   --zip       Output the copied content to a zip file.
   -h, --help  Show this message and exit.

Examples
========

Example1
---------

.. code-block::

   copy_resource ~/BOM/need_copy.csv ~/project/ ~/out/copied/

Example2
---------

.. code-block::

   copy_resource --zip ~/BOM/need_copy.xlsx ~/project/ ~/out/copied.zip

Notes
=====

The **INPUT** requires the "Resource" column. It'll prompt error if path does
not exist in the INPUT.

**--zip** is a boolean option to indicate if a zip file output is preferred.
