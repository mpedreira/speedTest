#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from classes.configuration import *

# CONSTANTES
CONFIGFILE = 'config/PRO-SpeedTest.ini'


class configurationSpeedTest(configuration):
    def __init__(self):
        configuration.__init__(self)
        self.teams = {}
        args = self.__parseArgs__()
        self.setConfigFile(args.configFile)
        logs = self.setConfigAttributes('LOGGING')
        self.debugFolder = logs['debugfolder']
        self.debugfile = self.debugFolder + logs['debugfile']
        consolelevel = logs['console_level']
        self.__setConsoleDebug__(consolelevel)
        self.args['debugLevel'] = self.__setDebug__(args)
        self.args['verbose'] = self.__setVerbose__(args)
        if not args.jiraID:
            self.args['jiraID'] = ''

    def __parseArgs__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-j', '--jiraID', help='Is the Jira ID you want to work with')
        parser.add_argument(
            '-d',
            '--debug',
            choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
            help='Debug level in logFile'
        )
        parser.add_argument('-c', '--configFile', help='ConfigFile Path')
        parser.add_argument(
            '-v',
            '--verbose',
            help='Saves the output of the failed interventions',
            action='store_true'
        )
        return parser.parse_args()

    def setConfigFile(self, configFile):
        if (configFile):
            self.__setConfigFile__(configFile)
        else:
            self.__setConfigFile__(CONFIGFILE)
