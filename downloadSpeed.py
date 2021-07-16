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
    'uri'] = 'https://static.zara.net/video///mkt/2021/7/aw21-north-new-in-woman/subhome-xmedia-video-28-tribute//large-landscape/subhome-xmedia-video-28-tribute_0_1080p/subhome-xmedia-video-28-tribute_0_1080p_058.ts?ts=1626351539792'
endpoint['certificate'] = False
payload['data'] = ''
payload['auth'] = ''
payload['config'] = config
payload['headers'] = None
httpInstance = httpRequest(endpoint, payload)
while True:
    print(httpInstance.downloadSpeed())
