#-------------------------------------------------------------------------------
# Name:        lobstercvartypedlg
# Purpose:      Contains group of checkboxes related to cvar type
#
# Author:      lakhu
#
# Created:     28/04/2014
# Copyright:   (c) Account Prism Pvt. Ltd.
# Licence:     all_rights_reserved
#-------------------------------------------------------------------------------

#imports
import wx
import lobstercvar

# class-name        : CTypeDialog
# class-description : it contains group of checkboxes related to CVar type
class CTypeDialog(wx.Dialog):
    def __init__(self, parent, dictFilterCVars):

        """
        Constructor :-

        Throws Exception : No

        Inputs : (i)  parent            : specifies parent of this dialog
                 (ii) dictFilterCVars   : dictionary contains user's search choices

        Outputs : does not return any values

        Purpose : initialize all the components of dialog

        """
        # calling parent class constructor
        wx.Dialog.__init__(
                            self, parent, title = "Types", pos = (450, 150),
                            size = (400, 230), name = "typesdialog"
                            )
        # position value of x and y, with reference to which controls are positioned in GUI.
        iXValue = 0
        iYValue = 0

        # assigning references to member dictioanry
        self.dictFilterCVars = dictFilterCVars
        self.lsObjCheckboxes = []

        # Creating checkbox for "Action" type
        self.m_objChkBoxAction = wx.CheckBox(
                                                self, -1, label = 'Action',
                                                pos = (iXValue + 15, iYValue + 40)
                                            )
        # Adding it into list of checkboxes
        self.lsObjCheckboxes.append(self.m_objChkBoxAction)
        # binding events for "Action" checkbox
        self.m_objChkBoxAction.Bind(wx.EVT_CHECKBOX, self.OnUnchecked)

        self.m_objChkBoxBitPattern = wx.CheckBox(
                                                self, -1, label = 'BitPattern',
                                                pos = (iXValue + 15, iYValue + 70)
                                            )
        self.lsObjCheckboxes.append(self.m_objChkBoxBitPattern)
        self.m_objChkBoxBitPattern.Bind(wx.EVT_CHECKBOX, self.OnUnchecked)

        self.m_objChkBoxBool = wx.CheckBox(
                                                self, -1, label = 'Bool',
                                                pos = (iXValue + 15, iYValue + 100)
                                            )
        self.lsObjCheckboxes.append(self.m_objChkBoxBool)
        self.m_objChkBoxBool.Bind(wx.EVT_CHECKBOX, self.OnUnchecked)

        self.m_objChkBoxColor = wx.CheckBox(
                                                self, -1, label = 'Color',
                                                pos = (iXValue + 15, iYValue + 130)
                                            )
        self.lsObjCheckboxes.append(self.m_objChkBoxColor)
        self.m_objChkBoxColor.Bind(wx.EVT_CHECKBOX, self.OnUnchecked)

        self.m_objChkBoxDouble = wx.CheckBox(
                                                self, -1, label = 'Double',
                                                pos = (iXValue + 100, iYValue + 40)
                                            )
        self.lsObjCheckboxes.append(self.m_objChkBoxDouble)
        self.m_objChkBoxDouble.Bind(wx.EVT_CHECKBOX, self.OnUnchecked)

        self.m_objChkBoxDoubleLockstep = wx.CheckBox(
                                                self, -1, label = 'DoubleLockstep',
                                                pos = (iXValue + 270, iYValue + 130)
                                            )
        self.lsObjCheckboxes.append(self.m_objChkBoxDoubleLockstep)
        self.m_objChkBoxDoubleLockstep.Bind(wx.EVT_CHECKBOX, self.OnUnchecked)

        self.m_objChkBoxEnum = wx.CheckBox(
                                                self, -1, label = 'Enum',
                                                pos = (iXValue + 100, iYValue + 100)
                                            )
        self.lsObjCheckboxes.append(self.m_objChkBoxEnum)
        self.m_objChkBoxEnum.Bind(wx.EVT_CHECKBOX, self.OnUnchecked)

        self.m_objChkBoxFileName = wx.CheckBox(
                                                self, -1, label = 'FileName',
                                                pos = (iXValue + 100, iYValue + 130)
                                            )
        self.lsObjCheckboxes.append(self.m_objChkBoxFileName)
        self.m_objChkBoxFileName.Bind(wx.EVT_CHECKBOX, self.OnUnchecked)

        self.m_objChkBoxImage = wx.CheckBox(
                                                self, -1, label = 'Image',
                                                pos = (iXValue + 185, iYValue + 40)
                                            )
        self.lsObjCheckboxes.append(self.m_objChkBoxImage)
        self.m_objChkBoxImage.Bind(wx.EVT_CHECKBOX, self.OnUnchecked)

        self.m_objChkBoxInteger = wx.CheckBox(
                                                self, -1, label = 'Integer',
                                                pos = (iXValue + 185, iYValue + 70)
                                            )
        self.lsObjCheckboxes.append(self.m_objChkBoxInteger)
        self.m_objChkBoxInteger.Bind(wx.EVT_CHECKBOX, self.OnUnchecked)

        self.m_objChkBoxLongInteger = wx.CheckBox(
                                                self, -1, label = 'Long Integer',
                                                pos = (iXValue + 185, iYValue + 100)
                                            )
        self.lsObjCheckboxes.append(self.m_objChkBoxLongInteger)
        self.m_objChkBoxLongInteger.Bind(wx.EVT_CHECKBOX, self.OnUnchecked)

        self.m_objChkBoxName = wx.CheckBox(
                                                self, -1, label = 'Name',
                                                pos = (iXValue + 185, iYValue + 130)
                                            )
        self.lsObjCheckboxes.append(self.m_objChkBoxName)
        self.m_objChkBoxName.Bind(wx.EVT_CHECKBOX, self.OnUnchecked)

        self.m_objChkBoxNotimpl = wx.CheckBox(
                                                self, -1, label = 'notimpl',
                                                pos = (iXValue + 270, iYValue + 40)
                                            )
        self.lsObjCheckboxes.append(self.m_objChkBoxNotimpl)
        self.m_objChkBoxNotimpl.Bind(wx.EVT_CHECKBOX, self.OnUnchecked)

        self.m_objChkBoxRegister = wx.CheckBox(
                                                self, -1, label = 'Register',
                                                pos = (iXValue + 270, iYValue + 70)
                                            )
        self.lsObjCheckboxes.append(self.m_objChkBoxRegister)
        self.m_objChkBoxRegister.Bind(wx.EVT_CHECKBOX, self.OnUnchecked)

        self.m_objChkBoxSafeArray = wx.CheckBox(
                                                self, -1, label = 'SafeArray',
                                                pos = (iXValue + 270, iYValue + 100)
                                            )

        self.lsObjCheckboxes.append(self.m_objChkBoxSafeArray)
        self.m_objChkBoxSafeArray.Bind(wx.EVT_CHECKBOX, self.OnUnchecked)

        self.m_objChkBoxString = wx.CheckBox(
                                                self, -1, label = 'String',
                                                pos = (iXValue + 100, iYValue + 70)
                                            )
        self.lsObjCheckboxes.append(self.m_objChkBoxString)
        self.m_objChkBoxString.Bind(wx.EVT_CHECKBOX, self.OnUnchecked)

        self.m_objChkBoxSelectAll = wx.CheckBox(
                                        self, -1, label = 'All',
                                        pos = (iXValue + 15, iYValue + 10)
                                    )
        self.m_objChkBoxSelectAll.Bind(wx.EVT_CHECKBOX, self.OnSelectAll)


        lsETypes = dictFilterCVars.get("Type")

        # iterating each checkbox and checked it if its checked earlier.
        for idx in range(0, len(self.lsObjCheckboxes)):
            if (lsETypes != None and idx in lsETypes):
                self.lsObjCheckboxes[idx].SetValue(True)

        self.m_btnApply = wx.Button(
                                        self, id = -1, label = "Apply",
                                        pos = (iXValue + 240, iYValue + 160), size = (50, 25)
                                    )

        self.m_btnApply.Bind(wx.EVT_BUTTON, self.OnApply)

        self.m_btnCancel = wx.Button(
                                        self, id = -1, label = "Cancel",
                                        pos = (iXValue + 300, iYValue + 160), size = (50, 25)
                                    )
        self.m_btnCancel.Bind(wx.EVT_BUTTON, self.OnCancel)

        return

    """----------------------------------------------------------------------"""
    def OnApply(self, event):
        """
        Handler Function :-

        Throws Exception    : No

        Inputs              : (i) event : event object

        Outputs             : does not return any values

        Purpose             : storing types for which user want to search cvars based on these types

        """
        # defining list inside dictionary of user's search choices, "Type" is a key
        self.dictFilterCVars["Type"] = []
        # iterating each checkbox and if it is checked then store it in list of types of user's choice
        for idx in range(0, len(self.lsObjCheckboxes)):
            if(self.lsObjCheckboxes[idx].GetValue() == True):
                self.dictFilterCVars["Type"].append(idx)
        # If user has not checked any type then consider all types are checked
        if(len(self.dictFilterCVars.get("Type")) == 0):
            for idx in range(0, len(self.lsObjCheckboxes)):
                self.dictFilterCVars["Type"].append(idx)

        #print self.dictFilterCVars.get("Type")
        self.Destroy()

        return

    """----------------------------------------------------------------------"""
    def OnSelectAll(self, event):
        """
        Handler Function :-

        Throws Exception    : No

        Inputs              : (i) event : event object

        Outputs             : does not return any values

        Purpose             : checked and unchecked all types on checking this "All" checkbox

        """
        # if "All" is checked then checked all the checkboxes
        if(self.m_objChkBoxSelectAll.GetValue() == True):
            for idx in range(0, len(self.lsObjCheckboxes)):
                self.lsObjCheckboxes[idx].SetValue(True)

        # if "All" is unchecked then unchecked all the checkboxes
        if(self.m_objChkBoxSelectAll.GetValue() == False):
            for idx in range(0, len(self.lsObjCheckboxes)):
                self.lsObjCheckboxes[idx].SetValue(False)

        return

    """----------------------------------------------------------------------"""
    def OnUnchecked(self, event):
        """
        Handler Function :-

        Throws Exception    : No

        Inputs              : (i) event : event object

        Outputs             : does not return any values

        Purpose             : If any one of the checkbox is unchecked then "All" checkbox will be unchecked

        """
        if (event.IsChecked() == False):
            self.m_objChkBoxSelectAll.SetValue(False)

        return

    """----------------------------------------------------------------------"""
    def OnCancel(self, event):
        """
        Handler Function :-

        Throws Exception    : No

        Inputs              : (i) event : event object

        Outputs             : does not return any values

        Purpose             : Disappear this dialog when user clicks on this cancel button

        """
        self.Destroy()

        return

    """----------------------------------------------------------------------"""
