.. _extract_source_path_from_maps:

=============================
Extract Source Path from .map
=============================

|div-page-outline|

.. contents:: :local:
    :depth: 7



Usage
=====

.. code-block::

    Usage: extract_map [OPTIONS] INPUT OUTPUT

      This utility is designed to extract source paths from .map files (.js.map /
      .css.map). These .map files contain multiple sections, but the primary focus
      of this utility is the "sources" section, which it will extract.

    Options:
      --csv       Output as CSV format (Default: XLSX format)
      -h, --help  Show this message and exit.

Example
=======

.. code-block::

  extract_map ~/project/ ~/project/scans/extracted_map_path.xlsx


Notes
=====
The input can be a directory or a file.

The .map file usually contains the following section:
 - version
 - file
 - mappingss
 - sources
 - sourcesContent
 - name
 - sourceRoot

The only interested bit in the .map file is the sources section.
