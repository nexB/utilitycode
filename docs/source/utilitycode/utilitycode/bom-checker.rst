.. _bom-checker:

===================
BOM Checker Utility
===================

|div-page-outline|

.. contents:: :local:
    :depth: 7



Usage
=====

.. code-block::

      Usage: bom-checker [OPTIONS] LOCATION DESTINATION

         This utility validate the license expression field and url fields from the
         XLSX input and return the same XLSX file with the Attention column.

         Note: license expression can be validated with the choice from DejaCode
         License Library, or ScanCode LicenseDB (default)

      Options:
      --api_url URL                   URL to DejaCode License Library.
      --api_key KEY                   API Key for the DejaCode License Library
      -e, --expression-field-name FIELD_NAME
                                       Name of the license expression field
      -url, --url-field-name FIELD_NAME
                                       Name of the URL field
      -h, --help                      Show this message and exit.


Example
=======
.. code-block::

   bom-checker -e "license_expression" ~/path/input.xlsx ~/path/output.xlsx

.. code-block::

   bom-checker -e "Concluded License Expression" ~/path/input.xlsx
   ~/path/output.xlsx
   --api_url='https://enterprise.dejacode.com/api/v2/licenses/'
   --api_key='<API_KEY>'

.. code-block::

   bom-checker -e "Concluded License Expression" -url "homepage_url"
   ~/path/input.xlsx ~/path/output.xlsx

.. code-block::

   bom-checker -e "Concluded License Expression" -url "homepage_url" -url
   "license_url" ~/path/input.xlsx ~/path/output.xlsx

Notes
=====
This utility validates the license expression field if the `-e` (or
`--expression-field-name`) option is flagged. Users can define the database
(License Library) to use for the validation with the '--api_key' and
'--api_url' option. Note that a valid API_KEY is required for this options.
If no `-api_url` option is set, by default, the utility will use the
ScanCode LicenseDB to do the validation. In addition, it can also validate
URL fields. User can provide multiple `-url` (or `--url-field-name`)
options if user want to validate multiple URL fields.
