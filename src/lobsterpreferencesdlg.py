#-------------------------------------------------------------------------------
# Name:     mydialog.py
# Purpose:  this module contains all the preferences settings of an application
#
# Author:      lakhu
#
# Created:     12/03/2014
# Copyright:   (c) Account Prism Pvt. Ltd.
# Licence:     all_rights_reserved
#-------------------------------------------------------------------------------

#imports
import wx
import mywxspinctrl
import lobstercvar
import lobsterpreferences

# class-name    : CPreferencesDlg
# class-description : this class initialize the preference dialog.
class CPreferencesDlg(wx.Dialog):

    def __init__(self, parent):

        """
        Constructor :-

        Throws Exception : No

        Inputs : (i) parent : specifies parent of this dialog

        Outputs : does not return any values

        Purpose : initialize all the components of dialog

        """
        # calling parent class constructor
        wx.Dialog.__init__(
                            self, parent, title = "Preferences", pos = (450, 150),
                            size = (400, 400), name = "preferencesDialog"
                            )
        # position value of x and y
        iXValue = 0
        iYValue = 0

        # creating panel which contains all components
        self.m_objPanel = wx.Panel(self)

        self.m_objGui = parent

        self.m_objCPreferences = parent.m_objLobsterDataContext.__m_objCPreferences__

        # creating a static box which contains some General settings of preferences
        sbGeneralPreferences = wx.StaticBox(
                                            self.m_objPanel, id = -1, label = "General",
                                            pos = (iXValue + 5, iYValue + 5), size = (150, 290)
                                            )

        # making group of two radio buttons for Application Mode. (i) Standard, (ii) Frequent
        # Note :    reason of choosing RadioBox instead of radio button is, if we choose radiobox, wee need to create object of each and
        #           every radiobutton. while radiobox provide a group of radio buttons. we nned to create only one obje and we get multile
        #           radio buttons by creating single object of radiobox
        self.m_rbAppMode = wx.RadioBox(
                                        self.m_objPanel, id = -1, label = "App Mode",
                                        pos = (iXValue + 25, iYValue + 25), size = (115, 70),
                                        choices = ["Standard", "Frequent"], majorDimension = 2, style = wx.RA_SPECIFY_ROWS,
                                        validator = wx.DefaultValidator, name = "appmode"
                                        )

        # Binding this group of radio buttons to event
        self.m_rbAppMode.Bind(wx.EVT_RADIOBOX, self.OnAppModeChoice)

        # making group of two radio buttons for Numeric Notation. (i) Standard, (ii) Engineering
        self.m_rbNumericNotation = wx.RadioBox(
                                                self.m_objPanel, id = -1, label = "Numeric Notation",
                                                pos = (iXValue + 25, iYValue + 100), size = (115, 90),
                                                choices = ["Standard", "Engineering", "Exponent"], majorDimension=3,
                                                style = wx.RA_VERTICAL, validator = wx.DefaultValidator, name = "numericnotation"
                                                )

        # Binding this group of radio buttons to event
        self.m_rbNumericNotation.Bind(wx.EVT_RADIOBOX, self.OnNumericNotationChoice)

        # making group of two radio buttons for making Search History enable or disable. (i) yes, (ii) No
        self.m_rbRememberSearchHistory = wx.RadioBox(
                                                        self.m_objPanel, id = -1, label = "Search History",
                                                        pos = (iXValue + 25, iYValue + 195), size = (115, 80), choices = ["Yes", "No"],
                                                        majorDimension = 2, style = wx.RA_SPECIFY_ROWS, validator = wx.DefaultValidator,
                                                        name = "searchhistory"
                                                    )

        # Binding this group of radio buttons to event
        self.m_rbRememberSearchHistory.Bind(wx.EVT_RADIOBOX, self.OnSearchHistoryChoice)

        # Creating Spin Control which specifies history of specific number of CVar
        self.m_spinHistoryValues = mywxspinctrl.CSpinCtrl(
                                                            self.m_objPanel, objMethod = None, iValue = 1,
                                                            tupPos = (iXValue + 80, iYValue + 215), tupSize = (50, 20),
                                                            iMin = 1, iMax = 100
                                                        )
        self.m_spinHistoryValues.SetValue(10)

        # Creating a group of radio buttons which specifies that how many columns you want to appear in the ListBox

        self.objSelectColumnStaticBox = wx.StaticBox(
                                                        self.m_objPanel, id = -1, label = "Select Column",
                                                        pos = (iXValue + 170, iYValue + 5), size = (140, 290)
                                                    )

        # creating static box for grouping some of the components
        stboxColumn = wx.StaticText(self.m_objPanel, id = -1, label = "Columns", pos = (iXValue + 180, iYValue + 30))

        # creating checkbox which is used to select all list items from checklistbox
        self.m_chkBoxAll = wx.CheckBox(self.m_objPanel, -1, label = 'Select All', pos = (iXValue + 190, iYValue + 50) )
        self.m_chkBoxAll.SetValue(True)

        # Binding to the event handler
        self.m_chkBoxAll.Bind(wx.EVT_CHECKBOX, self.OnSelectAllColumns)

        # creating CheckListBox which contains list of colum names with checkbox
        self.m_lscbColumns = wx.CheckListBox(
                                self.m_objPanel, pos = (iXValue + 185, iYValue + 70), size = (115, 200),
                                choices = lobstercvar.CVar.ms_lsStrHeaders, style = 0,
                                name = "columns"
                            )

        iLengthOfChkList = self.m_lscbColumns.GetCount()
        for iIndex in range(iLengthOfChkList):
               self.m_lscbColumns.Check(iIndex, check = True)

        # creating static box which groups the window related settings
        sbWindowPreferences= wx.StaticBox(
                                            self.m_objPanel, id = -1, label = "Window",
                                            pos = (iXValue + 325, iYValue + 5), size = (150, 170)
                                        )

        # Creatinf static text which display label of Refresh Time.
        lblRefreshTime = wx.StaticText(self.m_objPanel, id = -1, label = "Refresh Time: ", pos = (iXValue + 340, iYValue + 25))

        # creating Spin Control which take refesh time from user set refresh the application's data according to that time in seconds
        self.m_spinRefreshTime = mywxspinctrl.CSpinCtrl(
                                                        self.m_objPanel, objMethod = None, iValue = 1,
                                                        tupPos = (iXValue + 415, iYValue + 25), tupSize = (50, 20), iMin = 1, iMax = 100
                                                        )
        self.m_spinRefreshTime.SetValue(5)

        # creating group of radio buttons which specifies that you want to see plot related settings
        self.m_rbPlots = wx.RadioBox(
                                        self.m_objPanel, id = -1, label = "Plot", pos = (iXValue + 340, iYValue + 55),
                                        size = (100, 110), choices = ["Yes", "No"], majorDimension = 2,
                                        style = wx.RA_SPECIFY_COLS, validator = wx.DefaultValidator, name = "plot"
                                    )

        # binding this group to event handler
        self.m_rbPlots.Bind(wx.EVT_RADIOBOX, self.OnPlotChoice)

        # creating check boxes for plot, it allows to plot X, Y and as well as both
    	self.m_chkBoxPlotX = wx.CheckBox(self.m_objPanel, -1, label = 'Plot X', pos = (iXValue + 345, iYValue + 100) )
    	self.m_chkBoxPlotY = wx.CheckBox(self.m_objPanel, -1, label = 'Plot Y', pos = (iXValue + 345, iYValue + 120) )
        self.m_chkBoxPlotXY = wx.CheckBox(self.m_objPanel, -1, label = 'Plot XY', pos = (iXValue + 345, iYValue + 140) )

        # creating static box which groups the window related settings
        sbCopy= wx.StaticBox(
                                            self.m_objPanel, id = -1, label = "Copy",
                                            pos = (iXValue + 325, iYValue + 180), size = (114, 50)
                                        )

        self.m_chkBoxCopyPath = wx.CheckBox(self.m_objPanel, -1, label = 'Path', pos = (iXValue + 330, iYValue + 200) )
    	self.m_chkBoxCopyValue = wx.CheckBox(self.m_objPanel, -1, label = 'Value', pos = (iXValue + 380, iYValue + 200) )


        # Set size of Preferances Dialog
        self.SetSize((500, 350))

        # Creating Button, that will be useful to save all preferences configuration
        self.m_btnSave = wx.Button(self.m_objPanel, id = -1, label = "Save", pos = (iXValue + 340, iYValue + 290), size = (50, 25))

        # Binding event handler with this save button
        self.m_btnSave.Bind(wx.EVT_BUTTON, self.OnSave)

        # Creating Button, that will be useful to Close the Dialog
        self.m_btnClose = wx.Button(self.m_objPanel, id = -1, label = "Close", pos = (iXValue + 420, iYValue + 290), size = (50, 25))

        # binding event handler with this close button
        self.m_btnClose.Bind(wx.EVT_BUTTON, self.OnClose)

        if (self.m_objCPreferences != None):
            self.MInitPreferencesDialog(self.m_objCPreferences)

        return

    """----------------------------------------------------------------------"""

    def OnAppModeChoice(self, evt):
        """
        Event Handler Functions :-

        Throws Exception : No

        Inputs : (i) evt : event object

        Output : does not return any values

        Purpose : provide an option that you want to start application in standard mode or frequent mode

        """
        # TO DO : after developing lobsterpreferences code will be written here

        return

    """----------------------------------------------------------------------"""
    def OnNumericNotationChoice(self, evt):
        """
        Event Handler Functions :-

        Throws Exception : No

        Inputs : (i) evt : event object

        Output : does not return any values

        Purpose : provide an option that you want to see CVar's value in standars notation or engineering notations

        """
        # TO DO : after developing lobsterpreferences code will be written here

        return

    """----------------------------------------------------------------------"""
    def OnSearchHistoryChoice(self, evt):

        """
        Event Handler Functions :-

        Throws Exception : No

        Inputs : (i) evt : event object

        Output : does not return any values

        Purpose : According to user's choice it will set preferences configuration
                if User want to set configuration about history of cvar then it will
                ask number of latest changed cvar history
        """
        # fetchinng index of radio button which is selected by user
        # if user has selected Yes then its value will be 0 otherwise 1
        iSelected = evt.GetSelection()
        # if User has selected yes than only enable spin contron which takes number of cvar history user wants
        if (iSelected == 0):
            self.m_spinHistoryValues.Enable(True)
        else:
            self.m_spinHistoryValues.Enable(False)

        return

    """----------------------------------------------------------------------"""
    def OnFilterColumnChoice(self, evt):
        """
        Event Handler Functions :-

        Throws Exception : No

        Inputs : (i) evt : event object

        Output : does not return any values

        Purpose : According to user's choice it will set preferences configuration
                if user has checked 5 columns then it will save configuration that
                at the initial time of application it will display only 5 columns
        """
        # fetchinng index of radio button which is selected by user
        iSelected = evt.GetSelection()
        # if user has selected yes than only enable checklistbox of columns
        if (iSelected == 0):
            self.m_chkBoxAll.Enable(True)
            self.m_lscbColumns.Enable(True)
        else:
            self.m_chkBoxAll.Enable(False)
            self.m_lscbColumns.Enable(False)

        return

    """----------------------------------------------------------------------"""
    def OnSelectAllColumns(self, evt):
        """
        Event Handler Functions :-

        Throws Exception : No

        Inputs : (i) evt : event object

        Output : does not return any values

        Purpose : provide a facility to select all the items at one click.
        """
        # fetching data from checkbox, if user hass checked then this value will be 1 otherwise 0
        iSelected = evt.GetSelection()

        iLengthOfChkList = self.m_lscbColumns.GetCount()
        if (iSelected == 0):
        # if user has checked then check all the items in the check list items
            for iIndex in range(iLengthOfChkList):
               self.m_lscbColumns.Check(iIndex, check = False)
        else:
            for iIndex in range(iLengthOfChkList):
               self.m_lscbColumns.Check(iIndex, check = True)

        return

    """----------------------------------------------------------------------"""
    def OnPlotChoice(self, evt):
        """
        Event Handler Functions :-

        Throws Exception : No

        Inputs : (i) evt : event object

        Output : does not return any values

        Purpose : provide an option for ploting CVar.
                    if yes then it will be able to plot CVar's Value
        """
        # fetching index of a radio button which is selected by user
        iSelected = evt.GetSelection()
        # there are only two options (yes and No)
        # if yes then only it will allow to plot a CVar
        if (iSelected == 0):
            self.m_chkBoxPlotX.Enable(True)
            self.m_chkBoxPlotY.Enable(True)
            self.m_chkBoxPlotXY.Enable(True)
        else:
            self.m_chkBoxPlotX.Enable(False)
            self.m_chkBoxPlotY.Enable(False)
            self.m_chkBoxPlotXY.Enable(False)

        return

    """----------------------------------------------------------------------"""
    def OnClose(self, evt):
        """
        Event Handler Functions :-

        Throws Exception : No

        Inputs : (i) evt : event object

        Output : does not return any values

        Purpose : close preferences dialog box

        """
        self.Destroy()

        return

    """----------------------------------------------------------------------"""
    def OnSave(self, evt):
        """
        Event Handler Functions :-

        Throws Exception : No

        Inputs : (i) evt : event object

        Output : does not return any values

        Purpose : It will save all configuration settings for preferences

        """
        lsEPlots = []

        if (self.m_chkBoxPlotX.GetValue() == True):
            lsEPlots.append(0)
        if (self.m_chkBoxPlotY.GetValue() == True):
            lsEPlots.append(1)
        if (self.m_chkBoxPlotXY.GetValue() == True):
            lsEPlots.append(2)

        lsECopyPref = []

        if(self.m_chkBoxCopyPath.GetValue() == True):
            lsECopyPref.append(0)

        if(self.m_chkBoxCopyValue.GetValue() == True):
            lsECopyPref.append(1)

        self.m_objCPreferences.MSetAppMode(eAppMode = self.m_rbAppMode.GetSelection())
        self.m_objCPreferences.MSetNumericNotation(eNotation = self.m_rbNumericNotation.GetSelection())
        self.m_objCPreferences.MSetWatchWindowRefreshTime(iWatchWindowRefreshTime = self.m_spinRefreshTime.GetValue())
        self.m_objCPreferences.MSetHistorySize(iSearchHistorySize = self.m_spinHistoryValues.GetValue())
        self.m_objCPreferences.MSetFilteredColumns(lsIFilteredColumns = list(self.m_lscbColumns.Checked))
        self.m_objCPreferences.MSetPlots(lsEPlots = lsEPlots)
        self.m_objCPreferences.MSetCopyPref(lsECopyPref = lsECopyPref)

        lsIColumns = list(self.m_lscbColumns.Checked)

        for i in range(len(lobstercvar.CVar.ms_lsStrHeaders)):
            if(i not in lsIColumns):
                self.m_objGui.m_objCWxListView.SetColumnWidth(i, 0)
            else:
                self.m_objGui.m_objCWxListView.SetColumnWidth(i, 80)

        dlgSavePreferences = wx.MessageDialog(
                                                self, "Successfuly Saved...",
                                               "Save Preferences", wx.OK|wx.ICON_INFORMATION
                                               )

        result = dlgSavePreferences.ShowModal()

        dlgSavePreferences.Destroy()

        if result == wx.ID_OK:
            self.Destroy()

        return

    """----------------------------------------------------------------------"""
    def MInitPreferencesDialog(self, objCPreferences):
        """
        Member Function :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : does not return any values

        Purpose : initialize GUI of preferences dialog

        """
        self.m_rbAppMode.SetSelection(objCPreferences.MGetAppMode())
        self.m_rbNumericNotation.SetSelection(objCPreferences.MGetNumericNotation())

        self.m_rbRememberSearchHistory.SetSelection(1)
        if (objCPreferences.MGetHistorySize() == 0):
            self.m_spinHistoryValues.Disable()

        self.m_spinHistoryValues.SetValue(objCPreferences.MGetHistorySize())

        iLengthOfChkList = self.m_lscbColumns.GetCount()
        # if user has checked then check all the items in the check list items
        for iIndex in range(iLengthOfChkList):
           self.m_lscbColumns.Check(iIndex, check = False)

        for i in objCPreferences.MGetFilteredColumns():
            self.m_lscbColumns.Check(i, True)

        if (len(objCPreferences.MGetPlots()) == 0):
            self.m_rbPlots.SetSelection(1)
            self.m_chkBoxPlotX.Disable()
            self.m_chkBoxPlotY.Disable()
            self.m_chkBoxPlotXY.Disable()

        else:
            for i in objCPreferences.MGetPlots():
                if (i == 0):
                    self.m_chkBoxPlotX.SetValue(True)
                if (i == 1):
                    self.m_chkBoxPlotY.SetValue(True)
                if (i == 2):
                    self.m_chkBoxPlotXY.SetValue(True)

        self.m_spinRefreshTime.SetValue(objCPreferences.MGetWatchWindowRefreshTime())

        for iCounter in objCPreferences.MGetCopyPref():
            if(iCounter == 0):
                self.m_chkBoxCopyPath.SetValue(True)
            if(iCounter == 1):
                self.m_chkBoxCopyValue.SetValue(True)

        return

    """----------------------------------------------------------------------"""

if __name__ == '__main__':
    app = wx.App(False)
    objCPreferences = lobsterpreferences.CPreferences(
                                        eAppMode = 1, eNumericNotation = 0,
                                         iWatchWindowRefreshTime = 12, iSearchHistorySize = 0 ,
                                         lsIFilteredColumns = [2, 4], lsEPlots = [3] )
    dlg = CPreferencesDlg(None)
    dlg.ShowModal()
