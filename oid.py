#!/usr/bin/env python


def getResourceId():
    return 'OID'


def getResourceTag():
    return 'oids'


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
                      {'display': 'Oid',
                       'name': 'oid',
                       'type': 'str',
                       'dim': None,
                       'default': None,
                       'values': None, },
                      {'display': 'Location',
                       'name': 'location',
                       'type': 'str',
                       'dim': None,
                       'default': None,
                       'values':  None, }, ], }
