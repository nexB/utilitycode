=================
License Reference
=================

|div-page-outline|

.. contents:: :local:
    :depth: 7



Usage
=====

.. code-block::

   Usage: lref [OPTIONS] EXPRESSION_COLUMN_NAME LOCATION DESTINATION

   This utility will generate the "SPDX Short Identifier", "ScanCode License
   Category" and "ScanCode License URL" based on the license expression value.
   If no API information is provided, the tool will use data from ScanCode
   LicenseDB.

   Options:
   --api_url URL  URL to DejaCode License Library.
   --api_key KEY  API Key for the DejaCode License Library
   --help         Show this message and exit.


Example
=======

.. code-block::

   lref "license_expression" ~/path/to/input.xlsx ~/path/to/output.xlsx

.. code-block::

   lref --api_url='https://enterprise.dejacode.com/api/v2/licenses/'
   --api_key='<API_KEY>' "license_expression" ~/path/to/input.xlsx
   ~/path/to/output.xlsx


Notes
=====

URL for DejaCode Enterprise:
``https://enterprise.dejacode.com/api/v2/licenses/``
