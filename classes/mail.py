#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from classes.activeDirectory import activeDirectory
from classes.basics import *
from classes.logger import logger
from email.header import Header
from email.message import EmailMessage
from email.utils import formataddr
import json
import requests
import smtplib
import ssl


class mail:
    def __init__(self, config, endpoint):
        # pylint: disable=maybe-no-member
        self.config = config
        self.endpoint = {}
        self.response = {}
        self.payload = {}
        self.endpoint['server'] = endpoint['server']
        self.payload['sender'] = self.__getSender()
        self.payload['password'] = self.config.getPassword()
        self.endpoint['port'] = endpoint['port']
        self.log = logger(self.config, __name__)

    def __getSender(self):
        try:
            self.ldap = activeDirectory(self.config)
            self.ldap.connect()
            self.ldap.getQuery(self.ad['endpoints']['baseurl'],
                               'samAccountName=' + self.config.getUsername())
            formataddr((str(sender=Header(
                str(self.ldap.getAttributte('displayName')[0], 'utf-8'),
                'utf-8')), str(self.ldap.getAttributte('mail')[0], 'utf-8')))
        except:
            sender = self.config.getUsername() + '@inditex.com'
        return sender

    def sendHTMLEmail(self, payload):
        self.payload['subject'] = payload['subject']
        self.payload['html'] = payload['html']

        self.payload['receiver'] = payload['receiver']
        msg = EmailMessage()
        msg['From'] = self.payload['sender']
        msg['To'] = ','.join(self.payload['receiver'])
        msg['Subject'] = self.payload['subject']
        msg.set_content(self.payload['html'], subtype='html')
        msg = self.__addAttachments(msg, payload)
        text = msg.as_string()
        self.__sendMail(text)
        self.log.setInfo('Email HTML enviado')
        return True

    def __sendMail(self, text):
        s = smtplib.SMTP(self.endpoint['server'], self.endpoint['port'])
        s.ehlo()
        s.starttls()
        s.login(self.payload['sender'], self.payload['password'])
        s.sendmail(self.payload['sender'], self.payload['receiver'], text)
        s.quit()

    def sendPlainEmail(self, payload):
        self.payload['subject'] = payload['subject']
        self.payload['text'] = payload['text']
        self.payload['receiver'] = payload['receiver']
        msg = EmailMessage()
        msg['From'] = self.payload['sender']
        msg['To'] = ','.join(self.payload['receiver'])
        msg['Subject'] = self.payload['subject']
        msg.set_content(self.payload['text'])
        msg = self.__addAttachments(msg, payload)
        text = msg.as_string()
        self.__sendMail(text)
        self.log.setInfo('Email TXT enviado')
        return True

    def __addAttachments(self, msg, payload):
        for attachment in payload['attachments']:
            try:
                with open(attachment, 'rb') as file:
                    msg.add_attachment(file.read(),
                                       maintype='application',
                                       subtype='octet-stream',
                                       filename=file.name)
                    self.log.setError(attachment + " encontrado")
            except FileNotFoundError:
                self.log.setError(attachment + " no encontrado. Se omite")
        return msg
