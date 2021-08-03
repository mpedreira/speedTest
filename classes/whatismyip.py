#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from classes.httpRequest import *


class whatIsMyIP(httpRequest):
    def __init__(self, config):
        endpoint = {}
        payload = {}
        endpoint['uri'] = 'http://whatismyip.akamai.com'
        endpoint['certificate'] = False
        payload['data'] = ''
        payload['auth'] = None
        payload['headers'] = ''
        payload['config'] = config
        httpRequest.__init__(self, endpoint, payload)

    def getPublicIP(self):
        self.getRequest()
        ip = self.response.text
        return ip