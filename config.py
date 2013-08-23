import service
import tunnel
import accessport
import clientring
import networkring
import endpoint

RESOURCES = [service.RESOURCE,
             tunnel.RESOURCE,
             accessport.RESOURCE,
             clientring.RESOURCE,
             networkring.RESOURCE,
             endpoint.RESOURCE]

RES_TYPE_SINGLE        = 1
RES_TYPE_LIST          = 2
RES_TYPE_GROUP         = 3
RES_TYPE_SINGLE_ARRAY  = 11
RES_TYPE_LIST_ARRAY    = 12


def getResourceFromId(resId):
    result = [resource for resource in RESOURCES if resource['id'] == resId]
    return result[0] if len(result) == 1 else None


def getResourceIdFromIndex(index):
    return RESOURCES[index]['id'] if index >= 0 and index < len(RESOURCES) else None


def getResourceId(resource):
    return resource['id']


def getResourceTag(resource):
    return resource['tag']


def getResourceAttrs(resource):
    return resource['attrs']


def getResourceAttrDisplay(attr):
    return attr['display']


def getResourceAttrName(attr):
    return attr['name']


def getResourceAttrType(attr):
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
    return attr['dim']


def getResourceAttrDefault(attr):
    return attr['default']


def getResourceAttrValues(attr):
    return attr['values']


def isAttrTheAttrName(attr):
    return getResourceAttrName(attr) in ('name', )
