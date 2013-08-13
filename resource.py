import service
import tunnel
import accessport
import clientring
import networkring
import endpoint
import event


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

    def getAllResourcesOf(self, resourceClass):
        return [resource for resource in self.resources if isinstance(resource, resourceClass)]

    def getAllServices(self):
        return self.getAllResourcesOf(service.Service)

    def getAllTunnels(self):
        return self.getAllResourcesOf(tunnel.Tunnel)

    def getAllAccessPorts(self):
        return self.getAllResourcesOf(accessport.AccessPort)

    def getAllClientRings(self):
        return self.getAllResourcesOf(clientring.ClientRing)

    def getAllNetworkRings(self):
        return self.getAllResourcesOf(networkring.NetworkRing)

    def getAllEndPoints(self):
        return self.getAllResourcesOf(endpoint.EndPoint)
    
    def getAllEvents(self):
        return self.getAllResourcesOf(event.Event)

    def parseToYaml(self, resourceList):
        result = ""
        if resourceList:
            result = "%s:\n\t[\n" % (resourceList[0].RESOURCE_YAML_NAME, )
            for resource in resourceList:
                result += resource.parseToYaml()
            result += "\t]\n"
        return result

    def parseToYamlForAllServices(self):
        return self.parseToYaml(self.getAllServices())

    def parseToYamlForAllTunnels(self):
        return self.parseToYaml(self.getAllTunnels())

    def parseToYamlForAllAccessPorts(self):
        return self.parseToYaml(self.getAllAccessPorts())

    def parseToYamlForAllClientRings(self):
        return self.parseToYaml(self.getAllClientRings())

    def parseToYamlForAllNetworkRings(self):
        return self.parseToYaml(self.getAllNetworkRings())

    def parseToYamlForAllEndPoints(self):
        return self.parseToYaml(self.getAllEndPoints())
    
    def parseToYamlForAllEvents(self):
        return self.parseToYaml(self.getAllEvents())

    def getAllServicesName(self):
        return [resource.name for resource in self.getAllServices()]

    def getAllTunnelsName(self):
        return [resource.name for resource in self.getAllTunnels()]

    def getAllAccessPortsName(self):
        return [resource.name for resource in self.getAllAccessPorts()]

    def getAllPortsName(self):
        return self.getAllTunnelsName() + self.getAllAccessPortsName()
