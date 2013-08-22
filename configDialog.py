import wx
import commonDialog
import config


class Entity(object):

    def __init__(self, resource, attributes=None):
        self._resource = resource
        if attributes:
            for key, val in attributes.iteritems():
                attrVal = val if not isinstance(val, list) else [valItem for valItem in val] 
                setattr(self, key, attrVal)
                
    def getResourceId(self):
        return config.getResourceId(self._resource)
    
    def getResourceTag(self):
        return config.getResourceTag(self._resource)
    
    def getResourceName(self):
        return self.name
    
    def getData(self):
        result  = '[%s] ' % config.getResourceTag(self._resource)
        result += '%s ' % self.name
        for data in [data for data in config.getResourceAttrs(self._resource) if data['name'] not in ('name', )]:
            result += '%s ' % getattr(self, data['name'], None)
        return result
        #return self.getYamlDict()

    def _toStr(self):
        return str(self.getData())

    def __repr__(self):
        return self._toStr()

    def __str__(self):
        return self._toStr()

    def createDialog(self, panel, ID):
        dialog = ConfigDialog(panel, ID, self._resource, self)
        return dialog
    
    def getYamlDict(self):
        classId = config.getResourceId(self._resource)
        yamlData = {classId: {}, }
        yamlData[classId][self.name] = {}
        for attr in [attr for attr in config.getResourceAttrs(self._resource) if not config.isAttrTheAttrName(attr)]:
            attrName = config.getResourceAttrName(attr)
            yamlData[classId][self.name][attrName] = getattr(self, attrName, None)
        return yamlData


class ConfigDialog(commonDialog.CommonDialog):

    def __init__(self, parent, ID, resource, defaults=None):
        self.resource = resource
        commonDialog.CommonDialog.__init__(self, parent, ID, 'Create %s' % config.getResourceId(self.resource), size=(400, 300), defaults=defaults)

    def createCtrl(self):
        sizer = wx.FlexGridSizer(rows=len(config.getResourceAttrs(self.resource)), cols=2, hgap=5, vgap=10)
        self.ctrl = {}
        for attr in config.getResourceAttrs(self.resource):
            attrName = config.getResourceAttrName(attr)
            dispName = config.getResourceAttrDisplay(attr)
            attrType = config.getResourceAttrType(attr)
            attrDim  = config.getResourceAttrDim(attr)
            if attrType in (config.RES_TYPE_SINGLE, ):
                dummy, self.ctrl[attrName] = self.addLabelTextCtrlEntry(sizer, '%s: ' % dispName, attrName)
            elif attrType in (config.RES_TYPE_LIST, ):
                dummy, self.ctrl[attrName]  = self.addLabelChoiceEntry(sizer,
                                                                       '%s: ' % dispName,
                                                                       config.getResourceAttrValues(attr)(self),
                                                                       config.getResourceAttrDefault(attr)(self),
                                                                       attrName)
            elif attrType in (config.RES_TYPE_SINGLE_ARRAY, ):
                self.ctrl[attrName] = []
                for index in xrange(attrDim):
                    dummy, ctrl = self.addLabelTextCtrlEntry(sizer, 
                                                             '%s [%s]: ' % (dispName, index), 
                                                             attrName)
                    self.ctrl[attrName].append(ctrl)
            elif attrType in (config.RES_TYPE_LIST_ARRAY, ):
                self.ctrl[attrName] = []
                for index in xrange(attrDim):
                    dummy, ctrl = self.addLabelChoiceEntry(sizer, 
                                                           '%s [%s]: ' % (dispName, index), 
                                                           config.getResourceAttrValues(attr)(self),
                                                           config.getResourceAttrDefault(attr)(self),
                                                           attrName)
                    self.ctrl[attrName].append(ctrl)
        return sizer

    def GetSelection(self):
#         yamlData = {self.classId: {}, }
#         resourceName = str(self.ctrl['name'].GetValue())
#         yamlData[self.classId][resourceName] = {}
#         for data in [data for data in self.configDict if data['attr-name'] not in ('name', )]:
#             attrName = data['attr-name']
#             attrType = data['attr-type']
#             if attrType in ('int', 'str', ):
#                 yamlData[self.classId][resourceName][attrName] = str(self.ctrl[attrName].GetValue())
#             elif attrType in ('list', ):
#                 yamlData[self.classId][resourceName][attrName] = data['range'][self.ctrl[attrName].GetSelection()] 
            
        # This will be the new way to pass the data retrieved from the dialog.
        dictToEntity = {}    
        for attr in config.getResourceAttrs(self.resource):
            attrName = config.getResourceAttrName(attr)
            attrType = config.getResourceAttrType(attr)
            attrDim  = config.getResourceAttrDim(attr)
            if attrType in (config.RES_TYPE_SINGLE, ):
                dictToEntity[attrName] = str(self.ctrl[attrName].GetValue())
            elif attrType in (config.RES_TYPE_LIST, ):
                dictToEntity[attrName] = config.getResourceAttrValues(attr)(self)[self.ctrl[attrName].GetSelection()] 
            elif attrType in (config.RES_TYPE_SINGLE_ARRAY, ):
                dictToEntity[attrName] = []
                for index in xrange(attrDim):
                    dictToEntity[attrName].append(str(self.ctrl[attrName][index].GetValue()))
            elif attrType in (config.RES_TYPE_LIST_ARRAY, ):
                dictToEntity[attrName] = []
                for index in xrange(attrDim):
                    dictToEntity[attrName].append(config.getResourceAttrValues(attr)(self)[self.ctrl[attrName][index].GetSelection()])
                            
        entity = Entity(self.resource, dictToEntity)
        return entity
