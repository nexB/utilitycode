.. _scio2inv:

==========================================
Translate SCIO XLSX To Working BOM formart
==========================================

|div-page-outline|

.. contents:: :local:
    :depth: 7



Usage
=====

.. code-block::

  Usage: scio2inv [OPTIONS] INPUT OUTPUT

    This utility converts an SCIO-generated XLSX file to the inventory format we
    want for analysis and reporting. The objective is to reduce manual work and
    human errors.

  Options:
    --package name   Package worksheet name from the INPUT. (Default: PACKAGES)
    --resource name  Resource worksheet name from the INPUT. (Default:
                     RESOURCES)
    --reorder        Format and reorder all the original columns from the input.
                     See "packages_no_reported_fields_headers" and
                     "resources_no_reported_fields_headers" for the order.
    -h, --help       Show this message and exit.

Example
=======

.. code-block::

   scio2inv ~/analyzed/scancodeio_results.xlsx ~/report/project-bom-v0.10.xlsx

Notes
=====

The script will reformat the "PACAGES" and "RESOURCES" worksheet by adding
and reordering fields.


OUTPUT fields order
-------------------

PACKAGES
^^^^^^^^

 * Status
 * Notes
 * ToDo
 * Issue Ref
 * Product
 * Codebase
 * Package URL (purl)
 * Package Type
 * License Category
 * License Expression
 * Copyright Holders
 * Vulnerable
 * Disclosed
 * Deployed
 * Analysis Notes
 * Homepage URL
 * Download URL
 * Other URL
 * Detected License Expression
 * Detected Copyright Holder
 * Detected Copyright Notice
 * Primary Language
 * Description
 * Parties
 * Package Unique ID
 * sha1
 * copyright
 * other_license_expression
 * notice_text
 * declared_license_expression_spdx
 * other_license_expression_spdx
 * bug_tracking_url
 * code_view_url
 * vcs_url
 * repository_homepage_url
 * api_data_url
 * repository_download_url
 * namespace
 * name
 * version
 * qualifiers
 * subpath
 * package_uid
 * datasource_id
 * file_references
 * source_packages
 * size
 * md5
 * sha1
 * sha256
 * sha512
 * release_date
 * keywords
 * missing_resources
 * modified_resources
 * xlsx_errors'

RESOURCES
^^^^^^^^^

 * analysis_priority
 * file_category
 * file_subcategory
 * Status
 * Notes
 * ToDo
 * Issue Ref
 * Product
 * Codebase
 * Resource Path
 * Resource Name
 * Resource Type
 * for_packages
 * License Category
 * License Expression
 * Copyright Holders
 * Disclosed
 * Deployed
 * Analysis Notes
 * Homepage URL
 * Download URL
 * Other URL
 * Detected License Expression
 * Detected Copyright Holders
 * Detected Copyright Notice
 * tag
 * size
 * sha1
 * mime_type
 * file_type
 * status
 * extension
 * emails
 * urls
 * authors
 * detected_license_expression_spdx
 * percentage_of_license_text
 * package_data
 * md5
 * sha256
 * sha512
 * is_binary
 * is_text
 * is_archive
 * is_media
 * is_key_file
 * xlsx_errors'


The `--reorder` option reorder the "PACKAGES", "DEPENDENCIES", and
"RESOURCES" columns


`--reorder` fields order
-------------------------

PACKAGES
^^^^^^^^

 * purl
 * type
 * declared_license_expression
 * holder
 * copyright
 * homepage_url
 * download_url
 * primary_language
 * parties
 * package_uid
 * sha1
 * size
 * notice_text
 * other_license_expression
 * declared_license_expression_spdx
 * other_license_expression_spdx
 * api_data_url
 * bug_tracking_url
 * code_view_url
 * vcs_url
 * repository_homepage_url
 * repository_download_url
 * datasource_id
 * description
 * namespace
 * name
 * version
 * qualifiers
 * subpath
 * source_packages
 * file_references
 * keywords
 * release_date
 * missing_resources
 * modified_resources
 * md5
 * sha256
 * sha512
 * xlsx_errors

DEPENDENCIES
^^^^^^^^^^^^

* for_package_uid
* package_type
* purl
* extracted_requirement
* scope
* is_runtime
* is_optional
* is_resolved
* datasource_id
* datafile_path
* dependency_uid
* xlsx_errors'

RESOURCES
^^^^^^^^^

 * path
 * name
 * type
 * for_packages
 * status
 * detected_license_expression
 * holders
 * copyrights
 * size
 * emails
 * tag
 * sha1
 * urls
 * mime_type
 * file_type
 * extension
 * programming_language
 * sha512
 * detected_license_expression_spdx
 * percentage_of_license_text
 * authors
 * package_data
 * is_binary
 * is_key_file
 * is_text
 * is_archive
 * is_media
 * md5
 * sha256
 * xlsx_errors'
