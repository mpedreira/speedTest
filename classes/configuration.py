#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from classes.basics import *
from getpass import getpass
from requests.auth import HTTPBasicAuth
import argparse
import configparser
import datetime
import msal
import logging

CONFIGFILE = ''
'''
class configuration:
    def getBasicAuth(self):
    def getClientID(self):
    def getClientSecret(self):
    def getConfigfile(self):
    def getConfigfile(self):
    def getDebugFile(self):
    def getDebugFolder(self):
    def getDebugLevel(self):
    def getExecutionTime(self):
    def getJiraID(self):
    def getKeys(self):
    def getPassword(self):
    def getToken(self, product):
    def getUsername(self):
    def hasJiraID(self):
    def isDebug(self):
    def setClientID(self, clientID):
    def setClientSecret(self, clientSecret):
    def setConfigAttributes(self, section):
    def setToken(self, product, token):
'''


class configuration:
    def __init__(self):
        self.args = {}
        self.endpoints = {}
        self.user = {}
        self.user['token'] = {}
        self.TIMESTAMP = datetime.datetime.today().strftime('%s')

    def __getBasicAuth__(self):
        self.user['basicAuth'] = HTTPBasicAuth(self.user['username'],
                                               self.user['password'])

    def __setDebug__(self, args):
        if args.debug:
            return args.debug
        else:
            return 'INFO'

    def setClientID(self, clientID):
        self.user['oAuthclientID'] = clientID

    def setClientSecret(self, clientSecret):
        self.user['oAuthclientSecret'] = clientSecret

    def getClientID(self):
        return self.user['oAuthclientID']

    def getClientSecret(self):
        return self.user['oAuthclientSecret']

    def __setConsoleDebug__(self, consolelevel):
        if consolelevel == 'INFO':
            self.consoleLevel = logging.INFO
            return
        if consolelevel == 'DEBUG':
            self.consoleLevel = logging.DEBUG
            return
        if consolelevel == 'WARNING':
            self.consoleLevel = logging.WARNING
            return
        self.consoleLevel = logging.ERROR

    def __setPassword__(self, args):
        if args.password:
            self.user['password'] = args.password
        else:
            self.user['password'] = getpass()

    def setToken(self, product, token):
        self.user['token'][product] = token
        return True

    def __setVerbose__(self, args):
        if args.verbose:
            return args.verbose
        else:
            return 'ERROR'

    def hasJiraID(self):
        if (self.args['jiraID']):
            return True
        else:
            return False

    def getConfigfile(self):
        return self.configfile

    def getDebugFile(self):
        return self.debugfile

    def getDebugFolder(self):
        return self.debugFolder

    def getExecutionTime(self):
        return self.TIMESTAMP

    def getDebugLevel(self):
        return self.args['debugLevel']

    def getBasicAuth(self):
        return self.user['basicAuth']

    def getJiraID(self):
        return self.args['jiraID']

    def getKeys(self):
        return self.keys()

    def getUsername(self):
        return self.user['username']

    def getPassword(self):
        return self.user['password']

    def getToken(self, product):
        return self.user['token'][product]

    def __setConfigFile__(self, configfile):
        if configfile:
            self.configfile = configfile

    def isDebug(self):
        if self.args['verbose']:
            return True
        else:
            return False

    def setConfigAttributes(self, section):
        config = configparser.RawConfigParser()
        config.read(self.getConfigfile())
        self.args[section] = config[section]
        return self.args[section]

    def setConfigFile(self, configFile):
        if (configFile):
            self.__setConfigFile__(configFile)
        else:
            self.__setConfigFile__(CONFIGFILE)

    def getEMail(self):
        return self.user['email']

    def setEMail(self, email):
        self.user['email'] = email
        return True

    def getApplicationToken(self, resource):
        authority = self.teams['basics']['oauth_uri'] + self.teams['basics'][
            'tenant_id']
        clientID = self.teams['basics']['client_id']
        clientSecret = self.teams['basics']['client_secret']
        self.token = msal.ConfidentialClientApplication(
            clientID,
            client_credential=clientSecret,
            authority=authority,
        ).acquire_token_for_client([resource])
        return self.token['access_token']

    def getUserToken(self, resource):
        clientID = self.teams['basics']['client_id']
        authority = self.teams['basics']['oauth_uri'] + self.teams['basics'][
            'tenant_id']
        user = self.getEMail()
        password = self.getPassword()
        user = 'srvcSMOTeamsIntAX@inditex.com'
        password = 'atOWm@iEn9eOagK'
        self.token = msal.PublicClientApplication(
            clientID, authority=authority).acquire_token_by_username_password(
                user, password, [resource])
        return self.token['access_token']
