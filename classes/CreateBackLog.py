#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from classes.jira import *
from classes.activeDirectory import *
from classes.logger import *


class backlog:
    def __init__(self, config):
        self.config = config
        self.log = logger(self.config, __name__)
        self.jira = jira(self.config)
        self.ldap = activeDirectory(config)
        self.ldap.connect()

    def createBacklog(self):
        csv = getListfromCSVFile(self.config.args['filename'])
        for issue in csv:
            assignee = issue[0]
            epica = issue[1]
            priority = issue[2]
            summary = issue[3]
            description = issue[4]
            data = {
                'fields': {
                    "assignee": {
                        "name": assignee,
                    },
                    "reporter": {
                        "name": "manuelpa"
                    },
                    "issuetype": {
                        "id": "3"
                    },
                    "project": {
                        "id": "29889"
                    },
                    "description": description,
                    "summary": summary,
                    "priority": {
                        "name": priority
                    },
                    "customfield_11760": epica,
                    "security": {
                        "id": "14290"
                    },
                }
            }
            key = self.jira.setIssue(data)
            self.log.setInfo('Creada tarea con ID ' + key)
        return True