#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# while true; do echo Hola; sleep 10; done
from classes.jira import *
from classes.configurationChangeManagement import *
from dateutil.relativedelta import relativedelta
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
SLEEP = 30
NAME = 'Bandwidth'
METRIC = 'CASA'
UNIT = 'mbps'
TAGS = []


def setGrafanaInstance(config):
    endpoint = {}
    endpoint[
        'apikey'] = '174504:eyJrIjoiODVmYjc5NWI0M2Y5YzU5YmUzYjZjMGNkYzMxMTFmYjllYjE1NTg0MSIsIm4iOiJzcGVlZFRlc3QiLCJpZCI6NTI3NzM1fQ=='
    endpoint[
        'url'] = 'https://graphite-blocks-prod-us-central1.grafana.net/graphite/metrics'
    grafanaInstance = grafanaCloud(config, endpoint)
    return grafanaInstance


def setHttpInstance(config):
    endpoint = {}
    payload = {}
    endpoint[
        'uri'] = 'https://content.rolex.com/dam/homepage/hss/watches/classic-watches/day-date/day-date-40/homepage-day-date-40-m228238-0042.mp4'
    # endpoint[
    #    'uri'] = 'https://releases.ubuntu.com/20.04.2.0/ubuntu-20.04.2.0-desktop-amd64.iso'
    endpoint['certificate'] = False
    payload['data'] = ''
    payload['auth'] = ''
    payload['config'] = config
    payload['headers'] = None
    httpInstance = httpRequest(endpoint, payload)
    return httpInstance


def setGrafanaData(grafanaInstance, date, speed, sleep):
    metrics = [{
        'name': NAME,
        'metric': METRIC,
        'interval': sleep,
        'value': speed,
        'unit': UNIT,
        'tags': TAGS,
        'date': date
    }]
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
last_date = datetime.datetime.now() - relativedelta(second=+6)

while True:
    try:
        date = datetime.datetime.now()
        speed = httpInstance.speedTest()
        sleep = (date - last_date).seconds
        last_date = date
        setGrafanaData(grafanaInstance, date, speed, sleep)
        time.sleep(SLEEP)
    except:
        pass
