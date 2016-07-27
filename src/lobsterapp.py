#-------------------------------------------------------------------------------
# Name:        lobsterapp.py
# Purpose:      This class is used to start the application
#
# Author:      Kruti
#
# Created:     13/02/2014
# Copyright:   (c) Account Prism Pvt. Ltd.
# Licence:     all_rights_reserved
#-------------------------------------------------------------------------------

#   imports
import wx
import lobsterdatacontext as datacontext
import lobsterguicontext as gui

#   class-name :- MyApp
#   class-description :- This class is used to start the application
class MyApp(wx.App):

    def OnInit(self):

        """
        Member Method :-

        Throws Exception :- No

        Inputs :- does not receive any inputs

        Outputs :- does not return any value

        Purpose :- It sets the variables, which are used to start the application

        """

        objLobsterDataContext = datacontext.CDataContext()

        dictCVarCollection = objLobsterDataContext.m_dictCVarCollection

        #   specifying the value of the root
        strRoot = "XStreamDSO"

        #   getting the root
        root = dictCVarCollection.get(strRoot)

        #   inserting value of Root in the dictionary
        dictCVarCollection["Root"] = root

        #   creating the object of CGUIContext
        objCGUIContext = gui.CGUIContext(objLobsterDataContext)

        return True


    """----------------------------------------------------------------------"""

if __name__ == '__main__':
    app = MyApp(True)
    app.MainLoop()