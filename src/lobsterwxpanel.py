#-------------------------------------------------------------------------------
# Name:        lobsterwxpanel.py
# Purpose:     This module creates a panel that acts as a container of GUI
#              controls like Listview, toolbar which form the watch window of app.
#
# Author:      Kruti
#
# Created:     15-03-2014
# Copyright:   (c) Account Prism Pvt. Ltd.
# Licence:     all_rights_reserved
#-------------------------------------------------------------------------------

#   imports
import wx
import myWxProgressbar as progressbar
import mywxlistview as listview
import lobstercvar as cvar

#   class-name :- CWxPanel
#   class-description :- This class creates a panel that contains various GUI
#                        controls. It's responsible for showing watch window
#                        in the application
class CWxPanel(wx.Panel):

    def __init__(self, parent, iNumCols, *args, **kwargs):

        """
        Constructor :-

        Throws Exception :- No

        Inputs :- (i) parent :- parent window or class of the current class

                  (ii) iNumCols :- number of columns to be sorted

                  (iii) *args :- arbitrary number of arguments or
                                 list of arguments -as positional arguments,
                                 it is used to call the parent constructor

                  (iv) **kwargs :- keyword arguments or named arguments,
                                it is used to call the parent constructor

        Outputs :- does not return any value

        Purpose :- It initializes the CWxPanel class

        """

        #   calling constructor of wx.Panel class
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.m_objLobsterDataContext = parent.m_objLobsterDataContext

        dictCVarCollection = self.m_objLobsterDataContext.m_dictCVarCollection

        #   creating a toolbar
        toolbar = wx.ToolBar(self, -1, style=wx.TB_HORIZONTAL | wx.NO_BORDER)

        #   creating object of CWxListView class
        self.m_objCWxListView = listview.CWxListView(self, dictCVarCollection, iNumCols)

        #   creating a sizer
        panelsizer = wx.BoxSizer(wx.VERTICAL)

        #   adding toolbar to sizer
        panelsizer.Add(toolbar, 0, wx.LEFT | wx.TOP | wx.GROW)

        bShowToolBar = False

        if bShowToolBar:
            #   TODO :- in the next version
            #   adding tools to the toolbar
            toolbar.AddSimpleTool(1, wx.ArtProvider_GetBitmap(wx.ART_DELETE), 'Delete', '')
            toolbar.Realize()

            toggleButton1 = wx.ToggleButton(parent = self, id = -1, label =  "Plot X", pos = (80, 2), size = (45, 25), style = 0)
            toggleButton2 = wx.ToggleButton(parent = self, id = -1, label =  "Plot Y", pos = (130, 2), size = (45, 25), style = 0)
            toggleButton3 = wx.ToggleButton(parent = self, id = -1, label =  "Plot XY", pos = (180, 2), size = (45, 25), style = 0)
            toggleButton4 = wx.ToggleButton(parent = self, id = -1, label =  "Dump Into File", pos = (230, 2), size = (75, 25), style = 0)

            textctrl = wx.TextCtrl(parent = self, id = -1, pos = (310, 2), size = (75, 25), style = 0)

            panelsizer.Add(toggleButton1, 1, wx.LEFT | wx.TOP)
            panelsizer.Add(toggleButton2, 1, wx.LEFT | wx.TOP)
            panelsizer.Add(toggleButton3, 1, wx.LEFT | wx.TOP)
            panelsizer.Add(toggleButton4, 1, wx.LEFT | wx.TOP)
            panelsizer.Add(textctrl, 1, wx.LEFT | wx.TOP)

        #   adding the object of CWxListView to the sizer
        panelsizer.Add(self.m_objCWxListView, 1, wx.LEFT | wx.TOP | wx.GROW)

        #   setting panelsizer as the sizer of the current window
        self.SetSizer(panelsizer)

        #   fitting the window to the size, that enables it to contain its child-controls properly
        self.Fit()

        return

    """----------------------------------------------------------------------"""