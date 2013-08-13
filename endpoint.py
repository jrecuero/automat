#!/usr/bin/env python

import wx
import commonDialog


class EndPoint(object):

    RESOURCE_YAML_NAME = 'endpoints'

    def __init__(self, name=None, streamid=None, service=None, flags=None):
        self.name     = str(name) if name else None
        self.streamid = int(streamid) if streamid else None
        self.service  = str(service) if service else None
        self.flags    = str(flags) if flags else None
        self.xenaport = [None, None]
        self.resource = [None, None]

    def _toStr(self):
        return '[END POINT] %s  %s  %s  %s %s %s %s %s' % (self.name, self.streamid,
                                                           self.service, self.flags,
                                                           self.xenaport[0], self.resource[0],
                                                           self.xenaport[1], self.resource[1])

    def __repr__(self):
        return self._toStr()

    def __str__(self):
        return self._toStr()

    def createDialog(self, panel, ID):
        dialog = EndPointDialog(panel, ID, self)
        return dialog

    def parseToYaml(self):
        result  = "\t\t%s:\n\t\t\t{\n" % self.name
        result += "\t\t\t\tstreamId:\t%s,\n" % self.streamid
        result += "\t\t\t\tservice:\t%s,\n" % self.service
        #result += "\t\t\t\tflags:\t%s,\n" % self.flags
        result += "\t\t\t\tpaths:\n"
        result += "\t\t\t\t[\n"
        for xenaport, resource in zip(self.xenaport, self.resource):
            result += "\t\t\t\t\t{\n"
            result += "\t\t\t\t\t\tsrcXenaPort:\t%s,\n" % xenaport
            result += "\t\t\t\t\t\tsrcResource:\t%s,\n" % resource
            result += "\t\t\t\t\t},\n"
        result += "\t\t\t\t]\n"
        result += "\t\t\t},\n"
        return result


class EndPointDialog(commonDialog.CommonDialog):

    def __init__(self, parent, ID, defaults=None):
        commonDialog.CommonDialog.__init__(self, parent, ID, 'Create End Point', size=(400, 300), defaults=defaults)

    def createCtrl(self):
        self.serviceChoices = self.GetParent().resourceHdlr.getAllServicesName()
        self.resouceChoices = self.GetParent().resourceHdlr.getAllPortsName()
        sizer = wx.FlexGridSizer(rows=8, cols=2, hgap=5, vgap=10)
        dummy, self.nameTxtCtrl     = self.addLabelTextCtrlEntry(sizer, 'Name: ', 'name')
        dummy, self.streamidTxtCtrl = self.addLabelTextCtrlEntry(sizer, 'Stream ID: ', 'streamid')
        dummy, self.serviceChoice   = self.addLabelChoiceEntry(sizer, 'Service: ', self.serviceChoices, None, 'service')
        dummy, self.flagsTxtCtrl    = self.addLabelTextCtrlEntry(sizer, 'Flags: ', 'flags')
        self.xenaportTxtCtrl = []
        self.resourceChoice  = []
        for index in xrange(2):
            dummy, self.xenaportTxtCtrl.append(self.addLabelTextCtrlEntry(sizer, 'Xena Port %s: ' % index, ('xenaport', index)))
            dummy, self.resourceChoice.append(self.addLabelChoiceEntry(sizer, 'Resource: ', self.resouceChoices, None, ('resource', index)))
        return sizer

    def OnChoiceType(self, event):
        pass

    def GetSelection(self):
        endpoint = EndPoint()
        endpoint.name      = str(self.nameTxtCtrl.GetValue())
        endpoint.streamid  = int(self.streamidTxtCtrl.GetValue())
        endpoint.service   = self.serviceChoices[self.serviceChoice.GetSelection()]
        endpoint.flags     = str(self.flagsTxtCtrl.GetValue())
        for index in xrange(2):
            endpoint.xenaport[index] = str(self.xenaportTxtCtrl[index].GetValue())
            endpoint.resource[index]  = self.resouceChoices[self.resourceChoice[index].GetSelection()]
        return endpoint
