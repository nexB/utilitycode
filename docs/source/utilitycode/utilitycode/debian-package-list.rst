.. _debian-package-list:

===================
Debian Install Path
===================

|div-page-outline|

.. contents:: :local:
    :depth: 7



Usage
=====

.. code-block::

  Usage: debian-package-list [OPTIONS] INPUT OUTPUT

    Read the *.md5sums files under /var/lib/dpkg/info/ to get the file level
    installed path and the md5 value

  Options:
    --csv       Output as CSV format (Default: XLSX format)
    -h, --help  Show this message and exit.

Example
=======

.. code-block::

  debian-package-list ~/project/var/lib/dpkg/info/ ~/project/scans/debian-installed-path.xlsx


Notes
=====
An example of a md5sums file looks like the following:

.. code-block::

  e49c68a5448a0db2f84e836bfd30963f  bin/chacl
  b82a6d48d6cf95db2032c5df130d20e2  bin/getfacl
  67c409a573ceeab89767a200526db2a6  bin/setfacl
  0dac782f00a1e917495d6e636a5b532b  usr/share/doc/acl/PORTING
  71009906f71f0c554714d693076bef73  usr/share/doc/acl/README
