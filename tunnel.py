#!/usr/bin/env python


def getResourceId():
    return 'Tunnel'


def getResourceTag():
    return 'tunnels'


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
                      {'display': 'BVID',
                       'name': 'bvid',
                       'type': 'int',
                       'dim': None,
                       'default': None,
                       'values':  None, },
                      {'display': 'Port',
                       'name': 'port',
                       'type': 'str',
                       'dim': None,
                       'default': None,
                       'values':  None, },
                      {'display': 'BSA',
                       'name': 'bsa',
                       'type': 'str',
                       'dim': None,
                       'default': None,
                       'values':  None, }, ], }
