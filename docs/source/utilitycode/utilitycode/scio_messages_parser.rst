.. _scio_messages_parser:

========================
Parse SCIO XLSX MESSAGES
========================

|div-page-outline|

.. contents:: :local:
    :depth: 7



Usage
=====

.. code-block::

    Usage: scio_messages_parser [OPTIONS] INPUT OUTPUT

    This utility extracts data from the "details" column in the "MESSAGES"
    worksheet from SCIO's XLSX output. The parsed data will be saved to the xlsx
    output. Following are the sample that list the fields that need to be
    parsed:

            name:
            version:
            datafile_paths: []
            declared_license_expression: gpl-2.0-plus OR lgpl-2.1-plus
            extracted_license_statement: |
                GPL-2.0+
                LGPL-2.1+

    Options:
    -h, --help  Show this message and exit.

Example
=======

.. code-block::

   scio_messages_parser ~/project/scio_project.xlsx ~/project/output.xlsx

Notes
=====
The output will keep the "uuid" field and extract the "name", "version",
"datafile_paths", "declared_license_expression" and
"extracted_license_statement" from the "details" field.
