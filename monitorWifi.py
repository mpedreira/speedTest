#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# while true; do echo Hola; sleep 10; done
from classes.jira import *
from classes.configurationChangeManagement import *
from dateutil.relativedelta import relativedelta
from classes.logger import *
from classes.speedTest import *
from classes.grafanaCloud import *
import datetime

MINIMUM_SPEED = 100
NUM_ERRORS = 8
SLEEP = 330
NAME = 'en_INDITEX'
METRIC = 'en_INDITEX'
UNIT = 'mbps'
TAGS = []


def setGrafanaData(grafanaInstance, name, date, speed, sleep):
    metrics = [{
        'name': name,
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
date = datetime.datetime.now()
now = date.strftime('%d/%m/%Y %H:%M:%S')
log.setInfo('Running at ' + now)
grafanaInstance = grafanaCloud(config)
last_date = datetime.datetime.now() - relativedelta(second=+59)
server = '14979'
test = speedTest(config, server)
date = datetime.datetime.now()
result = test.run()
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
name = 'DOWNLOAD_' + NAME
setGrafanaData(grafanaInstance, name, date, download, sleep)
name = 'UPLOAD_' + NAME
setGrafanaData(grafanaInstance, name, date, upload, sleep)
name = 'LATENCY_' + NAME
setGrafanaData(grafanaInstance, name, date, latency, sleep)
#log.setInfo('Enviados datos por el server ' + server + ': Download -> ' +
#            str(round(download, 2)) + ' Mbps Upload -> ' +
#            str(round(upload, 2)) + ' Mbps Latency -> ' +
#            str(round(latency, 2)) + ' ms')
