#!/usr/bin/env python

import wx
import commonDialog


def parseToYaml(accessPortList):
    result = "accessports:\n\t[\n"
    for accessPort in accessPortList:
        result += "\t\t%s:\n\t\t\t{\n" % accessPort.name
        result += "\t\t\t\tnode:\t%s,\n" % accessPort.node
        result += "\t\t\t\tvlans:\t%s,\n" % accessPort.vlans
        result += "\t\t\t\tport:\t%s,\n" % accessPort.port
        result += "\t\t\t},\n"
    result += "\t]\n"
    return result


class AccessPort(object):

    RESOURCE_YAML_NAME = 'accessports'

    def __init__(self, name=None, vlans=None, port=None, node=None):
        self.name  = str(name) if name else None
        self.vlans = str(vlans) if vlans else None
        self.port  = int(port) if port else None
        self.node  = str(node) if node else None

    def _toStr(self):
        return '[ACCESS PORT] %s  %s  %s %s' % (self.name, self.vlans, self.port, self.node)

    def __repr__(self):
        return self._toStr()

    def __str__(self):
        return self._toStr()

    def createDialog(self, panel, ID):
        dialog = AccessPortDialog(panel, ID, self)
        return dialog

    def parseToYaml(self):
        result  = "\t\t%s:\n\t\t\t{\n" % self.name
        result += "\t\t\t\tnode:\t%s,\n" % self.node
        result += "\t\t\t\tvlans:\t%s,\n" % self.vlans
        result += "\t\t\t\tport:\t%s,\n" % self.port
        result += "\t\t\t},\n"
        return result


class AccessPortDialog(commonDialog.CommonDialog):

    def __init__(self, parent, ID, defaults=None):
        commonDialog.CommonDialog.__init__(self, parent, ID, 'Create Access Port', size=(400, 300), defaults=defaults)

    def createCtrl(self):
        sizer = wx.FlexGridSizer(rows=6, cols=2, hgap=5, vgap=10)
        dummy, self.nameTxtCtrl  = self.addLabelTextCtrlEntry(sizer, 'Name:  ', 'name')
        dummy, self.vlansTxtCtrl = self.addLabelTextCtrlEntry(sizer, 'Vlans: ', 'vlans')
        dummy, self.portTxtCtrl  = self.addLabelTextCtrlEntry(sizer, 'Port:  ', 'port')
        dummy, self.nodeTxtCtrl  = self.addLabelTextCtrlEntry(sizer, 'Node:  ', 'port')
        return sizer

    def GetSelection(self):
        accessport = AccessPort()
        accessport.name  = str(self.nameTxtCtrl.GetValue())
        accessport.vlans = str(self.vlansTxtCtrl.GetValue())
        accessport.port  = str(self.portTxtCtrl.GetValue())
        accessport.node  = str(self.nodeTxtCtrl.GetValue())
        return accessport
