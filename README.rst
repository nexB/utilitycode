================
nexB UtilityCode
================
UtilityCode is a suite of special utilities for software composition analysis (SCA). 
These are primarily sandbox-style utilities to complement the more robust tools
available from AboutCode at:
    https://github.com/aboutcode-org
Over time many of these utilities will be incorporated into one or more 
AboutCode projects. 

**Please note that these utilities are not tested or 
documented at the same level as we apply to AboutCode projects.**

REQUIREMENTS
------------
UtilityCode is tested with Python 3.7 or above only on Linux, Mac and
Windows. You will need to install a Python interpreter if you do not have
one already installed.

On Linux and Mac, Python is typically pre-installed. To verify which
version may be pre-installed, open a terminal and type:

python --version

Note:
Debian has decided that distutils is not a core python package, so it is
not included in the latest versions of debian and debian-based OSes.

A solution is to run: `sudo apt install python3-distutils`

On Windows or Mac, you can download the latest Python here:
    https://www.python.org/downloads/

Download the .msi installer for Windows or the .dmg archive for Mac. Open
and run the installer using all the default options.


INSTALLATION
------------
Checkout or download and extract the UtilityCode from:
    https://github.com/nexB/utilitycode/

To install all the needed dependencies in a virtualenv, run (on posix):
    ./configure
or on windows:
    configure


ACTIVATE the VIRTUALENV
-----------------------
To activate the virtualenv, run (on posix):
    source venv/bin/activate
or on windows:
    venv\\bin\\activate


DEACTIVATE the VIRTUALENV
-------------------------
To deactivate the virtualenv, run (on both posix and windows):
    deactivate


TESTS and DEVELOPMENT
---------------------
To install all the needed development dependencies, run (on posix):
    ./configure --dev
or on windows:
    configure --dev

To verify that everything works fine you can run the test suite with:
    pytest


CLEAN BUILD AND INSTALLED FILES
-------------------------------
To clean the built and installed files, run (on posix):
    ./configure --clean
or on windows:
    configure --clean


HELP and SUPPORT
----------------
If you have a question or find a bug, enter a ticket at:
https://github.com/nexB/utilitycode

For issues, you can use:
https://github.com/nexB/utilitycode/issues

HACKING
-------
We accept pull requests provided under the same license as this tool. You
agree to the http://developercertificate.org/


LICENSE
-------
The UtilityCode is released under the Apache 2.0 license. See the
utilitycode.ABOUT file for details.
