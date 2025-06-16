.. _binary_strings:

======================
Collect Binary Strings
======================

|div-page-outline|

.. contents:: :local:
    :depth: 7



Usage
=====

.. code-block::

    Usage: binary_strings [OPTIONS] LOCATION DESTINATION

      Collect binary strings from file(s) and output to a CSV.

    Options:
      --filter TEXT  Look for specific string in the binary_strings
      --help         Show this message and exit.

Example
=======

.. code-block::

    binary_strings ~/project/binary/ ~/project/scans/binary_strings.csv --filter license


Notes
======

This utility can use multiple `--filter` options as an "OR" condition.
For instance,

.. code-block::

    binary_strings ~/project/binary/ ~/project/scans/binary_strings.csv --filter
    license --filter gpl

The above command extracts strings from binaries that contain either
"license" or "gpl." Keep in mind that the `--filter`` string is case
insensitive.

