.. _parse_nuspec:

==================
Parse .nuspec File
==================

|div-page-outline|

.. contents:: :local:
    :depth: 7



Usage
=====

.. code-block::

    Usage: parse_nuspec [OPTIONS] LOCATION DESTINATION

    This utility iterates through the specified directory, identifies files with
    the .nuspec extension, parses their content, and stores the extracted data
    in an XLSX output file.

    Options:
    -h, --help  Show this message and exit.

Example
=======

.. code-block::

   parse_nuspec ~/projects/ ~/scans/nuspec-parsed.xlsx
