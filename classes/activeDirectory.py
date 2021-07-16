#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from classes.basics import *
from classes.configuration import *
from classes.httpRequest import *
from classes.logger import *
import ldap
'''
 class activeDirectory:
    def connect(self):
    def disconnect(self):
    def getAttributte(self, attribute):
    def getQuery(self, base, query):
    def getcurrentRow(self):
    def setFirstRow(self):
    def setNextRow(self):
'''


class activeDirectory:
    def __init__(self, config):
        self.query = {}
        self.ldap = {}
        self.config = config
        self.log = logger(self.config, __name__)
        self.log.setDebug('Got information from LDAP_DEFAULTS')
        self.ldap['basics'] = self.config.setConfigAttributes('LDAP')
        self.log.setDebug('Got information from LDAP_ENDPOINTS')
        self.ldap['endpoints'] = self.config.setConfigAttributes(
            'LDAP_ENDPOINTS')
        uri = 'ldaps://' + self.ldap['basics']['server'] + ':' + str(
            self.ldap['basics']['port'])
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
        self.connection = ldap.initialize(uri)

    def __UserHasDomain__(self):
        user = self.config.getUsername()
        if (user.find('\\') > 0):
            return True
        return False

    def __setUsername__(self):
        if (self.__UserHasDomain__()):
            return self.config.getUsername()
        return self.ldap['basics']['domain'] + '\\' + self.config.getUsername()

    def connect(self):
        self.connection.set_option(ldap.OPT_REFERRALS, 0)
        self.connection.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
        self.connection.set_option(ldap.OPT_X_TLS, ldap.OPT_X_TLS_DEMAND)
        self.connection.set_option(ldap.OPT_X_TLS_DEMAND, True)
        self.connection.set_option(ldap.OPT_DEBUG_LEVEL, 255)
        self.connection.simple_bind_s(self.__setUsername__(),
                                      self.config.getPassword())

    def disconnect(self):
        self.connection.unbind_ext_s()
        return True

    def getQuery(self, base, query):
        self.result = self.connection.search_s(base, ldap.SCOPE_SUBTREE, query)
        self.setFirstRow()
        return self.result

    def setFirstRow(self):
        self.row = 0

    def setNextRow(self):
        if (self.__hasMoreRows__()):
            return False
        self.row = self.row + 1
        return True

    def __hasMoreRows__(self):
        if (len(self.result) <= self.row()):
            return False
        return True

    def getcurrentRow(self):
        return self.result[self.row]

    def getAttributte(self, attribute):
        EMPTY = [b'']
        data = self.getcurrentRow()
        if (attribute in data[1].keys()):
            return data[1][attribute]
        return EMPTY
