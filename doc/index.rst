CTGViewer documentation
=======================

The CTGViewer a simple software used to display cardiotocography (CTG) records -- fetal heart rate and uterine contractions
together with a clinical information. It allows to easily browse directory of CTG files (e.g. the
CTU-UHB cardiotographic database).

**Features:**

* display CTG records in physionet (dat), matlab, and csv format
* view CTG together with clinical information (biochemical markers, length of I. and II. stage of labour etc)
* display CTG in European (1 cm/min, 20 bpm/cm) and US (3cm/min, 30 bpm/cm) formats.
* convert physionet (dat) format to csv
* download complete CTU-UHB database from physionet
* create simple annotations like basal heart rate, accelerations, decelerations, and notes
* export CTG to PDF (including annotations)

.. image:: images/CTGViewer_0_2_55.*
    :scale: 50

The CTGViewer was developed by `Jiri Spilka <http://people.ciirc.cvut.cz/~spilkjir/>`_ and
`Vaclav Chudacek <http://ctg.ciirc.cvut.cz/personal/chudacek.html>`_ at
`Czech Technical University in Prague <http://www.cvut.cz/>`_

The application is maintained at `CIIRC <http://www.ciirc.cvut.cz/>`_, `Czech Technical University in Prague <http://www.cvut.cz/>`_

**Note**: The CTGViewer was developed for research purposes and it is provided with no warranty.
The CTGViewer is distributed under GNU General Public License version 3.

Contents:

.. toctree::
   :maxdepth: 2

   installation
   downloads
   usermanual
   development
   reference

Changelog:
----------

* 2016-08-03 - added tool Caliper (used for measurement of time and bpm)
* 2016-07-12 - added export to PDF file
* 2016-04-13 - added annotations - ellipse, refactoring
* 2016-01-14 - added annotations (basal, baseline, etc.)
* 2016-01-06 - browse records in one folder
* 2016-01-01 - EU and US paper size, move in record using mouse wheel button and arrows
* 2014-04-01 - two bug fixes, one with settings ini and the other with database downloading
* 2014-03-30 - tool for batch download of the CTU-UHB CTG database
* 2014-03-29 - easy installation for Windows
* 2014-03-12 - fixed bug with reading physionet header

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

