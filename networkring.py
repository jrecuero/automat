#!/usr/bin/env python

import wx
import commonDialog


class NetworkRing(object):

    RESOURCE_YAML_NAME = 'networkrings'

    def __init__(self, name=None, node=None):
        self.name  = str(name) if name else None
        self.node  = str(node) if node else None

    def _toStr(self):
        return '[NETWORK RING] %s  %s' % (self.name, self.node)

    def __repr__(self):
        return self._toStr()

    def __str__(self):
        return self._toStr()

    def createDialog(self, panel, ID):
        dialog = NetworkRingDialog(panel, ID, self)
        return dialog

    def parseToYaml(self):
        result  = "\t\t%s:\n\t\t\t{\n" % self.name
        result += "\t\t\t\tnode:\t%s,\n" % self.node
        result += "\t\t\t},\n"
        return result


class NetworkRingDialog(commonDialog.CommonDialog):

    def __init__(self, parent, ID, defaults=None):
        commonDialog.CommonDialog.__init__(self, parent, ID, 'Create Network Ring', size=(400, 300), defaults=defaults)

    def createCtrl(self):
        sizer = wx.FlexGridSizer(rows=2, cols=2, hgap=5, vgap=10)
        dummy, self.nameTxtCtrl  = self.addLabelTextCtrlEntry(sizer, 'Name:  ', 'name')
        dummy, self.nodeTxtCtrl  = self.addLabelTextCtrlEntry(sizer, 'Node:  ', 'port')
        return sizer

    def GetSelection(self):
        networkRing = NetworkRing()
        networkRing.name  = str(self.nameTxtCtrl.GetValue())
        networkRing.node  = str(self.nodeTxtCtrl.GetValue())
        return networkRing
