.. _debian-copyright-parser:

=======================
Debian Copyright Parser
=======================

|div-page-outline|

.. contents:: :local:
    :depth: 7



Usage
=====

.. code-block::

  Usage: debut-copyright-parser [OPTIONS] INPUT OUTPUT

    Parse the debian's copyright file to get the information for "Files",
    "License", "Copyright", "Comment"

  Options:
    --csv       Output as CSV format (Default: XLSX format)
    -h, --help  Show this message and exit.

Example
=======

.. code-block::

    debut-copyright-parser ~/project/code/debian/ ~/project/scans/debian-copyright.xlsx


Notes
=====
An example of a debain copyright file looks like the following:

.. code-block::

    Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
    Upstream-Name: Planet Venus
    Upstream-Contact: John Doe <jdoe@example.com>
    Source: https://www.example.com/code/venus

    Files: *
    Copyright: 2008, John Doe <jdoe@example.com>
               2007, Jane Smith <jsmith@example.org>
               2007, Joe Average <joe@example.org>
               2007, J. Random User <jr@users.example.com>
    License: PSF-2

    Files: debian/*
    Copyright: 2008, Dan Developer <dan@debian.example.com>
    License: permissive
     Copying and distribution of this package, with or without
     modification, are permitted in any medium without royalty
     provided the copyright notice and this notice are
     preserved.

    Files: debian/patches/theme-diveintomark.patch
    Copyright: 2008, Joe Hacker <hack@example.org>
    License: GPL-2+

    Files: planet/vendor/compat_logging/*
    Copyright: 2002, Mark Smith <msmith@example.org>
    License: MIT
     [LICENSE TEXT]

    Files: planet/vendor/httplib2/*
    Copyright: 2006, John Brown <brown@example.org>
    License: MIT2
     Unspecified MIT style license.

    Files: planet/vendor/feedparser.py
    Copyright: 2007, Mike Smith <mike@example.org>
    License: PSF-2

    Files: planet/vendor/htmltmpl.py
    Copyright: 2004, Thomas Brown <coder@example.org>
    License: GPL-2+

    License: PSF-2
     [LICENSE TEXT]

    License: GPL-2+
     This program is free software; you can redistribute it
     and/or modify it under the terms of the GNU General Public
     License as published by the Free Software Foundation; either
     version 2 of the License, or (at your option) any later
     version.
     .
     This program is distributed in the hope that it will be
     useful, but WITHOUT ANY WARRANTY; without even the implied
     warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
     PURPOSE.  See the GNU General Public License for more
     details.
     .
     You should have received a copy of the GNU General Public
     License along with this package; if not, write to the Free
     Software Foundation, Inc., 51 Franklin St, Fifth Floor,
     Boston, MA  02110-1301 USA
     .
     On Debian systems, the full text of the GNU General Public
     License version 2 can be found in the file
     `/usr/share/common-licenses/GPL-2'.
