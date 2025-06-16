.. _system_file_index:

=================
System File Index
=================

|div-page-outline|

.. contents:: :local:
    :depth: 7



Usage
=====

.. code-block::

    Usage: sfi [OPTIONS] LOCATION DESTINATION

    Match file paths to Linux system packages.

    LOCATION is the path to a CSV with one column named `Resource` that contains
    the paths to be matched.

    DESTINATION is the path where the match results are to be saved as CSV.

    Options:
    --reindex             Recreate the system package files index before
                            matching.
    --contents-file TEXT  Create index from a specified Contents-<arch>.gz file.
                            Multiple Contents files can be specified and they will
                            be combined into a single index.
    --index-file TEXT     Specify an index file to use for matching. This option
                            is only used for testing purposes.
    -h, --help            Show this message and exit.


