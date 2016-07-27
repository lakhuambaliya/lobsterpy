#-------------------------------------------------------------------------------
# Name:        lobstersearchconfigurationdlg
# Purpose:      this module CSearchConfigurationDlg class, which shows GUI for
#               search operations in the application
#
# Author:      lakhu
#
# Created:     22/03/2014
# Copyright:   (c) Account Prism Pvt. Ltd.
# Licence:     all_rights_reserved
#-------------------------------------------------------------------------------

#imports
import wx
import lobstercvar
import lobstersearchconfiguration
import lobstereventhandler
import lobstercvartypedlg
import lobstercvarflagsdlg
import lobstersearchmanager

# class-name         : CSearchConfigurationDlg
# class-description  : this class display gui of search configuration to user
#                      so that user can set the search configurations prior to
#                      search operations
class CSearchConfigurationDlg(wx.Dialog):
    def __init__(self, parent):

        """
        Constructor :-

        Throws Exception : No

        Inputs : (i) parent : specifies parent of this dialog

        Outputs : does not return any values

        Purpose : initialize all the components of dialog

        """
        # calling parent class constructor
         # calling parent class constructor
        wx.Dialog.__init__(
                            self, parent, title = "Search Configuration", pos = (450, 150),
                            size = (600, 230), name = "searchconfiguration"

                                    )
        self.parent = parent
        self.m_objCSearchConfiguration = parent.m_objLobsterDataContext.__m_objCSearchConfiguration__
        if(self.m_objCSearchConfiguration == None):
            self.m_objCSearchConfiguration = lobstersearchconfiguration.CSearchConfiguration()
        self.m_objCSearchConfiguration.m_dictFilterCVars = {}
        # position value of x and y, with reference to which controls are positioned in GUI.
        iXValue = 0
        iYValue = 0

        objSBGeneralSearch = wx.StaticBox(
                                            self, id = -1, label = "General",
                                            pos = (iXValue + 5, iYValue + 50), size = (200, 290)
                                        )

        # creating Static text which is for displaying text followed by Text control
        objStSearchKeyword = wx.StaticText(
                                                    self, id = -1, label = "Search :  ",
                                                    pos = (iXValue + 150, iYValue + 20)
                                                )
        # creating text control
        self.m_objTxtCtrlSearchKeyword = wx.TextCtrl(self, pos = (iXValue + 200, iYValue + 20), size = (300,20))

        # making group of two radio buttons for Numeric Notation. (i) Standard, (ii) Engineering
        self.m_objRadioBoxSearchDirectory = wx.RadioBox(
                                                self, id = -1, label = "Search Directory",
                                                pos = (iXValue + 15, iYValue + 70), size = (170, 110),
                                                choices = ["Root Directory", "Current Directory", "Current with Nested Directory", "Favorite CVars"], majorDimension=4,
                                                style = wx.RA_VERTICAL, validator = wx.DefaultValidator, name = "searchdirectory"
                                                )

        # Binding this group of radio buttons to event
        #self.m_objRadioBoxSearchDirectory.Bind(wx.EVT_RADIOBOX, self.OnNumericNotationChoice)

        # creating static box for grouping search modes and columns
        sbSearchOption = wx.StaticBox(
                                            self, id = -1, label = "Search Mode",
                                            pos = (iXValue + 15, iYValue + 200), size = (170, 90)
                                        )

         # creating checkboxes for search mode and binding event to it
        self.m_objChkBoxMatchCase = wx.CheckBox(
                                                self, -1, label = 'Match Case',
                                                pos = (iXValue + 20, iYValue + 220)
                                            )

        #self.m_objChkBoxMatchCase.Bind(wx.EVT_CHECKBOX, self.OnSelectMatchCaseCheckBox)

        self.m_objChkBoxMatchWholeWord = wx.CheckBox(
                                                self, -1, label = 'Match Whole Word',
                                                pos = (iXValue + 20, iYValue + 240)
                                                )

        #self.m_objChkBoxMatchWholeWord.Bind(wx.EVT_CHECKBOX, self.OnSelectMatchWholeWordCheckBox)

        self.m_objChkBoxRegExpr = wx.CheckBox(
                                                self, -1, label = 'Regular Expression',
                                                pos = (iXValue + 20, iYValue + 260)
                                            )

        #self.m_objChkBoxRegExpr.Bind(wx.EVT_CHECKBOX, self.OnSelectRegExprCheckBox)

        objSBAdvanceSearch = wx.StaticBox(
                                            self, id = -1, label = "Advance",
                                            pos = (iXValue + 220, iYValue + 50), size = (400, 290)
                                        )

        self.m_objChkBoxType = wx.CheckBox(
                                                self, -1, label = 'Type',
                                                pos = (iXValue + 230, iYValue + 70)
                                            )
        self.m_objChkBoxType.Bind(wx.EVT_CHECKBOX, self.OnType)
        self.m_btnSelectType = wx.Button(
                                        self, id = -1, label = "...",
                                        pos = (iXValue + 320, iYValue + 70), size = (20, 17)
                                    )
        self.m_btnSelectType.Disable()
        self.m_btnSelectType.Bind(wx.EVT_BUTTON, self.OnTypes)

        self.m_objChkBoxFlags = wx.CheckBox(
                                                self, -1, label = 'Flags',
                                                pos = (iXValue + 230, iYValue + 100)
                                            )
        self.m_objChkBoxFlags.Bind(wx.EVT_CHECKBOX, self.OnFlag)
        self.m_btnSelectFlags = wx.Button(
                                        self, id = -1, label = "...",
                                        pos = (iXValue + 320, iYValue + 100), size = (20, 17)
                                    )
        self.m_btnSelectFlags.Disable()
        self.m_btnSelectFlags.Bind(wx.EVT_BUTTON, self.OnFlags)

        self.m_objChkBoxAdapted = wx.CheckBox(
                                                self, -1, label = 'Adapted',
                                                pos = (iXValue + 230, iYValue + 130)
                                            )
        self.m_objChkBoxAdapted.Bind(wx.EVT_CHECKBOX, self.OnAdapted)
        objStaticTextVal1 = wx.StaticText(
                                            self, id = -1, label = "Val1",
                                            pos = (iXValue + 320, iYValue + 128)
                                        )

        self.m_objTxtCtrlAdaptedVal1 = wx.TextCtrl(self, pos = (iXValue + 345, iYValue + 128), size = (75, 18))
        self.m_objTxtCtrlAdaptedVal1.Disable()
        lsStrConditions = lobstersearchconfiguration.CSearchConfiguration.mC_LS_STR_CONDITIONS
        self.m_objComboChoicesAdapted = wx.ComboBox(
                                            self, value = "Select", pos = (iXValue + 430, iYValue + 128),
                                            choices = lsStrConditions, size = (75, 5))
        self.m_objComboChoicesAdapted.Disable()
        objStaticTextVal2 = wx.StaticText(
                                            self, id = -1, label = "Val2",
                                            pos = (iXValue + 510, iYValue + 128)
                                        )

        self.m_objTxtCtrlAdaptedVal2 = wx.TextCtrl(self, pos = (iXValue + 535, iYValue + 128), size = (75, 18))
        self.m_objTxtCtrlAdaptedVal2.Disable()
        self.m_objChkBoxBits = wx.CheckBox(
                                                self, -1, label = 'Bits',
                                                pos = (iXValue + 230, iYValue + 160)
                                            )
        self.m_objChkBoxBits.Bind(wx.EVT_CHECKBOX, self.OnBits)
        objStaticTextVal1 = wx.StaticText(
                                            self, id = -1, label = "Val1",
                                            pos = (iXValue + 320, iYValue + 158)
                                        )

        self.m_objTxtCtrlBitsVal1 = wx.TextCtrl(self, pos = (iXValue + 345, iYValue + 158), size = (75, 18))
        self.m_objTxtCtrlBitsVal1.Disable()
        self.m_objComboChoicesBits = wx.ComboBox(
                                            self, value = "Select", pos = (iXValue + 430, iYValue + 158),
                                            choices = lsStrConditions, size = (75, 5))

        self.m_objComboChoicesBits.Disable()
        objStaticTextVal2 = wx.StaticText(
                                            self, id = -1, label = "Val2",
                                            pos = (iXValue + 510, iYValue + 158)
                                        )

        self.m_objTxtCtrlBitsVal2 = wx.TextCtrl(self, pos = (iXValue + 535, iYValue + 158), size = (75, 18))
        self.m_objTxtCtrlBitsVal2.Disable()
        self.m_objChkBoxRoot = wx.CheckBox(
                                                self, -1, label = 'Root',
                                                pos = (iXValue + 230, iYValue + 190)
                                            )
        self.m_objChkBoxRoot.Bind(wx.EVT_CHECKBOX, self.OnRoot)
        self.m_objTxtCtrlRoot = wx.TextCtrl(self, pos = (iXValue + 320, iYValue + 188), size = (225, 18))
        self.m_objTxtCtrlRoot.Disable()
        self.m_objChkBoxFilters = wx.CheckBox(
                                                self, -1, label = 'Filters',
                                                pos = (iXValue + 230, iYValue + 220)
                                            )
        self.m_objChkBoxFilters.Bind(wx.EVT_CHECKBOX, self.OnFilters)
        self.m_objTxtCtrlFilters = wx.TextCtrl(self, pos = (iXValue + 320, iYValue + 218), size = (225, 18))
        self.m_objTxtCtrlFilters.Disable()
        self.m_objChkBoxPath = wx.CheckBox(
                                                self, -1, label = 'Path',
                                                pos = (iXValue + 230, iYValue + 250)
                                            )
        self.m_objChkBoxPath.Bind(wx.EVT_CHECKBOX, self.OnPath)
        self.m_objTxtCtrlPath = wx.TextCtrl(self, pos = (iXValue + 320, iYValue + 248), size = (225, 18))
        self.m_objTxtCtrlPath.Disable()
        self.m_objChkBoxNbOfBits = wx.CheckBox(
                                                self, -1, label = 'NbOfBits',
                                                pos = (iXValue + 230, iYValue + 280)
                                            )
        self.m_objChkBoxNbOfBits.Bind(wx.EVT_CHECKBOX, self.OnNumberOfBits)

        objStaticTextVal1 = wx.StaticText(
                                            self, id = -1, label = "Val1",
                                            pos = (iXValue + 320, iYValue + 278)
                                        )

        self.m_objTxtCtrlNbOfBitsVal1 = wx.TextCtrl(self, pos = (iXValue + 345, iYValue + 278), size = (75, 18))
        self.m_objTxtCtrlNbOfBitsVal1.Disable()
        self.m_objComboChoicesNbOfBits = wx.ComboBox(
                                            self, value = "Select", pos = (iXValue + 430, iYValue + 278),
                                            choices = lsStrConditions, size = (75, 5))
        self.m_objComboChoicesNbOfBits.Disable()
        objStaticTextVal2 = wx.StaticText(
                                            self, id = -1, label = "Val2",
                                            pos = (iXValue + 510, iYValue + 278)
                                        )

        self.m_objTxtCtrlNbOfBitsVal2 = wx.TextCtrl(self, pos = (iXValue + 535, iYValue + 278), size = (75, 18))
        self.m_objTxtCtrlNbOfBitsVal2.Disable()
        self.m_objChkBoxHardwareAddress = wx.CheckBox(
                                                self, -1, label = 'H/W Address',
                                                pos = (iXValue + 230, iYValue + 310)
                                            )
        self.m_objChkBoxHardwareAddress.Bind(wx.EVT_CHECKBOX, self.OnHardwareAddress)
        self.m_objTxtCtrlHardwareAddress = wx.TextCtrl(self, pos = (iXValue + 320, iYValue + 308), size = (225, 18))
        self.m_objTxtCtrlHardwareAddress.Disable()
        # Creating Button, that will be useful to save all preferences configuration
        self.m_btnSearch = wx.Button(
                                        self, id = -1, label = "Search",
                                        pos = (iXValue + 500, iYValue + 350), size = (50, 25)
                                    )
        self.m_btnSearch.Bind(wx.EVT_BUTTON, self.OnSearch)
        # Creating Button, that will be useful to Close the Dialog
        self.m_btnClose = wx.Button(
                                        self, id = -1, label = "Close",
                                        pos = (iXValue + 570, iYValue + 350), size = (50, 25)
                                    )
        # binding event handler with this close button
        self.m_btnClose.Bind(wx.EVT_BUTTON, self.OnClose)

        self.SetSize((iXValue + 650, iYValue + 420))

        return

    """----------------------------------------------------------------------"""
    def OnTypes(self, event):
        """
        Event Handler :-

        Throws Exception : No

        Inputs : (i) event : event object

        Outputs : does not return any values

        Purpose : When user clicks on button of opening multiple types which can be selected by user

        """
        # creating object of CTypeDialog
        objTypeDlg = lobstercvartypedlg.CTypeDialog(self.parent, self.m_objCSearchConfiguration.m_dictFilterCVars)
        # Displaying CTypeDialog
        objTypeDlg.ShowModal()
        # applying types which are selected by user
        self.OnApplyTypes()

        return

    """----------------------------------------------------------------------"""
    def OnFlags(self, event):
        """
        Event Handler :-

        Throws Exception : No

        Inputs : (i) event : event object

        Outputs : does not return any values

        Purpose : when user clicks on button which opens dialog containing flags

        """
        # creating object of CFlagDialog
        objFlagsDlg = lobstercvarflagsdlg.CFlagsDialog(self.parent, self.m_objCSearchConfiguration.m_dictFilterCVars)
        # displaying Flag dialog
        objFlagsDlg.ShowModal()

        return

    """----------------------------------------------------------------------"""
    def OnSearch(self, event):
        """
        Event Handler :-

        Throws Exception : No

        Inputs :

        Outputs :

        Purpose :

        """
        # fetching value from search keyword text control
        strSearchKeyWord = self.m_objTxtCtrlSearchKeyword.GetValue().strip()
##        if (len(strSearchKeyWord) == 0):
##            dlgKeywordFound = wx.MessageDialog(
##                                                self, "Please enter search keyword...",
##                                               "Keyword not found", wx.OK|wx.ICON_INFORMATION
##                                               )
##
##            result = dlgKeywordFound.ShowModal()
##
##            if result == wx.ID_OK:
##                dlgKeywordFound.Destroy()
##                return

        # search keyword is inserted in searchconfiguration object
        self.m_objCSearchConfiguration.m_dictFilterCVars["Name"] = strSearchKeyWord

        self.m_objCSearchConfiguration.MSetSearchKeyword(strSearchKeyWord)
        # fetching value from GUI whether user want to search in Current Directory, Root Directory, Current with nested directory or favorite cvars
        eSearchDir = self.m_objRadioBoxSearchDirectory.GetSelection()
        # user's selection of directory is stored into serarchconfiguration object
        self.m_objCSearchConfiguration.m_eSearchDir = eSearchDir

        # Declaring list which contains user's search mode. ( Match case, Match whole word or Regular expression)
        lsESearchMode = []

        # preparing list for user's choices of search mode
        if(self.m_objChkBoxMatchCase.GetValue() == True):
            lsESearchMode.append(0)
        if(self.m_objChkBoxMatchWholeWord.GetValue() == True):
            lsESearchMode.append(1)
        if(self.m_objChkBoxRegExpr.GetValue() == True):
            lsESearchMode.append(2)
        self.m_objCSearchConfiguration.MSetSearchMode(lsESearchMode)

        lsAdapted = []
        lsAdapted.append(self.m_objComboChoicesAdapted.GetValue())
        lsAdapted.append(self.m_objTxtCtrlAdaptedVal1.GetValue())
        lsAdapted.append(self.m_objTxtCtrlAdaptedVal2.GetValue())

        if(self.m_objChkBoxAdapted.GetValue() == True):
            self.m_objCSearchConfiguration.m_dictFilterCVars["Adapted"] = lsAdapted

        lsBits = []
        lsBits.append(self.m_objComboChoicesBits.GetValue())
        lsBits.append(self.m_objTxtCtrlBitsVal1.GetValue())
        lsBits.append(self.m_objTxtCtrlBitsVal2.GetValue())

        # if Bits checkbox is checked then it will store data in search configuration
        if(self.m_objChkBoxBits.GetValue() == True):
            self.m_objCSearchConfiguration.m_dictFilterCVars["Bits"] = lsBits
        # if Root checkbox is checked then fetching value from GUI and storing it into search configuration
        if(self.m_objChkBoxRoot.GetValue() == True):
            self.m_objCSearchConfiguration.m_dictFilterCVars["Root"] = self.m_objTxtCtrlRoot.GetValue().strip()
        # if Path checkbox is checked then fetching value from GUI and storing it into search configuration
        if (self.m_objChkBoxPath.GetValue() == True):
            self.m_objCSearchConfiguration.m_dictFilterCVars["Path"] = self.m_objTxtCtrlPath.GetValue().strip()
        # if Filters checkbox is checked then fetching value from GUI and storing it into search configuration
        if(self.m_objChkBoxFilters.GetValue() == True):
            self.m_objCSearchConfiguration.m_dictFilterCVars["Filters"] = self.m_objTxtCtrlFilters.GetValue().strip()

        lsNbOfBits = []
        lsNbOfBits.append(self.m_objComboChoicesNbOfBits.GetValue())
        lsNbOfBits.append(self.m_objTxtCtrlNbOfBitsVal1.GetValue())
        lsNbOfBits.append(self.m_objTxtCtrlNbOfBitsVal2.GetValue())

        # if Path Bits is checked then fetching value from GUI and storing it into search configuration
        if(self.m_objChkBoxNbOfBits.GetValue() == True):
            self.m_objCSearchConfiguration.m_dictFilterCVars["NbOfBits"] = lsNbOfBits
         # if Path HardwareAddress is checked then fetching value from GUI and storing it into search configuration
        if(self.m_objChkBoxHardwareAddress.GetValue() == True):
            self.m_objCSearchConfiguration.m_dictFilterCVars["HardwareAddress"] = self.m_objTxtCtrlHardwareAddress.GetValue().strip()

        # Calling function which search cvars based on search configuration's attribute and fetching absolute path of all searched cvars and storing into list
        lsSearchResults = lobstersearchmanager.CSearchManager.MSSearch(self.m_objCSearchConfiguration, self.parent.m_objLobsterDataContext)
        iSerchFound = len(lsSearchResults)
         #   deleting the pane which contains listview
        self.parent.m_objPaneMgr.DetachPane(self.parent.m_objCWxListView)

        #   adding modified listview with the caption "Child CVar" to the pane
        self.parent.m_objPaneMgr.AddPane(self.parent.m_objCWxListView, wx.aui.AuiPaneInfo().Center().Caption("Search Results for keyword " + strSearchKeyWord + " (" + str(iSerchFound) + " hits found) "))

        #   updating the aui manager
        self.parent.m_objPaneMgr.Update()
        # populating searched cvars into list view
        self.parent.m_objCWxListView.MPopulateValuesInListView(lsSearchResults, bGenerateAbsPath = False)

        return

    """----------------------------------------------------------------------"""
    def OnClose(self, event):
        """
        Event Handler :-

        Throws Exception : No

        Inputs : (i) event : event object

        Outputs : does not return any values

        Purpose : disappear dialog when user clicks on close button

        """
        self.Destroy()

        return

    """----------------------------------------------------------------------"""
    def OnApplyTypes(self):
        """
        Event Handler :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : does not return any values

        Purpose : enable or disable some GUI components based on user's selection

        """
        # union operation of type which are selected by user
        setUnionTypes = lobstersearchmanager.CSearchManager.MSUnionAttributes(self.m_objCSearchConfiguration.m_dictFilterCVars.get("Type"))

        # if type is not in user's selection then disable type button otherwise enable it
        if ("Type" not in setUnionTypes):
            self.m_btnSelectType.Disable()
        else:
            self.m_btnSelectType.Enable()

        # if Flags is not in user's selection then disable Flag button otherwise enable it
        if("Flags" not in setUnionTypes):
            self.m_btnSelectFlags.Disable()
        else:
            self.m_btnSelectFlags.Enable()

        # if Adapted is not in user's selection then disable adapted checkbox button otherwise enable it
        if("Adapted" in setUnionTypes):
            self.m_objChkBoxAdapted.Enable()
            # enable or disable adapted components based on user's selection of type.
            # if user has selected numeric type then both textcontrol will be enabled otherwise disable it
            lsEType = self.m_objCSearchConfiguration.m_dictFilterCVars.get("Type")
            if (lsEType != None):
                for eType in lsEType:
                    if (eType in lobstercvar.CVar.ms_lsENonNumericTypes):
                        self.m_objComboChoicesAdapted.Disable()
                        self.m_objTxtCtrlAdaptedVal2.Disable()
                        break
        else:
            self.m_objChkBoxAdapted.Disable()
            self.m_objComboChoicesAdapted.Disable()
            self.m_objTxtCtrlAdaptedVal1.Disable()
            self.m_objTxtCtrlAdaptedVal2.Disable()

        # if Bits is not contained in set of types then disable it
        if("Bits" not in setUnionTypes):
            self.m_objChkBoxBits.Disable()
            self.m_objComboChoicesBits.Disable()
            self.m_objTxtCtrlBitsVal1.Disable()
            self.m_objTxtCtrlBitsVal2.Disable()
        else:
            self.m_objChkBoxBits.Enable()

        # if Root attribute is contained in set of types then disable components related to Root
        if("Root" not in setUnionTypes):
            self.m_objChkBoxRoot.Disable()
            self.m_objTxtCtrlRoot.Disable()
        else:
            self.m_objChkBoxRoot.Enable()

        # if Filters attribute is contained in set of types then disable components related to Filters
        if("Filters" not in setUnionTypes):
            self.m_objChkBoxFilters.Disable()
            self.m_objTxtCtrlFilters.Disable()
        else:
            self.m_objChkBoxFilters.Enable()

        # NbOfBits attribute is contained in set of types then disable components related to NbOfBits
        if("NbOfBits" not in setUnionTypes):
            self.m_objChkBoxNbOfBits.Disable()
            self.m_objComboChoicesNbOfBits.Disable()
            self.m_objTxtCtrlNbOfBitsVal1.Disable()
            self.m_objTxtCtrlNbOfBitsVal2.Disable()
        else:
            self.m_objChkBoxNbOfBits.Enable()

        # HardwareAddress attribute is contained in set of types then disable components related to HardwareAddress
        if("HardwareAddress" not in setUnionTypes):
            self.m_objChkBoxHardwareAddress.Disable()
            self.m_objTxtCtrlHardwareAddress.Disable()
        else:
            self.m_objChkBoxHardwareAddress.Enable()

        # Path attribute is contained in set of types then disable components related to Path
        if("Path" not in setUnionTypes):
            self.m_objChkBoxPath.Disable()
            self.m_objTxtCtrlPath.Disable()
        else:
            self.m_objChkBoxPath.Enable()

        return

    """----------------------------------------------------------------------"""
    def OnType(self, event):
        """
        Event Handler :-

        Throws Exception : No

        Inputs : (i) event object

        Outputs : does not return any values

        Purpose : called when user clicks on Type checkbox

        """
        # fetching vaue from GUI whether type checkbox is checked or not. if type checkbox is checked then enaable Button near checkbox
        if (self.m_objChkBoxType.GetValue() == True):
            self.m_btnSelectType.Enable()
        elif (self.m_objChkBoxType.GetValue() == False):
            self.m_btnSelectType.Disable()
    """----------------------------------------------------------------------"""
    def OnFlag(self, event):
        """
        Event Handler :-

        Throws Exception : No

        Inputs : (i) event : event object

        Outputs : does not return any values

        Purpose : called when user check or uncheck checkbox "Flags"

        """
        # enable button near Flags checkbox if user has checked Flags checkbox
        if (self.m_objChkBoxFlags.GetValue() == True):
            self.m_btnSelectFlags.Enable()
        elif (self.m_objChkBoxFlags.GetValue() == False):
            self.m_btnSelectFlags.Disable()
    """----------------------------------------------------------------------"""
    def OnAdapted(self, event):
        if (self.m_objChkBoxAdapted.GetValue() == True):
            self.m_objTxtCtrlAdaptedVal1.Enable()
            self.m_objComboChoicesAdapted.Enable()
            self.m_objTxtCtrlAdaptedVal2.Enable()
            for eType in self.m_objCSearchConfiguration.m_dictFilterCVars:
                if (eType in lobstercvar.CVar.ms_lsENonNumericTypes):
                    self.m_objComboChoicesAdapted.Disable()
                    self.m_objTxtCtrlAdaptedVal2.Disable()
                    break
        # if not checked then disable all components related to adapted value
        elif (self.m_objChkBoxAdapted.GetValue() == False):
            self.m_objComboChoicesAdapted.Disable()
            self.m_objTxtCtrlAdaptedVal1.Disable()
            self.m_objTxtCtrlAdaptedVal2.Disable()

        return

    """----------------------------------------------------------------------"""
    def OnBits(self, event):
        """
        Event Handler :-

        Throws Exception : No

        Inputs : (i) event : event object

        Outputs : does not return any values

        Purpose : called when user check or uncheck Bits checkbox

        """
        # if Bit checkbox is checked then enable components related to Bits otherwise disable it
        if (self.m_objChkBoxBits.GetValue() == True):
            self.m_objComboChoicesBits.Enable()
            self.m_objTxtCtrlBitsVal1.Enable()
            self.m_objTxtCtrlBitsVal2.Enable()
        elif (self.m_objChkBoxBits.GetValue() == False):
            self.m_objComboChoicesBits.Disable()
            self.m_objTxtCtrlBitsVal1.Disable()
            self.m_objTxtCtrlBitsVal2.Disable()
    """----------------------------------------------------------------------"""
    def OnRoot(self, event):
        if (self.m_objChkBoxRoot.GetValue() == True):
            self.m_objTxtCtrlRoot.Enable()
        elif (self.m_objChkBoxRoot.GetValue() == False):
            self.m_objTxtCtrlRoot.Disable()

        return

    """----------------------------------------------------------------------"""
    def OnFilters(self, event):
        """
        Event Handler :-

        Throws Exception : No

        Inputs : (i) event : event object

        Outputs : does not return any values

        Purpose : according to user's choice it will disable or enable Textcontrol of Filters attribute

        """
        # if Filters checkbox is checked then enable text control related to Filters otherwise disable it
        if (self.m_objChkBoxFilters.GetValue() == True):
            self.m_objTxtCtrlFilters.Enable()
        elif (self.m_objChkBoxFilters.GetValue() == False):
            self.m_objTxtCtrlFilters.Disable()

        return

    """----------------------------------------------------------------------"""
    def OnPath(self, event):
        """
        Event Handler :-

        Throws Exception : No

        Inputs : (i) event : event object

        Outputs : does not return any values

        Purpose : according to user's choice of Path it will disable or enable text control related to Path

        """
        # if Path checkbox is checked then enable text control related to Path attribute otherwise disable it
        if (self.m_objChkBoxPath.GetValue() == True):
            self.m_objTxtCtrlPath.Enable()
        elif (self.m_objChkBoxPath.GetValue() == False):
            self.m_objTxtCtrlPath.Disable()

        return

    """----------------------------------------------------------------------"""
    def OnNumberOfBits(self, event):
        """
        Event Handler :-

        Throws Exception : No

        Inputs : (i) event : event object

        Outputs : does not return any values

        Purpose : According to user's choice of NbOfBits it will enable or disable components related to NbOfBits

        """
        # if NbOfBits is checked then enable components related to NbOfBits otherwise disable
        if (self.m_objChkBoxNbOfBits.GetValue() == True):
            self.m_objComboChoicesNbOfBits.Enable()
            self.m_objTxtCtrlNbOfBitsVal1.Enable()
            self.m_objTxtCtrlNbOfBitsVal2.Enable()
        elif (self.m_objChkBoxNbOfBits.GetValue() == False):
            self.m_objComboChoicesNbOfBits.Disable()
            self.m_objTxtCtrlNbOfBitsVal1.Disable()
            self.m_objTxtCtrlNbOfBitsVal2.Disable()

        return

    """----------------------------------------------------------------------"""
    def OnHardwareAddress(self, event):
        """
        Event Handler :-

        Throws Exception : No

        Inputs : (i) event : event object

        Outputs : does not return any values

        Purpose : According to user's choice of HardwareAddress it will enable or disable components related to HardwareAddress

        """
        if (self.m_objChkBoxHardwareAddress.GetValue() == True):
            self.m_objTxtCtrlHardwareAddress.Enable()
        elif (self.m_objChkBoxHardwareAddress.GetValue() == False):
            self.m_objTxtCtrlHardwareAddress.Disable()

        return

    """----------------------------------------------------------------------"""
