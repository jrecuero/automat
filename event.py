#!/usr/bin/env python

def getResourceId():
    return 'Event'


def getResourceTag():
    return 'events'


def _getAllServices(dlg):
    return dlg.GetParent().resourceHdlr.getAllServicesName()


def _getAllTunnels(dlg):
    return dlg.GetParent().resourceHdlr.getAllTunnelsName()


def _getAllPorts(dlg):
    return dlg.GetParent().resourceHdlr.getAllPortsName()


def _getDefaultService(dlg):
    return None


def _getDefaultPort(dlg):
    return None


def _getDefaultNone(dlg):
    return None


RESOURCE = {'id':   getResourceId(),
            'tag':  getResourceTag(),
            'attrs': [{'display': 'Name',
                       'name': 'name',
                       'type': 'str',
                       'dim': None,
                       'default': None,
                       'values': None, },
                      {'display': 'Action',
                       'name': 'action',
                       'deps': [{'fields': {'name': 'flowdomain', 'action': ['create', 'delete', 'update'], },
                                 'handler': _getAllServices,
                                 'newfield': 'resource', },
                                {'fields': {'name': 'flowpoint',  'action': ['create', 'delete'], },
                                 'handler': _getAllServices,
                                 'newfield': 'service', },
                                {'fields': {'name': 'flowpoint',  'action': ['create', 'delete', 'update'], },
                                 'handler': _getAllPorts,
                                 'newfield': 'resource', },
                                {'fields': {'name': 'tunnel',     'action': ['create', 'delete', 'update'], },
                                 'handler': _getAllTunnels,
                                 'newfield': 'resource', },
                                {'fields': {'name': 'clienterp',  'action': ['create', 'delete', 'update'], },
                                 'handler': None,
                                 'newfield': 'resource', },
                                {'fields': {'name': 'networkerp', 'action': ['create', 'delete', 'update'], },
                                 'handler': None,
                                 'newfield': 'resource', }, ],
                       'type': 'str',
                       'dim': None,
                       'default': None,
                       'values': None, },
                      {'display': 'Pre-Delay',
                       'name': 'predelay',
                       'type': 'int',
                       'dim': None,
                       'default': None,
                       'values': None, },
                      {'display': 'Post-Delay',
                       'name': 'postedelay',
                       'type': 'int',
                       'dim': None,
                       'default': None,
                       'values': None, },
                      {'display': 'Service',
                       'name': 'service',
                       'enable': False,
                       'type': 'list',
                       'dim': None,
                       'default': _getDefaultNone,
                       'values': None, },
                      {'display': 'Resource',
                       'name': 'resource',
                       'enable': False,
                       'type': 'list',
                       'dim': None,
                       'default': _getDefaultNone,
                       'values': None, }, ], }