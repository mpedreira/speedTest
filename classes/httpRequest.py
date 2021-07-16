#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import truncate
from unicodedata import normalize
import json
import sys
import math
import time
import requests
from classes.basics import *
from classes.logger import logger

STATUS_CODE = {'OK': {201, 200, 204, 404}, 'ERROR': {401}}


class httpRequest:
    def __init__(self, endpoint, payload):
        # pylint: disable=maybe-no-member
        self.endpoint = {}
        self.payload = {}
        self.response = {}
        self.endpoint['uri'] = endpoint['uri']
        self.endpoint['certificate'] = endpoint['certificate']
        self.payload['config'] = payload['config']
        self.payload['headers'] = payload['headers']
        self.payload['data'] = payload['data']
        self.payload['auth'] = payload['auth']
        self.payload['files'] = self.setFiles(payload)
        self.log = logger(self.payload['config'], __name__)
        insecureWarning = requests.packages.urllib3.exceptions.InsecureRequestWarning
        requests.packages.urllib3.disable_warnings(insecureWarning)
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'

    def downloadSpeed(self):
        start = time.clock()
        self.getRequest()
        end = time.clock()
        seconds = (end - start) * 1000
        size = int(self.response.headers['Content-Length']) / 1024
        self.log.setDebug("Nos hemos bajado " + str(size) + "M en " +
                          str(math.trunc(seconds)) + " segundos")
        return round((size / seconds), 2)

    def setFiles(self, payload):
        if ('files' not in payload.keys()):
            return ''
        else:
            return payload['files']

    def getJSONResponse(self):
        jsonResponse = {}
        if self.isOKResponse():
            jsonResponse = json.loads(normalize('NFC', self.response.text))
        else:
            print(self.response.text)
            self.log.setDebug(self.response.text)
            self.log.setError('Authentication Failed')
            raise Exception('AuthenticationError')
        return jsonResponse

    def isOKResponse(self):
        try:
            if self.response.status_code in STATUS_CODE['OK']:
                return True
            self.log.setDebug('Status Code: ' + str(self.response.status_code))
            return False
        except AttributeError:
            return False

    def deleteRequest(self):
        self.response = requests.delete(self.endpoint['uri'],
                                        auth=self.payload['auth'],
                                        data=self.payload['data'],
                                        headers=self.payload['headers'],
                                        verify=self.endpoint['certificate'])
        self.log.setDebug('DELETE made to ' + self.endpoint['uri'])
        self.log.setDebug('The payload is' + str(self.payload['data']))
        return self.isOKResponse()

    # def deleteRequestAnonymous(self):
    #     self.response = requests.delete(
    #         self.endpoint['uri'],
    #         data=self.payload['data'],
    #         headers=self.payload['headers'],
    #         # HACK para WildCards
    #         verify=False,
    #         auth=None
    #         #verify=self.endpoint['certificate']
    #     )
    #     self.log.setDebug('DELETE made to ' + self.endpoint['uri'])
    #     self.log.setDebug('The payload is' + str(self.payload['data']))
    #     return self.isOKResponse()

    def getRequest(self):
        self.response = requests.get(
            self.endpoint['uri'],
            auth=self.payload['auth'],
            verify=self.endpoint['certificate'],
            #       headers=self.payload['headers']
        )
        self.log.setDebug('GET made to ' + self.endpoint['uri'])
        return self.isOKResponse()

    # def getRequestAnonymous(self):
    #     self.response = requests.get(
    #         self.endpoint['uri'],
    #         headers=self.payload['headers'],
    #         # HACK para WildCards
    #         verify=False
    #         #verify=self.endpoint['certificate']
    #     )
    #     self.log.setDebug('GET Anonymous made to ' + self.endpoint['uri'])
    #     return self.isOKResponse()

    def patchRequest(self):
        self.response = requests.patch(self.endpoint['uri'],
                                       data=self.payload['data'],
                                       headers=self.payload['headers'],
                                       auth=self.payload['auth'],
                                       verify=self.endpoint['certificate'])
        self.log.setDebug('PATCH made to ' + self.endpoint['uri'])
        self.log.setDebug('The payload is' + str(self.payload['data']))
        return self.isOKResponse()

    def postRequest(self):
        self.response = requests.post(self.endpoint['uri'],
                                      auth=self.payload['auth'],
                                      data=self.payload['data'],
                                      headers=self.payload['headers'],
                                      files=self.payload['files'],
                                      verify=self.endpoint['certificate'])
        self.log.setDebug('POST made to ' + self.endpoint['uri'])
        self.log.setDebug('The payload is' + str(self.payload['data']))
        return self.isOKResponse()

    # def postRequestAnonymous(self):
    #     self.response = requests.post(
    #         self.endpoint['uri'],
    #         data=self.payload['data'],
    #         headers=self.payload['headers'],
    #         # HACK para WildCards
    #         verify=False
    #         #verify=self.endpoint['certificate']
    #     )
    #     self.log.setDebug('POST made to ' + self.endpoint['uri'])
    #     self.log.setDebug('The payload is' + str(self.payload['data']))
    #     return self.isOKResponse()

    def putRequest(self):
        self.response = requests.put(self.endpoint['uri'],
                                     auth=self.payload['auth'],
                                     data=json.dumps(self.payload['data']),
                                     headers=self.payload['headers'],
                                     verify=self.endpoint['certificate'])
        self.log.setDebug('PUT made to ' + self.endpoint['uri'])
        self.log.setDebug('The payload is' + str(self.payload['data']))
        return self.isOKResponse()

    # def putRequestAnonymous(self):
    #     self.response = requests.put(
    #         self.endpoint['uri'],
    #         data=self.payload['data'],
    #         headers=self.payload['headers'],
    #         # HACK para WildCards
    #         verify=False
    #         #verify=self.endpoint['certificate']
    #     )
    #     self.log.setDebug('PUT made to ' + self.endpoint['uri'])
    #     self.log.setDebug('The payload is' + str(self.payload['data']))
    #     return self.isOKResponse()
