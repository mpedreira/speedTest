#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from classes.jira import *
'''
class jsd(configuration):
    def getAttribute(self, attribute):
    def getGroupMembers(self, group):
    def getIssue(self):
    def getJiraIDs(self, query):
    def getKeys(self, config):
    def getOrganizationID(self, org):
    def getUserbyEmail(self, email):
    def getUsersinaOrganization(self, org):
    def listOrganizations(self):
    def retrieveJiraIDs(self):
    def setGroupUser(self, name, groupID):
    def setID(self, jiraID):
    def setOrgID(org, data):
    def setOrganizationtoUser(self, userID, orgID):
    def setUser(self, user):
    def setUserID(email, data):
    def setcommentIssue(self, data):
    def updateIssue(self, data):
'''


class jsd(jira):
    def __init__(self, config):
        jira.__init__(self, config)
        self.jsd = {}
        self.jsd['endpoint'] = self.config.setConfigAttributes('JSD')
        self.jsd['query'] = self.config.setConfigAttributes('JSDQUERYS')
        self.log = logger(self.config, __name__)

    def listOrganizations(self):
        endpoint = {}
        payload = {}
        endpoint['uri'] = self.jira['endpoint']['baseurl'] + self.jsd[
            'endpoint']['organization']
        endpoint['certificate'] = self.jira['endpoint']['certificate']
        payload['headers'] = {
            'X-ExperimentalApi': 'opt-in',
            'Content-Type': 'application/json'
        }
        payload['data'] = ''
        payload['config'] = self.config
        obj = httpRequest(endpoint, payload)
        obj.getRequest()
        self.data = obj.getJSONResponse()
        orgs = self.data['data']
        while (self.__hasMoreUsers__(json)):
            endpoint['uri'] = json['_links']['next']
            obj = httpRequest(endpoint, payload)
            obj.getRequest()
            json = obj.getJSONResponse()
            orgs = orgs + json['data']
        self.log.setInfo('Got ' + str(len(orgs)) + ' orgs')
        self.jsd['orgs'] = orgs
        return orgs

    def getUsersinaOrganization(self, org):
        users = []
        endpoint = {}
        payload = {}
        endpoint['uri'] = self.jira['endpoint']['baseurl'] + self.jsd[
            'endpoint']['organization'] + '/' + str(org) + "/user"
        endpoint['certificate'] = self.jira['endpoint']['certificate']
        payload['headers'] = {
            'X-ExperimentalApi': 'opt-in',
            'Content-Type': 'application/json'
        }
        payload['data'] = ''
        payload['config'] = self.config
        obj = httpRequest(endpoint, payload)
        obj.getRequest()
        self.data = obj.getJSONResponse()
        users = self.data['values']
        while (self.__hasMoreUsers__(json)):
            endpoint['uri'] = json['_links']['next']
            obj = httpRequest(endpoint, payload)
            obj.getRequest()
            json = obj.getJSONResponse()
            users = users + json['values']
        self.log.setInfo('Got ' + str(len(users)) + ' users')
        return users

    def setOrganizationtoUser(self, userID, orgID):
        endpoint = {}
        payload = {}
        users = []
        endpoint['uri'] = self.jira['endpoint']['baseurl'] + self.jsd[
            'endpoint']['organization'] + '/' + str(orgID) + "/user"
        endpoint['certificate'] = self.jira['endpoints']['certificate']
        payload['data'] = '{"usernames": ["' + userID + '"]}'
        payload['headers'] = {
            'X-ExperimentalApi': 'opt-in',
            'Content-Type': 'application/json'
        }
        payload['config'] = self.config
        obj = httpRequest(endpoint, payload)
        return obj.postRequest()

    def getOrganizationID(self, org):
        orgID = ''
        endpoint = {}
        payload = {}
        endpoint['uri'] = self.jira['endpoint']['baseurl'] + self.jsd[
            'endpoint']['organization'] + '/' + str(org) + "/user"
        endpoint['certificate'] = self.jira['endpoint']['certificate']
        payload['headers'] = {
            'X-ExperimentalApi': 'opt-in',
            'Content-Type': 'application/json'
        }
        payload['data'] = ''
        payload['auth'] = self.config.getBasicAuth()
        payload['config'] = self.config
        obj = httpRequest(endpoint, payload)
        obj.getRequest()
        self.data = obj.getJSONResponse()
        orgID = self.setOrgID(org, self.data['data'])
        if (orgID):
            return orgID
        while (self.__hasMoreUsers__(json)):
            endpoint['uri'] = json['_links']['next']
            obj = httpRequest(endpoint, payload)
            obj.getRequest()
            json = obj.getJSONResponse()
            orgID = self.setOrgID(self.data['data'])
            if (orgID):
                return orgID
        return orgID

    def setOrgID(org, data):
        EMPTY = ''
        for organization in data:
            if (organization["name"] == org):
                return organization["id"]
        return EMPTY
