#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
class Teams:
    def getChannels(self, teamID) #App
    def getGroupEvents(self, GroupID) #User
    def getGroups(self) #App
    def getGroupsCalendars(self, GroupID) #User
    def getMembers(self, teamID) #App
    def getUser(self, userPrincipalName) #App
    def getUserCalendars(self, UserID) #User
    def setEvent(self, teamID, data) #App
    def setMember(self, teamID, data) #App
    def setMessage(self, teamID, channelID, data) #User
    def setOnlineMeeting(self, data) #App
    def setReply(self, teamID, channelID, messageID, data) #User
'''

from classes.basics import *
from classes.configuration import *
from classes.httpRequest import *
from classes.logger import *
import json


class Teams:
    def __init__(self, config):
        self.query = {}
        self.config = config
        self.log = logger(self.config, __name__)
        self.teams = {}
        self.log.setDebug('Got information from TEAMS')
        self.teams['basics'] = self.config.setConfigAttributes('TEAMS')
        self.log.setDebug('Got information from TEAMS_ENDPOINTS')
        self.teams['endpoints'] = self.config.setConfigAttributes(
            'TEAMS_ENDPOINTS')
        self.config.setClientID(self.teams['basics']['client_id'])
        self.config.setClientSecret(self.teams['basics']['client_secret'])

    def getGroups(self):
        resource = self.teams['basics']['resource']
        payload = {}
        endpoint = {}
        endpoint['uri'] = self.teams['basics']['graph_uri'] + self.teams[
            'endpoints']['groups']
        endpoint['certificate'] = False
        payload['auth'] = None
        payload['data'] = ''
        payload['headers'] = {
            "Authorization": "Bearer " + self.config.getUserToken(resource),
            "Content-Type": "application/json"
        }
        payload['config'] = self.config
        obj = httpRequest(endpoint, payload)
        if not (obj.getRequest()):
            self.log.setError('The server response is ' + obj.response.text)
            return []
        json = obj.getJSONResponse()
        groups = json['value']
        while (self.__hasMoreUsers__(json)):
            endpoint['uri'] = json['@odata.nextLink']
            obj = httpRequest(endpoint, payload)
            obj.getRequest()
            json = obj.getJSONResponse()
            groups = groups + json['value']
        self.log.setInfo('Got ' + str(len(groups)) + ' groups')
        self.opsgenie['groups'] = groups
        return groups

    def getUsers(self):
        resource = self.teams['basics']['resource']
        payload = {}
        endpoint = {}
        users = []
        endpoint['uri'] = self.teams['basics']['graph_uri'] + self.teams[
            'endpoints']['users']
        endpoint['certificate'] = False
        payload['auth'] = None
        payload['data'] = ''
        payload['headers'] = {
            "Authorization": "Bearer " + self.config.getUserToken(resource),
            "Content-Type": "application/json"
        }
        payload['config'] = self.config
        obj = httpRequest(endpoint, payload)
        if not (obj.getRequest()):
            self.log.setError('The server response is ' + obj.response.text)
            return []
        json = obj.getJSONResponse()
        users = json['value']
        while (self.__hasMoreUsers__(json)):
            endpoint['uri'] = json['@odata.nextLink']
            obj = httpRequest(endpoint, payload)
            obj.getRequest()
            json = obj.getJSONResponse()
            users = users + json['value']
        self.log.setInfo('Got ' + str(len(users)) + ' users')
        self.teams['users'] = users
        self.log.setInfo('There are ' + str(len(users)) + ' users')
        return users

    def getUser(self, userPrincipalName):
        resource = self.teams['basics']['resource']
        payload = {}
        endpoint = {}
        users = []
        endpoint['uri'] = self.teams['basics']['graph'] + self.teams[
            'endpoints']['users'] + '/' + userPrincipalName
        endpoint['certificate'] = False
        payload['auth'] = None
        payload['data'] = ''
        payload['headers'] = {
            "Authorization": "Bearer " + self.config.getUserToken(resource),
            "Content-Type": "application/json"
        }
        payload['config'] = self.config
        obj = httpRequest(endpoint, payload)
        if not (obj.getRequest()):
            self.log.setError('The server response is ' + obj.response.text)
            return []
        json = obj.getJSONResponse()
        return json

    def getMembers(self, teamID):
        resource = self.teams['basics']['resource']
        payload = {}
        endpoint = {}
        users = []
        endpoint['uri'] = self.teams['basics']['graph'] + self.teams[
            'endpoints']['groups'] + '/' + teamID + '/members'
        endpoint['certificate'] = False
        payload['auth'] = None
        payload['data'] = ''
        payload['headers'] = {
            "Authorization": "Bearer " + self.config.getUserToken(resource),
            "Content-Type": "application/json"
        }
        payload['config'] = self.config
        obj = httpRequest(endpoint, payload)
        if not (obj.getRequest()):
            self.log.setError('The server response is ' + obj.response.text)
            return []
        json = obj.getJSONResponse()
        users = json['value']
        while (self.__hasMoreUsers__(json)):
            endpoint['uri'] = json['@odata.nextLink']
            obj = httpRequest(endpoint, payload)
            obj.getRequest()
            json = obj.getJSONResponse()
            users = users + json['value']
        self.log.setInfo('Got ' + str(len(users)) + ' users')
        self.teams['users'] = users
        self.log.setInfo('There are ' + str(len(users)) + ' users')
        return users

    def __hasMoreUsers__(self, json):
        if ('@odata.nextLink' in json.keys()):
            self.log.setInfo('Needs More users')
            return True
        self.log.setInfo('Doesnt need More users')
        return False

    def setMember(self, teamID, data):
        resource = self.teams['basics']['resource']
        payload = {}
        endpoint = {}
        endpoint['uri'] = self.teams['basics']['graph'] + self.teams[
            'endpoints']['groups'] + '/' + teamID + '/members/$ref'
        endpoint['certificate'] = False
        payload['auth'] = None
        payload['data'] = json.dumps(data)
        payload['headers'] = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.config.getUserToken(resource)
        }
        payload['config'] = self.config
        obj = httpRequest(endpoint, payload)
        if not (obj.postRequest()):
            self.log.setError('The server response is ' + obj.response.text)
            return obj.response.text
        return obj.response.text

    def getGroupEvents(self, GroupID):
        resource = self.teams['basics']['resource']
        payload = {}
        endpoint = {}
        endpoint['uri'] = self.teams['basics']['graph'] + self.teams[
            'endpoints']['groups'] + '/' + GroupID + '/calendar/events'
        endpoint['certificate'] = False
        payload['auth'] = None
        payload['data'] = ''
        payload['headers'] = {
            "Authorization": "Bearer " + self.config.getUserToken(resource),
            "Content-Type": "application/json"
        }
        payload['config'] = self.config
        obj = httpRequest(endpoint, payload)
        if not (obj.getRequest()):
            self.log.setError('The server response is ' + obj.response.text)
            return []
        json = obj.getJSONResponse()
        events = json['value']
        return events

    def getGroupsCalendars(self, GroupID):
        resource = self.teams['basics']['resource']
        payload = {}
        endpoint = {}
        endpoint['uri'] = self.teams['basics']['graph'] + self.teams[
            'endpoints']['groups'] + '/' + GroupID + '/calendars/'
        endpoint['certificate'] = False
        payload['auth'] = None
        payload['data'] = ''
        payload['headers'] = {
            "Authorization": "Bearer " + self.config.getUserToken(resource),
            "Content-Type": "application/json"
        }
        payload['config'] = self.config
        obj = httpRequest(endpoint, payload)
        if not (obj.getRequest()):
            self.log.setError('The server response is ' + obj.response.text)
            return []
        json = obj.getJSONResponse()
        calendars = json['value']
        return calendars

    def getUserCalendars(self, UserID):
        resource = self.teams['basics']['resource']
        payload = {}
        endpoint = {}
        endpoint['uri'] = self.teams['basics']['graph'] + self.teams[
            'endpoints']['users'] + '/' + UserID + '/calendars/'
        endpoint['certificate'] = False
        payload['auth'] = None
        payload['data'] = ''
        payload['headers'] = {
            "Authorization": "Bearer " + self.config.getUserToken(resource),
            "Content-Type": "application/json"
        }
        payload['config'] = self.config
        obj = httpRequest(endpoint, payload)
        if not (obj.getRequest()):
            self.log.setError('The server response is ' + obj.response.text)
            return []
        json = obj.getJSONResponse()
        calendars = json['value']
        return calendars

    def getChannels(self, teamID):
        resource = self.teams['basics']['resource']
        payload = {}
        endpoint = {}
        endpoint['uri'] = self.teams['basics']['graph'] + self.teams[
            'endpoints']['teams'] + '/' + teamID + '/channels'
        endpoint['certificate'] = False
        payload['auth'] = None
        payload['data'] = ''
        payload['headers'] = {
            "Authorization": "Bearer " + self.config.getUserToken(resource),
            "Content-Type": "application/json"
        }
        payload['config'] = self.config
        obj = httpRequest(endpoint, payload)
        if not (obj.getRequest()):
            self.log.setError('The server response is ' + obj.response.text)
            return []
        json = obj.getJSONResponse()
        users = json['value']
        return users

    def setEvent(self, teamID, data):
        resource = self.teams['basics']['resource']
        payload = {}
        endpoint = {}
        endpoint['uri'] = self.teams['basics']['graph'] + self.teams[
            'endpoints']['groups'] + '/' + teamID + '/calendars/events'
        endpoint['certificate'] = False
        payload['auth'] = None
        payload['data'] = json.dumps(data)
        payload['headers'] = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.config.getUserToken(resource)
        }
        payload['config'] = self.config
        obj = httpRequest(endpoint, payload)
        if not (obj.postRequest()):
            self.log.setError('The server response is ' + obj.response.text)
            return obj.response.text
        return obj.response.text

    def setMessage(self, message, data):
        resource = self.teams['basics']['resource']
        payload = {}
        endpoint = {}
        endpoint['uri'] = self.teams['basics']['graph'] + self.teams[
            'endpoints']['teams'] + '/' + message[
                'teamID'] + '/channels/' + message['threadID'] + '/messages'
        endpoint['certificate'] = False
        payload['auth'] = None
        payload['data'] = json.dumps(data)
        payload['headers'] = {
            "Content-type": "application/json",
            "Authorization": "Bearer " + self.config.getUserToken(resource),
        }
        payload['config'] = self.config
        obj = httpRequest(endpoint, payload)
        if not (obj.postRequest()):
            responsecode = str(obj.response.status_code)
            self.log.setError('The server response is ' + obj.response.text +
                              ' with response code ' + responsecode)

            return []
        return obj.response.text

    def setOnlineMeeting(self, data):
        resource = self.teams['basics']['resource']
        payload = {}
        endpoint = {}
        endpoint['uri'] = self.teams['basics']['graph'] + self.teams[
            'endpoints']['meetings']
        endpoint['certificate'] = False
        payload['auth'] = None
        payload['data'] = json.dumps(data)
        payload['headers'] = {
            "Authorization": "Bearer " + self.config.getUserToken(resource),
            "Content-Type": "application/json"
        }
        payload['config'] = self.config
        obj = httpRequest(endpoint, payload)
        if not (obj.postRequest()):
            responsecode = str(obj.response.status_code)
            self.log.setError('The ' + endpoint['uri'] + ' response is ' +
                              obj.response.text + ' with response code ' +
                              responsecode)
            return []
        response = obj.getJSONResponse()
        return response

    def setReply(self, message, data):
        resource = self.teams['basics']['resource']
        payload = {}
        endpoint = {}
        endpoint[
            'uri'] = self.teams['basics']['graph'] + self.teams['endpoints'][
                'teams'] + '/' + message['teamID'] + '/channels/' + message[
                    'threadID'] + '/messages/' + message[
                        'messageID'] + '/replies'
        payload['data'] = json.dumps(data)
        endpoint['certificate'] = False
        payload['auth'] = None
        payload['headers'] = {
            "Authorization": "Bearer " + self.config.getUserToken(resource),
            "Content-Type": "application/json"
        }
        payload['config'] = self.config
        obj = httpRequest(endpoint, payload)
        if not (obj.postRequest()):
            self.log.setError('The server response is ' + obj.response.text)
            return []
        return obj.response.text
