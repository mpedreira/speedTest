#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from classes.basics import *
from classes.configuration import *
from classes.httpRequest import *
from classes.logger import *
import json
'''
class jira:
    def getAttribute(self, attribute):
    def getGroupMembers(self, group):
    def getIssue(self):
    def getJiraIDs(self, query):
    def getKeys(self, config):
    def getUserbyEmail(self, email):
    def retrieveJiraIDs(self):
    def setGroupUser(self, name, groupID):
    def setID(self, jiraID):
    def setIssue(self, data):
    def setUser(self, user):
    def setUserID(email, data):
    def setcommentIssue(self, data):
    def updateIssue(self, data):
'''


class jira:
    def __init__(self, config):
        self.config = config
        self.jira = {}
        self.jira['endpoint'] = self.config.setConfigAttributes('JIRA')
        self.jira['query'] = self.config.setConfigAttributes('JIRAQUERYS')
        self.log = logger(self.config, __name__)
        self.jiraID = None

    def getAttribute(self, attribute):
        if ('fields' in self.data.keys()):
            return self.data[attribute]
        return []

    def __writeDebugResponse__(self, obj):
        if not (self.jiraID):
            return False
        debug = self.config.getDebugFolder() + self.jiraID + '-' + str(
            self.config.getExecutionTime()) + '.html'
        if (self.config.isDebug() and not obj.isOKResponse()):
            data = obj.response.text
            writeDebug(debug, data)
        return True

    def getKeys(self, config):
        attributes = {}
        for attribute in config.keys():
            attributes[attribute] = config[attribute]
        return attributes

    def getIssue(self):
        endpoint = {}
        payload = {}
        endpoint['uri'] = self.jira['endpoint']['baseurl'] + self.jira[
            'endpoint']['issue'] + self.jiraID
        endpoint['certificate'] = self.jira['endpoint']['certificate']
        payload['data'] = ''
        payload['auth'] = self.config.getBasicAuth()
        payload['config'] = self.config
        payload['headers'] = None
        obj = httpRequest(endpoint, payload)
        obj.getRequest()
        self.data = obj.getJSONResponse()
        if (obj.isOKResponse()):
            self.log.setDebug('Got information from ' + self.jiraID)
            return True
        else:
            self.log.setError('Error Retrieving ' + self.jiraID)
            return False

    def setGroupUser(self, name, groupID):
        endpoint = {}
        payload = {}
        endpoint['uri'] = self.jira['endpoint']['baseurl'] + self.jsd[
            'endpoint']['add_group'] + groupID
        endpoint['certificate'] = self.jira['endpoints']['certificate']
        payload['data'] = '{"name": "' + name + '"}'
        payload['auth'] = self.config.getBasicAuth()
        payload['headers'] = {'Content-Type': 'application/json'}
        payload['config'] = self.config
        obj = httpRequest(endpoint, payload)
        return obj.postRequest()

    def getGroupMembers(self, group):
        endpoint = {}
        users = []
        payload = {}
        endpoint['uri'] = self.jira['endpoint']['baseurl'] + self.jsd[
            'endpoint']['add_group'] + group
        endpoint['certificate'] = self.jira['endpoint']['certificate']
        payload['headers'] = ''
        payload['data'] = ''
        payload['config'] = self.config
        payload['auth'] = self.config.getBasicAuth()
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

    def getUserbyEmail(self, email):
        endpoint = {}
        payload = {}
        endpoint['uri'] = self.jira['endpoint']['baseurl'] + self.jsd[
            'endpoint']['user'] + email
        endpoint['certificate'] = self.jira['endpoint']['certificate']
        payload['headers'] = ''
        payload['data'] = ''
        payload['auth'] = self.config.getBasicAuth()
        payload['config'] = self.config
        obj = httpRequest(endpoint, payload)
        obj.getRequest()
        self.data = obj.getJSONResponse()
        userID = self.setUserID(email, self.data['data'])
        return userID

    def setUser(self, user):
        directoryID = '3'
        endpoint = {}
        payload = {}
        endpoint['uri'] = self.jira['endpoint']['baseurl'] + self.jsd[
            'endpoint']['user']
        endpoint['certificate'] = self.jira['endpoints']['certificate']
        payload['data'] = '{"name": "' + user['login'] + '", "password": "' + user[
            'password'] + '", "emailAddress": "' + user[
                'email'] + '", "displayName": "' + user[
                    'name'] + '", "directoryID": "' + directoryID + '", "applicationKeys": ' + user[
                        'permissions'] + '}'
        payload['headers'] = {'Content-Type': 'application/json'}
        payload['auth'] = self.config.getBasicAuth()
        payload['config'] = self.config
        obj = httpRequest(endpoint, payload)
        return obj.postRequest()

    def getJiraIDs(self, query):
        endpoint = {}
        payload = {}
        endpoint['uri'] = self.jira['endpoint']['baseurl'] + self.jira[
            'endpoint']['search'] + query
        endpoint['certificate'] = self.jira['endpoint']['certificate']
        payload['headers'] = ''
        payload['data'] = ''
        payload['auth'] = self.config.getBasicAuth()
        payload['config'] = self.config
        obj = httpRequest(endpoint, payload)
        obj.getRequest()
        self.data = obj.getJSONResponse()
        jiraIDs = self.retrieveJiraIDs()
        self.log.setDebug('Retrieved ' + str(jiraIDs))
        return jiraIDs

    def retrieveJiraIDs(self):
        result = {'Total': self.data['total'], 'ids': []}
        for i in self.data['issues']:
            result['ids'].append(i['key'])
        return result

    def setID(self, jiraID):
        self.jiraID = jiraID
        self.getIssue()

    def getFields(self, fields):
        data = {}
        data['fields'] = {}
        for key in fields:
            data['fields'][fields[key]] = self.data['fields'][fields[key]]
        return data

    def updateIssue(self, data):
        endpoint = {}
        payload = {}
        endpoint['uri'] = self.jira['endpoint']['baseurl'] + self.jira[
            'endpoint']['issue'] + self.jiraID
        endpoint['certificate'] = self.jira['endpoint']['certificate']
        payload['headers'] = {'Content-Type': 'application/json'}
        payload['data'] = data
        payload['auth'] = self.config.getBasicAuth()
        payload['config'] = self.config
        obj = httpRequest(endpoint, payload)
        obj.putRequest()
        if (obj.isOKResponse()):
            self.log.setDebug('Actualizada en JIRA la issue ' + self.jiraID)
            return True
        self.__writeDebugResponse__(obj)
        self.log.setError('Error actualizando en JIRA la issue ' + self.jiraID)
        return False

    def transitionIssue(self, data):
        endpoint = {}
        payload = {}
        endpoint['uri'] = self.jira['endpoint']['baseurl'] + self.jira[
            'endpoint']['issue'] + self.jiraID + '/transitions'
        endpoint['certificate'] = self.jira['endpoint']['certificate']
        payload['headers'] = {'Content-Type': 'application/json'}
        payload['data'] = json.dumps(data)
        payload['auth'] = self.config.getBasicAuth()
        payload['config'] = self.config
        obj = httpRequest(endpoint, payload)
        obj.postRequest()
        if (obj.isOKResponse()):
            self.log.setDebug('Actualizada en JIRA la issue' + self.jiraID)
            return True
        self.__writeDebugResponse__(obj)
        self.log.setError('Error actualizando en JIRA la issue' + self.jiraID)
        return False

    def __hasMoreUsers__(self, json):
        if ('next' in json['_links'].keys()):
            return True
        return False

    def setUserID(email, data):
        EMPTY = ''
        for user in data:
            if (user["email"] == email):
                return email["id"]
        return EMPTY

    def setcommentIssue(self, data):
        endpoint = {}
        payload = {}
        endpoint['uri'] = self.jira['endpoint']['baseurl'] + self.jira[
            'endpoint']['issue'] + self.jiraID + '/comment'
        endpoint['certificate'] = self.jira['endpoint']['certificate']
        payload['auth'] = self.config.getBasicAuth()
        payload['headers'] = {'Content-Type': 'application/json'}
        payload['data'] = data
        payload['config'] = self.config
        obj = httpRequest(endpoint, payload)
        obj.postRequest()
        if (obj.isOKResponse()):
            self.log.setDebug('Añadido comentario en JIRA  a la issue' +
                              self.jiraID)
            return True
        self.__writeDebugResponse__(obj.response.text)
        self.log.setError('Error añadiendo en JIRA el comentario a la issue' +
                          self.jiraID)
        return False

    def setIssue(self, data):
        endpoint = {}
        payload = {}
        endpoint['uri'] = self.jira['endpoint']['baseurl'] + self.jira[
            'endpoint']['issue']
        endpoint['certificate'] = self.jira['endpoint']['certificate']
        payload['auth'] = self.config.getBasicAuth()
        payload['headers'] = {'Content-Type': 'application/json'}
        payload['data'] = json.dumps(data)
        payload['config'] = self.config
        obj = httpRequest(endpoint, payload)
        obj.postRequest()
        if (obj.isOKResponse()):
            data = obj.getJSONResponse()
            self.log.setDebug('Añadido JIRA issue' + data['key'])
            return data['key']
        self.log.setError(obj.response.text)
        self.log.setError('Error añadiendo el JIRA')
        return ''
