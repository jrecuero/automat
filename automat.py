#!/usr/bin/env python

# @startuml
# class Automatization {
#    + configListBox
#    + outputTextCtrl
#    - createResourceButtons()
#    - createConfigurationPanel()
#    - createOutputPanel()
#    - _sendToOutput()
#    - OnClickService()
#    - OnClickTunnel()
#    - OnClickAccessPort()
#    - OnClickClientRing()
#    - OnClickNetworkRing()
#    - OnClickEndPoint()
#    - OnClickEvent()
#    - OnChoiceConfig()
#    - OnCloseWindow()
# }
# Automatization <|-- wx.Frame
# class ServiceDialog <|-- wx.Dialog
# class TunnelDialog <|-- wx.Dialog
# class AccessPortDialog<|-- wx.Dialog
# class ClientRingDialog <|-- wx.Dialog
# class NetworkRingDialog <|-- wx.Dialog
# class EndPointDialog <|-- wx.Dialog
# class EventDialog <|-- wx.Dialog
# Automatization -right- ServiceDialog
# Automatization -right- TunnelDialog
# Automatization -right- AccessPortDialog
# Automatization -right- ClientRingDialog
# Automatization -right- NetworkRingDialog
# Automatization -right- EndPointDialog
# Automatization -right- EventDialog
# @enduml

import wx
import service
import tunnel
import accessport
import clientring
import networkring
import endpoint
import event
import resource


class Automatization(wx.Frame):

    def __init__(self, parent, ID):
        wx.Frame.__init__(self, parent, ID, 'Automatization YAML Configuration', size=(800, 480))

        self.resourceHdlr     = resource.ResourceHandler()

        mainPanel = wx.Panel(self)
        mainPanel.SetBackgroundColour('White')
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.createResourceButtons(mainPanel), 1, wx.EXPAND | wx.ALL, border=1)
        mainSizer.Add(self.createConfigurationPanel(mainPanel), 2, wx.EXPAND | wx.ALL, border=1)
        mainSizer.Add(self.createOutputPanel(mainPanel), 3, wx.EXPAND | wx.ALL, border=1)
        mainPanel.SetSizer(mainSizer)
        mainPanel.Fit()

    def _sendToOutput(self):
        self.outputTextCtrl.Clear()
        self.outputTextCtrl.AppendText(self.resourceHdlr.parseToYamlForAllServices())
        self.outputTextCtrl.AppendText(self.resourceHdlr.parseToYamlForAllTunnels())
        self.outputTextCtrl.AppendText(self.resourceHdlr.parseToYamlForAllAccessPorts())
        self.outputTextCtrl.AppendText(self.resourceHdlr.parseToYamlForAllClientRings())
        self.outputTextCtrl.AppendText(self.resourceHdlr.parseToYamlForAllNetworkRings())
        self.outputTextCtrl.AppendText(self.resourceHdlr.parseToYamlForAllEndPoints())
        self.outputTextCtrl.AppendText(self.resourceHdlr.parseToYamlForAllEvents())
        self.outputTextCtrl.SetInsertionPoint(0)

    def _createResource(self, dialog):
        result = dialog.ShowModal()
        if result == wx.ID_OK:
            instance = dialog.GetSelection()
            self.resourceHdlr.addResource(instance)
            self._sendToOutput()

    def createResourceButtons(self, panel):
        #sizer = wx.GridSizer(rows=5, cols=1, hgap=5, vgap=25)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        serviceBtn     = wx.Button(panel, -1, 'Service')
        tunnelBtn      = wx.Button(panel, -1, 'Tunnel')
        accessPortBtn  = wx.Button(panel, -1, 'Access Port')
        clientRingBtn  = wx.Button(panel, -1, 'Client Ring')
        networkRingBtn = wx.Button(panel, -1, 'Network Ring')
        endPointBtn = wx.Button(panel, -1, 'End Point')
        eventBtn    = wx.Button(panel, -1, 'Event')

        sizer.Add(serviceBtn, 1, wx.HORIZONTAL)
        sizer.Add(tunnelBtn, 1, wx.HORIZONTAL)
        sizer.Add(accessPortBtn, 1, wx.HORIZONTAL)
        sizer.Add(clientRingBtn, 1, wx.HORIZONTAL)
        sizer.Add(networkRingBtn, 1, wx.HORIZONTAL)
        sizer.Add(endPointBtn, 1, wx.HORIZONTAL)
        sizer.Add(eventBtn, 1, wx.HORIZONTAL)

        self.Bind(wx.EVT_BUTTON, self.OnClickService, serviceBtn)
        self.Bind(wx.EVT_BUTTON, self.OnClickTunnel, tunnelBtn)
        self.Bind(wx.EVT_BUTTON, self.OnClickAccessPort, accessPortBtn)
        self.Bind(wx.EVT_BUTTON, self.OnClickClientRing, clientRingBtn)
        self.Bind(wx.EVT_BUTTON, self.OnClickNetworkRing, networkRingBtn)
        self.Bind(wx.EVT_BUTTON, self.OnClickEndPoint, endPointBtn)
        self.Bind(wx.EVT_BUTTON, self.OnClickEvent, eventBtn)

        return sizer

    def createConfigurationPanel(self, panel):
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        configListBox = wx.ListBox(panel, -1, style=wx.LB_SINGLE)
        mainSizer.Add(configListBox, 1, wx.EXPAND | wx.ALL, border=10)
        self.resourceHdlr.widget = configListBox

        editBtn   = wx.Button(panel, -1, 'EDIT')
        removeBtn = wx.Button(panel, -1, 'REMOVE')
        self.Bind(wx.EVT_BUTTON, self.OnClickEdit, editBtn)
        self.Bind(wx.EVT_BUTTON, self.OnClickRemove, removeBtn)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddSpacer(50)
        sizer.Add(editBtn, 0, wx.HORIZONTAL)
        sizer.AddSpacer(5)
        sizer.Add(removeBtn, 0, wx.HORIZONTAL)
        mainSizer.AddSpacer(10)
        mainSizer.Add(sizer, 0, wx.EXPAND)
        mainSizer.AddSpacer(10)
        return mainSizer

    def createOutputPanel(self, panel):
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.outputTextCtrl = wx.TextCtrl(panel, -1, "", style=wx.TE_MULTILINE | wx.TE_RICH2)
        outputStyle = wx.TextAttr()
        outputStyle.SetTabs([40, 80, 120, 160, 200, 240, 280])
        self.outputTextCtrl.SetDefaultStyle(outputStyle)
        sizer.Add(self.outputTextCtrl, 1, wx.EXPAND | wx.ALL, border=10)
        return sizer

    def OnCloseWindow(self, ev):
        self.Destroy()

    def OnClickService(self, ev):
        serviceDlg = service.ServiceDialog(self, -1)
        self._createResource(serviceDlg)

    def OnClickTunnel(self, ev):
        tunnelDlg = tunnel.TunnelDialog(self, -1)
        self._createResource(tunnelDlg)

    def OnClickAccessPort(self, ev):
        accessPortDlg = accessport.AccessPortDialog(self, -1)
        self._createResource(accessPortDlg)

    def OnClickClientRing(self, ev):
        clientRingDlg = clientring.ClientRingDialog(self, -1)
        self._createResource(clientRingDlg)

    def OnClickNetworkRing(self, ev):
        networkRingDlg = networkring.NetworkRingDialog(self, -1)
        self._createResource(networkRingDlg)

    def OnClickEndPoint(self, ev):
        endPointDlg = endpoint.EndPointDialog(self, -1)
        self._createResource(endPointDlg)

    def OnClickEvent(self, ev):
        eventDlg = event.EventDialog(self, -1)
        self._createResource(eventDlg)

    def OnClickEdit(self, ev):
        selection = self.resourceHdlr.widget.GetSelection()
        if selection != -1:
            instance = self.resourceHdlr.resources[selection]
            dialog = instance.createDialog(self, -1)
            result = dialog.ShowModal()
            if result == wx.ID_OK:
                instance = dialog.GetSelection()
                self.resourceHdlr.replaceResource(instance, selection)
                self._sendToOutput()

    def OnClickRemove(self, ev):
        selection = self.resourceHdlr.widget.GetSelection()
        if selection != -1:
            self.resourceHdlr.deleteResource(selection)
            self._sendToOutput()


if __name__ == '__main__':
    app = wx.PySimpleApp(False)
    frame = Automatization(parent=None, ID=-1)
    frame.Show()
    app.MainLoop()