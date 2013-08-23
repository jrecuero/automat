#!/usr/bin/env python

import wx
import commonDialog


SERVICE_PATTERN     = {'label': 'Service',      'name': 'service',     'handler': 'getAllServicesName'}
TUNNEL_PATTERN      = {'label': 'Tunnel',       'name': 'tunnel',      'handler': 'getAllTunnelsName'}
ACCESSPORT_PATTERN  = {'label': 'Access Port',  'name': 'accessport',  'handler': 'getAllAccessPortsName'}
PORT_PATTERN        = {'label': 'UNI/NNI Port', 'name': 'port',        'handler': 'getAllPortsName'}
CLIENTRING_PATTERN  = {'label': 'Client Ring',  'name': 'clientring',  'handler': 'getAllClientRingsName'}
NETWORKRING_PATTERN = {'label': 'Network Ring', 'name': 'networkring', 'handler': 'getAllNetworkRingName'}
ENDPOINT_PATTERN    = {'label': 'End Point',    'name': 'endpoint',    'handler': 'getAllEndPointsName'}

EVENTS_DICT = {'flowdomain': {'create': [SERVICE_PATTERN, ], 'delete': [SERVICE_PATTERN, ], },
               'flowpoint':  {'create': [PORT_PATTERN, SERVICE_PATTERN, ], 'delete': [PORT_PATTERN, SERVICE_PATTERN, ], },
               'tunnel':     {'create': [TUNNEL_PATTERN, ], 'delete': [TUNNEL_PATTERN, ], }, }


class EventValidator(wx.PyValidator):

    def __init__(self):
        wx.PyValidator.__init__(self)

    def Clone(self):
        return EventValidator()

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True

    def Validate(self, win):
        textCtrl = self.GetWindow()
        text     = textCtrl.GetValue()
        if 'flowdomain' == text:
            print 'flowdomain event'


class Event(object):

    RESOURCE_YAML_NAME = 'events'

    def __init__(self, name=None, action=None, predelay=0, postdelay=0):
        self.name      = name
        self.action    = action
        self.predelay  = predelay
        self.postdelay = postdelay
        self.extra     = {}

    def _toStr(self):
        result = '[EVENT] %s %s %s %s' % (self.name, self.action, self.predelay, self.postdelay)
        for value in self.extra.values():
            result += ' %s' % value
        return result

    def __repr__(self):
        return self._toStr()

    def __str__(self):
        return self._toStr()

    def createDialog(self, panel, ID):
        dialog = EventDialog(panel, ID, self)
        return dialog

    def parseToYaml(self):
        result  = "\t\t%s:\n\t\t\t{\n" % self.name
        result += "\t\t\t\taction:   \t%s,\n" % self.action
        result += "\t\t\t\tpredelay: \t%s,\n" % self.predelay
        result += "\t\t\t\tpostdelay:\t%s,\n" % self.postdelay
        for key, value in self.extra.iteritems():
            result += "\t\t\t\t%s:\t%s,\n" % (key, value)
        result += "\t\t\t},\n"
        return result


class EventDialog(commonDialog.CommonDialog):

    def __init__(self, parent, ID, defaults=None):
        commonDialog.CommonDialog.__init__(self, parent, ID, 'Create Event', size=(400, 300), defaults=defaults)

    def createCtrl(self):
        self.sizer = wx.FlexGridSizer(rows=6, cols=2, hgap=5, vgap=10)
        self.labelCtrl  = {}
        self.textCtrl   = {}
        dummy, self.nameTxtCtrl      = self.addLabelTextCtrlEntry(self.sizer, 'Name: ', 'name')
        dummy, self.actionTxtCtrl    = self.addLabelTextCtrlEntry(self.sizer, 'Action: ', 'action')
        dummy, self.predelayTxtCtrl  = self.addLabelTextCtrlEntry(self.sizer, 'Pre-Delay: ', 'predelay')
        dummy, self.postdelayTxtCtrl = self.addLabelTextCtrlEntry(self.sizer, 'Post-Delay: ', 'postdelay')

        if self.defaults:
            eventStr  = getattr(self.defaults, 'name', '')
            actionStr = getattr(self.defaults, 'action', '')
            if eventStr in EVENTS_DICT and actionStr in EVENTS_DICT[eventStr]:
                self.createExtraEntries(actionStr, eventStr)

        self.Bind(wx.EVT_TEXT, self.OnTextAction, self.actionTxtCtrl)
        return self.sizer

    def createExtraEntries(self, actionStr, eventStr):
        self.Freeze()
        pos = 4
        for action in EVENTS_DICT[eventStr][actionStr]:
            label, name = action['label'], action['name']
            #self.labelCtrl[name], self.textCtrl[name]= self.addLabelTextCtrlEntry(self.sizer, '%s: ' % label, ('extra', name))
            self.labelCtrl[name], self.textCtrl[name] = self.insertLabelTextCtrlEntry(self.sizer, pos, '%s: ' % label, ('extra', name))
        self.sizer.Layout()
        self.Fit()
        self.Refresh()
        self.Update()
        self.Thaw()

    def removeExtraEntries(self):
        for key in self.textCtrl.keys():
            self.sizer.Remove(self.labelCtrl[key])
            self.sizer.Remove(self.textCtrl[key])
            self.labelCtrl[key].Destroy()
            self.textCtrl[key].Destroy()
            del self.labelCtrl[key]
            del self.textCtrl[key]
        self.sizer.Layout()
        self.Fit()

    def OnTextAction(self, ev):
        actionStr = ev.GetEventObject().GetValue()
        eventStr  = self.nameTxtCtrl.GetValue()
        if eventStr in EVENTS_DICT and actionStr in EVENTS_DICT[eventStr]:
            self.createExtraEntries(actionStr, eventStr)
        if eventStr not in EVENTS_DICT or (eventStr in EVENTS_DICT and actionStr not in EVENTS_DICT[eventStr]):
            self.removeExtraEntries()

    def GetSelection(self):
        event = Event()
        event.name      = str(self.nameTxtCtrl.GetValue())
        event.action    = str(self.actionTxtCtrl.GetValue())
        event.predelay  = int(self.predelayTxtCtrl.GetValue()) if self.predelayTxtCtrl.GetValue() else 0
        event.postdelay = int(self.postdelayTxtCtrl.GetValue()) if self.postdelayTxtCtrl.GetValue() else 0
        for key in self.textCtrl.keys():
            event.extra[key] = self.textCtrl[key].GetValue()
        return event
