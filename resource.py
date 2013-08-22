import service
import tunnel
import accessport
import clientring
import networkring
import endpoint
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
        #return [resource for resource in self.resources if isinstance(resource, resourceClass)]
        resourceTag  = config.getResourceTag(config.getResourceFromId(resourceId))
        resourceList = [resource.getYamlDict()[resourceId] 
                        for resource in self.resources if resourceId in resource.getResourceId()]
        return {resourceTag: resourceList} if resourceList else {}

#     def getAllServices(self):
#         #return self.getYamlDictForAllResourcesOf(service.Service)
#         return self.getYamlDictForAllResourcesOf("services")
# 
#     def getAllTunnels(self):
#         #return self.getYamlDictForAllResourcesOf(tunnel.Tunnel)
#         return self.getYamlDictForAllResourcesOf("tunnels")
# 
#     def getAllAccessPorts(self):
#         #return self.getYamlDictForAllResourcesOf(accessport.AccessPort)
#         return self.getYamlDictForAllResourcesOf("accessports")
# 
#     def getAllClientRings(self):
#         return self.getYamlDictForAllResourcesOf(clientring.ClientRing)
# 
#     def getAllNetworkRings(self):
#         return self.getYamlDictForAllResourcesOf(networkring.NetworkRing)
# 
#     def getAllEndPoints(self):
#         return self.getYamlDictForAllResourcesOf(endpoint.EndPoint)
    
    def getAllEvents(self):
        return self.getYamlDictForAllResourcesOf(event.Event)

    def parseToYaml(self, resourceList):
        result = ""
        if resourceList:
#             result = "%s:\n\t[\n" % (resourceList[0].RESOURCE_YAML_NAME, )
#             for resource in resourceList:
#                 result += resource.parseToYaml()
#             result += "\t]\n"
            result += yaml.dump(resourceList, default_flow_style=False)
        return result
    
    def parseToYamlForAll(self, resourceClass):
        return self.parseToYaml(self.getYamlDictForAllResourcesOf(resourceClass))

#     def parseToYamlForAllServices(self):
#         return self.parseToYaml(self.getAllServices())
# 
#     def parseToYamlForAllTunnels(self):
#         return self.parseToYaml(self.getAllTunnels())
# 
#     def parseToYamlForAllAccessPorts(self):
#         return self.parseToYaml(self.getAllAccessPorts())
# 
#     def parseToYamlForAllClientRings(self):
#         return self.parseToYaml(self.getAllClientRings())
# 
#     def parseToYamlForAllNetworkRings(self):
#         return self.parseToYaml(self.getAllNetworkRings())
# 
#     def parseToYamlForAllEndPoints(self):
#         return self.parseToYaml(self.getAllEndPoints())
    
    def parseToYamlForAllEvents(self):
        return self.parseToYaml(self.getAllEvents())    

    def getAllServicesName(self):
#         return [resource.name for resource in self.getAllServices()]
        return [resource.getResourceName() for resource in self.getAllResourcesOf(service.getResourceId())]
    
    def getAllTunnelsName(self):
#         return [resource.name for resource in self.getAllTunnels()]
        return [resource.getResourceName() for resource in self.getAllResourcesOf(tunnel.getResourceId())]

    def getAllAccessPortsName(self):
#         return [resource.name for resource in self.getAllAccessPorts()]
        return [resource.getResourceName() for resource in self.getAllResourcesOf(accessport.getResourceId())]

    def getAllPortsName(self):
        return self.getAllTunnelsName() + self.getAllAccessPortsName()
