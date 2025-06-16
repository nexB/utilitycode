.. _vcio_report:

===========
VCIO Report
===========

|div-page-outline|

.. contents:: :local:
    :depth: 7


Usage
=====

.. code-block::

  Usage: vcio_report [OPTIONS] LOCATION DESTINATION API_KEY

    vcio_report is a command-line utility that enables a user to submit a .txt
    containing a list of one or more syntactically-correct PURLs and retrieve a
    .xlsx of vulnerabilities (if any) for each listed PURL contained in the VCIO
    database.

  Options:
    -h, --help  Show this message and exit

Example
=======

.. code-block::

   vcio_report <path-to-input-purls.txt> <path-to-output-vulnerability-data.xlsx> <API-key>
