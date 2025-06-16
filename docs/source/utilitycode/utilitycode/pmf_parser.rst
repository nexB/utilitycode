.. _pmf_parse:

======================================
Package Management Files Parse Utility
======================================

|div-page-outline|

.. contents:: :local:
    :depth: 7



Usage
=====

.. code-block::

      Usage: pmf_parser [OPTIONS] INPUT_LOCATION OUTPUT

      Recursively parse the package management files from the input location and
      output the parsed data.

      Supported files:
         - Gemfile.lock
         - package-lock.json
         - yarn.lock
         - go.mod
         - go.sum
         - pubspec.lock
         - Pipfile.lock
         - requirements.txt
         - Podfile.lock
         - *.control

      Options:
      --csv          Output as CSV format (Default: XLSX format)
      --ignore TEXT  File to be ignored.
      --no-dev       Exclude dependencies that have ["dev": true] in package-
                     lock.json
      -h, --help     Show this message and exit.


Example
=======
.. code-block::

   pmf_parser --csv ~/path/to/gemfile.lock ~/path/to/gemfile-parsed.csv

.. code-block::

   pmf_parser ~/path/to/project/ ~/path/to/pmf-parsed.xlsx

.. code-block::

   pmf_parser --ignore go.sum --ignore requirements.txt ~/path/to/project/ ~/path/to/pmf_parsed.xlsx

The above command will ignore and not parse the `go.sum` and
`requirements.txt` files.

Notes
=====
This utility will walk thru the input location and look for the package
management files (Gemfile.lock, package-lock.json, yarn.lock, go.mod, go.sum,
pubspec.lock, Pipfile.lock, requirements.txt, Podfile.lock) and perform parsing
on these files. It will then use the parsed result (name, version) to extract
package information from various sources such as npmjs.org, rubygems.org,
pkg.go.dev etc. The package information will then be put in the OUTPUT.

The different between this utility's package-lock.json scan and the
:ref:`npm-package-analyzer` is this utility needs the lock file as the input
(one lock file at a time) while the :ref:`npm-package-analyzer` uses the
package scan data from scancode as the input.
