.. _load_inventories:

================
Load Inventories
================

|div-page-outline|

.. contents:: :local:
    :depth: 7


The script is located under src/scio/load_inventories.sh

This script creates SCIO project(s) from a directory containing SCIO/SCTK
generated JSON file(s).


Usage
=====

.. code-block::

  ./load_inventories.sh <scio_repo_path or scio_installed_path> <input_directory_path_with_set_of_jsons>


Examples
========

.. code-block::

  ./load_inventories.sh /tools/scancode.io /projects/scans/


Notes
=====
The created project(s) name will be the file basename of the JSON file(s).
