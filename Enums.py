# -*- coding: utf-8 -*-
#
# Created on June 24, 2016
# @author: Jiri Spilka
# http://people.ciirc.cvut.cz/~spilkjir
# @2015, CIIRC, Czech Technical University in Prague
#
# Licensed under the terms of the GNU GENERAL PUBLIC LICENSE
# (see CTGViewerLite.py for details)


class EnumIniVar:
    """
    Variables used in ini file
    """
    def __init__(self):
        pass

    lastUsedDirFiles = 'lastUsedDirFiles'
    dockClinInfoVisible = 'dockClinInfoVisible'
    dockDataBrowseVisible = 'dockDataBrowseVisible'
    dataBrowserSelectedAttributes = 'dataBrowserSelectedAttributes'
    annotationToolbar = 'annotationToolbar'
    annotationToolbarAlignR = 'annotationToolbarAlignR'
    paperformat = 'paperFormat'
    windowGeometry = 'windowGeometry'
    windowState = 'windowState'
    caliperVisible = 'caliperVisible'
    caliperFHR = 'caliperFHR'
    caliperTOCO = 'caliperTOCO'


class EnumVariableName:
    """
    Class EnumVariableName contains description and names of variables in a matlab file that can be used in python

    Examples of variables in mat-file (others not supported yet):

    :param fhr: fetal heart rate signal
    :param uc: uterine contractions signal
    :param timestamp: time stamp giving samples that are valid
    :type fhr: numeric vector
    :type uc: numeric vector
    :type timestamp: numeric vector

    | Example of matlab file:
    | fhr = [150,150,151,152,150]
    | uc = [7,10,10,9,8]
    | timestamp = [1,2,3,10,11] % timestamp represents timesamples; that is during time: 4,5,6,7,8,9 there is no recording.
    | Do not substitute with artifacts! The timestamp is used for situations when the recording was stopped and started again.

    save('temp.mat','fhr','uc','timestamp')

    | View file in ctgViewerLite
    | 1) open via menu bar in ctgViewerLite
    | 2) call ctgViewerLite from command prompt, see REFERENCE NEEDED: for details
    | 3) call ctgViewerLite from matlab, see REFERENCE NEEDED: for details

    """

    def __init__(self):
        pass

    fhr = 'fhr'  # required
    uc = 'uc'  # required
    timestamp = 'timestamp'  # required
    sBaseline = 'baseline'  # optional
    time_samp = 'time_samp'  # optional
    time_ms = 'time_ms'  # optional
    fs = 'fs'  # optional - sampling frequency


class EnumPlotBpm:
    """
    Plot/paper bpm size enum - defines bpm/cm ratio.
    """
    def __init__(self):
        pass
    step = 10
    min = twentyBpmCm = 20
    max = thirtyBpmCm = 30


class EnumPlotSpeed:
        """
        Plot/paper speed enum - defines cm/min ratio.
        """

        def __init__(self):
            pass

        step = 1
        min = oneCmMin = 1
        twoCmMin = 2
        max = threeCmMin = 3


class EnumPaperFormat:

    def __init__(self):
        pass

    EU = 'EU'
    US = 'US'


class EnumAnnType:
    """
    Types of annotations: basal, baseline, recovery
    """
    def __init__(self):
        pass

    select = 'select'
    basal = 'basal'
    baseline = 'baseline'
    recovery = 'recovery'
    no_recovery = 'no_recovery'
    excessive_ua = 'excessive_ua'
    ellipse = 'ellipse'
    ellipsenote = 'ellipsenote'
    note = 'note'
    plot_fhr = 'fhr'
    plot_toco = 'toco'
    floating_baseline = 'floating_baseline'
    deceleration = 'deceleration'
    acceleration = 'acceleration'
    uterine_contraction = 'uterine_contraction'
    caliper = 'caliper'
