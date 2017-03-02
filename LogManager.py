#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging as log
import os


class LogManager(object):

    """Docstring for LogManager. """

    def __init__(self, log_path, file_name):
        """TODO: to be defined1. """
        self.__log_path = log_path
        self.__file_name = file_name

        # Cria o diretório de log caso ele não exista
        if not os.path.exists(self.__log_path):
            os.makedirs(self.__log_path)
        log_format = "[%(asctime)s] [%(levelname)s] : %(message)s"
        logFormatter = log.Formatter(log_format,
                                     datefmt='%d-%m-%Y %H:%M:%S'
                                     )
        self.__rootLogger = log.getLogger()
        self.__rootLogger.setLevel(log.INFO)

        fileHandler = log.FileHandler(("{0}/{1}.log"
                                       .format(self.__log_path,
                                               self.__file_name)
                                       )
                                      )
        fileHandler.setFormatter(logFormatter)
        self.__rootLogger.addHandler(fileHandler)

        consoleHandler = log.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        self.__rootLogger.addHandler(consoleHandler)

    def log_info(self, message):
        """TODO: Docstring for show_info.
        :returns: TODO

        """
        log.info(message)

    def log_error(self, message):
        """TODO: Docstring for error.

        :arg1: TODO
        :returns: TODO

        """
        log.error(message)
