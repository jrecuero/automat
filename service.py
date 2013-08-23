#!/usr/bin/env python


def getResourceId():
    return 'Service'


def getResourceTag():
    return 'services'


def _getServiceTypes(dlg):
    return ['ELINE',  'EVLINE', 'ELAN', 'EVLAN']


def _getDefaultServiceType(dlg):
    return 'EVLAN'


RESOURCE = {'id':   getResourceId(),
            'tag':  getResourceTag(),
            'attrs': [{'display': 'Name',
                       'name': 'name',
                       'type': 'str',
                       'dim': None,
                       'default': None,
                       'values': None, },
                      {'display': 'Node',
                       'name': 'node',
                       'type': 'str',
                       'dim': None,
                       'default': None,
                       'values':  None, },
                      {'display': 'Type',
                       'name': 'type',
                       'type': 'list',
                       'dim': None,
                       'default': _getDefaultServiceType,
                       'values': _getServiceTypes, },
                      {'display': 'Isid',
                       'name': 'isid',
                       'type': 'int',
                       'dim': None,
                       'default': None,
                       'values':  None, }, ], }
