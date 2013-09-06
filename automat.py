#!/usr/bin/env python

import wx
import event
import resource
import config
import configDialog


class Automatization(wx.Frame):
    """ Main application Frame.

    This is the main frame to be displayed by the application. It creates all
    sort of widget and resources required to make the application work.
    """

    def __init__(self, parent, ID):
        """ Automatization initialization.

        Initializes the main frame. Create all sizer and widgets.
        """
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
        """ Parse all resources and send information to the outputTextCtrl.

        For every resource, information is parsed in the final YAML format and
        it is displayed in the outputTextCtrl widget.
        """
        self.outputTextCtrl.Clear()
        for resId in [config.getResourceId(resource) for resource in config.RESOURCES]:
            self.outputTextCtrl.AppendText(self.resourceHdlr.parseToYamlForAll(resId))
            self.outputTextCtrl.SetInsertionPoint(0)

    def _createResource(self, dialog):
        """ Creates a resource entry.

        It creates a resource entry which keep information about the format
        and the data for every entry added.
        """
        result = dialog.ShowModal()
        if result == wx.ID_OK:
            instance = dialog.GetSelection()
            self.resourceHdlr.addResource(instance)
            self._sendToOutput()
        dialog.Destroy()

    def createResourceButtons(self, panel):
        """ Create all resource buttons.

        It creates all resource buttons and bind them to the OnClickEvent
        handler.
        """
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        for resId in [config.getResourceId(resource) for resource in config.RESOURCES]:
            button = wx.Button(panel, -1, resId)
            sizer.Add(button, 1, wx.HORIZONTAL)
            self.Bind(wx.EVT_BUTTON, self.OnClickConfig, button)

        #eventBtn    = wx.Button(panel, -1, 'Event')

        #sizer.Add(eventBtn, 1, wx.HORIZONTAL)

        #self.Bind(wx.EVT_BUTTON, self.OnClickEvent, eventBtn)

        return sizer

    def createConfigurationPanel(self, panel):
        """ Create configuration panel.

        It creates the configuration panel which holds widget that display all
        resources entered. Resources can be edited and deleted using this panel.
        """
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
        """ Create output panel.

        It created the output panel which holds widget that display all
        resources entered in YAML format.
        """
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.outputTextCtrl = wx.TextCtrl(panel, -1, "", style=wx.TE_MULTILINE | wx.TE_RICH2)
        outputStyle = wx.TextAttr()
        outputStyle.SetTabs([40, 80, 120, 160, 200, 240, 280])
        self.outputTextCtrl.SetDefaultStyle(outputStyle)
        sizer.Add(self.outputTextCtrl, 1, wx.EXPAND | wx.ALL, border=10)
        return sizer

    def OnCloseWindow(self, ev):
        """ Close window event handler.
        """
        self.Destroy()

    def OnClickConfig(self, ev):
        """ OnClick any resource button event handler.

        It handles events when a resource button is clicked. Dialog for the
        given resource will be launched.
        """
        resId    = ev.GetEventObject().Label
        resource = config.getResourceFromId(resId)
        dialog   = configDialog.ConfigDialog(self, -1, resource)
        self._createResource(dialog)

    def OnClickEdit(self, ev):
        """ OnClick edit resource event.

        It handles when the EDIT resource button is clicked. Selected resource
        will be launched with resource data.
        """
        selection = self.resourceHdlr.widget.GetSelection()
        if selection != -1:
            instance = self.resourceHdlr.resources[selection]
            dialog = instance.createDialog(self, -1)
            result = dialog.ShowModal()
            if result == wx.ID_OK:
                instance = dialog.GetSelection()
                self.resourceHdlr.replaceResource(instance, selection)
                self._sendToOutput()
            dialog.Destroy()

    def OnClickRemove(self, ev):
        """ OnClick delete resource event.

        It handles when the REMOVE resource button is ckicled. Selected
        resource will be removed.
        """
        selection = self.resourceHdlr.widget.GetSelection()
        if selection != -1:
            self.resourceHdlr.deleteResource(selection)
            self._sendToOutput()


if __name__ == '__main__':
    app = wx.PySimpleApp(False)
    frame = Automatization(parent=None, ID=-1)
    frame.Show()
    app.MainLoop()
