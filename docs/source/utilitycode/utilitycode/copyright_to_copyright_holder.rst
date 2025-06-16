.. _copyright_to_copyright_holder:

=============================
Copyright to Copyright Holder
=============================

|div-page-outline|

.. contents:: :local:
    :depth: 7



Usage
=====

.. code-block::

    Usage: copyright_to_holder [OPTIONS] LOCATION DESTINATION

    The utility generate a "Copyright Holder" field based on the copyright
    column defined by the user in the input.

    Options:
    -c, --copyright-column-name TEXT
                                    [required]
    -h, --help                      Show this message and exit.

Example
=======

.. code-block::

   copyright_to_holder -c "Confirmed Copyright" ~/project/input.xlsx ~/project/output.xlsx

Notes
=====
The **Copyright to Copyright Holder** utility reads the copyright column
(based on the column name provided by the -c option) from the input XLSX.
Then, it will use the "CopyrightDetector()" from scancode to extract the
copyright holder's information. The tool will then generate a new excel
output which contains all the original data from the input with the new
extra column named "Copyright Holder"
