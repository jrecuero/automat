#!/usr/bin/env python

import wx
import commonDialog


def parseToYaml(tunnelList):
    result = "tunnels:\n\t[\n"
    for tunnel in tunnelList:
        result += "\t\t%s:\n\t\t\t{\n" % tunnel.name
        result += "\t\t\t\tnode:\t%s,\n" % tunnel.node
        result += "\t\t\t\tbvid:\t%s,\n" % tunnel.bvid
        result += "\t\t\t\tport:\t%s,\n" % tunnel.port
        result += "\t\t\t\tbsa: \t%s,\n" % tunnel.bsa
        result += "\t\t\t\tbda: \t%s,\n" % tunnel.bda
        result += "\t\t\t},\n"
    result += "\t]\n"
    return result


class Tunnel(object):

    RESOURCE_YAML_NAME = 'tunnels'

    def __init__(self, name=None, bvid=None, port=None, bsa=None, bda=None, node=None):
        self.name = str(name) if name else None
        self.bvid = str(bvid) if bvid else None
        self.port = int(port) if port else None
        self.bsa  = int(bsa) if bsa else None
        self.bda  = int(bda) if bda else None
        self.node = str(node) if node else None

    def _toStr(self):
        return '[TUNNEL] %s  %s  %s  %s %s %s' % (self.name, self.bvid, self.port, self.bsa, self.bda, self.node)

    def __repr__(self):
        return self._toStr()

    def __str__(self):
        return self._toStr()

    def createDialog(self, panel, ID):
        dialog = TunnelDialog(panel, ID, self)
        return dialog

    def parseToYaml(self):
        result  = "\t\t%s:\n\t\t\t{\n" % self.name
        result += "\t\t\t\tnode:\t%s,\n" % self.node
        result += "\t\t\t\tbvid:\t%s,\n" % self.bvid
        result += "\t\t\t\tport:\t%s,\n" % self.port
        result += "\t\t\t\tbsa: \t%s,\n" % self.bsa
        result += "\t\t\t\tbda: \t%s,\n" % self.bda
        result += "\t\t\t},\n"
        return result


class TunnelDialog(commonDialog.CommonDialog):

    def __init__(self, parent, ID, defaults=None):
        commonDialog.CommonDialog.__init__(self, parent, ID, 'Create Tunnel', size=(400, 300), defaults=defaults)

    def createCtrl(self):
        sizer = wx.FlexGridSizer(rows=6, cols=2, hgap=5, vgap=10)
        dummy, self.nameTxtCtrl = self.addLabelTextCtrlEntry(sizer, 'Name: ', 'name')
        dummy, self.bvidTxtCtrl = self.addLabelTextCtrlEntry(sizer, 'BVID: ', 'bvid')
        dummy, self.portTxtCtrl = self.addLabelTextCtrlEntry(sizer, 'Port: ', 'port')
        dummy, self.bsaTxtCtrl  = self.addLabelTextCtrlEntry(sizer, 'BSA:  ', 'bsa')
        dummy, self.bdaTxtCtrl  = self.addLabelTextCtrlEntry(sizer, 'BDA:  ', 'bda')
        dummy, self.nodeTxtCtrl = self.addLabelTextCtrlEntry(sizer, 'Node: ', 'node')
        return sizer

    def GetSelection(self):
        tunnel = Tunnel()
        tunnel.name = str(self.nameTxtCtrl.GetValue())
        tunnel.bvid = int(self.bvidTxtCtrl.GetValue())
        tunnel.port = str(self.portTxtCtrl.GetValue())
        tunnel.bsa  = str(self.bsaTxtCtrl.GetValue())
        tunnel.bda  = str(self.bdaTxtCtrl.GetValue())
        tunnel.node = str(self.nodeTxtCtrl.GetValue())
        return tunnel
