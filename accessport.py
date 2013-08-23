#!/usr/bin/env python


def getResourceId():
    """ Get the Access Port Resource Id.
    """
    return 'Access Ports'


def getResourceTag():
    """ Get the Access Port Resouce YAML Tag.
    """
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
