#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import inspect


class logger:
    def __init__(self, config, application):
        self.setDebugLevel(config.getDebugLevel())
        self.application = application
        self.logger = logging.getLogger(self.application)
        self.logger.setLevel(self.level)
        self.fileHandler = logging.FileHandler(config.getDebugFile())
        self.consoleHandler = logging.StreamHandler()
        self.consoleHandler.setLevel(config.consoleLevel)
        self.__setFormat__()
        self.logger.addHandler(self.fileHandler)
        self.logger.addHandler(self.consoleHandler)

    def __isDebug__(self, debug):
        if (debug == 'DEBUG'):
            return True
        return False

    def __isError__(self, debug):
        if (debug == 'ERROR'):
            return True
        return False

    def __isInfo__(self, debug):
        if (debug == 'INFO'):
            return True
        return False

    def __isWarning__(self, debug):
        if (debug == 'WARNING'):
            return True
        return False

    def setDebugLevel(self, debug):
        if (self.__isDebug__(debug)):
            self.level = logging.DEBUG
            return True
        if (self.__isInfo__(debug)):
            self.level = logging.INFO
            return True
        if (self.__isWarning__(debug)):
            self.level = logging.WARNING
            return True
        if (self.__isError__(debug)):
            self.level = logging.ERROR
            return True
        return False

    def __setFormat__(self):
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
        # create formatter and add it to the handlers
        self.fileHandler.setFormatter(self.formatter)
        self.consoleHandler.setFormatter(self.formatter)

    def setDebug(self, data):
        caller = self.__getCaller__()
        self.logger.debug(caller + ' - ' + data)

    def setError(self, data):
        caller = self.__getCaller__()
        self.logger.error(caller + ' - ' + data)

    def setInfo(self, data):
        caller = self.__getCaller__()
        self.logger.info(caller + ' - ' + data)

    def setWarning(self, data):
        caller = self.__getCaller__()
        self.logger.warning(caller + ' - ' + data)

    def __getCaller__(self):
        currentFrame = inspect.currentframe()
        callerFrame = inspect.getouterframes(currentFrame, 2)
        return callerFrame[2][3]
