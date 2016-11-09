# -*- coding: utf-8 -*-
#
# Created on Oct 15, 2013
# @author: Jiri Spilka
# http://people.ciirc.cvut.cz/~spilkjir
# @2015, CIIRC, Czech Technical University in Prague
#
# Licensed under the terms of the GNU GENERAL PUBLIC LICENSE
# (see CTGViewer.py for details)

from os.path import expanduser, join
from datetime import datetime
import logging

import ConfigParser
from Enums import EnumPaperFormat, EnumIniVar, EnumAnnType


class ConfigIni:

    def __init__(self):

        self.__ini_var_section = dict()
        self.__ini_var_section[EnumIniVar.lastUsedDirFiles] = 'Directories'
        self.__ini_var_section[EnumIniVar.dataBrowserSelectedAttributes] = 'GUI'
        self.__ini_var_section[EnumIniVar.paperformat] = 'GUI'
        self.__ini_var_section[EnumIniVar.annotationToolbarAlignR] = 'GUI'
        self.__ini_var_section[EnumIniVar.caliperVisible] = 'GUI'
        self.__ini_var_section[EnumIniVar.caliperFHR] = 'GUI'
        self.__ini_var_section[EnumIniVar.caliperTOCO] = 'GUI'
        self.__ini_var_section[EnumIniVar.windowGeometry] = 'Geometry'
        self.__ini_var_section[EnumIniVar.windowState] = 'Geometry'

        self.__ini_defaults = dict()
        self.__ini_defaults[EnumIniVar.lastUsedDirFiles] = ' '
        # self.__ini_defaults[EnumIniVar.dataBrowserSelectedAttributes] = 'pH, BDecf'
        self.__ini_defaults[EnumIniVar.dataBrowserSelectedAttributes] = ''
        self.__ini_defaults[EnumIniVar.paperformat] = EnumPaperFormat.US
        self.__ini_defaults[EnumIniVar.annotationToolbarAlignR] = True
        self.__ini_defaults[EnumIniVar.caliperVisible] = True
        self.__ini_defaults[EnumIniVar.caliperFHR] = True
        self.__ini_defaults[EnumIniVar.caliperTOCO] = True
        self.__ini_defaults[EnumIniVar.windowGeometry] = ''
        self.__ini_defaults[EnumIniVar.windowState] = ''

        self._ini_var = dict()

        self._configParser = ConfigParser.ConfigParser()

        self._log = logging.getLogger(ConfigStatic.logger_name)

        # self.dirLastUsed = ''
        # self.dockClinInfoVisible = 0
        # self.dataBrowserSelectedAttributes = ''

        # self._lSections = ['Directories','GUI']

        # self.__ensure_settings_ini()
        self.read_config()

    # def __ensure_settings_ini(self):
    #     default_ini = 'default.ini'
    #     app_path = Common.get_application_path()
    #     file2copy = os.path.join(app_path, default_ini)
    #     if not Common.file_exists(ConfigStatic.setting_file):
    #         shutil.copy(file2copy, ConfigStatic.setting_file)
    #         self._log.info("ConfigStatic file not exists, copy from application path")

    def read_config(self, ini_file=None):

        if ini_file is None:
            ini_file = ConfigStatic.setting_file

        self._log.info("reading config file {0}".format(ini_file))
        # if not Common.file_exists(ini_file):
        #    return

        self._configParser.read(ConfigStatic.setting_file)

        for key in self.__ini_var_section:

            if key == EnumIniVar.dockClinInfoVisible or key == EnumIniVar.dockDataBrowseVisible \
                    or key == EnumIniVar.annotationToolbar or key == EnumIniVar.annotationToolbarAlignR \
                    or key == EnumIniVar.caliperVisible or key == EnumIniVar.caliperFHR \
                    or key == EnumIniVar.caliperTOCO:
                p_get = self._configParser.getboolean
            else:
                p_get = self._configParser.get

            try:
                self._ini_var[key] = p_get(self.__ini_var_section[key], key)
            except:
                self._ini_var[key] = self.__ini_defaults[key]

        self.attr_remove_apostroph_white_space()

        # try:
        #    self.dirLastUsed = self._configParser.get('DEFAULT', 'lastUsedDirFiles')
        #    #self.dirLastUsed = self._configParser.get('Directories', 'lastUsedDirFiles')
        #    self.dockClinInfoVisible = self._configParser.getboolean('GUI', 'dockClinInfoVisible')
        #    self.dataBrowserSelectedAttributes = self._configParser.get('GUI', 'dataBrowserSelectedAttributes')
        #    self.attributesRemoveApostrophsAndWhiteSpaces()
        # except Exception, e:
        #    pass
        #    #raise Exception('Error when reading config file {0}, message:{1}'.format(ini_file,e))

    def attr_remove_apostroph_white_space(self):

        temp = self.get_var(EnumIniVar.dataBrowserSelectedAttributes)
        temp = temp.split(',')

        # remove apostrophes and whitespaces
        cnt = 0
        for dummy in temp:
            temp[cnt] = (str(temp[cnt].replace("'", ""))).strip()
            cnt += 1

        self.set_var(EnumIniVar.dataBrowserSelectedAttributes, temp)

    def write_config(self):
        # lets create that config file for next time...
        cfgf = open(ConfigStatic.setting_file, 'w+')

        # add the settings to the structure of the file, and lets write it out...
        # for l in self._lSections:
        #     try:
        #         self._configParser.add_section(l)
        #     except Exception,msg:
        #         self._log.info("A section exist {0}".format(msg))
        for key in self.__ini_var_section:
            try:
                self._configParser.add_section(self.__ini_var_section[key])
            except Exception, msg:
                self._log.info("A section exist {0}".format(msg))

            temp = self.get_var(key)

            if key == EnumIniVar.dataBrowserSelectedAttributes:
                # print type(temp)
                if type(temp) == list:
                    temp = str(temp).strip('[]')

                # print type(temp)

            self._configParser.set(self.__ini_var_section[key], key, temp)

        # self._configParser.set('GUI', 'dataBrowserSelectedAttributes', ','.join(self.dataBrowserSelectedAttributes))
        # self._configParser.set('Directories', 'lastUsedDirFiles', self.dirLastUsed)

        self._configParser.write(cfgf)
        cfgf.close()

        self._log.info("Ini file has been written successfully")

    def get_var(self, name):
        try:
            value = self._ini_var[name]
        except Exception, e:
            raise Exception('Error - value {0} not in settings ini, message:{1}'.format(name, e))

        return value

    def set_var(self, name, value):
        try:
            self._ini_var[name] = value
        except Exception, e:
            raise Exception('Error - value {0} not in settings ini, message:{1}'.format(name, e))


class ConfigStatic:

    def __init__(self):
        pass

    _configParser = ConfigParser.ConfigParser()

    user_directory = expanduser("~/.CTGViewer")

    # logging
    logging_level = logging.ERROR
    logger_name = 'CTGViewer'
    log_path = join(user_directory, 'logs')
    log_name = 'log_' + datetime.today().strftime("%Y-%m-%d_%H-%M-%S") + '.log'
    log_file = join(log_path, log_name)

    # temp directory
    temp_data = join(user_directory, 'temp_data')

    # date time format
    date_format = '%d.%m.%Y'
    time_format = '%H:%M:%S:%f'

    setting_file = join(user_directory, 'settings.ini')

    navigation_plot_downsample_fs = 2
    plot_toco_offset = int(50)
