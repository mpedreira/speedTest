#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from typing import Awaitable
from classes.basics import *
from classes.logger import logger
import json

SERVER = '41201'


class speedTest:
    def __init__(self, config, server=SERVER):
        # pylint: disable=maybe-no-member
        self.config = config
        self.server = server
        self.log = logger(self.config, __name__)

    def run(self):
        command = './speedtest -f json-pretty -s ' + self.server
        stream = os.popen(command)
        speed = stream.read()
        try:
            result = json.loads(speed)
        except:
            return ''
        return result