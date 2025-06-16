.. _license-category:

=======================
License Category (lcat)
=======================

|div-page-outline|

.. contents:: :local:
    :depth: 7



Usage
=====

.. code-block::

   Usage: lcat [OPTIONS] LOCATION DESTINATION API_KEY

   Retrieve details—including category, license name, attribution, and
   redistribution value—from DejaCode using the license expression found in the
   input.

   Options:
   -e, --expression-column-name TEXT
                                    [required]
   -o, --owner-column-name TEXT    [required]
   -lc, --license-category-column-name TEXT
   -ln, --license-name-column-name TEXT
   -a, --attribution-column-name TEXT
   -r, --redistribution-column-name TEXT
   -f, --force                     Force lcat to run even if there are errors
   -ws, --worksheet TEXT           Define the name of the worksheet to work on.
   --help                          Show this message and exit.


Examples
========

Pull data from DejaCode
-----------------------

.. code-block::

   lcat -e "License Expression" -o "Owner" -lc "Category" -ln "License Name" -a
   "Attribution" -r "Redistribution" <path to input inventory/BOM XLSX file>
   <path to output inventory/BOM XLSX file> <CommScope API key>


Pull data from DejaCode using '--force'
---------------------------------------

.. code-block::

   lcat -e "License Expression" -o "Owner" --force <path to input inventory/BOM
   XLSX file> <path to output inventory/BOM XLSX file> <DejaCode API key>


Notes
=====

API key
-------

The **License Category** utility ("LCAT") is designed to be used with audits in
which the license-related data will be retrieved from DejaCode using your
API key.

Contents of the output file
---------------------------

LCAT adds 6 new columns on the far right of the output file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

LCAT processes license expressions contained in an Excel worksheet (e.g.,
in the ``License Expression`` column) and creates a new workbook with one
worksheet containing all of the data from the input worksheet plus the four
additional columns to the right of the last column from the input
worksheet:

1. **ScanCode License Category**: This cell contains the DejaCode
   ``category`` value such as ``Permissive`` or
   ``Copyleft AND Permissive`` for the license expression in the input
   column cell. |br| |br|
2. **Normalized ScanCode License Category**: This cell contains the normalized
   value for the ScanCode License Category.
   |br| |br|
3. **ScanCode License Short Name**: This cell contains the ScanCode License
   ``name`` value for the license expression in the input column cell.
   |br| |br|
4. **Attribution**: This cell contains an ``x`` if the license expression
   in the input column cell indicates that the license requires attribution
   in the source code or documentation (or both) of the product where the
   licensed software is being used.
   |br| |br|
5. **Redistribution**: This cell contains an ``x`` if the license
   expression in the input column cell indicates that the license requires
   the product documentation to include instructions regarding how to
   obtain source code for the licensed software.
   |br| |br|
6. **SPDX Short Identifier**: This cell contains the SPDX Short Identifier
   collected from DejaCode


LCAT will keep the original value if the specific options are used
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

During the course of an audit -- and before running LCAT -- an auditor may
decide to manually add his or her conclusion regarding the license category,
license name, attribution and redistribution columns.

These are the optional flags:

.. code-block::

      -lc, --license-category-column-name TEXT
      -ln, --license-name-column-name TEXT
      -a, --attribution-column-name TEXT
      -r, --redistribution-column-name TEXT

This is an example of the optional flags being used in a command:

.. code-block::

    lcat -e "License Expression" -o "Owner" -lc "Category" -ln "License Name" -a
    "Attribution" -r "Redistribution" <path to input inventory/BOM XLSX file>
    <path to output inventory/BOM XLSX file> <DejaCode API key>

- **Note that if the original value is blank, LCAT will procduce data based
  on the value of the License Expression**. For instance, if the "Category"
  cell is empty and the -lc option is used, LCAT will generate the
  "Category" value based on the "License Expression". On the other hand, if
  the "Category" cell has value and the -lc option is used, LCAT will keep
  the original value for the "Category".


Error reporting and the '--force' flag
--------------------------------------

If LCAT detects any errors in the license expression column (e.g.,
``License Expression``), including blank cells or cells with a license
expression value not found in the queried DejaCode, LCAT will report the
errors in stdout and the error.log in the destination directory:

- e.g.

  .. code-block::

      Empty license_expression value at coord: "Y5" Empty license_expression
      value at coord: "Y6" Invalid license_expression value: "foo-3.0" at coord:
      "Y2" Invalid license_expression value: "commercial" at coord: "Y9"


By default, if LCAT identifies any errors, it will report them and then **exit
without creating an output file**.  However, you can force LCAT to create an
output file by including the ``--force`` or ``-f`` flag with your command,
e.g.,

.. code-block::

   lcat -e "License Expression" -o "Owner" -lc "Category" -ln "License Name" -a
   "Attribution" -r "Redistribution" --force <path to input inventory/BOM XLSX
   file> <path to output inventory/BOM XLSX file> <DejaCode API key>



Output worksheet formatting
---------------------------

- The output created by the utility will contain all the workseehts in the
  input.


Input values must be a license expression
-----------------------------------------

- LCAT will process license expressions that include any combination of ``AND``
  and ``OR`` operators, including nested parentheticals.

- LCAT will treat the ``WITH`` exception as the primary license. The generated
  license short name will keep both license and the ``WITH`` exception license.
  However, the category and attribution will only take the ``WITH`` exception
  license as the primary license. For instance, ``gpl-2.0 WITH
  classpath-exception-2.0`` will be evaluated like this: |br| |br|

  .. code-block::

      License Short Name: GPL 2.0 WITH Classpath exception to GPL 2.0 or later
      Category: Copyleft Limited
      Attribution: x


Selection of the input worksheet
--------------------------------

- By default, the utility “selects” the worksheet in which the :kbd:`save`
  function was last performed.

- Use the ``--ws`` option to define the specific worksheet in the input
  that should be worked on.


Passing the API key value
-------------------------

- The API key can be included in the CLI command directly, as the last value in
  the command, or indirectly, by running ``export API_KEY=`` plus the key prior
  to running the ``lcat`` command.

