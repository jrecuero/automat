import service
import tunnel
import accessport
import event
import config
import yaml


class ResourceHandler(object):
    """ ResouceHandler class handles resources in the main Frame.
    """

    def __init__(self, widget=None, resources=[]):
        """ ResourceHandler initialization method.
        """
        self.widget    = widget
        self.resources = resources

    def addResource(self, resource):
        """ Add a new resource.

        It adds a new resouce to the database and to the widget.
        """
        self.resources.append(resource)
        self.widget.Append(str(resource))

    def replaceResource(self, resource, selection):
        """ Replace a resource.

        It replaces a resource in the database and in the widget.
        """
        self.resources[selection] = resource
        self.widget.Delete(selection)
        self.widget.InsertItems([str(resource), ], selection)

    def deleteResource(self, selection):
        """ Delete a resource.

        It deletes a resource from the database and from the widget.
        """
        del self.resources[selection]
        self.widget.Delete(selection)

    def getAllResourcesOf(self, resourceId):
        """ Get all resources for a given resource ID.

        It returns all resources in the database with the same resource ID.
        """
        return [resource for resource in self.resources if resourceId in resource.getResourceId()]

    def getYamlDictForAllResourcesOf(self, resourceId):
        """ Get a dictionary with all resources with data to be YAMLed.

        It returns a dictionary with data that can be processed by the yaml module.
        """
        resourceTag  = config.getResourceTag(config.getResourceFromId(resourceId))
        resourceList = [resource.getYamlDict()[resourceId]
                        for resource in self.resources if resourceId in resource.getResourceId()]
        return {resourceTag: resourceList} if resourceList else {}

    def getAllEvents(self):
        return self.getYamlDictForAllResourcesOf(event.Event)

    def parseToYaml(self, resourceList):
        """ Generate YAML data for a list of resources.
        """
        result = ""
        if resourceList:
            result += yaml.dump(resourceList, default_flow_style=False)
        return result

    def parseToYamlForAll(self, resourceId):
        """ Parse to YAML format for all resources witht the given resource ID.
        """
        return self.parseToYaml(self.getYamlDictForAllResourcesOf(resourceId))

    def parseToYamlForAllEvents(self):
        return self.parseToYaml(self.getAllEvents())

    def getAllServicesName(self):
        """ Get all Services Names in the database.
        """
        return [resource.getResourceName() for resource in self.getAllResourcesOf(service.getResourceId())]

    def getAllTunnelsName(self):
        """ Get all Tunnels Names in the database.
        """
        return [resource.getResourceName() for resource in self.getAllResourcesOf(tunnel.getResourceId())]

    def getAllAccessPortsName(self):
        """ Get all Access Ports Names in the database.
        """
        return [resource.getResourceName() for resource in self.getAllResourcesOf(accessport.getResourceId())]

    def getAllPortsName(self):
        """ Get all ports names in the database.

        It retrieves all tunnels and access ports names.
        """
        return self.getAllTunnelsName() + self.getAllAccessPortsName()
