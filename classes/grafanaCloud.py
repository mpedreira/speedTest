#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from classes.activeDirectory import activeDirectory
from classes.basics import *
from classes.logger import logger
from classes.httpRequest import *
import json
import requests
import smtplib
import ssl


class grafanaCloud:
    def __init__(self, config, endpoint):
        # pylint: disable=maybe-no-member
        self.config = config
        self.log = logger(self.config, __name__)
        self.endpoint = {}
        self.endpoint['url'] = endpoint['url']
        self.endpoint['apikey'] = endpoint['apikey']
        self.log = logger(self.config, __name__)

    def setMetrics(self, metrics):
        grafana_data = []
        for m in metrics:
            grafana_data.append({
                'name': m['name'],
                'metric': m['metric'],
                'value': float(m['value']),
                'interval': int(m['interval']),
                'unit': m['unit'],
                'time': int(m['date'].timestamp()),
                'mtype': 'count',
                'tags': m['tags'],
            })
        # sort by ts
        grafana_data.sort(key=lambda obj: obj['time'])
        endpoint = {}
        payload = {}
        endpoint['uri'] = self.endpoint['url']
        endpoint['certificate'] = False
        payload['headers'] = {
            "Authorization": "Bearer %s" % self.endpoint['apikey'],
            'Content-Type': 'application/json'
        }
        payload['config'] = self.config
        payload['auth'] = None
        payload['data'] = json.dumps(grafana_data)
        obj = httpRequest(endpoint, payload)
        obj.postRequest()
        if not obj.isOKResponse():
            self.log.setError('Error posting the metrics with response code ' +
                              str(obj.response.status_code))
            raise Exception(obj.response.text)
        self.log.setDebug('%s: %s' %
                          (obj.response.status_code, obj.response.text))
        obj = ''
        return True
