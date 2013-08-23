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

    def addCtrlFromResource(self, attr, index=None):
        attrName = config.getResourceAttrName(attr)
        dispName = config.getResourceAttrDisplay(attr)
        attrType = config.getResourceAttrType(attr)
        attrDim  = config.getResourceAttrDim(attr)
        attrDeps = config.getResourceAttrDim(attr)
        lbl, ctrl = [], []
        if attrType in (config.RES_TYPE_SINGLE, ):
            lbl, ctrl = self.addLabelTextCtrlEntry(self.sizer,
                                                   '%s: ' % dispName,
                                                   fieldName=attrName if index is None else (attrName, index),
                                                   data=attrDeps)
            self.Bind(wx.EVT_TEXT, self.OnTextCtrlAction, ctrl)
        elif attrType in (config.RES_TYPE_LIST, ):
            lbl, ctrl = self.addLabelChoiceEntry(self.sizer,
                                                 '%s: ' % dispName,
                                                 choices=config.getResourceAttrValues(attr)(self),
                                                 initSel=config.getResourceAttrDefault(attr)(self),
                                                 fieldName=attrName if index is None else (attrName, index),
                                                 data=attrDeps)
        elif attrType in (config.RES_TYPE_SINGLE_ARRAY, ):
            for i in xrange(attrDim):
                lbl, aCtrl = self.addLabelTextCtrlEntry(self.sizer,
                                                        '%s [%s]: ' % (dispName, i),
                                                        attrName if index is None else (attrName, index),
                                                        data=attrDeps)
                ctrl.append(aCtrl)
                self.Bind(wx.EVT_TEXT, self.OnTextCtrlAction, aCtrl)
        elif attrType in (config.RES_TYPE_LIST_ARRAY, ):
            for i in xrange(attrDim):
                lbl, aCtrl = self.addLabelChoiceEntry(self.sizer,
                                                      '%s [%s]: ' % (dispName, i),
                                                      choices=config.getResourceAttrValues(attr)(self),
                                                      initSel=config.getResourceAttrDefault(attr)(self),
                                                      fieldName=attrName if index is None else (attrName, index),
                                                      data=attrDeps)
                self.ctrl.append(aCtrl)
        elif attrType in (config.RES_TYPE_GROUP, ):
            for i in xrange(attrDim):
                lbl.append({})
                ctrl.append({})
                for childAttr in [aAttr for aAttr in config.getResourceAttrValues(attr) if self.isAttrEnable(aAttr)]:
                    childAttrName = config.getResourceAttrName(childAttr)
                    lbl[i][childAttrName], ctrl[i][childAttrName] = self.addCtrlFromResource(childAttr, i)
        return (lbl, ctrl)

    def isAttrEnable(self, attr):
        return  config.getResourceAttrEnable(attr)

    def createCtrl(self):
        self.sizer = wx.FlexGridSizer(rows=len(config.getResourceAttrs(self.resource)), cols=2, hgap=5, vgap=10)
        self.lbl, self.ctrl = {}, {}
        for attr in config.getResourceAttrs(self.resource):
            if self.isAttrEnable(attr):
                attrName = config.getResourceAttrName(attr)
                self.lbl[attrName], self.ctrl[attrName] = self.addCtrlFromResource(attr)
        return self.sizer

    def createNewCtrl(self, attr):
        attrName = config.getResourceAttrName(attr)
        if not hasattr(self.lbl, attrName) and not hasattr(self.ctrl, attrName):
            self.lbl[attrName], self.ctrl[attrName] = self.addCtrlFromResource(attr)
            self.sizer.Layout()
            self.Fit()
            self.Refresh()
            self.Update()
            self.Thaw()

    def removeNewCtrl(self, attr):
        attrName = config.getResourceAttrName(attr)
        if hasattr(self.lbl, attrName) and hasattr(self.ctrl, attrName):
            self.sizer.Remove(self.lbl[attrName])
            self.sizer.Remove(self.ctrl[attrName])
            self.lbl[attrName].Destroy()
            self.ctrl[attrName].Destroy()
            del self.lbl[attrName]
            del self.ctrl[attrName]
            self.sizer.Layout()
            self.Fit()

    def OnTextCtrlAction(self, ev):
        evObj = ev.GetEventObject()
        for dep in evObj.customData:
            fields   = config.getResourceAttrDepsFields(dep)
            handler  = config.getResourceAttrDepsHandler(dep)
            newField = config.getResourceAttrDepsHandler(dep)
            for field, fieldValue in fields.iteritems():
                if self.ctrl[field].GetValue() not in fieldValue:
                    continue
            print fields, handler, newField
            newAttr = config.lookForResourceAtttWithName(self.resource, newField)
            if newAttr:
                self.createNewCtrl(newAttr)

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
