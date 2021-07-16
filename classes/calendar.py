#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from classes.configuration import *
from classes.httpRequest import *
from classes.logger import *

CALENDAR_STATUS = {
    'cancel': {
        'Rechazada', 'Canceled', 'Pendiente correo cancelación', 'Cancelada',
        'Pendiente correo', 'Waiting cancel mail'
    },
    'closed': {
        'Cerrada', 'Closed', 'Pendiente correo finalización',
        'Waiting close mail', 'Waiting mail'
    },
    'created': {'Nueva', 'New', 'Pendiente correo'},
    'acepted': {'Accepted', 'Aceptada', 'Waiting mail', 'Pendiente correo'}
}


class calendar:
    def __init__(self, config):
        self.calendar = {}
        self.config = config
        config = configparser.RawConfigParser()
        config.read(self.config.getConfigfile())
        self.calendar['endpoint'] = self.config.setConfigAttributes('INET')
        self.changeID = None
        self.status = ''
        self.log = logger(self.config, __name__)

    def __hasbeenAcepted__(self):
        if self.status in CALENDAR_STATUS['acepted']:
            return True
        else:
            return False

    def __hasbeenCreated__(self):
        if self.status in CALENDAR_STATUS['created']:
            return True
        else:
            return False

    def __hasbeenCanceled__(self):
        if self.status in CALENDAR_STATUS['cancel']:
            return True
        else:
            return False

    def __hasbeenClosed__(self):
        if self.status in CALENDAR_STATUS['closed']:
            return True
        else:
            return False

    def __getChangeID__(self):
        HTML = str(self.data)
        SIZE = 17
        # SUMAMOS 19 porque son los caracteres desde los que empieza la intervencion
        OFFSET = 19
        if (not self.__hasChangeID__()):
            self.changeID = 'None'
            return 'None'
        offset = HTML.find('<span>ID</span>') + OFFSET
        # NUMERO DE CARACTERES DE LA INTERVENCION
        self.changeID = HTML[offset:offset + SIZE]
        self.log.setDebug('Retrieved ' + self.changeID)
        return self.changeID

    def __getKeys__(self, config):
        attributes = {}
        for attribute in config.keys():
            attributes[attribute] = config[attribute]
        return attributes

    def __getStatus__(self):
        HTML = str(self.data)
        # SUMAMOS 19 porque son los caracteres desde los que empieza la intervencion
        OFFSET = 23
        SUBSET_SIZE = 400
        if (HTML.find('<span>Estado</span>') > 0):
            OFFSET = 23
            offset = HTML.find('<span>Estado</span>') + OFFSET
        else:
            OFFSET = 22
            offset = HTML.find('<span>State</span>') + OFFSET
        subset = HTML[offset:offset + SUBSET_SIZE]
        size = subset.find('</p>')
        self.status = HTML[offset:offset + size]
        return self.status

    def __hasChangeID__(self):
        HTML = self.data
        if (HTML.find('<span>ID</span>') < 0):
            return False
        return True

    def __writeDebugResponse__(self, obj):
        debug = self.config.getDebugFolder(
        ) + self.changeID + '-' + self.config.getExecutionTime() + '.html'
        if (self.config.isDebug()):  # and not obj.isOKResponse()):
            writeDebug(debug, obj.response.text)

    def acceptChange(self):
        endpoint = {}
        payload = {}
        accion = 'approveIntervencion'
        comentario = 'Intervención Aceptada'
        endpoint['uri'] = self.calendar['endpoint']['modifychange'] + accion
        endpoint['certificate'] = self.calendar['endpoint']['certificate']
        payload['headers'] = ''
        payload['auth'] = self.config.getBasicAuth()
        payload['data'] = {
            'workOrderId': self.changeID,
            'comentario': comentario,
        }
        payload['config'] = self.config
        obj = httpRequest(endpoint, payload)
        obj.postRequest()
        self.data = obj.response.text
        self.__getStatus__()
        if (self.__hasbeenAcepted__()):
            self.log.setDebug('Aceptada en INET la intervencion ' +
                              self.changeID)
            self.__getChangeID__()
            return True
        self.__writeDebugResponse__(obj)
        self.log.setError('Error aceptando en INET la intervencion ' +
                          self.changeID)
        return False

    def cancelChange(self):
        endpoint = {}
        payload = {}
        accion = 'cancelIntervencion'
        comentario = 'Intervención Cancelada'
        endpoint['uri'] = self.calendar['endpoint']['modifychange'] + accion
        endpoint['certificate'] = self.calendar['endpoint']['certificate']
        payload['headers'] = ''
        payload['auth'] = self.config.getBasicAuth()
        payload['data'] = {
            'workOrderId': self.changeID,
            'comentario': comentario,
        }
        payload['config'] = self.config
        obj = httpRequest(endpoint, payload)
        obj.postRequest()
        self.data = obj.response.text
        self.__getStatus__()
        if (self.__hasbeenCanceled__() or self.__hasbeenClosed__()):
            self.log.setDebug('Cancelada en INET la intervencion ' +
                              self.changeID)
            self.__getChangeID__()
            return True
        self.__writeDebugResponse__(obj)
        self.log.setError('Error cancelando en INET la intervencion ' +
                          self.changeID)
        return False

    def closeChange(self):
        endpoint = {}
        payload = {}
        accion = 'closeIntervencion'
        comentario = 'Intervención Finalizada'
        endpoint['uri'] = self.calendar['endpoint']['modifychange'] + accion
        endpoint['certificate'] = self.calendar['endpoint']['certificate']
        payload['headers'] = ''
        payload['auth'] = self.config.getBasicAuth()
        payload['data'] = {
            'workOrderId': self.changeID,
            'comentario': comentario
        }
        payload['config'] = self.config
        obj = httpRequest(endpoint, payload)
        obj.postRequest()
        self.data = obj.response.text
        self.__getStatus__()
        if (self.__hasbeenClosed__() or self.__hasbeenCanceled__()):
            self.log.setDebug('Canceled ' + self.changeID)
            self.__getChangeID__()
            return True
        self.__writeDebugResponse__(obj)
        self.log.setError('Error cerrando ' + self.changeID)
        return False

    def getChange(self):
        endpoint = {}
        payload = {}
        endpoint[
            'uri'] = self.calendar['endpoint']['calendario'] + self.changeID
        endpoint['certificate'] = self.calendar['endpoint']['certificate']
        payload['headers'] = ''
        payload['data'] = ''
        payload['auth'] = self.config.getBasicAuth()
        payload['config'] = self.config
        obj = httpRequest(endpoint, payload)
        obj.getRequest()
        if (obj.isOKResponse()):
            self.log.setDebug('Retrieved info from change ' + self.changeID)
            self.data = obj.response.text
        else:
            self.log.setError('Error retrieving info from change ' +
                              self.changeID)
            self.data = ''
        return self.data

    def getChangeID(self):
        return self.changeID

    def getStatus(self):
        if self.status == '':
            self.__getStatus__()
        return self.status

    def rejectChange(self):
        self.log.setError('Method rejectChange not implemented')
        return

    def sendMail(self):
        endpoint = {}
        payload = {}
        accion = 'sendMailIntervencion'
        comentario = 'Envio de eMail'
        eMail = 'null@example.com'
        content = 'test'
        subject = 'test'
        endpoint['uri'] = self.calendar['endpoint']['modifychange'] + accion
        endpoint['certificate'] = self.calendar['endpoint']['certificate']
        payload['headers'] = ''
        payload['auth'] = self.config.getBasicAuth()
        payload['data'] = {
            'workOrderId': self.changeID,
            'comentario': comentario,
            'mailTo': eMail,
            'mailSubject': subject,
            'mailContent': content
        }
        payload['config'] = self.config
        obj = httpRequest(endpoint, payload)
        obj.postRequest()
        self.data = obj.response.text
        self.__getStatus__()
        if (self.__hasbeenAcepted__()):
            self.log.setDebug('Enviado correo para ' + self.changeID)
            self.__getChangeID__()
            return True
        self.__writeDebugResponse__(obj)
        self.log.setError('Error enviando Correo ' + self.changeID)
        return False

    def setChangeInfo(self, data):
        endpoint = {}
        payload = {}
        accion = 'saveIntervencion'
        endpoint['uri'] = self.calendar['endpoint']['modifychange'] + accion
        endpoint['certificate'] = self.calendar['endpoint']['certificate']
        payload['headers'] = ''
        payload['auth'] = self.config.getBasicAuth()
        payload['data'] = data
        payload['config'] = self.config
        obj = httpRequest(endpoint, payload)
        obj.postRequest()
        self.data = obj.response.text
        self.__getStatus__()
        self.__getChangeID__()
        if (self.__hasbeenCreated__()):
            self.__getChangeID__()
            self.log.setDebug('Set info from change ' + self.changeID)
            return self.__getChangeID__()
        self.log.setError('Error setting info from change ' + self.changeID)
        return None

    def setChangeID(self, changeID):
        self.changeID = changeID
