#-------------------------------------------------------------------------------
# Name:        lobsterguicontext.py
# Purpose:      This module CGUIContext class contains all the information about
#               all the GUI controls used in the application and binds those
#               controls with their respective events
#
# Author:      Kruti
#
# Created:     13/02/2014
# Copyright:   (c) Account Prism Pvt. Ltd.
# Licence:     all_rights_reserved
#-------------------------------------------------------------------------------

#   imports
import wx
import wx.aui
import yaml
import mywxtreeview as treeview
import mywxlistview as listview
import lobsterbase
import lobstereventhandler
import lobstercvar as cvar
import mywxgridview as gridview
import lobsterwxpanel as panel
import arrayeditdialog
import mywxpopupmenu as popupmenu
import mymenu as menu
import myWxProgressbar as progressbar

#   class-name :- CGUIContext
#   class-description :- This class extends wx.Frame class and contains information about all the GUI
#                        controls used in the application and binds those controls
#                        with theie respective events
class CGUIContext(wx.Frame):

    #   static constant member representing types of the CVars displayed in the listview
    #   for eg. Normal Child CVars, Favorite CVars or CVars displayed as a resuls
    #   of Search
    mC_NORMAL_CHILD_CVARS = 0
    mC_FAVORITE_CVARS = 1
    mC_SEARCHED_CVARS = 2
    mC_NO_CVARS = None

    def __init__(self, objLobsterDataContext, *args, **kwargs):

        """
        Constructor :-

        Throws Exception :- No

        Inputs :- (i) objLobsterDataContext :- object of class CDataContext

                  (ii) *args :- arbitrary number of arguments or
                                list of arguments -as positional arguments,
                                it is used to call the parent constructor or
                                function with the arguments specified by the
                                user.

                  (iii) **kwargs :- keyword arguments or named arguments,
                                it is used to call the parent constructor or
                                function with the arguments specified by the
                                user.

        Outputs :- does not return any value

        Purpose :- initializes the GUI controls and prepares graphical layout for
                   the application
        """

        #   calling the super class' constructor
        wx.Frame.__init__(self, parent = None, title = "LobsterPy", *args, **kwargs)

        #   storing reference to object of datacontext in the application
        self.m_objLobsterDataContext = objLobsterDataContext

        #   setting icon for the application
        self.SetIcon(wx.Icon(r'..\res\Lobster.ico', wx.BITMAP_TYPE_ICO, 16, 16))

        # creating the menubar object
        self.m_objMenuBar = menu.CMenuBar()

        #   calling the method MCreateMenuBar
        self.MCreateMenuBar()

        # setting the menubar as the application menubar
        self.SetMenuBar(self.m_objMenuBar.m_menubarInstance)

        #   creating toolbar in the application
        toolbar = wx.ToolBar(self, -1, style=wx.TB_HORIZONTAL | wx.NO_BORDER)

        #   adding tools to the toolbar

        toolbar.AddSimpleTool(
                                id = 7,
                                bitmap = wx.Bitmap(r'../res/edit.ico'),
                                shortHelpString = 'Edit',
                                longHelpString = ''
                            )

        toolbar.AddSimpleTool(12, wx.ArtProvider_GetBitmap(wx.ART_FILE_SAVE), 'Save', '')

        toolbar.AddSimpleTool(
                                id = 2,
                                bitmap = wx.ArtProvider_GetBitmap(wx.ART_COPY),
                                shortHelpString = 'Copy',
                                longHelpString = ''
                            )

        toolbar.AddSimpleTool(
                                id = 4,
                                bitmap = wx.ArtProvider_GetBitmap(wx.ART_UNDO),
                                shortHelpString = 'Undo',
                                longHelpString = ''
                            )

        toolbar.AddSimpleTool(
                                id = 5,
                                bitmap = wx.ArtProvider_GetBitmap(wx.ART_REDO),
                                shortHelpString = 'Redo',
                                longHelpString = ''
                            )

        #   adding tools with custom images
        toolbar.AddSimpleTool(
                                id = 6,
                                bitmap = wx.Bitmap(r'../res/star_gold_16.ico'),
                                shortHelpString = 'Add to Favorite',
                                longHelpString = ''
                            )



        toolbar.AddSimpleTool(
                                id = 8,
                                bitmap = wx.Bitmap(r'../res/Window.ico'),
                                shortHelpString = 'Add to Watch Window',
                                longHelpString = ''
                            )

        toolbar.AddSimpleTool(
                                id = 11,
                                bitmap = wx.Bitmap(r'../res/folder-bookmarks.ico'),
                                shortHelpString = 'Favorite CVars List',
                                longHelpString = ''
                            )

        toolbar.AddSimpleTool(
                                id = 9,
                                bitmap = wx.ArtProvider_GetBitmap(wx.ART_CROSS_MARK),
                                shortHelpString = 'Exit',
                                longHelpString = ''
                            )

##        toolbar.AddSimpleTool(
##                                id = 10,
##                                bitmap = wx.ArtProvider_GetBitmap(wx.ART_PASTE),
##                                shortHelpString = 'Paste',
##                                longHelpString = ''
##                            )





        #   invoking Realize() method. This method must have to invoked,
        #   after, every tool have been added
        toolbar.Realize()

        #   setting the toolbar in the GUI
        self.SetToolBar(toolbar)

        #   binding the events to the tools
        self.Bind(wx.EVT_TOOL, self.MOnCopy, id = 2)
        self.Bind(wx.EVT_TOOL, self.MOnUndo, id = 4)
        self.Bind(wx.EVT_TOOL, self.MOnRedo, id = 5)
        self.Bind(wx.EVT_TOOL, self.MOnAddToFavorite, id = 6)
        self.Bind(wx.EVT_TOOL, self.MOnEdit, id = 7)
        self.Bind(wx.EVT_TOOL, self.MOnAddToWatchWindow, id = 8)
        self.Bind(wx.EVT_TOOL, self.MOnClose, id = 9)
        self.Bind(wx.EVT_TOOL, self.MOnWatchFavoriteCVars, id = 11)
        self.Bind(wx.EVT_TOOL, self.MOnSave, id = 12)

        #   binding close event with the frame
        self.Bind(wx.EVT_CLOSE, self.MOnClose)

        #   creating status bar
        self.m_objStatusBar = self.CreateStatusBar()

        #   creating progress bar
        self.m_objCWxProgressBar = progressbar.CWxProgressbar(
                                                windowObj = self.m_objStatusBar,
                                                tupPgbarLoc = (1130, 2),
                                                tupPgbarSize = (75, 20),
                                                tupStatusTimeTxtLoc = (1220, 2),
                                                tupStatusTimeTxtSize = (65, 20),
                                                tupStaticBoxLoc = (1300, 2),
                                                iMaxNoOfProcessorsAvailable = 2
                                            )

        self.m_objCWxProgressBar.MShowProgressBar(tupTime = (0, 0, 10))

        #   creating object of CWxTreeView class
        self.m_objCWxTreeView = treeview.CWxTreeView(
                                                self.m_objLobsterDataContext.m_dictCVarCollection,
                                                self.m_objLobsterDataContext.__m_strCurrentWorkingDirectory__,
                                                parent = self
                                                )

        #   creating object og CWxListView class
        self.m_objCWxListView = listview.CWxListView(
                                                self,
                                                self.m_objLobsterDataContext.m_dictCVarCollection,
                                                numCols = len(cvar.CVar.ms_lsStrHeaders)
                                                )

        #   binding a method to the listview, which is to be executed when
        #   a listitem is selected
        self.m_objCWxListView.Bind(wx.EVT_LIST_ITEM_SELECTED, self.MOnListItemClick)

        #   binding a method to the treeview,which is to be executed when
        #   the treeitem is expanding
        self.m_objCWxTreeView.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.MExpandTreeItem)

        #   binding a method to the treeview, which is to be executed when
        #   the treeitem is collapsing
        self.m_objCWxTreeView.Bind(wx.EVT_TREE_ITEM_COLLAPSING, self.MCollapseTreeItem)

        #   binding a method to the treeview, which is to be executed when
        #   the user clicks the right button on the tree item
        self.m_objCWxTreeView.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.MOnRightDown)

        #   binding a method to the treeview, which is to be executed when
        #   the user left clicks on the treeitem
        self.m_objCWxTreeView.Bind(wx.EVT_MOUSE_EVENTS, self.MOnItemClick)

        #   creating object of CWxPanel class
        self.m_objWxPanel = panel.CWxPanel(self, iNumCols = len(cvar.CVar.ms_lsStrHeaders))

        #   displaying watch window CVars
        self.m_objWxPanel.m_objCWxListView.MPopulateValuesInListView(
                                self.m_objLobsterDataContext.__m_lsStrWatchWindowCVars__,
                                None, False
                                )

        #   creating object of wx.aui.AuiManager
        #   wx.aui.AuiManager manages the panes associated with it for a particular wx.Frame
        self.m_objPaneMgr = wx.aui.AuiManager(self)

##        treePaneInfo = wx.aui.AuiPaneInfo()
##        treePaneInfo.Caption("TreeView")
##        treePaneInfo.Left()
##        treePaneInfo.MinSize((150,150))
##        treePaneInfo.Resizable(True)

        #   adding the treeview to the left side of the window
##        self.m_objPaneMgr.AddPane(self.m_objCWxTreeView, wx.aui.AuiPaneInfo().Left().Caption("TreeView"))
        self.m_objPaneMgr.AddPane(self.m_objCWxTreeView, wx.aui.AuiPaneInfo().Left().Caption("Directories").MinSize((150, 150)).Resizable(True))

        #   adding the listview to the center side of the window
        self.m_objPaneMgr.AddPane(self.m_objCWxListView, wx.aui.AuiPaneInfo().Center())

        #   adding the panel in the bottom of the window
        self.m_objPaneMgr.AddPane(self.m_objWxPanel, wx.aui.AuiPaneInfo().Bottom().Caption("Watch Window").MinSize((150, 150)))

        #   updating the AuiManager to save the changes
        self.m_objPaneMgr.Update()


        self.m_etypeOfDisplayedCVars = CGUIContext.mC_NO_CVARS

        #   By default, opening application in full screen mode
        self.Maximize(True)

        #   displaying the frame
        self.Show()

        return

    """----------------------------------------------------------------------"""

    def MOnSave(self, event):

        """
        Event handler method :-

        Purpose :- This method acts as a stub method. It invokes MSOnSaveEdit
                   method present in CEventHandler class
        """

        lobstereventhandler.CEventHandler.MSOnSaveEdit(event, self.m_objCWxListView)

        return

    """----------------------------------------------------------------------"""

    def MOnUndo(self, event):

        """
        Event handler method :-

        Purpose :- This method acts as a stub method. It invokes MSOnUndo method
                    present in CEventHandler class
        """

        lobstereventhandler.CEventHandler.MSOnUndo(self, event)

        return

    """----------------------------------------------------------------------"""

    def MOnRedo(self, event):

        """
        Event handler method :-

        Purpose :- This method acts as a stub method. It invokes MSOnUndo method
                    present in CEventHandler class
        """
        lobstereventhandler.CEventHandler.MSOnRedo(self, event)

        return

    """----------------------------------------------------------------------"""

    def MGetTypeOfDisplayedCVars(self):

        """
        Member Method :-

        Throws Exception :- No

        Inputs :- does not receive any inputs

        Outputs :- (i) self.m_etypeOfDisplayedCVars :- represents the type of the
                                                      CVars being displayed in
                                                      listview. For eg.
                                                      self.mC_NORMAL_CHILD_CVARS,
                                                      self.mC_FAVORITE_CVARS,
                                                      self.mC_SEARCHED_CVARS,

        Purpose :- This method is used to get the type of the CVar being
                    displayes in the listview

        """

        return self.m_etypeOfDisplayedCVars

    """----------------------------------------------------------------------"""

    def MCreateMenuBar(self):

        """
        Member Method :-

        Throws Exception :- No

        Inputs :- does not receive any inputs

        Outputs :- does not return any value

        Purpose :- This method creates a menubar

        """

        #   creating the list of the names of the menus
        lsMenuName = ["File", "Edit", "Options", "Help"]

        #   creating a dictionary that contains index of the menu name as a key
        #   and a list, that contains sublist of ids, names, tooltips,
        #   event handlers of the menu items, as values
        dictMenus = {
                        #   details about file-menu
                        0 : [
                                #   ids
                                [-1, -1],
                                #   menu labels
                                ["Favorite CVars", "Exit"],
                                #   tooltips
                                [
                                    "Click to see list of favorite cVars",
                                    "Click to close application"
                                ],
                                #   event handlers
                                [
                                    self.MOnWatchFavoriteCVars,
                                    self.MOnClose
                                ]
                            ],
                        #   details about edit menu
                        1 : [
                                #   ids
                                [-1, -1, -1, -1, -1],
                                #   menu labels
                                [
                                    "Copy", "Add to Favorite",
                                    "Add to Watch Window",
                                    "Undo", "Redo"
                                ],
                                #   tooltips
                                [
                                    "Click to copy selected cvar's value",
                                    "Click to make selected cvar Favorite",
                                    "Click to add selected cvar to Add to Watch Window",
                                    "Click to undo recent changes",
                                    "Click to redo recent changes"
                                ],
                                #   event handlers
                                [
                                    self.MOnCopy, self.MOnAddToFavorite,
                                    self.MOnAddToWatchWindow, self.MMethodToBeImplemented,
                                    self.MMethodToBeImplemented
                                ]
                            ],
                        #   details about options menu
                        2 : [
                                #   ids
                                [-1, -1, -1],
                                #   menu lables
                                [
                                    "Preferences", "Show Search History",
                                    "Advance Search"
                                ],
                                #   tooltips
                                [
                                    "Click to set Preferences",
                                    "Click to see Search History",
                                    "Click to perform Advance Search"
                                ],
                                #   event handlers
                                [
                                    self.MOnPreferences,
                                    self.MMethodToBeImplemented,
                                    self.MOnSearchConfiguration
                                ]
                            ],
                        #   details about Help menu
                        3 : [
                                #   ids
                                [-1, -1],
                                #   menu labels
                                ["About", "Show Help File"],
                                #   tooltips
                                [
                                    "Click to see About dialog box",
                                    "Click to see HTML help file"
                                ],
                                #   event handlers
                                [
                                    self.MMethodToBeImplemented,
                                    self.MMethodToBeImplemented
                                ]
                            ]
                    }

        #   iterating through the dictionary
        for iKey in dictMenus :
            #   getting the value of iKey from the dictionary
            lsList = dictMenus.get(iKey)
            #   creating parent menu object
            parentMenu = menu.CMenu(
                            strTitle = lsMenuName[iKey],
                            menubarParent = self.m_objMenuBar.m_menubarInstance,
                            liCMenuItemMenuItems = []
                            )

            #   iterating through each list item, retrived from the dictionary.
            #   This list item contains information about menu item
            for i in range(len(lsList[0])):
                #   creating menu item
                menu.CMenuItem(
                                iId = lsList[0][i], strTitle = lsList[1][i],
                                strTooltip = lsList[2][i],
                                strEvtHandlerMethod = lsList[3][i],
                                menuParentMenu = parentMenu.m_menuInstance,
                                frameParent = self
                            )

        return

    """----------------------------------------------------------------------"""

    def MOnListItemClick(self, event):

        """
        Event handler method :-

        Purpose : it a stub function which calls event handler function of CEventHandler class

        """
        lobstereventhandler.CEventHandler.MSOnListItemClick(event, self)

        return

    """----------------------------------------------------------------------"""

    def MOnEdit(self, event):

        """
        Event-handler Method :-

        Purpose :- it a stub function which calls MSOnEdit() function of CEventHandler class

        """

        lobstereventhandler.CEventHandler.MSOnEdit(event, self)

        return

    """----------------------------------------------------------------------"""

    def MOnAddToFavorite(self, event):

        """
        Event Handler Method :=

        Purpose : it a stub function which calls MSOnAddToFavorite()
                  function of CEventHandler class

        """

        lobstereventhandler.CEventHandler.MSOnAddToFavorite(event, self)

        return

    """----------------------------------------------------------------------"""

    def MOnWatchFavoriteCVars(self, event):

        """
        EventHandler Function :-

        Purpose : it a stub function which calls MOnWatchFavoriteCVars()
                  function of CEventHandler class

        """

        lobstereventhandler.CEventHandler.MSOnWatchFavoriteCVars(event, self)

        return

    """----------------------------------------------------------------------"""

    def MOnAddToWatchWindow(self, event):

        """
        EventHandler Function :-

        Purpose : it a stub function which calls MOnAddToWatchWindow() method
                  of CEventHandler class

        """

        lobstereventhandler.CEventHandler.MSOnAddToWatchWindow(event, self)

        return

    """----------------------------------------------------------------------"""

    def MOnCopy(self, event):

        """
        EventHandler Function :-

        Purpose : it a stub function which calls MSOnCopy()
                  function of CEventHandler class

        """

        lobstereventhandler.CEventHandler.MSOnCopy(event, self)

        return

    """----------------------------------------------------------------------"""

    def MOnPreferences(self, event):

        """
        EventHandler Function :-

        Purpose : it a stub function which calls MOnPreferences()
                  function of CEventHandler class

        """

        lobstereventhandler.CEventHandler.MSOnPreferences(event, self)

        return

    """----------------------------------------------------------------------"""

    def MOnSearchConfiguration(self, event):

        """
        EventHandler Function :-

        Purpose : it a stub function which calls MSOnSearchConfiguration()
                  function of CEventHandler class

        """

        lobstereventhandler.CEventHandler.MSOnSearchConfiguration(event, self)

        return

    """----------------------------------------------------------------------"""

    def MOnWindowClose(self, event):

        """
        EventHandler Function :-

        Purpose : it a stub function which calls MOnWindowClose function
                  of CEventHandler class

        """

        lobstereventhandler.CEventHandler.MSOnWindowClose(event, self)

        return

    """----------------------------------------------------------------------"""

    #   dummy method. It's acting as event-handler for certain
    #   menu-items, whose logic is yet not implemented.
    def MMethodToBeImplemented(self, event):
        pass

        return

    """----------------------------------------------------------------------"""


    def MOnRightDown(self, event):

        """
        Memeber Method :-

        Purpose :- This method creates a popup menu when the user clicks the
                    right button of the mouse on the tree item

        """
        #   creating a member variable to store the event, so that this
        #   variable can be used in MOnAddToFrequent() method as event object
        #   because self.m_event object will contain the event related to
        #   treeview, by which we can call GetItem() method.
        self.m_event = event

        self.m_objLobsterDataContext.__m_strCurrentWorkingDirectory__ = self.m_objCWxTreeView.m_currentDirectory

        #   creating a popup menu
        objMenu = popupmenu.CWxPopupMenu(
                                                    self,
                                                    lsStrTitle = ["Add to Frequent"],
                                                    lsStrEventHandler = [self.MOnAddToFrequent],
                                                    lsIntId = None, lsStrToolTip = None
                                                )

        #   displaying the popup menu
        self.PopupMenu(objMenu.m_menuInstance, event.GetPoint())

        return

    """----------------------------------------------------------------------"""

    def MOnAddToFrequent(self, event):

        """
        Member Method :-

        Purpose :- This method calls that method of CEventHandler class which
                    performs actions that should be performed when the user
                    selects "Add to Frequent" option from the popup menu

        """

        lobstereventhandler.CEventHandler.MSOnAddToFrequent(self, self.m_event)

        return

    """----------------------------------------------------------------------"""


    def MExpandTreeItem(self, event):

        """
        Member Method :-

        Purpose :- This method calls that method of CEventHandler class which
                    performs actions that should be performed when an item of
                    the treeview is expanding.

        """

        #   calling the OnExpandItem() method of CEventHandler class
        lobstereventhandler.CEventHandler.OnExpandItem(event, self)

        return

    """----------------------------------------------------------------------"""

    def MCollapseTreeItem(self, event):

        """
        Member Method :-

        Purpose :- This method calls that method of CEventHandler class which
                   performs actions that should be performed when an node of the
                   treeview is collapsing.

        """

        #   calling the OnCollapseItem() method of CEventHandler class
        lobstereventhandler.CEventHandler.OnCollapseItem(event, self)

        return

    """----------------------------------------------------------------------"""

    def MOnItemClick(self, event):

        """
        Member Method :-

        Purpose :- This method calls that method of CEventHandler class which
                    performs actions that should be performed when user left
                    clicks on a tree item.

        """

        #   calling the OnItemClick() method of the CEventHandler class
        lobstereventhandler.CEventHandler.OnItemClick(event, self)

        return

    """----------------------------------------------------------------------"""

    def MOnClose(self, evt):

        """
        Member Method :-

        Purpose : This method writes application configuration information on the
                  secondary storage, when the application is closed

        """

        # displaying confirmation dialog
        dlg = wx.MessageDialog(
                                self,
                                "Do you really want to close this application?",
                                "Confirm Exit",
                                wx.OK | wx.CANCEL | wx.ICON_QUESTION
                               )
        result = dlg.ShowModal()

        dlg.Destroy()
        if result == wx.ID_OK:
            #   opening the file in the writing mode
            favoriteCVarFile = open("favoriteCVars.txt", "w")

            #   writing the list of favorite CVars to the file
            yaml.dump(self.m_objLobsterDataContext.__m_lsStrFavoriteCVars__, favoriteCVarFile)

            favoriteCVarFile.close()

            #   opening the file in the writing mode
            watchWindowFile = open("watchWindowCVars.txt", "w")

            #   writing the list of watch window CVars to the file
            yaml.dump(self.m_objLobsterDataContext.__m_lsStrWatchWindowCVars__, watchWindowFile)

            watchWindowFile.close()

            # writing preferences object to file
            self.m_objLobsterDataContext.MGetPreferences().MWriteYaml("preferences.txt")

            self.Destroy()

        return

    """----------------------------------------------------------------------"""

    def __del__(self):

        """
        Destructor :-

        Throws Exception :- No

        Inputs :- does not receive any inputs

        Outputs :- does not return any value

        Purpose :- it releases the memory allocated to the member variables
                   of this class

        """

        self.m_etypeOfDisplayedCVars = None

        self.m_event = None

        self.m_objCWxListView = None

        self.m_objCWxProgressBar = None

        self.m_objCWxTreeView = None

        self.m_objLobsterDataContext = None

        self.m_objMenuBar = None

        self.m_objPaneMgr = None

        self.m_objStatusBar = None

        self.m_objWxPanel = None

    """----------------------------------------------------------------------"""

if __name__ == '__main__':
    app = wx.App(True)
    c = CGUIContext(None)
    c.Show()
    app.MainLoop()