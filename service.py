#!/usr/bin/env python

# import wx
# import commonDialog

def getResourceId():
    return 'Service'

def getResourceTag():
    return 'services'

def _getServiceTypes(dlg):
    return ['ELINE',  'EVLINE', 'ELAN', 'EVLAN']

def _getDefaultServiceType(dlg):
    return 'EVLAN'

RESOURCE = {'id':   getResourceId(),
            'tag':  getResourceTag(),
            'attrs': [{'display': 'Name', 
                       'name': 'name', 
                       'type': 'str',  
                       'dim': None, 
                       'default': None, 
                       'values': None, },
                      {'display': 'Node', 
                       'name': 'node', 
                       'type': 'str',  
                       'dim': None, 
                       'default': None, 
                       'values':  None, },
                      {'display': 'Type', 
                       'name': 'type', 
                       'type': 'list', 
                       'dim': None, 
                       'default': _getDefaultServiceType, 
                       'values': _getServiceTypes, },
                      {'display': 'Isid', 
                       'name': 'isid', 
                       'type': 'int',  
                       'dim': None, 
                       'default': None, 
                       'values':  None, }, ], }

# SERVICE_TYPES = ['ELINE', 'EVLINE', 'ELAN', 'EVLAN']
# 
# 
# class Service(object):
# 
#     RESOURCE_YAML_NAME = 'services'
# 
#     def __init__(self, name=None, TYPE=None, isid=None, node=None):
#         self.name = str(name) if name else None
#         self.type = str(TYPE) if TYPE else None
#         self.isid = int(isid) if isid else None
#         self.node = str(node) if node else None
# 
#     def _toStr(self):
#         return '[SERVICE] %s  %s  %s  %s' % (self.name, self.type, self.isid, self.node)
# 
#     def __repr__(self):
#         return self._toStr()
# 
#     def __str__(self):
#         return self._toStr()
# 
#     def createDialog(self, panel, ID):
#         dialog = ServiceDialog(panel, ID, self)
#         return dialog
# 
#     def parseToYaml(self):
#         result  = "\t\t%s:\n\t\t\t{\n" % self.name
#         result += "\t\t\t\tnode:\t%s,\n" % self.node
#         result += "\t\t\t\ttype:\t%s,\n" % self.type
#         result += "\t\t\t\tisid:\t%s,\n" % self.isid
#         result += "\t\t\t},\n"
#         return result
# 
# 
# class ServiceDialog(commonDialog.CommonDialog):
# 
#     def __init__(self, parent, ID, defaults=None):
#         commonDialog.CommonDialog.__init__(self, parent, ID, 'Create Service', size=(400, 300), defaults=defaults)
# 
#     def createCtrl(self):
#         sizer = wx.FlexGridSizer(rows=4, cols=2, hgap=5, vgap=10)
#         dummy, self.nameTxtCtrl = self.addLabelTextCtrlEntry(sizer, 'Name: ', 'name')
#         dummy, self.typeChoice  = self.addLabelChoiceEntry(sizer, 'Type: ', SERVICE_TYPES, 'EVLAN', 'type')
#         dummy, self.isidTxtCtrl = self.addLabelTextCtrlEntry(sizer, 'ISID: ', 'isid')
#         dummy, self.nodeTxtCtrl = self.addLabelTextCtrlEntry(sizer, 'Node: ', 'node')
#         return sizer
# 
#     def OnChoiceType(self, event):
#         print event.GetSelection()
# 
#     def GetSelection(self):
#         service = Service()
#         service.name = str(self.nameTxtCtrl.GetValue())
#         service.type = SERVICE_TYPES[self.typeChoice.GetSelection()]
#         service.isid = int(self.isidTxtCtrl.GetValue())
#         service.node = str(self.nodeTxtCtrl.GetValue())
#         return service
