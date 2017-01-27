# -*- coding: utf-8 -*-
#
# Created on Oct 15, 2013
# @authors: Jiri Spilka
# http://people.ciirc.cvut.cz/~spilkjir
# @2015, CIIRC, Czech Technical University in Prague
#
# Licensed under the terms of the GNU GENERAL PUBLIC LICENSE
# (see CTGViewer.py for details)

import logging
from Config import ConfigStatic


class Logger:
    """
    Class for logging
    """

    def __init__(self, logger_name):

        LOG_LEVEL = ConfigStatic.logging_level
        """
        self.my_logger = logging.getLogger('Logger')
        self.my_logger = logging.basicConfig(filename=LOG_FILENAME,level=LOG_LEVEL,filemode = 'w')
        """

        # create logger
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(LOG_LEVEL)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(LOG_LEVEL)

        fh = logging.FileHandler(ConfigStatic.log_file, 'a')

        # create formatter
        formatter = logging.Formatter("%(levelname)-8s: %(filename)-16s: %(funcName)-12s: %(lineno)d: msg = %(message)s")

        # add formatter to ch
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        # add ch to logger
        self.logger.addHandler(ch)
        self.logger.addHandler(fh)

        # "application" code
        """
        self.logger.debug("debug message")
        self.logger.info("info message")
        self.logger.warn("warn message")
        self.logger.error("error message")
        self.logger.critical("critical message")
        """





