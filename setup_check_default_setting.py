# -*- coding: utf-8 -*-
#
# Created on July, 13 2016
# @authors: Jiri Spilka
# http://people.ciirc.cvut.cz/~spilkjir
# @2015, CIIRC, Czech Technical University in Prague
#
# Licensed under the terms of the GNU GENERAL PUBLIC LICENSE
# (see CTGViewer.py for details)

import io
import re

"""
Auxillary function that checks setting of multiple default values.
Just to have everything at one place.
"""


# desired for Barry Schifrin
lfiles = [["MainWindow.py", "dockDataBrowser.setVisible", "dockDataBrowser.setVisible(False)"],
          ["MainWindow.py", "dockClinInfo.setVisible", "dockClinInfo.setVisible(False)"],
          ["MainWindow.py", "DEBUG_PROFILE = ", "False"],
          ["MainWindow.py", "DEBUG_FIGO_ANN = ", "False"],
          ["Config.py", "logging_level =", "logging.ERROR"],
          ["Config.py", "__ini_defaults\[EnumIniVar.paperformat\] =", "EnumPaperFormat.US"],
          ["Config.py", "__ini_defaults\[EnumIniVar.annotationToolbarAlignR\] =", "True"]
          ]

print "{0:15}: {1:50} - {2}".format("File", "Set value", "desired value")
print "-----------------------------------------------------------------------------------------------------------"

for l in lfiles:

    sfile = l[0]
    pattern = l[1]
    desired = l[2]

    print "{0:15}:".format(sfile),

    with io.open(sfile, "rt", encoding='utf-8') as fr:
        for s in fr.readlines():
            if re.search(pattern, s) is not None:
                print "{0:70} - {1}".format(s.strip(), desired)
