#-------------------------------------------------------------------------------
# Name:        stringeditdialog.py
# Purpose:     This class is used to create a dialog window for editing the
#               values of CVar of type String
#
# Author:      Kruti
#
# Created:     19-03-2014
# Copyright:   (c) Account Prism Pvt. Ltd.
# Licence:     all_rights_reserved
#-------------------------------------------------------------------------------

#   imports
import wx
import lobstercvar as cvar
import lobstereventhandler

#   class-name :- CWxDialog
#   class-description :- This class is used to create a dialog window for
#                        value of CVars of type String
class CWxDialog(wx.Dialog):

    def __init__(self, objCvar, parent, id, title, pos, size):

        """
        Constructor :-

        Throws Exception :- Yes, throws exception when
                            (i) object of CVar is not of type String

        Inputs :- (i) objCvar :- object of class lobstercvar

                  (ii) parent :- parent class or window of CWxDialog

                  (iii) id :- id of the Dialog control

                  (iv) title :- title of the dialog window

                  (v) pos :- a tuple, representing the position of the dialog
                              window

                  (vi) size :- a tuple, represemting the size of the dialog
                                window

        Outputs :- does not return any value

        Purpose :- initializes the dialog window and member variables to default
                    values

        """

        #   calling the contrcutor of the parent class
        wx.Dialog.__init__(self, parent, id = wx.ID_ANY, title = "String Edit Dialog",
                         pos = (0,0), size = (500, 500))

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

        #   getting the type of the CVar
        intType = self.m_objCVar.MGetCVarType()

        #   if the type of the CVar is not SafeArray then throw an exception
        if(intType != 15):
            raise Exception("stringeditdialog.py : CVar of String type is expected")

        #   getting the adapted value of the CVar
        value = self.m_objCVar.MGetCVarAdaptedValue()

##        print value

        #   creating a TextCtrl
        self.m_textctrl = wx.TextCtrl(self)

        #   setting the adapted value of the CVar to the TextCtrl
        self.m_textctrl.SetValue(value)

        #   binding the method to the tool "Save"
        self.Bind(wx.EVT_TOOL, self.MOnSave, id = 6)

        #   creating a asizer
        sizer = wx.BoxSizer(wx.VERTICAL)

        #   adding toolbar to the sizer at the top most position
        sizer.Add(toolbar, 0, wx.GROW)

        #   adding the TextCtrl to the sizer below the toolbar
        sizer.Add(self.m_textctrl, 1, wx.TOP|wx.GROW)

        #   settingi the sizer to the the window
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

        #   getting the value of the TextCtrl
        strModifiedValue = self.m_textctrl.GetValue()

        #   setting the modified adapted value to the object of CVar
        self.m_objCVar.MSetCVarAdaptedValue(strModifiedValue)

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
    dictCVarAttributeAndValue = {"AbsolutePath" : "XStreamDSO.ExecsNameAllGeneric",
    "Type" :"String",
    "Requested" : "StringValue",
    "Adapted" : "StringValue",
    "Default" : "StringValue",
    "Flags" : "RG"}

    #   creating the object of CVar with dictCVarAttributeAndValue
    objLobsterCVar = cvar.CVar(dictCVarAttributeAndValue)

    #   creating the object of CWxDialog
    frame = CWxDialog(objLobsterCVar, None, None, None, None, None)

    #   displaying the dialog window
    frame.Show(True)

    app.MainLoop()
