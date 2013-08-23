import service
import tunnel
import accessport
#import clientring
#import networkring
#import endpoint
import event
import config
import yaml


class ResourceHandler(object):

    def __init__(self, widget=None, resources=[]):
        self.widget    = widget
        self.resources = resources

    def addResource(self, resource):
        self.resources.append(resource)
        self.widget.Append(str(resource))

    def replaceResource(self, resource, selection):
        self.resources[selection] = resource
        self.widget.Delete(selection)
        self.widget.InsertItems([str(resource), ], selection)

    def deleteResource(self, selection):
        del self.resources[selection]
        self.widget.Delete(selection)

    def getAllResourcesOf(self, resourceId):
        return [resource for resource in self.resources if resourceId in resource.getResourceId()]

    def getYamlDictForAllResourcesOf(self, resourceId):
        resourceTag  = config.getResourceTag(config.getResourceFromId(resourceId))
        resourceList = [resource.getYamlDict()[resourceId]
                        for resource in self.resources if resourceId in resource.getResourceId()]
        return {resourceTag: resourceList} if resourceList else {}

    def getAllEvents(self):
        return self.getYamlDictForAllResourcesOf(event.Event)

    def parseToYaml(self, resourceList):
        result = ""
        if resourceList:
            result += yaml.dump(resourceList, default_flow_style=False)
        return result

    def parseToYamlForAll(self, resourceClass):
        return self.parseToYaml(self.getYamlDictForAllResourcesOf(resourceClass))

    def parseToYamlForAllEvents(self):
        return self.parseToYaml(self.getAllEvents())

    def getAllServicesName(self):
        return [resource.getResourceName() for resource in self.getAllResourcesOf(service.getResourceId())]

    def getAllTunnelsName(self):
        return [resource.getResourceName() for resource in self.getAllResourcesOf(tunnel.getResourceId())]

    def getAllAccessPortsName(self):
        return [resource.getResourceName() for resource in self.getAllResourcesOf(accessport.getResourceId())]

    def getAllPortsName(self):
        return self.getAllTunnelsName() + self.getAllAccessPortsName()
