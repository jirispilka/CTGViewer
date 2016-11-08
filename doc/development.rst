.. _developement:

Development
===========

The application is written in python. The following dependencies are required:

Dependencies
````````````
   * python 2.6 or higher - http://www/python.org:
   * PyQt4 - bindings to QT - http://www.riverbankcomputing.co.uk/software/pyqt/
   * pyqwt5 - graphical plotting - http://pyqwt.sourceforge.net/
   * numpy - numerical python - http://www.numpy.org/
   * Scipy - scientific computing
   * Argparse - arguments parsing
   * Reportlab - export to PDF files

**In the case of interest in development do not hesitate to contact us.**

Feature request
---------------

We appreciate any help regarding the developing and testing the CTGViewerLite.
The following things are planned to be implemented (when time allows):

* view clinical information in one table
* improve documentation
* test under Mac OS
* show progress bar when converting files

Reported bugs
-------------
* none reported

Building Windows executables
````````````````````````````

Introduction
------------

There are several ways to build windows executables from python scripts the most known are:

* `cx_Freeze <http://cx-freeze.sourceforge.net/>`_
* `py2exe <http://www.py2exe.org/>`_
* `pyinstaller <http://www.pyinstaller.org/>`_

It is difficult to choose between them since there is no clear sure fire method. For the current project I have found the py2exe unsuitable since it is not multi-platform and might have 
problems with numpy package (see `py2exe/WorkingWithVariousPackagesAndModules <http://www.py2exe.org/index.cgi/WorkingWithVariousPackagesAndModules>`_). 
I don't remember the reason why I've preferred *cx_Freeze* over pyinstaller. I guess I've found cx_Freeze more easy to get started with.

When having the windows executables it is convinient to make a single installer file that unpack the executables to desired location and handles the possible dependent files.
For this purpose I have found  `Inno setup <http://www.jrsoftware.org/isinfo.php>`_ simple and easy to use.

**In summary the CTGViewerLite installer is based on** `cx_Freeze <http://cx-freeze.sourceforge.net/>`_ **plus** `Inno setup <http://www.jrsoftware.org/isinfo.php>`_.

Useful links
------------

There are plenty of manuals and tutorials on *cx_Freeze* and *Inno Setup*. My intention here is to offer the final solution since the step by step explanation could be found elsewhere.
This manual is based on several resources. I do not list all of them here, just a selection of the best:

* http://cx-freeze.readthedocs.org/en/latest/index.html - documentation for cx_Freeze
* http://www.jrsoftware.org/ishelp/ - documentation for Inno setup
* http://unpythonic.blogspot.cz/2007/07/pygtk-py2exe-and-inno-setup-for-single.html - very nice tutorial. Although it is for py2exe with Inno Setup, it is nice and detailed description.
* http://www.aronhelser.com/2010/09/inno-setup-msvc-vcredist-without.html - Inno Setup MSVC vcredist without bothering users

Manual
------

**1. Run file set_version_number.py**  

This file automatically sets a new software version number in several files (setup.py, AboutUI.ui, setup_inno.iss, conf.py, AboutUI.ui). For the AboutUI.ui it also executes 
pyuic4 file to make AboutUI.py.

**2. Run python setup.py install** 

In the command prompt run::

    python setup.py install

*This file executes multiple tasks:*

* It first creates the windows executables using the cx_Freeze and place them into a build directory: build/exe.win32-2.6
* It runs the Inno Setup (using the *setup_inno.iss*) and creates windows installer and places it into a build directory: build

**The results is an executables installer file CTGViewerLite_v*.exe placed in the directory build.**

Files
-----

All required files are available in the CTGViewerLite.zip file (see :ref:`downloads`).

**An example of setup.py file:**

.. literalinclude:: ../setup.py

**An example of setup_inno.iss file:**

.. literalinclude:: ../setup_inno.iss
   :language: guess
