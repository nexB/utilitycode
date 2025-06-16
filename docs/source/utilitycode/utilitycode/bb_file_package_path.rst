.. _bb_file_package_path:

==========================================
BitBake/Yocto - Parse files-in-package.txt
==========================================

|div-page-outline|

.. contents:: :local:
    :depth: 7



Usage
=====

.. code-block::

  Usage: bb_file_package_path [OPTIONS] LOCATION OUTPUT

    Parse and collect package's installed path from files-in-package.txt. The
    input can be a directory or a file.

  Options:
    --csv   Output as CSV format (Default: XLSX format)
    --help  Show this message and exit.

Example
=======

.. code-block::

   bb_file_package_path ~/project/buildhistory/ ~/project/parse/result.xlsx

Notes
=====
This utility looks for the "files-in-package.txt" from the input location
(either file or directory) and do the parsing to get the "Package Name" and
"Install Path"

.. code-block::

    drwxr-xr-x root       root             4096 ./usr
    drwxr-xr-x root       root             4096 ./usr/lib
    -rwxr-xr-x root       root           113644 ./usr/lib/libexpat.so.1.6.9
    lrwxrwxrwx root       root               17 ./usr/lib/libexpat.so.1 -> libexpat.so.1.6.9


Assuming the above is from
`/project/buildhistory/packages/arm/expat/expat/files-in-package.txt`

The utility will take the parent directory name (`expat`) as the "Package
Name" and capture the "file" (i.e. `./usr/lib/libexpat.so.1.6.9`) in the
above list to the "Install Path"

i.e. It will not capture directory and link files.
