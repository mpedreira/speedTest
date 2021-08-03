#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from classes.jira import *
from classes.configurationChangeManagement import *
from classes.whatismyip import *
from classes.logger import *
from classes.httpRequest import *
from classes.grafanaCloud import *
import datetime
import csv
import json
import sys
import ssl
from classes.jsd import *

MINIMUM_SPEED = 100
NUM_ERRORS = 8
SLEEP = 10
METRIC = 'Velocidad en CASA'


def setGrafanaInstance(config):
    endpoint = {}
    endpoint[
        'apikey'
    ] = '174504:eyJrIjoiODVmYjc5NWI0M2Y5YzU5YmUzYjZjMGNkYzMxMTFmYjllYjE1NTg0MSIsIm4iOiJzcGVlZFRlc3QiLCJpZCI6NTI3NzM1fQ=='
    endpoint['url'] = 'https://graphite-blocks-prod-us-central1.grafana.net/graphite/metrics'
    grafanaInstance = grafanaCloud(config, endpoint)
    return grafanaInstance


def setHttpInstance(config):
    endpoint = {}
    payload = {}
    endpoint[
        'uri'
    ] = 'https://content.rolex.com/dam/homepage/hss/watches/classic-watches/day-date/day-date-40/homepage-day-date-40-m228238-0042.mp4'
    # endpoint[
    #    'uri'] = 'https://releases.ubuntu.com/20.04.2.0/ubuntu-20.04.2.0-desktop-amd64.iso'
    endpoint['certificate'] = False
    payload['data'] = ''
    payload['auth'] = ''
    payload['config'] = config
    payload['headers'] = None
    httpInstance = httpRequest(endpoint, payload)
    return httpInstance


def setGrafanaData(grafanaInstance, date, speed):
    metrics = [(METRIC, SLEEP, speed, date)]
    grafanaInstance.setMetrics(metrics)


# MAIN
config = configurationChangeManagement()
log = logger(config, 'main')
if (not config.isDebug()):
    sys.tracebacklimit = 0
# MAIN
date = datetime.datetime.now()
now = date.strftime('%d/%m/%Y %H:%M:%S')
log.setInfo('Running at ' + now)
ip = whatIsMyIP(config)
httpInstance = setHttpInstance(config)
grafanaInstance = setGrafanaInstance(config)
while True:
    date = datetime.datetime.now()
    speed = httpInstance.speedTest()
    setGrafanaData(grafanaInstance, date, speed)
    time.sleep(SLEEP)
