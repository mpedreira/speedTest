#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import truncate
import json
import sys
import math
import time
import os
import requests
from classes.basics import *
from classes.logger import logger


class speedTest:
    def __init__(self, config):
        self.config = config
        self.log = logger(self.config, __name__)
        self.info = self.config.setConfigAttributes('SPEEDTEST')
        # pylint: disable=maybe-no-member
        self.server = self.info['server']

    def setServer(self, server):
        if (not server.isnumeric()):
            return False
        self.server = server
        return True

    def run(self):
        command = 'speedtest -f json-pretty -s ' + self.server
        stream = os.popen(command)
        commandResult = stream.read()
        speedtestResult = {}
        try:
            speedtestResult = json.loads(commandResult)
        except:
            self.log.setError(
                'This command requires speedTestCLI https://www.speedtest.net/apps/cli'
            )
            return speedtestResult
        download = speedtestResult['download']['bandwidth'] * 8 / 1000.0 / 1000.0

        upload = speedtestResult['upload']['bandwidth'] * 8 / 1000.0 / 1000.0
        latency = speedtestResult['ping']['latency']
        self.log.setInfo(
            'Enviados datos por el server ' + self.server + ': Download -> ' +
            str(round(download, 2)) + ' Mbps Upload -> ' + str(round(upload, 2)) +
            ' Mbps Latency -> ' + str(round(latency, 2)) + ' ms'
        )
        return speedtestResult

    def __getSpeed(self, speed):
        return speed['bandwidth']

    def __getMegaBites(self, bytes):
        return str(round(bytes / 1024 / 1024 / 8, 2))
