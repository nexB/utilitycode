.. _analyze-gem:

=================
Analyze Gem Files
=================

|div-page-outline|

.. contents:: :local:
    :depth: 7



Usage
=====

.. code-block::

    Usage: analyze-gem [OPTIONS] LOCATION DESTINATION

    Given an XLSX input file containing two columns: the gem's name in the first
    column and its version in the second column. Retrieve metadata from
    RubyGems.org, including details such as the owner, license, and download
    URL. Alternatively, PurlDB can be used to collect the gem's metadata.

    Options:
    -h, --help  Show this message and exit

Example
=======

.. code-block::

   analyze-gem ~/project/input.xlsx ~/project/output.xlsx

Note
====
The input excel file should only contains 2 columns.
The column A should be the name value, and the column B should be the
version value.

This utility will get the 'Owner', 'License' and 'Download URL' information
from rubygems.org based on the provided name and version.
