============
Installation
============

Installation for Windows
------------------------

Download and install the windows installer below

  * Download the CTGViewerLite installer, run it and follow the installation steps (:ref:`downloads`)
  * In the case of trouble, try to download and install package `vcredist_x86.exe <http://www.microsoft.com/en-us/download/details.aspx?id=5555>`_


Linux and MAC
-------------

Linux:
``````
We expect that Linux users will be able to install required packages in their distribution by themselves.

 * Download the source files (:ref:`downloads`) and unpack it to desired directory.
 * Install all dependencies as desribed in (:ref:`developement`)

After installation run command::

    > python ctgViewerLite.py

It is also possible (though not recommended) to download the Windows installer and run CTGViewerLite under wine.

MAC users:
``````````
The application was not tested on Macintosh machines.

Please see `http://www.python.org/getit/mac/ <http://www.python.org/getit/mac/>`_
for further details on how to install Python to MAC.

See the (:ref:`developement`) for details on required packages.

It is also possible (though not recommended) to download the Windows installer and run CTGViewerLite under wine.

Installation from source
------------------------

Download the ziped source in the section (:ref:`downloads`).

Windows
```````
Since the application relies on library pyqwt (used for plotting) we strongly recommend to use version of
packages that was pyqwt compiled with (http://pyqwt.sourceforge.net/download.html). See the example below.
We also recommend to use win32 binaries.

An example of files to download and install:

* Python 2.6 `python-2.6.2.msi <https://www.python.org/ftp/python/2.6.2/python-2.6.2.msi>`_
* PyQt 4.5. `PyQt-Py2.6-gpl-4.5.4-1.exe <http://pyqwt.sourceforge.net/support/PyQt-Py2.6-gpl-4.5.4-1.exe>`_
* PyQwt 5.2.0 `PyQwt5.2.0-Python2.6-PyQt4.5.4-NumPy1.3.0-1.exe <http://prdownloads.sourceforge.net/pyqwt/PyQwt5.2.0-Python2.6-PyQt4.5.4-NumPy1.3.0-1.exe>`_
* Numpy 1.3.0 `numpy-1.3.0-win32-superpack-python2.6.exe <http://prdownloads.sourceforge.net/numpy/numpy-1.3.0-win32-superpack-python2.6.exe>`_
* Scipy 0.7.2 `scipy-0.7.2-win32-superpack-python2.6.exe <http://sourceforge.net/projects/scipy/files/scipy/0.7.2/scipy-0.7.2-win32-superpack-python2.6.exe/download>`_
* Argparse 1.1. `argparse-1.1.win32.msi <http://code.google.com/p/argparse/downloads/detail?name=argparse-1.1.win32.msi&can=2&q=>`_
* Reportlab 3.0 `Reportlab 3.0 <https://pypi.python.org/pypi/reportlab>`_

Linux
`````

Installation for debian based distributions::

    > sudo apt-get install python python-qt4 python-qwt5-qt4 python-numpy python-scipy python-reportlab