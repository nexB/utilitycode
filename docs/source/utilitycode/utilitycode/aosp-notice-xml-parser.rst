.. _aosp-notice-xml-parser:

=====================
Parse AOSP XML Notice
=====================

|div-page-outline|

.. contents:: :local:
    :depth: 7



Usage
=====

.. code-block::

    Usage: aosp-notice-xml-parser [OPTIONS] INPUT OUTPUT LIC_LOCATION

    Take the AOSP XML Notice as an input. Parse the contentID, reference path
    and capture the license text. Save the contentID and the reference path to
    the output and save the captured licenses with the contentID as the filename
    to the lic_location.

    Options:
    --csv       Output as CSV format (Default: XLSX format)
    -h, --help  Show this message and exit.

Example
=======

.. code-block::

    aosp-notice-xml-parser ~/project/aosp.xml ~/project/scans/output.xlsx ~/project/captured_lic/

Notes
=====

.. code-block::

    <?xml version="1.0" encoding="utf-8"?>
    <licenses>
    <file-name contentId="45d4ee055bdf34776905c04117951798">/vendor/bin/blah</file-name>


    <file-content contentId="45d4ee055bdf34776905c04117951798"><![CDATA[

    /*-
     * Copyright (c) blah blah
     *
     * This is under a public domain.
     */
    ]]></file-content>

    </licenses>



The above is a sample for the AOSP notice xml file. This utility will parse the
`<file-name
contentId="45d4ee055bdf34776905c04117951798">/vendor/bin/sh</file-name>` to get
the contentID and the reference path. In addition, it will also capture the
license texts within the <file-content ... </file-content> and named as
contentID
