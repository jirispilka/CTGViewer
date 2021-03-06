# -*- coding: utf-8 -*-
#
# Created on Oct 15, 2013
# @authors: Jiri Spilka
# http://people.ciirc.cvut.cz/~spilkjir
# @2015, CIIRC, Czech Technical University in Prague
#
# Licensed under the terms of the GNU GENERAL PUBLIC LICENSE
# (see CTGViewer.py for details)

import os
import sys
import numpy as np
from PyQt4.QtCore import QTime
from PyQt4.Qt import QString

"""
"static" functions
"""

# log = logging.getLogger(Config.logger_name)


def ensure_dir(sdir):
    if not os.path.exists(sdir):
        os.makedirs(sdir)


def file_exists(infile):
    """ check if a file exist """
    if os.path.exists(infile):
        return True
    else:
        # log.error("File not exists: {0}".format(inFile))
        return False


def get_filename_with_ext(infile):
    dummy, file_name_with_ext = os.path.split(infile)
    return file_name_with_ext


def get_filename_without_ext(infile):
    file1 = get_filename_with_ext(infile)
    file_name, dummy = os.path.splitext(file1)
    return file_name


def get_filename_and_ext(infile):
    file1 = get_filename_with_ext(infile)
    file_name, ext = os.path.splitext(file1)
    return file_name, ext


def get_number_lines_in_stream(fstream):
    """ count lines in a stream, when done return stream to the beginning of a file """
    lines = 0
    buf_size = 1024 * 1024
    read_f = fstream.read  # loop optimization

    buf = read_f(buf_size)
    while buf:
        lines += buf.count('\n')
        buf = read_f(buf_size)

    fstream.seek(0)
    return lines


def get_mumber_lines(filename):
    """ count lines in a file """

    f = open(filename, "r+")
    lines = get_number_lines_in_stream(f)
    f.close()
    return lines


def get_files_with_ext_mask(dir_name, ext_mask):
    """
    Get all files in directory with specified extension
    :param dir_name:
    :param ext_mask:
    :return: list of files
    :rtype: list()
    """
    if ext_mask[0] == '.':
        ext_mask = ext_mask[1:]

    files = directory_listing(dir_name)
    output = list()
    for f in files:
        dummy, ext = get_filename_and_ext(f)

        if len(ext) == 0:
            continue

        if ext[0] == '.':
            ext = ext[1:]

        if ext_mask == ext:
            output.append(f)

    return output


def directory_listing(dir_name):
    output = []
    for dirname, dummy, filenames in os.walk(dir_name):
        for filename in filenames:
            output.append(os.path.join(dirname, filename))

    return output


def get_application_path():
    """ determine if application is a script file or frozen exe """
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    elif __file__:
        return os.path.dirname(__file__)


def remove_nans_at_begin_and_end(x):

    # if a signal begins or ends with NaNs --> do not interpolate there
    gap_at_begin = []
    # ind_samples = np.where(x != 0)[0]
    ind_samples = np.where(np.logical_and(x != 0, ~np.isnan(x)))[0]

    if len(ind_samples) > 0:
        if ind_samples[0] != 0: # if there is no signal at position 0
            gap_at_begin = np.arange(0, ind_samples[0])

    gap_at_end = []
    if len(ind_samples) > 0:
        if ind_samples[-1] != len(x):
            gap_at_end = np.arange(ind_samples[-1]+1, len(x))

    ifrom = ind_samples[0]
    ito = ind_samples[-1]+1
    x_out = x[ifrom:ito]
    return x_out, gap_at_begin, gap_at_end, ifrom, ito


def generate_calib_signal(fs=4, sformat='EU'):
    """
    Generate step function for calibration of plots
    The FHR signal starts at min value and then each seconds increments by 10

    """

    n1 = fs*60
    if sformat == 'EU':
        first_val = 50
        nmin = 60
        nmax = 210
    else:
        first_val = 20
        nmin = 30
        nmax = 240

    fhr = first_val * np.ones((n1, 1))
    for i in range(nmin, nmax + 1, 10):
        x = i*np.ones((n1, 1))
        fhr = np.vstack((fhr, x))

    uc = np.zeros((n1, 1))
    for i in range(10, 101, 5):
        x = i * np.ones((n1, 1))
        uc = np.vstack((uc, x))

    fhr = np.vstack((fhr, fhr))
    uc = np.vstack((uc, uc))

    res = len(uc) - len(fhr)
    uc = uc[0:len(uc) - res]
    # print len(uc) - len(fhr)

    fhr = fhr.ravel()
    uc = uc.ravel()

    # timestamp = range(0, len(fhr), 1)
    timestamp = np.arange(1, len(fhr) + 1, 1, np.int)

    return fhr, uc, timestamp


def time_locator(time_string, locator_min, locator_hour, nlastsample, fs):
    """
    Locates time points at the X axis. The points could be either minutes or hours.
    If both are equal to -1 the time set to hours and time is quesed.
    """

    if time_string is None:
        return

    bminute_locator = False
    bhour_locator = False

    if not locator_min == -1:
        bminute_locator = True
        interval_time = locator_min
        ninterval_samples = fs * 60
        arange = range(0, 59, interval_time)

    elif not locator_hour == -1:
        bhour_locator = True
        interval_time = locator_hour
        ninterval_samples = fs * 3600
        arange = range(0, 24, interval_time)
    else:
        # guess range for hours locator
        qfirst_time = QTime.fromString(time_string[0], "hh:mm:ss:zzz")
        qlast_time = QTime.fromString(time_string[-1], "hh:mm:ss:zzz")
        qdiff_time = qlast_time.hour() - qfirst_time.hour()

        # interval time based on signal length
        if qdiff_time > 120:
            interval_time = 0
        elif qdiff_time > 48:
            interval_time = 6
        elif qdiff_time > 24:
            interval_time = 2
        else:
            interval_time = 1

        bhour_locator = True
        ninterval_samples = fs * 3600
        arange = range(0, 24, interval_time)

    # nlastsample = int(self._x[-1])
    qfirst_time = QTime.fromString(time_string[0], "hh:mm:ss:zzz")

    # find the first xtick of axis
    t = 0
    startsample = 0
    while t < nlastsample:
        qtime = qfirst_time.addMSecs(1000 * t / fs)
        if bhour_locator:
            if (qtime.hour() in arange) & (qtime.minute() == 0) & (qtime.second() == 0) & (qtime.msec() == 0):
                startsample = t
                break

        elif bminute_locator:
            if (qtime.minute() in arange) & (qtime.second() == 0) & (qtime.msec() == 0):
                startsample = t
                break

        t += 1

    # compute ticks
    time_tics_located = []
    value = startsample
    while value < nlastsample:

        if not value in time_tics_located:
            time_tics_located.append(value)

        # update for next iteration
        value += interval_time * ninterval_samples

    return time_tics_located


def samples2time(nr_samples, fs, time_begin=QString("00:00:00:000")):
    """
    Compute time axis for a signal

    :param nr_samples:
    :param fs: sampling frequency
    :param time_begin:
    :return: list of times in a format e.g. 00:00:10, 00:00:20, 00:00:30
    """
    sformat = "hh:mm:ss:zzz"
    qtime = QTime.fromString(time_begin, sformat)
    ms = 1000 / fs
    atime = list()

    for dummy in range(0, nr_samples):
        qtime = qtime.addMSecs(ms)
        atime.append(qtime.toString(sformat))

    return atime
