.. _ort_analyzer_parser:

===================
ORT Analyzer Parser
===================

|div-page-outline|

.. contents:: :local:
    :depth: 7



Usage
=====

.. code-block::

  Usage: ort_analyzer_parser [OPTIONS] INPUT_FILE OUTPUT

    Parser and format the ORT's analyzer-result.yml to XLSX

  Options:
    -h, --help  Show this message and exit.

Example
=======

.. code-block::

   ort_analyzer_parser ~/path/to/analyzer-result.yml ~/path/to/parsed-result.xlsx


Notes
=====
This utility parses the ORT's analyzer-result.yml file.
It will output 6 worksheets:


* repository_data
* project
* packages
* dependency_graphs
* packages_dependencies
* dependency_graphs_flatten

Note that the "dependency_graphs_flatten" is the "dependency_graphs" based
with the "direct" and "indirect" packages dependency from the
"packages_dependencies" worksheet.
