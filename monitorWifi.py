#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# while true; do echo Hola; sleep 10; done
from classes.jira import *
from classes.configurationChangeManagement import *
from dateutil.relativedelta import relativedelta
from classes.logger import *
from classes.grafanaCloud import *
from classes.speedTest import *
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
UBICACION = 'CASA'
UNIT = 'mbps'
TAGS = []


def setGrafanaInstance(config):
    endpoint = {}
    endpoint[
        'apikey'
    ] = '174504:eyJrIjoiODVmYjc5NWI0M2Y5YzU5YmUzYjZjMGNkYzMxMTFmYjllYjE1NTg0MSIsIm4iOiJzcGVlZFRlc3QiLCJpZCI6NTI3NzM1fQ=='
    endpoint['url'] = 'https://graphite-blocks-prod-us-central1.grafana.net/graphite/metrics'
    grafanaInstance = grafanaCloud(config, endpoint)
    return grafanaInstance


def setGrafanaData(grafanaInstance, date, name, metric, interval, value, unit, tags=[]):
    metrics = [{
        'name': name,
        'metric': metric,
        'interval': interval,
        'value': value,
        'unit': unit,
        'tags': tags,
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
grafanaInstance = setGrafanaInstance(config)
last_date = datetime.datetime.now() - relativedelta(second=+59)
speedInstance = speedTest(config)
while True:
    date = datetime.datetime.now()
    interval = (date - last_date).seconds
    interval = 59
    speed = speedInstance.run()
    download = speed['download']['bandwidth'] / 1000 / 1000
    upload = speed['upload']['bandwidth'] / 1000 / 1000
    latency = speed['ping']['latency']
    metric = 'Download'
    name = metric + '_' + UBICACION
    setGrafanaData(grafanaInstance, date, name, metric, interval, download, UNIT)
    metric = 'Upload'
    name = metric + '_' + UBICACION
    setGrafanaData(grafanaInstance, date, name, metric, interval, upload, UNIT)
    metric = 'Latency'
    name = metric + '_' + UBICACION
    setGrafanaData(grafanaInstance, date, name, metric, interval, latency, 'ms')
    log.setInfo('metricas enviadas')
    time.sleep(59)
