#-------------------------------------------------------------------------------
# Name:        arrayeditdialog.py
# Purpose:      This module contains class is used to create a dialog window for
#                editing the values of CVars of type SafeArray
#
# Author:      Kruti
#
# Created:     19-03-2014
# Copyright:   (c) Account Prism Pvt. Ltd.
# Licence:     all_rights_reserved
#-------------------------------------------------------------------------------

#   imports
import wx
import mywxgridview as gridview
import lobstercvar as cvar
import lobstereventhandler

#   class-name :- CWxDialog
#   class-description :- This class is used to create a dialog window for
#                        value of CVars of type SafeArray
class CWxDialog(wx.Dialog):

    def __init__(self, objCvar, parent, id, title, tupPos, tupSize):

        """
        Constructor :-

        Throws Exception :- Yes, throws exception when
                            (i) object of CVar is not of type SafeArray

        Inputs :- (i)   objCvar :- object of class lobstercvar

                  (ii)  parent :- parent class or window of CWxDialog

                  (iii) id :- id of the Dialog control

                  (iv)  title :- title of the dialog window

                   (v)  pos :- a tuple, representing the position of the dialog
                              window

                   (vi) size :- a tuple, represemting the size of the dialog
                                window

        Outputs :- does not return any value

        Purpose :- initializes the dialog window and member variables to default
                    values

        """

        #   calling the contrcutor of the parent class
        wx.Dialog.__init__(self, parent, id = wx.ID_ANY, title = title,
                         pos = tupPos, size = tupSize)

        #   creating a toolbar
        toolbar = wx.ToolBar(self, -1, style=wx.TB_HORIZONTAL | wx.NO_BORDER)

        #   adding tools to the toolbar
        toolbar.AddSimpleTool(1, wx.ArtProvider_GetBitmap(wx.ART_COPY), 'Copy', '')
        toolbar.AddSimpleTool(2, wx.ArtProvider_GetBitmap(wx.ART_CUT), 'Cut', '')
        toolbar.AddSimpleTool(3, wx.ArtProvider_GetBitmap(wx.ART_PASTE), 'Paste', '')
        toolbar.AddSimpleTool(4, wx.ArtProvider_GetBitmap(wx.ART_UNDO), 'Undo', '')
        toolbar.AddSimpleTool(5, wx.ArtProvider_GetBitmap(wx.ART_REDO), 'Redo', '')
        toolbar.AddSimpleTool(6, wx.ArtProvider_GetBitmap(wx.ART_FILE_SAVE), 'Save','')
        toolbar.Realize()

        #   creating a member variable to store the parent object
        self.parent = parent

        #   creating a member variable to store the object of lobstercvar
        self.m_objCVar = objCvar

        #   binding the method to the tool "Save"
        self.Bind(wx.EVT_TOOL, self.MOnSave, id = 6)

        #   TODO :- Code for the copy, cut, paste, undo, redo will be written in
        #           next revision of this file

        #   getting the type of the CVar
        intType = self.m_objCVar.MGetCVarType()

        #   if the type of the CVar is not SafeArray then throw an exception
        if(intType != cvar.CVar.mC_SAFEARRAY):
            raise Exception("arrayeditdialog.py : CVar of SafeArray type is expected")

        #   getting the adapted value of the CVar
        value = self.m_objCVar.MGetCVarAdaptedValue()

        #   creating an object of class CWxGridView
        self.m_objCWxGridView = gridview.CWxGridView(value = value, parent = self, ID = -1, size = (50, 50), style = 0)

        #   creating a asizer
        sizer = wx.BoxSizer(wx.VERTICAL)

        #   adding toolbar to the sizer at the top most position
        sizer.Add(toolbar, 0, wx.GROW)

        #   adding the object of CWxGridView to the sizer below the toolbar
        sizer.Add(self.m_objCWxGridView, 1, wx.TOP | wx.GROW)

        #   setting the sizer to the the window
        self.SetSizer(sizer)

        #   displaying the entire window
        self.Show()

        return

    """----------------------------------------------------------------------"""

    def MOnSave(self, event):

        """
        Member Method :-

        Throws Exception :- No

        Inputs :- (i) event :- event object

        Outputs :- does not return any value

        Purpose :- This method performs the operations when the user clicks the
                    Save tool of the dialog window

        """

        self.m_iNumRows, self.m_iNumCols, self.m_lsColumns = self.m_objCWxGridView.MGetNumRowsColsAndColsValues()

        #   defining a variable to store the value combining values of all the
        #   cells of the gridview
        strTempCellValue = ""

        #   defining a variable to store the value of each cell of the gridview
        strCellValue = ""

        #   iterating a loop until the number of rows
        for iIdx in range(self.m_iNumRows):
            #   iterating a loop until the number of columns
            for i in range(self.m_iNumCols):
                #   getting the value of the cell at possition (iIdx, i)
                strCellValue = self.m_objCWxGridView.GetCellValue(iIdx, i)
                #   concatinating the cell values
                strTempCellValue += strCellValue
                #   if the current cell is not the last cell of the column, then
                #   append a comma to the cell value
                if(i < (self.m_iNumCols - 1)):
                    strTempCellValue += ","
            #   append a semi colon to the value of the last cell of the row
            strTempCellValue += ";"

        #   removing the semi colon from the last index
        strTempCellValue = strTempCellValue[:-1]

        #   setting the updated adapted value to the object of CVar
        self.m_objCVar.MSetCVarAdaptedValue(strTempCellValue)

        #   calling the method of lobstereventhandler class
        lobstereventhandler.CEventHandler.MSOnSaveEdit(event, self.parent)

        #   disappearing the dialog window when the edited value is saved in the
        #   object
        self.Destroy()

        return

    """----------------------------------------------------------------------"""


#   for testing purpose
if __name__ == '__main__':

    #   creating the object of PySimpleApp
    app = wx.PySimpleApp()

    #   creating a dictionary having the attributes of the CVar
    dictCVarAttributeAndValue = {"AbsolutePath" : "XStreamDSO.InternalCollection.Acquisition.Simulator.Channels.C4.Mfe670BGainOffsetCurve",
     "Type" :"SafeArray","Requested" : "0,0E-3;","Adapted" : "34,22;23,56;12,24","Default" : "0,0E-3;",
     "Range" : "19,0,65535,1;5,-400,400,0.001", "Flags" : "-"}

    #   creating the object of CVar with dictCVarAttributeAndValue
    objLobsterCVar = cvar.CVar(dictCVarAttributeAndValue)

    #   creating the object of CWxDialog
    frame = CWxDialog(objLobsterCVar, parent = None, id = wx.ID_ANY, title = "Array Edit Dialog", tupPos = (0,0), tupSize = (300, 300))

    #   displaying the dialog window
    frame.Show(True)

    app.MainLoop()