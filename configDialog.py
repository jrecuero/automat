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
                self._expandAttrList(attrVal)

    def _expandAttrList(self, attrVal):
        """ Expand a list as attributes.

        This method takes a list of entries, and for every one, it creates
        attributes in the object.
        List is an array, and every entry in the array is a dictionary, where
        the key will be the attribute and the value will be the attribute value.
        """
        if isinstance(attrVal, list):
            for k, v in [(k, v) for value in attrVal for (k, v) in value.iteritems()]:
                if not hasattr(self, k):
                    setattr(self, k, [])
                getattr(self, k).append(v)

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

    def addCtrlFromResource(self, sizer, attr, index=None):
        attrName = config.getResourceAttrName(attr)
        dispName = config.getResourceAttrDisplay(attr)
        attrType = config.getResourceAttrType(attr)
        attrDim  = config.getResourceAttrDim(attr)
        ctrl = []
        if attrType in (config.RES_TYPE_SINGLE, ):
            dummy, ctrl = self.addLabelTextCtrlEntry(sizer,
                                                     '%s: ' % dispName,
                                                     attrName if index is None else (attrName, index))
        elif attrType in (config.RES_TYPE_LIST, ):
            dummy, ctrl = self.addLabelChoiceEntry(sizer,
                                                   '%s: ' % dispName,
                                                   config.getResourceAttrValues(attr)(self),
                                                   config.getResourceAttrDefault(attr)(self),
                                                   attrName if index is None else (attrName, index))
        elif attrType in (config.RES_TYPE_SINGLE_ARRAY, ):
            for index in xrange(attrDim):
                dummy, aCtrl = self.addLabelTextCtrlEntry(sizer,
                                                          '%s [%s]: ' % (dispName, index),
                                                          attrName if index is None else (attrName, index))
                ctrl.append(aCtrl)
        elif attrType in (config.RES_TYPE_LIST_ARRAY, ):
            for index in xrange(attrDim):
                dummy, aCtrl = self.addLabelChoiceEntry(sizer,
                                                        '%s [%s]: ' % (dispName, index),
                                                        config.getResourceAttrValues(attr)(self),
                                                        config.getResourceAttrDefault(attr)(self),
                                                        attrName if index is None else (attrName, index))
                self.ctrl.append(aCtrl)
        elif attrType in (config.RES_TYPE_GROUP, ):
            for index in xrange(attrDim):
                ctrl.append({})
                for childAttr in config.getResourceAttrValues(attr):
                    childAttrName = config.getResourceAttrName(childAttr)
                    ctrl[index][childAttrName] = self.addCtrlFromResource(sizer, childAttr, index)
        return ctrl

    def createCtrl(self):
        sizer = wx.FlexGridSizer(rows=len(config.getResourceAttrs(self.resource)), cols=2, hgap=5, vgap=10)
        self.ctrl = {}
        for attr in config.getResourceAttrs(self.resource):
            attrName = config.getResourceAttrName(attr)
            self.ctrl[attrName] = self.addCtrlFromResource(sizer, attr)
        return sizer

    def getSelectionFromResource(self, attr, ctrl):
        dicta = []
        attrName = config.getResourceAttrName(attr)
        attrType = config.getResourceAttrType(attr)
        attrDim  = config.getResourceAttrDim(attr)
        if attrType in (config.RES_TYPE_SINGLE, ):
            dicta = str(ctrl[attrName].GetValue())
        elif attrType in (config.RES_TYPE_LIST, ):
            dicta = config.getResourceAttrValues(attr)(self)[ctrl[attrName].GetSelection()]
        elif attrType in (config.RES_TYPE_SINGLE_ARRAY, ):
            for index in xrange(attrDim):
                dicta.append(str(ctrl[attrName][index].GetValue()))
        elif attrType in (config.RES_TYPE_LIST_ARRAY, ):
            for index in xrange(attrDim):
                dicta.append(config.getResourceAttrValues(attr)(self)[ctrl[attrName][index].GetSelection()])
        elif attrType in (config.RES_TYPE_GROUP, ):
            for index in xrange(attrDim):
                dicta.append({})
                for childAttr in config.getResourceAttrValues(attr):
                    childAttrName = config.getResourceAttrName(childAttr)
                    dicta[index][childAttrName] = self.getSelectionFromResource(childAttr, self.ctrl[attrName][index])
        return dicta

    def GetSelection(self):

        # This will be the new way to pass the data retrieved from the dialog.
        dictToEntity = {}
        for attr in config.getResourceAttrs(self.resource):
            attrName = config.getResourceAttrName(attr)
            dictToEntity[attrName] = self.getSelectionFromResource(attr, self.ctrl)

        entity = Entity(self.resource, dictToEntity)
        return entity
