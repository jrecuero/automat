import service
import tunnel
import accessport
import clientring
import networkring
import oid
import endpoint
import event

RESOURCES = [service.RESOURCE,
             tunnel.RESOURCE,
             accessport.RESOURCE,
             clientring.RESOURCE,
             networkring.RESOURCE,
             oid.RESOURCE,
             endpoint.RESOURCE,
             event.RESOURCE, ]

RES_TYPE_SINGLE        = 1
RES_TYPE_LIST          = 2
RES_TYPE_GROUP         = 3
RES_TYPE_SINGLE_ARRAY  = 11
RES_TYPE_LIST_ARRAY    = 12


def getResourceFromId(resId):
    """ Return resource entry for a given ID.
    """
    result = [resource for resource in RESOURCES if resource['id'] == resId]
    return result[0] if len(result) == 1 else None


def getResourceIdFromIndex(index):
    """ Return resource entry for a given index.
    """
    return RESOURCES[index]['id'] if index >= 0 and index < len(RESOURCES) else None


def getResourceId(resource):
    """ Return ID for a given resource.
    """
    return resource['id']


def getResourceTag(resource):
    """ Return YAML tag for a given resource.
    """
    return resource['tag']


def getResourceAttrs(resource):
    """ Return all attributes for a given resource.
    """
    return resource['attrs']


def getResourceAttrDisplay(attr):
    """ Return attribute display name for a given attribute.
    """
    return attr['display']


def getResourceAttrName(attr):
    """ Return attribute name for a given attribute.
    """
    return attr['name']


def getResourceAttrType(attr):
    """ Return attribute type for a given attribute.
    """
    resType = attr['type']
    resDim  = attr['dim']
    if resType in ('int', 'str') and not resDim:
        return RES_TYPE_SINGLE
    elif resType in ('list', ) and not resDim:
        return RES_TYPE_LIST
    elif resType in ('int', 'str') and resDim:
        return RES_TYPE_SINGLE_ARRAY
    elif resType in ('list', ) and resDim:
        return RES_TYPE_LIST_ARRAY
    elif resType in ('group', ) and resDim:
        return RES_TYPE_GROUP
    else:
        return None


def getResourceAttrDim(attr):
    """ Return attribute dimension for a given attribute.
    """
    return attr['dim']


def getResourceAttrDefault(attr):
    """ Return attribute default value for a given attribute.
    """
    return attr['default']


def getResourceAttrValues(attr):
    """ Return attribute possible values for a given attribute.
    """
    return attr['values']


def setResourceAttrValues(attr, value):
    """ Set attrribute possible values for a given attribute.
    """
    attr['values'] = value


def getResourceAttrEnable(attr):
    """ Return if attribute is enable or not for a given attribute.
    """
    return attr.setdefault('enable', True)


def setResourceAttrEnable(attr, value):
    """ Set if attribute is enable or not for a given attribute.
    """
    attr['enable'] = value


def getResourceAttrDeps(attr):
    """ Return all attribute dependencies for a given attribute.
    """
    return attr.setdefault('deps', [])


def getResourceAttrDepsFields(dep):
    """ Return all fields for a given dependency.
    """
    return dep.setdefault('fields', {})


def getResourceAttrDepsHandler(dep):
    """ Return (values) handler for a given dependency.
    """
    return dep.setdefault('handler', None)


def getResourceAttrDepsNewField(dep):
    """ Return new field to be created for a given dependency.
    """
    return dep.setdefault('newfield', None)


def getResourceAttrDepsEnable(dep):
    """ Return if dependency has been met or not for a given dependency.
    """
    return dep.setdefault('enable', False)


def setResourceAttrDepsEnable(dep, value):
    """ Set if a dependency has been met or not for a given dependency.
    """
    dep['enable'] = value


def isAttrTheAttrName(attr):
    """ Check if the given attribute is the attribute 'name' for a resource.
    """
    return getResourceAttrName(attr) in ('name', )


def lookForResourceAttrWithName(resource, attrName):
    """ Look for a resource with the given name.
    """
    for attr in getResourceAttrs(resource):
        if attrName == getResourceAttrName(attr):
            return attr
    return None
