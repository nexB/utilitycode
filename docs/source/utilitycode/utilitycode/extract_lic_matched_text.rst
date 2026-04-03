.. _extract_lic_matched_text:

==========================================
Extract Matched Text for Detected Licenses
==========================================

|div-page-outline|

.. contents:: :local:
    :depth: 7



Usage
=====

.. code-block::

  Usage: extract_detected_license_text [OPTIONS] INPUT OUTPUT

    Take an SCTK JSON input that has '"--license-text": true' and pull out each
    detected license’s matched_text. Save each one into its own file, using the
    identifier as the filename, in a directory.

  Options:
    -h, --help  Show this message and exit.

Example
=======

.. code-block::

  extract_detected_license_text ~/project/scans/scan_results.json ~/project/license_texts/

