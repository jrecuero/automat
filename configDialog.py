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
        """ Return data to be displayed in a log window.

        It returns a string with information to be displayed in edit/remove
        widget.
        """
        result  = '[%s] ' % config.getResourceTag(self._resource)
        result += '%s ' % self.name
        for data in [data for data in config.getResourceAttrs(self._resource) if data['name'] not in ('name', )]:
            if config.getResourceAttrEnable(data):
                result += '%s ' % getattr(self, data['name'], None)
        return result

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
        """ Return dictionary to be YAMLed.

        It returns the dictionary to be used to generate YAML data.
        """
        classId = config.getResourceId(self._resource)
        yamlData = {classId: {}, }
        yamlData[classId][self.name] = {}
        for attr in [attr for attr in config.getResourceAttrs(self._resource) if not config.isAttrTheAttrName(attr)]:
            attrName = config.getResourceAttrName(attr)
            if config.getResourceAttrEnable(attr):
                yamlData[classId][self.name][attrName] = getattr(self, attrName, None)
        return yamlData


class ConfigDialog(commonDialog.CommonDialog):
    """ Class with all widgets created when a new configuration entry.

    A configuration entry could be any service, access port, tunnel, end point,
    event, ... to be added as a YAML input.

    It process dictionary with data for every entry, and generates all required
    fields.
    """

    def __init__(self, parent, ID, resource, defaults=None):
        """ Class initialization method.
        """
        self.resource = resource
        self.cache    = {}
        commonDialog.CommonDialog.__init__(self, parent, ID, 'Create %s' % config.getResourceId(self.resource), size=(400, 300), defaults=defaults)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnClose(self, ev):
        self.disableAllAttributes()
        self.Destroy()

    def enableAttribute(self, attr):
        """ Enable attribute to be display in the dialog.
        
        It enables the given attribute to be displayed in the dialog, and it
        is cached internally in order to be re-initialized when dialog is
        closed.
        """
        config.setResourceAttrEnable(attr, True)
        attrName = config.getResourceAttrName(attr)
        self.cache[attrName] = attr

    def disableAttribute(self, attr):
        """ Disable attribute to be display in the dialog.
        
        It disables the given attribute to be displayed in the dialog, and it
        is removed from the cached .
        """
        config.setResourceAttrEnable(attr, False)
        attrName = config.getResourceAttrName(attr)
        del self.cache[attrName]
        
    def disableAllAttributes(self):
        """ Disable all attributes cached.
        """
        for attr in self.cache.values():
            config.setResourceAttrEnable(attr, False)
            
    def addCtrlFromResource(self, attr, index=None):
        """ Create a new control widget in the dialog.

        It process data from a new entry and it creates the proper widget for
        that. Data is coming from the resource.attribute entry.
        """
        attrName = config.getResourceAttrName(attr)
        dispName = config.getResourceAttrDisplay(attr)
        attrType = config.getResourceAttrType(attr)
        attrDim  = config.getResourceAttrDim(attr)
        attrDeps = config.getResourceAttrDeps(attr)
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
                for childAttr in [aAttr for aAttr in config.getResourceAttrValues(attr) if config.getResourceAttrEnable(aAttr)]:
                    childAttrName = config.getResourceAttrName(childAttr)
                    lbl[i][childAttrName], ctrl[i][childAttrName] = self.addCtrlFromResource(childAttr, i)
        return (lbl, ctrl)

    def createCtrl(self):
        """ Creates all widgets for a given resource.

        It creates all widget for all attributes in the given resource.
        """
        self.sizer = wx.FlexGridSizer(rows=len(config.getResourceAttrs(self.resource)), cols=2, hgap=5, vgap=10)
        self.lbl, self.ctrl = {}, {}
        for attr in config.getResourceAttrs(self.resource):
            if config.getResourceAttrEnable(attr):
                attrName = config.getResourceAttrName(attr)
                self.lbl[attrName], self.ctrl[attrName] = self.addCtrlFromResource(attr)
        return self.sizer

    def createNewCtrl(self, attr):
        """ Create a new control on the fly.

        It creates a new control when dialog has been already created and
        populated
        """
        attrName = config.getResourceAttrName(attr)
        if not hasattr(self.lbl, attrName) and not hasattr(self.ctrl, attrName):
            self.lbl[attrName], self.ctrl[attrName] = self.addCtrlFromResource(attr)
            self.sizer.Layout()
            self.Fit()
            self.Refresh()
            self.Update()

    def removeNewCtrl(self, attr):
        """ Remove a new control on the fly.

        It removes a new control that was created when the dialog was already
        created and populated.
        """
        attrName = config.getResourceAttrName(attr)
        if attrName in self.lbl and attrName in self.ctrl:
            self.sizer.Remove(self.lbl[attrName])
            self.sizer.Remove(self.ctrl[attrName])
            self.lbl[attrName].Destroy()
            self.ctrl[attrName].Destroy()
            del self.lbl[attrName]
            del self.ctrl[attrName]
            self.sizer.Layout()
            self.Fit()

    def createNewField(self, dep, newField):
        """ Create a new field on the fly.

        It creates a new field when conditions are met.
        """
        if not config.getResourceAttrDepsEnable(dep):
            # Create new dialog entry here.
            config.setResourceAttrDepsEnable(dep, True)
            handler = config.getResourceAttrDepsHandler(dep)
            newAttr = config.lookForResourceAttrWithName(self.resource, newField)
            if newAttr:
                self.enableAttribute(newAttr)
                config.setResourceAttrValues(newAttr, handler)
                self.createNewCtrl(newAttr)

    def removeNewField(self, dep, newField):
        """ Remote a new field on the fly.

        It removes a new field already created when conditions are not met.
        """
        if config.getResourceAttrDepsEnable(dep):
            # Delete dialog entry here, because conditions are not met.
            config.setResourceAttrDepsEnable(dep, False)
            oldAttr = config.lookForResourceAttrWithName(self.resource, newField)
            if oldAttr:
                self.disableAttribute(oldAttr)
                config.setResourceAttrValues(oldAttr, None)
                self.removeNewCtrl(oldAttr)

    def OnTextCtrlAction(self, ev):
        """ Check if there are any condition to be met.

        It checks if the input field has any dependency, and proceed to create
        or remove fields when those dependencies are met or broken.
        """
        evObj = ev.GetEventObject()
        if evObj.customData is None:
            return
        for dep in evObj.customData:
            fields   = config.getResourceAttrDepsFields(dep)
            newField = config.getResourceAttrDepsNewField(dep)
            for field, fieldValue in fields.iteritems():
                if self.ctrl[field].GetValue() not in fieldValue:
                    break
            else:
                self.createNewField(dep, newField)
                continue

            self.removeNewField(dep, newField)

    def getSelectionFromResource(self, attr, ctrl):
        """ Get the data entered for a given attribute.

        It returns the dialog values entered by the user for the given
        attribute.
        """
        dicta = []
        attrName = config.getResourceAttrName(attr)
        attrType = config.getResourceAttrType(attr)
        attrDim  = config.getResourceAttrDim(attr)
        if attrName not in ctrl:
            return
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
        """ Collect all dialog input data.

        It collects all information entered in the dialog for every widget and
        it creates an instance that contain that data to be used for YAML code
        generation.
        """
        # This will be the new way to pass the data retrieved from the dialog.
        dictToEntity = {}
        for attr in config.getResourceAttrs(self.resource):
            attrName = config.getResourceAttrName(attr)
            dictToEntity[attrName] = self.getSelectionFromResource(attr, self.ctrl)

        self.disableAllAttributes()
        entity = Entity(self.resource, dictToEntity)
        return entity
