.. _column-matching:

===============
Column Matching
===============

|div-page-outline|

.. contents:: :local:
    :depth: 7



Overview
========

The ``column_match`` command will match the defined columns from the two inputs
and return the matched value and matched_scores.

This utility can help do column matching, which is particularly useful when
trying to match DWARF references to the development codebase path. In
addition, a user can also use this utility to perform other kinds of
matching such as file_name match, file_base_name match, sha1match and so
on. Moreover, it can be used for Java D2D matching with a little twist.

The following will be in the generated output:

1. all the columns from the first input (the input in the first argument);
2. a ``resolved_`` column that has the normalized value (this is
   implemented specifically for dwarf references matching as, sometimes,
   dwarf references contains ``./`` or ``../`` that we want to normalized);
3. a ``matched`` column containing the value from the second input that was
   matched with the first input with the defined column;
4. ``matched_score`` columns that reflect the number fo consecutive
   segments matched from right to left, and from left to right;
5. ``totla_path_segments_count`` and ``matched_percentage`` are the stats
   of the matching;
6. for each remaining column in the second input that also exists in the
   first input, these columns and its related values will be included in
   the output with the column name prefix ``matched_`` (e.g.,
   ``about_resource`` ==> ``matched_about_resource``).

Usage
======

.. code-block::

  Usage: column_match [OPTIONS] INPUT1 INPUT2 OUTPUT

    Get the header keys from both input.

  Options:
    --best_matches_only  Return only the highest scoring matches. If no match is
                        available for a row from INPUT1, then that row is
                        returned in OUTPUT with no match result added.
    --csv                Output as CSV format (Default: XLSX format)
    -k1, --key1 key1     Column name from INPUT1 for matching.  [required]
    -k2, --key2 key2     Column name from INPUT2 for matching.  [required]
    -h, --help           Show this message and exit.


Input
-----

Let have the following input as the input examples:

``input1.csv``

.. list-table::
   :widths: 30 20 30
   :header-rows: 1

   * - about_resource
     - hash1
     - license
   * - /project/test.c
     - aaa
     - apache-2.0
   * - /project/test.java
     - bbb
     - public-domain
   * - /project/hello.h
     - aaa
     - public-domain

``input2.csv``

.. list-table::
   :widths: 30 20 30
   :header-rows: 1

   * - about_resource
     - hash2
     - license
   * - /project/test.c
     - ccc
     - gpl-2.0
   * - /project/test/test.c
     - ccc
     - public-domain
   * - /tmp/project/hello.h
     - bbb
     - public-domain

Example 1
---------

.. code-block::

   column_match -k1 about_resource -k2 about_resource input1.csv input2.csv
   output.xlsx

``output.xlsx``

.. list-table::
   :widths: 10 10 10 10 10 10 10 10 10 10 10 10 10
   :header-rows: 1

   * - about_resource
     - hash1
     - license
     - resolved_about_resource
     - matched
     - matched_score_from_right
     - matched_score_from_left
     - total_path_segments_count
     - match_percentage_from_right
     - match_percentage_from_left
     - matched_about_resource
     - hash2
     - matched_license
   * - /project/test.c
     - aaa
     - apache-2.0
     - project/test.c
     - project/test.c
     - 2
     - 2
     - 2
     - 100
     - 100
     - /project/test.c
     - ccc
     - gpl-2.0
   * - /project/test.c
     - aaa
     - apache-2.0
     - project/test.c
     - project/test/test.c
     - 1
     - 2
     - 2
     - 50
     - 100
     - /project/test/test.c
     - ccc
     - public-domain
   * - /project/test.java
     - bbb
     - public-domain
     - project/test.java
     -
     -
     -
     -
     -
     -
     -
     -
     -
   * - /project/hello.h
     - aaa
     - public-domain
     - project/hello.h
     - tmp/project/hello.h
     - 2
     - 2
     - 2
     - 100
     - 100
     - /tmp/project/hello.h
     - bbb
     - public-domain



.. code-block::

   column_match -k1 about_resource -k2 about_resource input1.csv input2.csv
   output.xlsx --best_matches_only

``output.xlsx``

.. list-table::
   :widths: 10 10 10 10 10 10 10 10 10 10 10 10 10
   :header-rows: 1

   * - about_resource
     - hash1
     - license
     - resolved_about_resource
     - matched
     - matched_score_from_right
     - matched_score_from_left
     - total_path_segments_count
     - match_percentage_from_right
     - match_percentage_from_left
     - matched_about_resource
     - hash2
     - matched_license
   * - /project/test.c
     - aaa
     - apache-2.0
     - project/test.c
     - project/test.c
     - 2
     - 2
     - 2
     - 100
     - 100
     - /project/test.c
     - ccc
     - gpl-2.0
   * - /project/test.java
     - bbb
     - public-domain
     - project/test.java
     -
     -
     -
     -
     -
     -
     -
     -
     -
   * - /project/hello.h
     - aaa
     - public-domain
     - project/hello.h
     - tmp/project/hello.h
     - 2
     - 2
     - 2
     - 100
     - 100
     - /tmp/project/hello.h
     - bbb
     - public-domain


Notes
~~~~~

The above command matches the **about_resource** column from ``input1.csv``
with the **about_resource** column from ``input2.csv``.  The matched score
is calculated by the number of segments matched.  Note that for
``/project/test.java``, although this entry does not have any matches, it
will still be kept in ``output.xlsx``. In the second run with the
**--best_matches_only** option, only the highest/best_matches result will
be kept.

Example 2
---------

.. code-block::

   column_match -k1 hash1 -k2 hash2 input1.csv input2.csv output.xlsx


``output.xlsx``

.. list-table::
   :widths: 10 10 10 10 10 10 10 10 10 10 10 10 10
   :header-rows: 1

   * - about_resource
     - hash1
     - license
     - resolved_hash1
     - matched
     - matched_score_from_right
     - matched_score_from_left
     - total_path_segments_count
     - match_percentage_from_right
     - match_percentage_from_left
     - matched_about_resource
     - hash2
     - matched_license
   * - /project/test.c
     - aaa
     - apache-2.0
     - aaa
     -
     -
     -
     -
     -
     -
     -
     -
     -
   * - /project/hello.h
     - aaa
     - public-domain
     - aaa
     -
     -
     -
     -
     -
     -
     -
     -
     -
   * - /project/test.java
     - bbb
     - public-domain
     - bbb
     - bbb
     - 1
     - 1
     - 1
     - 100
     - 100
     - /tmp/project/hello.h
     - bbb
     - public-domain

Notes
~~~~~

The above command matches the ``hash1`` column from ``input1.csv`` with the
``hash2`` column from ``input2.csv``.  Note that the matched key ``hash2`` from
``input2.csv`` will be displayed in the ``matched`` column.

Example 3
---------

This example demonstrate the little twist to use this utility to perform
Java D2D matching.

``input3.csv``

.. list-table::
   :widths: 30
   :header-rows: 1

   * - path
   * - /project/abc.java
   * - /project/test/generated.java
   * - /project/main.java

``input4.csv``

.. list-table::
   :widths: 30
   :header-rows: 1

   * - path
   * - /deploy/component.jar
   * - /deploy/component.jar-extract/project/abc.class
   * - /deploy/component.jar-extract/project/main.class

The ``column_match`` will not work directly as the paths in both inputs are
different. (i.e. ``input3.csv`` contains .java files while ``input4.csv``
has .class files)

In order to use the ``column_match``, we can do a little twist to create a
new column in ``input4.csv`` and copy/paste the ``path`` column and
replacing ``.class`` with ``.java``


``input4-mod.csv``

.. list-table::
   :widths: 30 30
   :header-rows: 1

   * - path
     - modified_path
   * - /deploy/component.jar
     - /deploy/component.jar
   * - /deploy/component.jar-extract/project/abc.class
     - /deploy/component.jar-extract/project/abc.java
   * - /deploy/component.jar-extract/project/main.class
     - /deploy/component.jar-extract/project/main.java

Now, we can use ``column_match``

.. code-block::

   column_match -k1 path -k2 modified_path input3.csv input4-mod.csv output.xlsx


``output.xlsx``

.. list-table::
   :widths: 10 10 10 10 10 10 10 10 10 10
   :header-rows: 1

   * - path
     - resolved_path
     - matched
     - matched_score_from_right
     - matched_score_from_left
     - total_path_segments_count
     - match_percentage_from_right
     - match_percentage_from_left
     - matched_path
     - modified_path
   * - /project/abc.java
     - project/abc.java
     - deploy/component.jar-extract/project/abc.java
     - 2
     - 2
     - 2
     - 100
     - 100
     - /deploy/component.jar-extract/project/abc.class
     - /deploy/component.jar-extract/project/abc.java
   * - /project/test/generated.java
     - project/test/generated.java
     -
     -
     -
     -
     -
     -
     -
     -
   * - /project/main.java
     - project/main.java
     - deploy/component.jar-extract/project/main.java
     - 2
     - 2
     - 2
     - 100
     - 100
     - /deploy/component.jar-extract/project/main.class
     - /deploy/component.jar-extract/project/main.java

Notes
~~~~~

The above example shows although the input may not suitable to use for
``column_match`` at first, doing a little twist will make it work and
can have desire result.
