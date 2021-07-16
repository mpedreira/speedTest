#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unicodedata import normalize
import json
import requests
from classes.basics import *
from classes.logger import logger
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

STATUS_CODE = {'OK': {201, 200, 204, 404}, 'ERROR': {401}}


class mail:
    def __init__(self, config, endpoint):
        # pylint: disable=maybe-no-member
        self.config = config
        self.endpoint = {}
        self.response = {}
        self.payload = {}
        self.endpoint['server'] = endpoint['server']
        self.endpoint['port'] = endpoint['port']
        self.log = logger(self.config, __name__)

    def sendEmail(self, payload):
        self.payload['subject'] = payload['subject']
        self.payload['text'] = payload['text']
        self.payload['html'] = payload['html']
        self.payload['sender'] = payload['sender']
        self.payload['receiver'] = payload['receiver']
        self.payload['password'] = payload['password']
        message = MIMEMultipart("alternative")
        part1 = MIMEText(self.payload['text'], "plain")
        part2 = MIMEText(self.payload['html'], "html")
        message.attach(part1)
        message.attach(part2)
        context = ssl.create_default_context()
        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        with smtplib.SMTP_SSL(self.endpoint['server'],
                              self.endpoint['port'],
                              context=context) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(self.payload['sender'], self.payload['password'])
            server.sendmail(self.payload['sender'],
                            recself.payload['receiver'], message.as_string())
        return True

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
