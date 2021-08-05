#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from classes.jira import *
from classes.configurationChangeManagement import *
from classes.logger import *
from classes.mail import *
from classes.httpRequest import *
import datetime
import csv
import json
import sys
import ssl
from classes.jsd import *

MINIMUM_SPEED = 100
NUM_ERRORS = 3
SLEEP = 60

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
endpoint['server'] = 'smtp.office365.com'
endpoint['port'] = 587
mailInstance = mail(config, endpoint)
endpoint = {}
payload = {}
endpoint[
    'uri'] = 'https://content.rolex.com/dam/homepage/hss/watches/classic-watches/day-date/day-date-40/homepage-day-date-40-m228238-0042.mp4'
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
                payloadEmail = {}
                payloadEmail[
                    'subject'] = 'Problemas de rendimiento de la wifi de Zara.com'
                payloadEmail['html'] = """\
                <html>
                <head></head>
                <body>
                    <p>Hola!<br>
                    Te envio este correo porque el rendimiento de la wifi 
                    de Zara.com no ha sido bueno en los ultimos minutos.
                    La ultima metrica es de
                """ + str(speed) + """\
                     que esta por debajo de 
                """ + str(MINIMUM_SPEED) + """\
                    <br>
                    Si la incidencia continua escaladselo a JC
                    </p>
                </body>
                </html>
                """

                payloadEmail['receiver'] = [
                    'manuelpa@inditex.com', 'xabiergd@inditex.com'
                ]
                log.setInfo('Llevamos más de ' + str(NUM_ERRORS) +
                            ' por debajo del objetivo de ' +
                            str(MINIMUM_SPEED))
                mailInstance.sendHTMLEmail(payloadEmail)
                i = -1
        else:
            i = -1
        time.sleep(SLEEP)
