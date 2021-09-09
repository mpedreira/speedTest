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

SERVER = '41201'


class speedTest:
    def __init__(self, config, server=SERVER):
        self.config = config
        self.log = logger(self.config, __name__)
        # pylint: disable=maybe-no-member
        self.server = server

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
        download = speedtestResult['download']['bandwidth']

        upload = speedtestResult['upload']['bandwidth']
        latency = speedtestResult['ping']['latency']
        self.log.setInfo('Enviados datos por el server ' + self.server +
                         ': Download -> ' + str(round(download, 2)) +
                         ' Mbps Upload -> ' + str(round(upload, 2)) +
                         ' Mbps Latency -> ' + str(round(latency, 2)) + ' ms')
        return speedtestResult

    def __getSpeed(self, speed):
        return speed['bandwidth']

    def __getMegaBites(self, bytes):
        return str(round(bytes / 1024 / 1024 / 8, 2))