#!/usr/bin/env python


def getResourceId():
    return 'Access Ports'


def getResourceTag():
    return 'accessports'

RESOURCE = {'id':   getResourceId(),
            'tag':  getResourceTag(),
            'attrs': [{'display': 'Name',
                       'name': 'name',
                       'type': 'str',
                       'dim': None,
                       'default': None,
                       'values':  None, },
                      {'display': 'Node',
                       'name': 'node',
                       'type': 'str',
                       'dim': None,
                       'default': None,
                       'values':  None, },
                      {'display': 'Port',
                       'name': 'port',
                       'type': 'str',
                       'dim': None,
                       'default': None,
                       'values':  None, },
                      {'display': 'Vlans',
                       'name': 'vlans',
                       'type': 'str',
                       'dim': None,
                       'default': None,
                       'values':  None, }, ], }
