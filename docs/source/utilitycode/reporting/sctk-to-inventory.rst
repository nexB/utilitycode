.. _sctk2inv:

===================================
ScanCode TK Scan To Excel Inventory
===================================

|div-page-outline|

.. contents:: :local:
    :depth: 7



Usage
=====

.. code-block::

  Usage: sctk2inv [OPTIONS] LOCATION DESTINATION

    This utility will convert a ScanCode Toolkit scan file to a XLSX file. The
    objective is to reduce manual work and errors by automating a manual task.

  Options:
    --report    Generate an project INVENTORY worksheet.
    -h, --help  Show this message and exit.

Example
=======

.. code-block::

   sctk2inv ~/scan/scan-clipeu.json ~/project/output.xlsx --report

Notes
=====

The package information will be integrated to the main row if there is only
one package. However, if there are multiple package information (such as
from package-lock.json), new rows will be created for each of the package.

See https://github.com/nexB/utilitycode/blob/main/src/reporting/sctk_to_inventory.py for the fields
that will be ignored.

See the `fields_header` list for the fields that will be created when the
`--report` option is used.
