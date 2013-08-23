#!/usr/bin/env python


def getResourceId():
    """ Get the End Point Resource Id.
    """
    return 'End Point'


def getResourceTag():
    """ Get the End Point Resource YAML Tag.
    """
    return 'endpoints'


def _getAllServices(dlg):
    """ Get all Services Names entered in the system.
    """
    return dlg.GetParent().resourceHdlr.getAllServicesName()


def _getDefaultService(dlg):
    """ Get default service name.
    """
    return None


def _getAllPorts(dlg):
    """ Get all Ports Names entered in the system.
    """
    return dlg.GetParent().resourceHdlr.getAllPortsName()


def _getDefaultPort(dlg):
    """ Get default port name.
    """
    return None


RESOURCE = {'id':   getResourceId(),
            'tag':  getResourceTag(),
            'attrs': [{'display': 'Name',
                       'name': 'name',
                       'type': 'str',
                       'dim': None,
                       'default': None,
                       'values': None, },
                      {'display': 'Stream ID',
                       'name': 'streamId',
                       'type': 'int',
                       'dim': None,
                       'default': None,
                       'values':  None, },
                      {'display': 'Service',
                       'name': 'service',
                       'type': 'list',
                       'dim': None,
                       'default': _getDefaultService,
                       'values': _getAllServices, },
                      {'display': 'Flags',
                       'name': 'flags',
                       'type': 'str',
                       'dim': None,
                       'default': None,
                       'values':  None, },
                      {'display': 'Paths',
                       'name': 'paths',
                       'type': 'group',
                       'dim': 2,
                       'default': None,
                       'values':  [{'display': 'XENA Port',
                                   'name': 'srcXenaPort',
                                   'type': 'str',
                                   'dim': None,
                                   'default': None,
                                   'values':  None, },
                                   {'display': 'Resource',
                                    'name': 'srcResource',
                                    'type': 'list',
                                    'dim': None,
                                    'default': _getDefaultPort,
                                    'values':  _getAllPorts, }, ], }, ], }
