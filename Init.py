# -*- coding: utf-8 -*-
#
# Created on Oct 15, 2013
# @authors: Jiri Spilka
# http://people.ciirc.cvut.cz/~spilkjir
# @2015, CIIRC, Czech Technical University in Prague
#
# Licensed under the terms of the GNU GENERAL PUBLIC LICENSE
# (see CTGViewerLite.py for details)

import Common
from Config import ConfigStatic
import os
import shutil
from Logger import Logger


def init():
    __create_dirs()
    Logger(ConfigStatic.logger_name)
    # __copy_setting_ini()


def __create_dirs():
    # init dirs - create directories if not exist
    Common.ensure_dir(ConfigStatic.user_directory)
    Common.ensure_dir(ConfigStatic.log_path)
    Common.ensure_dir(ConfigStatic.temp_data)


def __copy_files():
    app_path = Common.get_application_path()
    head, dummy = os.path.split(app_path)
    dir_files = os.path.join(head, 'files')
    files = Common.directory_listing(dir_files)

    for f in files:
        if not (f.endswith('svn-base') or f.endswith('entries') or f.endswith('~')):
            dummy, file_name = os.path.split(f)
            file_name = os.path.join(ConfigStatic.user_directory, file_name)
            if not Common.file_exists(file_name):
                shutil.copy(f, ConfigStatic.user_directory)


if __name__ == '__main__':
    init()
