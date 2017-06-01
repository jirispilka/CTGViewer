# -*- coding: utf-8 -*-
#
# Created on Oct 15, 2013
# @authors: Jiri Spilka
# http://people.ciirc.cvut.cz/~spilkjir
# @2015, CIIRC, Czech Technical University in Prague
#
# Licensed under the terms of the GNU GENERAL PUBLIC LICENSE
# (see CTGViewer.py for details)

"""
LoadWriteData
-------------

Load and write data in several formats.
    * text files
    * matlab files
    * csv files
    * txt: mb: loading csv directly from TXT/CSV file generated from BDI

Reference
~~~~~~~~~

.. autoclass:: EnumVariableName
.. autoclass:: LoadData
   :members:
"""

# Import global modules
import numpy as np
import logging
import os
import struct
from scipy.io import loadmat
import csv

import Common
from Enums import EnumVariableName
from Config import ConfigStatic


class LoadData:
    """
    Load data from various types of files
    """

    def __init__(self):
        self._log = logging.getLogger(ConfigStatic.logger_name)

    def get_physionet_header_name_for_dat(self, infile):
        path, name_all = os.path.split(infile)
        name, dummy = os.path.splitext(name_all)
        return os.path.join(path, name + ".hea")

    def read_data(self, infile):
        """
        Interface function for reading data
        :param infile: input file dat, mat, hea
        :return:
        """
        dummy, ext = Common.get_filename_and_ext(infile)

        # physionet data files
        if ext == '.dat':
            adata, lheader = self.read_physionet_signal16(infile)
            adata = transform_physionet(adata, lheader)

        elif ext == '.hea':
            lheader, dummy, dummy, dummy = self.read_physionet_header(infile)

            adata = dict()
            adata = transform_physionet(adata, lheader)

        # matlab files
        elif ext == '.mat':
                adata = self.read_matlab_file(infile)
        else:
            raise Exception('Uknown extension={0} of file {1}'.format(ext, infile))

        return adata

    def read_physionet_header(self, infile):
        """
        Read a file header in physionet format

        :param infile: filename to read
        :type infile: string
        :return lheader:
        :rtype lheader: list of dict
        """
        if Common.file_exists(infile) is False:
            raise IOError('File not exists: {0}'.format(infile))

        self._log.info('Loading file {0}'.format(infile))

        f = open(infile, 'r')

        firstline = f.readline()
        a = firstline.split(' ')

        # fileName = a[0]
        nr_signals = int(a[1])
        nfs = int(a[2])
        nrsamples = int(a[3])

        lheader = list()  # save information to a list
        for dummy in range(nr_signals):

            dictheader = dict()
            a = f.readline()
            a = a.split(' ')
            dictheader['name'] = a[0]
            dictheader['format'] = int(a[1])

            # get type of signal (either FHR or UX)
            stype = str(a[8])
            n = len(stype)
            stype = stype[0:n - 1]

            s = a[2]
            if stype == 'FHR':
                idx = s.index('(')
                dictheader['gain'] = int(s[0:idx])
            elif stype == 'UC':
                idx = s.index('/')
                dictheader['gain'] = int(s[0:idx])

            dictheader['bitres'] = int(a[3])
            dictheader['zerovalue'] = int(a[4])
            dictheader['firstvalue'] = int(a[5])
            dictheader['checksum'] = int(a[6])

            dictheader['fs'] = nfs

            lheader.append(dictheader)

        clin_info = dict()
        line = f.readline()
        while line:
            if not line == '\n':
                if not line[1] == '-':
                    param = line[1:13]
                    param = param.strip()
                    param = self.__removeSpecificChar(param)

                    try:
                        if param == 'Sig2Birth':
                            value = self.__parse_number(line[14:len(line)])
                        else:
                            value = self.__parse_number(line[14:-1])
                    except Exception, msg:
                        if param == 'BDecf' or param == 'BE' or param == 'pCO2' or param == 'Gravidity'\
                                or param == 'Weight_g' or param == 'Presentation':
                            value = np.nan
                        else:
                            self._log.error('Parse int error: param: {0}, msg:{1}'.format(param, msg))

                    clin_info[param] = value

            line = f.readline()

        lheader.append(clin_info)
        f.close()
        return lheader, nr_signals, nfs, nrsamples

    def read_physionet_header_for_dat(self, infile):
        """
        Read a physionet header when the name of signal is provided.

        :param infile: filename of signal, which header is desired
        :type infile: string
        :return: list of parameters
        """

        headerfile = self.get_physionet_header_name_for_dat(infile)
        return self.read_physionet_header(headerfile)

    def read_physionet_signal16(self, in_file, l_header=None):
        """ read a signal in physionet format, only format 16 is supported """

        if Common.file_exists(in_file) is False:
            raise IOError('File not exists: {0}'.format(in_file))

        nrsignals = 0
        nrsamples = 0
        if l_header is None:
            # read a header if it was not supplied
            l_header, nrsignals, dummy, nrsamples = self.read_physionet_header_for_dat(in_file)

        fhr_head = l_header[0]
        toco_head = l_header[1]
        if not fhr_head['format'] == 16:
            raise IOError("Error trying to read signal in different format!")

        f = open(in_file, 'rb')
        data_packed = f.read()
        nr = len(data_packed) / 2  # 2 does not mean two signals
        myfmt = 'H' * nr  # H means uint16

        if not nr / 2 == nrsamples:
            self._log.error("Error number of samples incorrect")

        if not len(data_packed) == struct.calcsize(myfmt):
            print len(data_packed)
            print struct.calcsize(myfmt)
            self._log.error("Invalid argument for reading binary file")

        data = struct.unpack(myfmt, data_packed)  # note the ',' in 'value,': unpack apparently returns a n-uple

        # init numpy array
        data_temp = np.zeros((nrsamples, nrsignals + 1), np.float)

        cnt = 0
        for i in range(0, nr, 2):
            data_temp[cnt, 0] = float(data[i]) / fhr_head['gain']
            data_temp[cnt, 1] = float(data[i + 1]) / toco_head['gain']
            data_temp[cnt, 2] = cnt
            cnt += 1

        data_all = dict()
        data_all[EnumVariableName.fhr] = data_temp[:, 0]
        data_all[EnumVariableName.uc] = data_temp[:, 1]
        data_all[EnumVariableName.time_samp] = data_temp[:, 2]
        data_all[EnumVariableName.timestamp] = data_all[EnumVariableName.time_samp]

        return data_all, l_header

    def read_matlab_file(self, sfile):
        """Read a signal in matlab format, for specification of matlab file see :py:class:`EnumVariableName`
        :param sfile: input file
        :type sfile: str
        :return adata: dict of data like FHR, UC, etc
        :rtype dict
        """
        if Common.file_exists(sfile) is False:
            raise IOError('File not exists: {0}'.format(sfile))

        adata = loadmat(sfile)

        # handle the Lyon matfile version
        adata = transform_lyon_format(adata)

        if EnumVariableName.fhr not in adata:
            raise Exception("The variable 'fhr' must be present in the file: {0}".format(sfile))

        if EnumVariableName.uc not in adata:
            raise Exception("The variable 'uc' must be present in the file: {0}".format(sfile))

        if EnumVariableName.timestamp not in adata:
            raise Exception("The variable 'timestamp' must be present in the file: {0}".format(sfile))

        # the adata from matfile were loaded in numpy arrays in a different shape, we want to get rid of it
        datadict = dict()
        assert isinstance(adata, dict)
        n = len(adata[EnumVariableName.fhr])

        for s in adata.keys():
            if not s[0] == '_':  # if the variable is global var.
                t = adata[s]

                # print s
                # print t

                # handling of Lyon database
                if s == 'info':
                    datadict = self.transform_lyon_info(t, n)
                    continue

                if t.dtype == np.int:  # if it is not numpy array
                    continue

                t = np.ravel(t)

                adata[s] = t

                if len(t) == 1:
                    adata[s] = t[0]
                else:
                    adata[s] = t

        # print fhr[:,0]

        for key in datadict.keys():
            adata[key] = datadict[key]

        nrsamples = len(adata[EnumVariableName.fhr])
        adata[EnumVariableName.time_samp] = np.linspace(1, nrsamples, nrsamples)

        if EnumVariableName.fs not in adata:
            raise Exception("The variable 'fs' must be present in the file: {0}".format(sfile))

        return adata

    def read_bdi_txtfile(self, infile):
        """
        load data from txt file (generated from BDI file), the structure of csv is expected as:
        timestamp, fhr, uc (fields: 1, 4, 11)
        :param: infile: input file
        :type: infile: str()
        """
        f = open(infile, 'r')

        # count no_lines: not very elegant...
        nNrSamples = 0
        for dummy in range(0, 11):
            f.next()

        for line in f:
            if not line[:4] == '****':
                nNrSamples += 1

        f.seek(0)
        for dummy in range(0, 11):
            f.next()

        count = 0
        timestamp = np.zeros((nNrSamples, 1), np.int)
        data = np.zeros((nNrSamples, 2), np.float)

        for line in f:
            if not line[:4] == '****':
                row = line.split(',')
                # print row
                timestamp[count] = int(row[0].strip())
                data[count, 0] = float(row[3].strip())
                data[count, 1] = float(row[10].strip())
                if not data[count, 0] == 0.0:
                    data[count, 0] = data[count, 0] / 4;

                #              if count == 1024:
                #                  print data[count,0],data[count,1],timestamp[count]
                count += 1

        aDataAll = dict()
        aDataAll[EnumVariableName.timestamp] = timestamp
        aDataAll[EnumVariableName.fhr] = data[:, 0]
        aDataAll[EnumVariableName.uc] = data[:, 1]

        f.close()

        return aDataAll, 0

    def read_csv_file(self, infile):
        """
        load data from csv file, the structure of csv is expected as:
        timestamp, fhr, uc
        """
        f = open(infile, 'r')

        nrsamples = Common.get_number_lines_in_stream(f)
        filecontent = csv.reader(f, delimiter=',')

        bhasheader = csv.Sniffer().has_header(f.read(1024))
        f.seek(0)  # return to begin

        if bhasheader:
            nrsamples -= 1

        timestamp = np.zeros((nrsamples, 1), np.int)
        data = np.zeros((nrsamples, 2), np.float)
        count = 0

        for row in filecontent:
            # print row
            if count == 0 and bhasheader is True:
                count = 0
                bhasheader = False
                continue

            timestamp[count] = int(row[0])
            data[count, 0] = float(row[1])
            data[count, 1] = float(row[2])
            count += 1

        adataall = dict()
        adataall[EnumVariableName.timestamp] = timestamp
        adataall[EnumVariableName.fhr] = data[:, 0]
        adataall[EnumVariableName.uc] = data[:, 1]

        f.close()

        return adataall, 0

    def write_csv_file(self, infile, data, sheader=None):
        """
        write data into csv file.
        the function is not using the python csv module because of unable to setup float precision
        """

        if isinstance(infile, file):
            f = infile
        else:
            f = open(infile, 'w+')

        # write header
        if sheader is None:
            sheader = '{0},{1},{2}\n'.format(EnumVariableName.timestamp, EnumVariableName.fhr, EnumVariableName.uc)

        f.write(sheader)

        timestamp = data[EnumVariableName.timestamp]
        fhr = data[EnumVariableName.fhr]
        uc = data[EnumVariableName.uc]

        nrsamples = len(timestamp)
        # print nrsamples

        for i in range(0, nrsamples):
            s = '{0},{1},{2}\n'.format(int(timestamp[i]), round(fhr[i], 2), round(uc[i], 2))
            f.write(s)

        if f != infile:
            f.close()

        return data

    def __parse_number(self, svalue=None):

        if svalue.find('.') > 0:
            return float(svalue)
        else:
            return int(svalue)

    def __removeSpecificChar(self, s):

        s = s.replace(' ', '_')
        s = s.replace('.', '')
        s = s.replace('(', '_')
        s = s.replace(')', '')
        s = s.replace('/', '_')

        return s

    def transform_lyon_info(self, cdata, n):
        """
        Transform loaded matlab file into compatible format for CTGViewer

        :param cdata: metainfo from Lyon database
        :param n: length of the FHR data
        :type cdata: loaded matlab structure
        :return: datadict: diconary with clinical information to be displayed
        """
        var_list_in = ['pH', 'BDecf', 'dataLengthOrig_min', 'fs', 'sig2End_min', 'sig2End_samp', 'fileNameMat',
                       'apgar1', 'apgar5', 'stageII_min', 'stageII_samp', 'operativeSFA', 'birthWeight', 'sexM',
                       'resuscitationWard', 'NICU', 'moveToSFA', 'ind_stageII', 'obsolete_ind_stageII']
        var_list_out = ['pH', 'BDecf', 'dataLengthOrig_min', 'fs', 'Sig2Birth', 'sig2End_samp', 'name',
                        'Apgar1', 'Apgar5', 'IIstage', 'Pos_IIst', 'ClinAnnotation', 'Weight_g', 'Sex',
                        'resuscitationWard', 'NICU', 'NICUacidosis', 'ind_stageII','obsolete_ind_stageII']

        datadict = dict()

        for i in range(0, len(var_list_in)):
            s = var_list_in[i]
            sout = var_list_out[i]

            try:
                temp = cdata[s]
                # print '{0},{1}'.format(temp, temp.dtype)
            except Exception:
                self._log.info('Field {0} does not exists in Matlab structure'.format(s))
                datadict[sout] = 0
                continue

            temp = np.ravel(temp[0])
            temp = temp[0].flatten()

            if temp.dtype == np.float:
                datadict[sout] = float(temp)

            elif temp.dtype == np.int or temp.dtype == np.uint8 or temp.dtype == np.uint16:
                datadict[sout] = int(temp)

            else:
                datadict[sout] = str(temp[0])

            # print datadict[sout]

        if 'ind_stageII' in datadict:
            datadict['Pos_IIst'] = datadict['ind_stageII']
        else:

            if 'IIstage' in datadict:
                # fix the position of second stage
                stage2_min = datadict['IIstage']
                sig2end_min = datadict['Sig2Birth']
                fs = datadict['fs']

                if stage2_min <= sig2end_min:
                    datadict['Pos_IIst'] = np.nan
                else:
                    datadict['Pos_IIst'] = n - round(60 * fs * (stage2_min - sig2end_min))

                datadict['Sig2Birth'] = round(datadict['Sig2Birth'], 2)

        return datadict


def transform_physionet(adata, lheader):

    adata['fs'] = lheader[0]['fs']
    val = lheader[0]['name']
    val = val.split('.')
    adata['name'] = str(val[0])

    for key in lheader[2].keys():
        adata[key] = lheader[2][key]

    return adata


def transform_lyon_format(data):
    """
    :param data: loaded matlab file of Lyon database
    :return:
    """

    if EnumVariableName.fhr not in data:
        data[EnumVariableName.fhr] = data['bpm_nan']
        data[EnumVariableName.fhr] = np.ravel(data[EnumVariableName.fhr])

        """
        # posible display of NaN values
        x = data['bpm_nan']
        ind = np.isnan(x)
        x[ind] = 0
        data[EnumVariableName.fhr] = x
        """

        data = save_delete_from_dict(data, 'bpm')
        data = save_delete_from_dict(data, 'bpm_nan')

    # print data[EnumVariableName.fhr]
    # print type(data[EnumVariableName.fhr])
    # print len(data[EnumVariableName.fhr])
    n = len(data[EnumVariableName.fhr])

    if 'uc' not in data:
        data[EnumVariableName.uc] = np.ones(n, np.int)

    if 'timestamp' not in data:
        data[EnumVariableName.timestamp] = np.arange(1, n + 1, 1, np.float64)

    return data


def save_delete_from_dict(d, key):
    if key in d:
        d.pop(key)

    return d


if __name__ == '__main__':
    # file1 = 'files/1001.dat'
    file1 = '/home/jirka/data/CurrentDB_10Hz/matfiles/EHA0020_2005.mat'
    # file1 = '/tmp/tpbea73b7c_79e5_453c_8f1f_14e46e695fd1.mat'
    data_loader = LoadData()
    # data_loader.readPhysionetSignal16(file1)
    # data_loader.readPhysionetHeader(file1)
    # data_loader.read_matlab_file(file1)
    data_loader.read_data(file1)

