import wx
import commonDialog

configuration = {'services': [{'disp-name': 'Name', 'attr-name': 'name', 'attr-type': 'int',  'attr-dim': None, 'default': None, 'ranage':None, },
                              {'disp-name': 'Type', 'attr-name': 'type', 'attr-type': 'list', 'attr-dim': None, 'default': 'EVLAN', 'range': ['ELINE',  'EVLINE', 'ELAN', 'EVLAN'], },
                              {'disp-name': 'Node', 'attr-name': 'node', 'attr-type': 'str',  'attr-dim': None, 'default': None, 'range':  None, },
                              {'disp-name': 'Isid', 'attr-name': 'isid', 'attr-type': 'str',  'attr-dim': None, 'default': None, 'range':  None, }, ], }


class ConfigDialog(commonDialog.CommonDialog):

    def __init__(self, parent, ID, defaults=None):
        commonDialog.CommonDialog.__init__(self, parent, ID, 'Create ', size=(400, 300), defaults=defaults)
        self.config = configuration['services']

    def CreateCtrl(self):
        sizer = wx.FlexGridSizer(rows=len(self.config), cols=2, hgap=5, vgap=10)
        self.ctrl = {}
        for data in self.config:
            attrName = data['attr-name']
            dispName = data['disp-name']
            attrType = data['attr-type']
            if attrType in ('int', 'str', ):
                dummy, self.ctrl[attrName] = self.addLabelTextCtrlEntry(sizer, '%s: ' % dispName, attrName)
            elif attrType in ('list', ):
                dummy, self.ctrl[attrName]  = self.addLabelChoiceEntry(sizer, '%s: ' % dispName, data['range'], data['default'], attrName)
        return sizer

    def GetSelection(self):
        return None
