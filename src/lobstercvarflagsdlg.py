#-------------------------------------------------------------------------------
# Name:        lobstercvarflagsdlg
# Purpose:      this dialog contains all the flags related checkboxes
#
# Author:      lakhu
#
# Created:     28/04/2014
# Copyright:   (c) Account Prism Pvt. Ltd.
# Licence:     all_rights_reserved
#-------------------------------------------------------------------------------

#imports
import wx

# class-name        : CFlagsDialog
# class-description : it contains group of checkboxes related to CVar flags

class CFlagsDialog(wx.Dialog):
    def __init__(self, parent, dictFilterCvars):

        """
        Constructor :-

        Throws Exception : No

        Inputs :    (i) parent              : specifies parent of this dialog
                    (ii) dictFilterCvars    : dictionary contains user's search choices

        Outputs : does not return any values

        Purpose : initialize all the components of dialog

        """
        # calling parent class constructor
        wx.Dialog.__init__(
                            self, parent, title = "Flags", pos = (450, 150),
                            size = (280, 230), name = "typesdialog"
                            )
        # position value of x and y, with reference to which controls are positioned in GUI.
        iXValue = 0
        iYValue = 10

        # dictionary contains information about user's search configurations
        self.dictFilterCVars = dictFilterCvars
        # define list of checkboxes
        self.lsObjCheckboxes = []
        # Creating checkbox for "None Flag"
        self.m_objChkBoxSelectNone = wx.CheckBox(
                                                self, -1, label = 'None',
                                                pos = (iXValue + 80, iYValue + 10)
                                            )
        # Binding events for None checkbox
        self.m_objChkBoxSelectNone.Bind(wx.EVT_CHECKBOX, self.OnUnchecked)
        # adding checkbox into list of checkboxes
        self.lsObjCheckboxes.append(self.m_objChkBoxSelectNone)

        self.m_objChkBoxFlagR = wx.CheckBox(
                                                self, -1, label = 'R',
                                                pos = (iXValue + 15, iYValue + 40)
                                            )
        self.m_objChkBoxFlagR.Bind(wx.EVT_CHECKBOX, self.OnUnchecked)
        self.lsObjCheckboxes.append(self.m_objChkBoxFlagR)

        self.m_objChkBoxFlagH = wx.CheckBox(
                                                self, -1, label = 'H',
                                                pos = (iXValue + 15, iYValue + 70)
                                            )
        self.m_objChkBoxFlagH.Bind(wx.EVT_CHECKBOX, self.OnUnchecked)
        self.lsObjCheckboxes.append(self.m_objChkBoxFlagH)

        self.m_objChkBoxFlagL = wx.CheckBox(
                                                self, -1, label = 'L',
                                                pos = (iXValue + 15, iYValue + 100)
                                            )
        self.m_objChkBoxFlagL.Bind(wx.EVT_CHECKBOX, self.OnUnchecked)
        self.lsObjCheckboxes.append(self.m_objChkBoxFlagL)

        self.m_objChkBoxFlagG = wx.CheckBox(
                                                self, -1, label = 'G',
                                                pos = (iXValue + 15, iYValue + 130)
                                            )
        self.m_objChkBoxFlagG.Bind(wx.EVT_CHECKBOX, self.OnUnchecked)
        self.lsObjCheckboxes.append(self.m_objChkBoxFlagG)

        self.m_objChkBoxFlagY = wx.CheckBox(
                                                self, -1, label = 'Y',
                                                pos = (iXValue + 80, iYValue + 40)
                                            )
        self.m_objChkBoxFlagY.Bind(wx.EVT_CHECKBOX, self.OnUnchecked)
        self.lsObjCheckboxes.append(self.m_objChkBoxFlagY)

        self.m_objChkBoxFlagA = wx.CheckBox(
                                                self, -1, label = 'A',
                                                pos = (iXValue + 80, iYValue + 70)
                                            )
        self.m_objChkBoxFlagA.Bind(wx.EVT_CHECKBOX, self.OnUnchecked)
        self.lsObjCheckboxes.append(self.m_objChkBoxFlagA)

        self.m_objChkBoxFlagN = wx.CheckBox(
                                                self, -1, label = 'N',
                                                pos = (iXValue + 80, iYValue + 100)
                                            )
        self.m_objChkBoxFlagN.Bind(wx.EVT_CHECKBOX, self.OnUnchecked)
        self.lsObjCheckboxes.append(self.m_objChkBoxFlagN)

        self.m_objChkBoxFlagD = wx.CheckBox(
                                                self, -1, label = 'D',
                                                pos = (iXValue + 80, iYValue + 130)
                                            )
        self.m_objChkBoxFlagD.Bind(wx.EVT_CHECKBOX, self.OnUnchecked)
        self.lsObjCheckboxes.append(self.m_objChkBoxFlagD)

        self.m_objChkBoxFlagP = wx.CheckBox(
                                                self, -1, label = 'P',
                                                pos = (iXValue + 155, iYValue + 40)
                                            )
        self.m_objChkBoxFlagP.Bind(wx.EVT_CHECKBOX, self.OnUnchecked)
        self.lsObjCheckboxes.append(self.m_objChkBoxFlagP)

        self.m_objChkBoxFlagS = wx.CheckBox(
                                                self, -1, label = 'S',
                                                pos = (iXValue + 155, iYValue + 70)
                                            )
        self.m_objChkBoxFlagS.Bind(wx.EVT_CHECKBOX, self.OnUnchecked)
        self.lsObjCheckboxes.append(self.m_objChkBoxFlagS)

        self.m_objChkBoxFlagB = wx.CheckBox(
                                                self, -1, label = 'B',
                                                pos = (iXValue + 155, iYValue + 100)
                                            )
        self.m_objChkBoxFlagB.Bind(wx.EVT_CHECKBOX, self.OnUnchecked)
        self.lsObjCheckboxes.append(self.m_objChkBoxFlagB)

        self.m_objChkBoxFlagN = wx.CheckBox(
                                                self, -1, label = 'N',
                                                pos = (iXValue + 155, iYValue + 130)
                                            )
        self.m_objChkBoxFlagN.Bind(wx.EVT_CHECKBOX, self.OnUnchecked)
        self.lsObjCheckboxes.append(self.m_objChkBoxFlagN)

        self.m_objChkBoxFlagW = wx.CheckBox(
                                                self, -1, label = 'W',
                                                pos = (iXValue + 230, iYValue + 40)
                                            )
        self.m_objChkBoxFlagW.Bind(wx.EVT_CHECKBOX, self.OnUnchecked)
        self.lsObjCheckboxes.append(self.m_objChkBoxFlagW)

        self.m_objChkBoxFlagU = wx.CheckBox(
                                                self, -1, label = 'U',
                                                pos = (iXValue + 230, iYValue + 70)
                                            )
        self.m_objChkBoxFlagU.Bind(wx.EVT_CHECKBOX, self.OnUnchecked)
        self.lsObjCheckboxes.append(self.m_objChkBoxFlagU)

        self.m_objChkBoxFlagV = wx.CheckBox(
                                                self, -1, label = 'V',
                                                pos = (iXValue + 230, iYValue + 100)
                                            )
        self.m_objChkBoxFlagV.Bind(wx.EVT_CHECKBOX, self.OnUnchecked)
        self.lsObjCheckboxes.append(self.m_objChkBoxFlagV)

        self.m_objChkBoxFlagM = wx.CheckBox(
                                                self, -1, label = 'M',
                                                pos = (iXValue + 230, iYValue + 130)
                                            )
        self.m_objChkBoxFlagM.Bind(wx.EVT_CHECKBOX, self.OnUnchecked)
        self.lsObjCheckboxes.append(self.m_objChkBoxFlagM)

        self.m_objChkBoxSelectAll = wx.CheckBox(
                                                self, -1, label = 'All',
                                                pos = (iXValue + 15, iYValue + 10)
                                            )
        self.m_objChkBoxSelectAll.Bind(wx.EVT_CHECKBOX, self.OnSelectAll)

        lsEFlags = self.dictFilterCVars.get("Flags")

        # iterating all checkboxes and settting its default value True(Checked) if its stored in search configuration
        for idx in range(0, len(self.lsObjCheckboxes)):
            if (lsEFlags != None and idx in lsEFlags):
                self.lsObjCheckboxes[idx].SetValue(True)

        # creating Button for apply preferences
        self.m_btnApply = wx.Button(
                                        self, id = -1, label = "Apply",
                                        pos = (iXValue + 150, iYValue + 160), size = (50, 25)
                                    )

        # Binding events with Apply button
        self.m_btnApply.Bind(wx.EVT_BUTTON, self.OnApply)
        # creating Button for cancelation of this dialog
        self.m_btnCancel = wx.Button(
                                        self, id = -1, label = "Cancel",
                                        pos = (iXValue + 210, iYValue + 160), size = (50, 25)
                                    )
        # Binding events with Cancel button
        self.m_btnCancel.Bind(wx.EVT_BUTTON, self.OnCancel)

        return

    """----------------------------------------------------------------------"""
    def OnApply(self, event):
        """
        Handler Function :-

        Throws Exception    : No

        Inputs              : (i) event : event object

        Outputs             : does not return any values

        Purpose             : storing flags for which user want to search cvars based on these flags

        """

        self.dictFilterCVars["Flags"] = []
        # Iterating each flags and store it into user's choces of falgs for search configuration
        for idx in range(0, len(self.lsObjCheckboxes)):
            # If checkbox is checked then add it into choices
            if(self.lsObjCheckboxes[idx].GetValue() == True):
                self.dictFilterCVars["Flags"].append(idx)

        # if user has not selected any flags then by default it will consider all the flags
        if (len(self.dictFilterCVars.get("Flags")) == 0 ):
            for idx in range(0, len(self.lsObjCheckboxes)):
                self.dictFilterCVars["Flags"].append(idx)
        # disappearing dialog when user click apply button
        self.Destroy()

        return

    """----------------------------------------------------------------------"""
    def OnSelectAll(self, event):
        """
        Handler Function :-

        Throws Exception    : No

        Inputs              : (i) event : event object

        Outputs             : does not return any values

        Purpose             : it will checked all the checkboxes of flag

        """
        # If user checked these checkbox, all checkboxes will be checked automatically
        if(self.m_objChkBoxSelectAll.GetValue() == True):
            # iterating each checkbox and checked it.
            for idx in range(0, len(self.lsObjCheckboxes)):
                self.lsObjCheckboxes[idx].SetValue(True)

        # If user unchecked these checkbox, all checkboxes will be unchecked automatically
        if(self.m_objChkBoxSelectAll.GetValue() == False):
            # iterating each checkbox and unchecked it.
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

        Purpose             : If all flags are checked and user unchecked any one
                               is unchecked "All select" checkboxes
        """
        # fetching whether all select checkbox is checked or unchecked when user click on checkbox
        if (event.IsChecked() == False):
            # unchecked "All" checkbox
            self.m_objChkBoxSelectAll.SetValue(False)

        return

    """----------------------------------------------------------------------"""
    def OnCancel(self, event):
        """
        Handler Function :-

        Throws Exception    : No

        Inputs              : (i) event : event object

        Outputs             : does not return any values

        Purpose             : Disappear Flags dialog when cancel buton is clicked

        """
        self.Destroy()

        return

    """----------------------------------------------------------------------"""
