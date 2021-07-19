#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from classes.jira import *
from classes.configurationChangeManagement import *
from classes.logger import *
from classes.httpRequest import *
import datetime
import csv
import json
import sys
import ssl
from classes.jsd import *

MINIMUM_SPEED = 100
NUM_ERRORS = 8

# MAIN
config = configurationChangeManagement()
log = logger(config, 'main')
if (not config.isDebug()):
    sys.tracebacklimit = 0
# MAIN
date = datetime.datetime.now()
now = date.strftime('%d/%m/%Y %H:%M:%S')
log.setInfo('Running at ' + now)
endpoint = {}
payload = {}
endpoint[
    'uri'] = 'https://content.rolex.com/dam/homepage/hss/watches/classic-watches/day-date/day-date-40/homepage-day-date-40-m228238-0042.mp4'
#endpoint[
#    'uri'] = 'https://releases.ubuntu.com/20.04.2.0/ubuntu-20.04.2.0-desktop-amd64.iso'
endpoint['certificate'] = False
payload['data'] = ''
payload['auth'] = ''
payload['config'] = config
payload['headers'] = None
httpInstance = httpRequest(endpoint, payload)
j = 0

while True:
    i = 0
    while i >= 0:
        speed = httpInstance.speedTest()
        if (speed < MINIMUM_SPEED):
            i = i + 1
            if i > NUM_ERRORS:
                log.setInfo('Llevamos más de ' + str(NUM_ERRORS) +
                            ' por debajo del objetivo de ' +
                            str(MINIMUM_SPEED))
                i = -1
        else:
            i = -1
        time.sleep(10)
