.. _analyze-debian-status:

==========================
Analyze Debian Status File
==========================

|div-page-outline|

.. contents:: :local:
    :depth: 7


Usage
=====

.. code-block::

  Usage: analyze-debian [OPTIONS] INPUT OUTPUT

    Read the /var/lib/dpkg/status file (status for the installed packages) and
    do the parsing using the debian-inspector library.

  Options:
    --csv       Output as CSV format (Default: XLSX format)
    --json      Output as JSON format (Default: XLSX format)
    -h, --help  Show this message and exit.

Example
=======

.. code-block::

   analyze-debian --csv ~/project/os/var/lib/dpkg/status ~/project/output.csv

.. code-block::

   analyze-debian ~/project/os/var/lib/dpkg/status ~/project/output.xlsx
