#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from classes.configurationSpeedTest import *
from dateutil.relativedelta import relativedelta
from classes.logger import *
from classes.grafanaCloud import *
from classes.speedTest import *
import datetime

MINIMUM_SPEED = 100
NUM_ERRORS = 8
SLEEP = 330


def setGrafanaData(grafanaInstance, name, date, speed, sleep, unit, metric, tags=[]):
    metrics = [{
        'name': name,
        'metric': metric,
        'interval': sleep,
        'value': speed,
        'unit': unit,
        'tags': tags,
        'date': date
    }]
    grafanaInstance.setMetrics(metrics)


# MAIN
config = configurationSpeedTest()
log = logger(config, 'main')
if (not config.isDebug()):
    sys.tracebacklimit = 0
date = datetime.datetime.now()
now = date.strftime('%d/%m/%Y %H:%M:%S')
log.setInfo('Running at ' + now)
grafanaInstance = grafanaCloud(config)
last_date = datetime.datetime.now() - relativedelta(second=+59)
speedTestInstance = speedTest(config)
ubicacion = speedTestInstance.info['ubicacion']
metric = speedTestInstance.info['metric']
unit = speedTestInstance.info['unit']
server = speedTestInstance.info['server']
date = datetime.datetime.now()
linea = '_ORANGE'
result = speedTestInstance.run()
try:
    download = result['download']['bandwidth'] * 8 / 1000.0 / 1000.0
except:
    print(result)

upload = result['upload']['bandwidth'] * 8 / 1000.0 / 1000.0
latency = result['ping']['latency']
sleep = (date - last_date).seconds
if (sleep == 0):
    sleep = 1
last_date = date
name = 'DOWNLOAD_' + ubicacion + linea
setGrafanaData(grafanaInstance, name, date, download, sleep, unit, metric)
name = 'UPLOAD_' + ubicacion + linea
setGrafanaData(grafanaInstance, name, date, upload, sleep, unit, metric)
name = 'LATENCY_' + ubicacion + linea
setGrafanaData(grafanaInstance, name, date, latency, sleep, unit, metric)

linea = '_REDESSALMANTINAS'
server = '41201'
speedTestInstance.setServer(server)
result = speedTestInstance.run()
try:
    download = result['download']['bandwidth'] * 8 / 1000.0 / 1000.0
except:
    print(result)

upload = result['upload']['bandwidth'] * 8 / 1000.0 / 1000.0
latency = result['ping']['latency']
sleep = (date - last_date).seconds
if (sleep == 0):
    sleep = 1

last_date = date
name = 'DOWNLOAD_' + ubicacion + linea
setGrafanaData(grafanaInstance, name, date, download, sleep, unit, metric)
name = 'UPLOAD_' + ubicacion + linea
setGrafanaData(grafanaInstance, name, date, upload, sleep, unit, metric)
name = 'LATENCY_' + ubicacion + linea
setGrafanaData(grafanaInstance, name, date, latency, sleep, unit, metric)
