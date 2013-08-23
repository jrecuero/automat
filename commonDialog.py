#!/usr/bin/env python

import wx


class CommonDialog(wx.Dialog):

    def __init__(self, parent, ID, title, size, defaults=None):
        wx.Dialog.__init__(self, parent, ID, title, size=size)
        self.defaults = defaults
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.AddSpacer(25)
        ctrlSizer = wx.BoxSizer(wx.VERTICAL)
        ctrlSizer.AddSpacer(25)
        ctrlSizer.Add(self.createCtrl())
        btnSizer  = wx.BoxSizer(wx.HORIZONTAL)
        createBtn = wx.Button(self, wx.ID_OK, 'Create')
        cancelBtn = wx.Button(self, wx.ID_CANCEL, 'Cancel')
        btnSizer.Add(createBtn)
        btnSizer.Add(cancelBtn)
        ctrlSizer.AddSpacer(25)
        ctrlSizer.Add(btnSizer, 0, wx.CENTER)
        ctrlSizer.AddSpacer(25)
        mainSizer.Add(ctrlSizer, 0, 0)
        mainSizer.AddSpacer(25)
        self.SetSizer(mainSizer)
        self.Fit()

    def _handleDefaults(self, fieldName):
        txtValue = ''
        if self.defaults:
            if isinstance(fieldName, tuple) or isinstance(fieldName, list):
                fieldValue = getattr(self.defaults, fieldName[0], [])
                txtValue = fieldValue[fieldName[1]] if fieldValue else ''
            else:
                txtValue = getattr(self.defaults, fieldName, '')
        return txtValue

    def _createLabelTextCtrlEntry(self, label, fieldName, size, validator):
        txtValue = self._handleDefaults(fieldName)
        lblCtrl = wx.StaticText(self, -1, label)
        txtCtrl = wx.TextCtrl(self, -1, str(txtValue), size=size, validator=validator)
        return lblCtrl, txtCtrl

    def addLabelTextCtrlEntry(self, sizer, label, fieldName, size=(200, -1), validator=wx.DefaultValidator):
        lblCtrl, txtCtrl = self._createLabelTextCtrlEntry(label, fieldName, size, validator)
        sizer.Add(lblCtrl, 0, 0)
        sizer.Add(txtCtrl, 0, 0)
        return (lblCtrl, txtCtrl)

    def insertLabelTextCtrlEntry(self, sizer, pos, label, fieldName, size=(200, -1), validator=wx.DefaultValidator):
        lblCtrl, txtCtrl = self._createLabelTextCtrlEntry(label, fieldName, size, validator)
        sizer.Insert(pos, lblCtrl, 0, 0)
        sizer.Insert(pos + 1, txtCtrl, 0, 0)
        return (lblCtrl, txtCtrl)

    def addLabelChoiceEntry(self, sizer, label, choices, initSel, fieldName):
        lblCtrl = wx.StaticText(self, -1, label)
        choice  = wx.Choice(self, -1, choices=choices)
        if not isinstance(fieldName, tuple):
            selectValue = getattr(self.defaults, fieldName, initSel)
        else:
            lista = getattr(self.defaults, fieldName[0], [])
            selectValue = lista[fieldName[1]] if lista else initSel
        selectIndex = choices.index(selectValue) if selectValue is not None else 0
        choice.SetSelection(selectIndex)
        #self.Bind(wx.EVT_CHOICE, self.OnChoiceType, choice)
        sizer.Add(lblCtrl, 0, 0)
        sizer.Add(choice, 0, 0)
        return (lblCtrl, choice)
