#-------------------------------------------------------------------------------
# Name:        lobstereventhandler.py
# Purpose:      This class handles all the functions that handlesevents
#               triggered by the GUI controls, used in the application.
# Author:      Kruti
#
# Created:     22-02-2014
# Copyright:   (c) Account Prism Pvt. Ltd.
# Licence:     all_rights_reserved
#-------------------------------------------------------------------------------

#   imports
import wx
import LecroyUtil_portable as LecP
import lobsterpreferences
import lobsterpreferencesdlg
import lobstersearchconfigurationdlg
import re
import lobstercvar
import arrayeditdialog
import stringeditdialog
#   class-name :- CEventHandler
#   class-description :- This class handles all the events triggered by the GUI
#                        controls, used in the application.
class CEventHandler():

    @staticmethod
    def MSOnWindowClose(event, objGuiContext):

        """
        Static Member Method :-

        Throws Exception :- No

        Inputs :-  (i) event :- object of wx.Event, it specifies for which event
                               the method is called

                  (ii) objCGuiContext :- object of class CGUIContext

        Outputs :- does not return any value

        Purpose :- This method writes the object of CDataContext class to the
                    file when the window is closed

        """

        objGuiContext.m_objLobsterDataContext.WriteYaml("lobsterconfig.inf")

        return

    """----------------------------------------------------------------------"""

    @staticmethod
    def MSOnUndo(objGuiContext, event):
        return
    """----------------------------------------------------------------------"""

    @staticmethod
    def MSOnRedo(objGuiContext, event):
        return
    """----------------------------------------------------------------------"""

    @staticmethod
    def MSOnSaveEdit(event, listview):

        """
        Static Member Method :-

        Throws Exception :- No

        Inputs :- (i) event :- event obect

                  (ii) listview :- object of listview, works as parent for the
                                   dialog window
        """

        #   getting the object of lobsterguicontext
        objGuiContext = listview.GetParent()

        #   getting the type of the CVars which are being dispayed on the listview
        #   for eg. If type is 0, it means normal child CVars are displayed
        #   If type is 1, it means favorite CVars are displayed
        typeOfDisplayedCVars = objGuiContext.MGetTypeOfDisplayedCVars()

        #   if normal child CVars are displayed
        if(typeOfDisplayedCVars == 0):

            #   getting the current working directory
            currentDirectory = objGuiContext.m_objLobsterDataContext.__m_strCurrentWorkingDirectory__

            #   creating an object of lobsterdirectory
            objDir = objGuiContext.m_objCWxTreeView.m_dictCVarCollection.get(currentDirectory)

            #   creating a list to store the child CVars of the current directory
            lsStrChildCVar = []

            #   creating a variable to store the absolute path of the directory
            strDirAbsolutePath = None

            #   clearing all the columns and items of the listview
            objGuiContext.m_objCWxListView.DeleteAllColumns()
            objGuiContext.m_objCWxListView.DeleteAllItems()

            #   getting the child CVars of the current directory
            lsStrChildCVar = objDir.MGetChildCVars()

            #   getting the absolute path of the current directory
            strDirAbsolutePath = objDir.MGetAbsolutePath()

            #   deleting the pane which contains listview
            objGuiContext.m_objPaneMgr.DetachPane(objGuiContext.m_objCWxListView)

            #   adding modified listview with the caption "Child CVar" to the pane
            objGuiContext.m_objPaneMgr.AddPane(objGuiContext.m_objCWxListView, wx.aui.AuiPaneInfo().Center().Caption("Child CVars"))

            #   updating the aui manager
            objGuiContext.m_objPaneMgr.Update()

            #   populating the listview which will have the updated values of
            #   CVars
            objGuiContext.m_objCWxListView.MPopulateValuesInListView(lsStrChildCVar, strDirAbsolutePath)

        #   if favorite CVars are displayed
        if(typeOfDisplayedCVars == 1):
            #   populating the listview which will have the updated values of
            #   CVars
            objGuiContext.m_objCWxListView.MPopulateValuesInListView(objGuiContext.m_objLobsterDataContext.__m_lsStrFavoriteCVars__, None, False)

        return

    """----------------------------------------------------------------------"""

    @staticmethod
    def MSOnListItemClick(event, objGuiContext):

        """
        Static Member Method :-

        Throws Exception :- No

        Inputs :-  (i) event :- object of wx.Event, it specifies for which event
                               the method is called

                  (ii) objGuiContext :- object of class CGUIContext

        Outputs :- does not return any value

        Purpose :- When the user clicks on a CVar displayed in the listview,
                    this method fetches its absolute path and displays it on
                    the statusbar

        """

        #   fetching the current directory
        strCurrentDirectory = objGuiContext.m_objCWxTreeView.MGetCurrentDirectory()

        # fetching index of selected cvar
        index = objGuiContext.m_objCWxListView.GetFirstSelected()

        #   fetching the item containing the absolute path of the selected CVar,
        #   which is at the column number 20
        strCVarAbsPathFromListView = objGuiContext.m_objCWxListView.GetItem(index, 20)

        #   getting the text of the selected item
        strCVarAbsPath = strCVarAbsPathFromListView.GetText()

        # set text in status bar.
        objGuiContext.m_objStatusBar.SetStatusText(strCVarAbsPath)

        return

    """----------------------------------------------------------------------"""

    @staticmethod
    def OnExpandItem(event, objCGuiContext):

        """
        Static Member Method :-

        Throws Exception :- No

        Inputs :- (i) event :- object of wx.Event, it specifies for which event
                               the method is called

                  (ii) objCGuiContext :- object of class CGUIContext

        Outputs :- does not return any value

        Purpose :- This method performs the operations that are to be executed
                    when a treeitem is expanding

        """

        #   getting the current treeitem
        item = event.GetItem()

        #   calling the MAddNode() method of the class CWxTreeView
        objCGuiContext.m_objCWxTreeView.MAddNode(item)

        return

    """----------------------------------------------------------------------"""

    @staticmethod
    def OnCollapseItem(event, objCGuiContext):

        """
        Static Member Method :-

        Throws Exception :- No

        Inputs :- (i) event :- object of wx.Event, it specifies for which event
                               the method is called

                  (ii) objCGuiContext :- object of class CGUIContext

        Outputs :- does not return any value

        Purpose :- This method performs the operations that are to be executed
                    when a treeitem is collapsing

        """

        #   checking whether the treeitem can collapse or not
        if objCGuiContext.m_objCWxTreeView.m_bCanCollapse:
            #   stops processing the event
            event.Veto()
        else:
            objCGuiContext.m_objCWxTreeView.m_bCanCollapse = True
            #   getting the current treeitem
            item = event.GetItem()
            #   collapasing and resetting the item
            objCGuiContext.m_objCWxTreeView.CollapseAndReset(item)
            #   setting the children to the current tree item
            objCGuiContext.m_objCWxTreeView.SetItemHasChildren(item)
            objCGuiContext.m_objCWxTreeView.m_bCanCollapse = False

        return

    """----------------------------------------------------------------------"""

    @staticmethod
    def OnItemClick(event, objCGuiContext):

        """
        Static Member Method :-

        Throws Exception :- No

        Inputs :- (i) event :- object of wx.Event, it specifies for which event
                               the method is called

                  (ii) objCGuiContext :- object of class CGUIContext

        Outputs :- does not return any value

        Purpose :- This method performs the operations that are to be executed
                    when the user clicks the left button of the mouse

        """

        #   if left button of mouse is pressed
        if event.LeftDown() and not objCGuiContext.m_objCWxTreeView.HasFlag(wx.TR_MULTIPLE):

            #   getting the current treeitem
            item, ht_flags = objCGuiContext.m_objCWxTreeView.HitTest(event.GetPosition())

            if (ht_flags & wx.TREE_HITTEST_ONITEM) != 0:

                objCGuiContext.m_objCWxTreeView.SetFocus()
                objCGuiContext.m_objCWxTreeView.SelectItem(item)

                #   setting the image for the item when that item is selected but not expanded
                objCGuiContext.m_objCWxTreeView.SetItemImage(item, objCGuiContext.m_objCWxTreeView.m_fldrselectedclose, wx.TreeItemIcon_Selected)
                #   setting the image for the item when that item is selected and expanded
                objCGuiContext.m_objCWxTreeView.SetItemImage(item, objCGuiContext.m_objCWxTreeView.m_fldrselectedopen, wx.TreeItemIcon_SelectedExpanded)

                #   getting the data passed to the current treeitem
                data = objCGuiContext.m_objCWxTreeView.GetItemData(item)

                #   getting the object from the objCGuiContext.objCWxTreeView.m_dictCVarCollection.
                #   by the absolute path of the treeitem
                objDir = objCGuiContext.m_objCWxTreeView.m_dictCVarCollection.get(data.Data)

                #   checking whether the current directory has child CVars or not
                bHasChildCVars = objDir.MHasChildCVars()

                lsStrChildCVar = []

                strDirAbsolutePath = None

                #   clearing all the columns and items of the listview
                objCGuiContext.m_objCWxListView.DeleteAllColumns()
                objCGuiContext.m_objCWxListView.DeleteAllItems()

                #   if the current directory has child CVars
                if(bHasChildCVars):

                    #   getting the child CVars of the current directory
                    lsStrChildCVar = objDir.MGetChildCVars()

                    #   getting the absolute path of the current directory
                    strDirAbsolutePath = objDir.MGetAbsolutePath()

                    #   setting the current directory
                    objCGuiContext.m_objCWxTreeView.MSetCurrentDirectory(strDirAbsolutePath)

                    #   setting the current directory in the data context class
                    objCGuiContext.m_objLobsterDataContext.__m_strCurrentWorkingDirectory__ = strDirAbsolutePath

                    #   deleting the pane which contains listview
                    objCGuiContext.m_objPaneMgr.DetachPane(objCGuiContext.m_objCWxListView)

                    #   adding modified listview with the caption "Child CVar" to the pane
                    objCGuiContext.m_objPaneMgr.AddPane(objCGuiContext.m_objCWxListView, wx.aui.AuiPaneInfo().Center().Caption("Child CVars"))

                    #   updating the aui manager
                    objCGuiContext.m_objPaneMgr.Update()

                    #   assigning the type of the displayed CVar by the value of
                    #   objGuiContext.mC_NORMAL_CHILD_CVARS
                    objCGuiContext.m_etypeOfDisplayedCVars = objCGuiContext.mC_NORMAL_CHILD_CVARS

                    #   calling the MPopulateValuesInListView() method of the CWxListView class
                    objCGuiContext.m_objCWxListView.MPopulateValuesInListView(lsStrChildCVar, strDirAbsolutePath)

                else:
                    #   if the current directory does not have any child CVar
                    #   then modify the pane containing listview which has no
                    #   caption
                    objCGuiContext.m_objPaneMgr.DetachPane(objCGuiContext.m_objCWxListView)
                    objCGuiContext.m_objPaneMgr.AddPane(objCGuiContext.m_objCWxListView, wx.aui.AuiPaneInfo().Center())
                    objCGuiContext.m_objPaneMgr.Update()

            else:
                event.Skip()

        #   if the left button of mouse is released
        elif event.LeftUp():
            item, ht_flags = objCGuiContext.m_objCWxTreeView.HitTest(event.GetPosition())

        else:
            event.Skip()

        return

    """----------------------------------------------------------------------"""

    @staticmethod
    def MSOnWatchFavoriteCVars(event, objGuiContext):

        """
        Static Member Method :-

        Throws Exception :- No

        Inputs :- (i) event :- object of wx.Event, it specifies for which event
                               the method is called

                  (ii) objGuiContext :- object of class CGUIContext

        Outputs :- does not return any value

        Purpose :- This method displays favorite CVars in the listview

        """

        #   assigning the type of the displayed CVar by the value of
        #   objGuiContext.mC_FAVORITE_CVARS
        objGuiContext.m_etypeOfDisplayedCVars = objGuiContext.mC_FAVORITE_CVARS

        #   deleting the pane which contains the listview
        objGuiContext.m_objPaneMgr.DetachPane(objGuiContext.m_objCWxListView)

        #   clearing all the columns and items of the listview
        objGuiContext.m_objCWxListView.DeleteAllColumns()
        objGuiContext.m_objCWxListView.DeleteAllItems()

        #   adding the listview which has caption "Favorite CVar" to the pane
        objGuiContext.m_objPaneMgr.AddPane(objGuiContext.m_objCWxListView, wx.aui.AuiPaneInfo().Center().Caption("Favorite CVars"))

        #   updating the aui manager
        objGuiContext.m_objPaneMgr.Update()

        #   getting the list of the favorite CVars
        favoriteCVars = objGuiContext.m_objLobsterDataContext.__m_lsStrFavoriteCVars__

        #   calling the MPopulateValuesInListView() method of the CWxListView class
        objGuiContext.m_objCWxListView.MPopulateValuesInListView(favoriteCVars, None, False)

        return

    """----------------------------------------------------------------------"""

    @staticmethod
    def MSOnCopy(event, objGuiContext):

        """
        Static Member Method :-

        Throws Exception :- No

        Inputs :- (i) event :- object of wx.Event, it specifies for which event
                               the method is called

                  (ii) objCGuiContext :- object of class CGUIContext

        Outputs :- does not return any value

        Purpose :- This method performs the actions that are to be performed
                    when the user selects the "Copy" option from the popup menu
                    displayed on the right click of the list item

        """

        #   creating a list for storing the index of the selected CVars
        selection = []

        #   storing the index of the first selected CVar
        index = objGuiContext.m_objCWxListView.GetFirstSelected()

        #   appending the index of the selected CVars to the list
        selection.append(index)

        #   iterate a loop in the till the length of the index of selected CVars
        #   and number of selected items are not same
        while len(selection) != objGuiContext.m_objCWxListView.GetSelectedItemCount():
            index = objGuiContext.m_objCWxListView.GetNextSelected(index)
            #   append the index to the list of index of the selected CVar
            selection.append(index)

        #   creating a variable for storing the name of the selected CVar
        strCVarsToCopy = ""

        #   creating a variable for storing the adapted value of the selected
        #   CVar
        strSelectedAdaptedValue = ""

        #   iterating through the list of index of the selected CVar
        for iIdx in range(len(selection)):

            #   fetching the value from the listview
            strSelectedCVar = objGuiContext.m_objCWxListView.GetItemText(selection[iIdx])

            #   fetching the item from the column index 1(which contains type
            #   of the selected CVar)
            strSelectedListItemForType = objGuiContext.m_objCWxListView.GetItem(selection[iIdx], 1)

            #   fetching the text of that item
            strSelectedType =strSelectedListItemForType.GetText()

            #   fetching the item from the column index 4(which contains adapted value
            #   of the selected CVar)
            strSelectedListItemForAdaptedValue = objGuiContext.m_objCWxListView.GetItem(selection[iIdx], 4)

            #   fetching the text of that item
            strSelectedAdaptedValue = strSelectedListItemForAdaptedValue.GetText()

            #   checking whether the type is String or Enum
            if((strSelectedType == "String") or(strSelectedType == "Enum")):
                #   put inverted comma before and after the value
                strSelectedAdaptedValue = '"' + str(strSelectedListItemForAdaptedValue.GetText()) + '"'

            #   getting the preferences for the copy functionality
            lsECopyPreferences =  objGuiContext.m_objLobsterDataContext.MGetPreferences().MGetCopyPref()

            if (lsECopyPreferences == lobsterpreferences.CPreferences.mC_LS_COPY_PREF):
                #   storing the full path of the CVar
                strCurrentCVarFullPath = str(objGuiContext.m_objCWxTreeView.MGetCurrentDirectory()) + "." + str(strSelectedCVar) + " = " + strSelectedAdaptedValue
                #strCVarsToCopy += str(strCurrentCVarFullPath) + "\n"

            elif(lsECopyPreferences == [lobsterpreferences.CPreferences.mC_COPY_PATH]):
                strCurrentCVarFullPath = str(objGuiContext.m_objCWxTreeView.MGetCurrentDirectory()) + "." + str(strSelectedCVar)

            else:
                strCurrentCVarFullPath = strSelectedAdaptedValue

            #   concatinating all the selected CVars' full path
            strCVarsToCopy += str(strCurrentCVarFullPath) + "\n"

        #   calling the copy function of the LecroyUtil_portable
        LecP.Copy(strCVarsToCopy)

        return

    """----------------------------------------------------------------------"""
    @staticmethod
    def MSOnPreferences(event, objGuiContext):
        objCPreferencesDlg = lobsterpreferencesdlg.CPreferencesDlg(objGuiContext)
        objCPreferencesDlg.Show()
        return
    """----------------------------------------------------------------------"""

    @staticmethod
    def MSOnSearchConfiguration(event, objGuiContext):
        objCSearchConfiguration = lobstersearchconfigurationdlg.CSearchConfigurationDlg(objGuiContext)
        objCSearchConfiguration.Show()

    """----------------------------------------------------------------------"""

    @staticmethod
    def MSOnEdit(event, objGuiContext):

        """
        Static Member Method :-

        Throws Exception :- No

        Inputs :- (i) event :- object of wx.Event, it specifies for which event
                               the method is called

                  (ii) objCGuiContext :- object of class CGUIContext

        Outputs :- does not return any value

        Purpose :- This method performs the actions to be performed when the
                    user clicks on the "Edit" option of the popup menu displayed
                    on the listview

        """

        #   fetching the current directory
        strCurrentDirectory = objGuiContext.m_objCWxTreeView.MGetCurrentDirectory()

        #   getting the index of the selected CVar
        index = objGuiContext.m_objCWxListView.GetFirstSelected()

        #   fetching the item from the column index 4(which contains adapted value
        #   of the selected CVar)
        strSelectedListItemForAdaptedValue = objGuiContext.m_objCWxListView.GetItem(index, 4)

        #   fetching the text of that item
        strSelectedAdaptedValue = strSelectedListItemForAdaptedValue.GetText()

        print strSelectedAdaptedValue

        #   getting the item at the column number 20, which has absolute path of
        #   the current selected CVar
        strCVarAbsPathFromListView = objGuiContext.m_objCWxListView.GetItem(index, 20)

        #   getting the text of that item
        strCVarAbsPath = strCVarAbsPathFromListView.GetText()

        #   getting the object of the CVar class
        objCVar = objGuiContext.m_objCWxListView.m_dictCVarCollection.get(strCVarAbsPath)

##        #   getting the attributes of the CVar
##        dictValues = objCVar.__m_dictListItemInfo__

        #   getting the type of the CVar
        intType = objCVar.MGetCVarType()

        #   if type is SafeArray
        if(intType == 14):
            #   creating an object of array edit dialog
##            arraydialog = arrayeditdialog.CWxDialog(objCVar, dictValues, objGuiContext.m_objCWxListView ,None, None, None, None)
            arraydialog = arrayeditdialog.CWxDialog(objCVar, objGuiContext.m_objCWxListView ,
                                        id = wx.ID_ANY, title = "Array Edit Dialog",
                                        tupPos = (0, 0), tupSize = (400, 400))

        #   if type is String
        elif(intType == 15):
            #   creating an object of string edit dialog
            stringdialog = stringeditdialog.CWxDialog(objCVar, objGuiContext.m_objCWxListView, None, None, None, None)

        #   if type is any other than String and SafeArray
        else:
            objGuiContext.m_objCWxListView.OpenEditor(4, index)
##            pass

        return

    """----------------------------------------------------------------------"""

    @staticmethod
    def MSOnAddToFavorite(event, objGuiContext):

        """
        Static Member Method :-

        Throws Exception :- No

        Inputs :- (i) event :- object of wx.Event, it specifies for which event
                               the method is called

                  (ii) objCGuiContext :- object of class CGUIContext

        Outputs :- does not return any value

        Purpose :- This method performs the actions to be performed when the
                    user clicks on the "Add to Favorite" option of the popup
                    menu displayed on the listview

        """

        #   fetching the current directory
        strCurrentDirectory = objGuiContext.m_objCWxTreeView.MGetCurrentDirectory()

        #   creating a list for storing the indexes of the selected CVars
        selection = []

        #   fetching the index of the first selected CVar
        index = objGuiContext.m_objCWxListView.GetFirstSelected()

        #   appending the index to the list of indexes of the selected CVars
        selection.append(index)

        #   iterating through the list of indexes of the selected CVars
        while len(selection) != objGuiContext.m_objCWxListView.GetSelectedItemCount():
            #   fetching the index of the currently selected CVar
            index = objGuiContext.m_objCWxListView.GetNextSelected(index)
            #   appending that index to the list of indexes of the selected CVars
            selection.append(index)

        #   itarating throught the list of indexes of the selected CVars
        for iIdx in range(len(selection)):

            #   setting an image to the CVar which is selected as favorite
            objGuiContext.m_objCWxListView.SetItemImage(selection[iIdx], objGuiContext.m_objCWxListView.m_objFavImg)

            #   getting the item of the listview from the column number 20
            #   which has the absolute path of the CVar
            strCVarAbsPathFromListView = objGuiContext.m_objCWxListView.GetItem(selection[iIdx], 20)

            #   getting the text of that item
            strCVarAbsPath = strCVarAbsPathFromListView.GetText()

            #   if list of favorite CVars is none, then assign an empty list to
            #   that list
            if(objGuiContext.m_objLobsterDataContext.__m_lsStrFavoriteCVars__ == None):
                objGuiContext.m_objLobsterDataContext.__m_lsStrFavoriteCVars__ = []

            #   append the currently selected CVar to the list of favorite CVars
            objGuiContext.m_objLobsterDataContext.__m_lsStrFavoriteCVars__.append(strCVarAbsPath)

            #   iterating through the list of favorite CVars
            for iIdx in range(len(objGuiContext.m_objLobsterDataContext.__m_lsStrFavoriteCVars__)):

                #   checking whether the CVar is already present in the list of
                #   favorite CVars
                if(objGuiContext.m_objLobsterDataContext.__m_lsStrFavoriteCVars__.count(strCVarAbsPath)>1):
                    #   if CVars is already present in the list of favorite CVars
                    #   then remove its duplicate entry
                    objGuiContext.m_objLobsterDataContext.__m_lsStrFavoriteCVars__.remove(strCVarAbsPath)

        return

    """----------------------------------------------------------------------"""

    @staticmethod
    def MSOnAddToFrequent(objGuiContext, event):

        """
        Static Member Method :-

        Throws Exception :- No

        Inputs :- (i) objCGuiContext :- object of class CGUIContext

                  (ii) event :- object of wx.Event, it specifies for which event
                               the method is called

        Outputs :- does not return any value

        Purpose :- This method performs the actions to be performed when the
                    user clicks on the "Add to Frequent" option of the popup
                    menu displayed on the treeview

        """

        #   getting the current tree item
        item = event.GetItem()

        #   setting the images to the directories which are marked as frequent
        objGuiContext.m_objCWxTreeView.SetItemImage(item, objGuiContext.m_objCWxTreeView.m_fldrfrequentclose, wx.TreeItemIcon_Normal)
        objGuiContext.m_objCWxTreeView.SetItemImage(item, objGuiContext.m_objCWxTreeView.m_fldrfrequentopen, wx.TreeItemIcon_Expanded)

        #   getting the data of the treeitem
        data = objGuiContext.m_objCWxTreeView.GetItemData(item)

        #   creating the object of CDirectory
        objDir = objGuiContext.m_objCWxTreeView.m_dictCVarCollection.get(data.Data)

        #   getting the absolute path of the directory
        strDirAbsolutePath = objDir.MGetAbsolutePath()

        #   setting the current directory
        objGuiContext.m_objCWxTreeView.MSetCurrentDirectory(strDirAbsolutePath)

        strCurrentDirectoryFullPath = str(objGuiContext.m_objCWxTreeView.MGetCurrentDirectory())

        #   if the list of frequent directories is None, then assign the list to
        #   the empty list
        if(objGuiContext.m_objLobsterDataContext.__m_lsStrFrequentDirectories__ == None):
            objGuiContext.m_objLobsterDataContext.__m_lsStrFrequentDirectories__ = []

        #   appending the frequent directory to the list of frequent directories
        objGuiContext.m_objLobsterDataContext.__m_lsStrFrequentDirectories__.append(strCurrentDirectoryFullPath)

        #   iterating through the list of frequent directories
        for iIdx in range(len(objGuiContext.m_objLobsterDataContext.__m_lsStrFrequentDirectories__)):
                #   if the currently selected directory exists in the list of
                #   frequent directory then remove its redundant entries
                if(objGuiContext.m_objLobsterDataContext.__m_lsStrFrequentDirectories__.count(strCurrentDirectoryFullPath)>1):
                    objGuiContext.m_objLobsterDataContext.__m_lsStrFrequentDirectories__.remove(strCurrentDirectoryFullPath)

        return

    """----------------------------------------------------------------------"""

    @staticmethod
    def MSOnAddToWatchWindow(event, objGuiContext):

        """
        Static Member Method :-

        Throws Exception :- No

        Inputs :- (i) event :- object of wx.Event, it specifies for which event
                               the method is called

                  (ii) objCGuiContext :- object of class CGUIContext

        Outputs :- does not return any value

        Purpose :- This method adds the selected CVars to the watch window

        """

        #   fetching the current directory
        strCurrentDirectory = objGuiContext.m_objCWxTreeView.MGetCurrentDirectory()

        #   clearing the listview
        objGuiContext.m_objWxPanel.m_objCWxListView.DeleteAllColumns()
        objGuiContext.m_objWxPanel.m_objCWxListView.DeleteAllItems()

        #   creating a list to store the indexes of the rows which are
        #   selected to be added to watch window
        selection = []

        #   storing the index of the first selected item
        index = objGuiContext.m_objCWxListView.GetFirstSelected()

        #   appending the index to the list of indexes
        selection.append(index)

        #   iterating a loop until the length of the list of selected indexes
        #   is not equal to the number of selected items
        while len(selection) != objGuiContext.m_objCWxListView.GetSelectedItemCount():
            #   getting the index of the next selected item
            index = objGuiContext.m_objCWxListView.GetNextSelected(index)
            #   appending the index to the list of indexes of selected items
            selection.append(index)

        #   iterating through the list of indexes of the selected items
        for iIdx in range(len(selection)):

            #   getting the item at the column number 20, which has the
            #   absolute path of the CVar
            strCVarAbsPathFromListView = objGuiContext.m_objCWxListView.GetItem(selection[iIdx], 20)

            #   getting the text of that item
            strCVarAbsPath = strCVarAbsPathFromListView.GetText()

            #   if the list of watch window CVars is None, then make the list
            #   empty list
            if(objGuiContext.m_objLobsterDataContext.__m_lsStrWatchWindowCVars__ == None):
                objGuiContext.m_objLobsterDataContext.__m_lsStrWatchWindowCVars__ = []

            #   appending the currently selected CVar to the list of watch
            #   window CVars
            objGuiContext.m_objLobsterDataContext.__m_lsStrWatchWindowCVars__.append(strCVarAbsPath)

            #   iterating through the list of watch window CVars
            for iIdx in range(len(objGuiContext.m_objLobsterDataContext.__m_lsStrWatchWindowCVars__)):

                #   if any CVar occurs more than one time in the list of watch window
                #   CVars, then remove its redundant entries
                if(objGuiContext.m_objLobsterDataContext.__m_lsStrWatchWindowCVars__.count(strCVarAbsPath)>1):
                    objGuiContext.m_objLobsterDataContext.__m_lsStrWatchWindowCVars__.remove(strCVarAbsPath)

        #   calling the method to populate the listview
        objGuiContext.m_objWxPanel.m_objCWxListView.MPopulateValuesInListView(objGuiContext.m_objLobsterDataContext.__m_lsStrWatchWindowCVars__, None, bGenerateAbsPath = False)

        return

    """----------------------------------------------------------------------"""

    @staticmethod
    def MSSearch(objDict, objCSearchConfig):

        """
        Static Member Function :-

        Throws Exception : No

        Input : (i) objDict : object of dictionary which contains all cvars ans directories
                (ii) objSearchConfig : object of CSearchCongiguration

        Output : (i) lsCVarAbsPath : list of string containing absolute path of cvar

        Purpose : it will search matches with search keyword and return list of those matched cvars

        """

        objGuiContext.m_strTypeOfDisplayedCVars = "Search Result"

        # defining list of cvar absolute path
        lsCVarAbsPath = []

        # fetching text from search keyword text control
        strSearchKeyword = objCSearchConfig.MGetSearchKeyword()
        # fetching list of enum which is checked by user in search configuraion dialog
        lsEColumns = objCSearchConfig.MGetColumnsForSearch()
        # defining list of string columns
        lsStrColumns = []
        # iterating list which contains enum, Its tast to fetching list of string from list enum
        for i in lsEColumns:
            # appending column name as a string
            lsStrColumns.append(lobstercvar.CVar.ms_lsStrHeaders[i])

        # iteratig list of absolute path
        for strAbsPath in objDict:
            # fetching object from dictionary(dictionary has two type of object CVar and CDirectory
            obj = objDict.get(strAbsPath)
            # process the object if obj is an object of CVar
            if(isinstance(obj, lobstercvar.CVar)):

                # if user has checked Name checkbox
                if("Name" in lsStrColumns):
                    # fetching name of cvar
                    strCVarName = str(obj.MGetCVarName())
                    # comparing the input text with cvar name, if match then add to list
                    if (re.search(strSearchKeyword, strCVarName)):
                        lsCVarAbsPath.append(strAbsPath)

                # if user has checked Type checkbox
                if("Type" in lsStrColumns):
                   strCVarType = lobstercvar.CVar.ms_lsStrTypes[obj.MGetCVarType()]
                   if (re.search(strSearchKeyword, strCVarType)):
                        lsCVarAbsPath.append(strAbsPath)

                lsECVarFlags = []
                # if user has checked Flags checkbox
                if("Flags" in lsStrColumns):
                    try:
                        strFlags = ""

                        lsStrSearchedFlags = re.split("\,", strSearchKeyword)
                        lsESearchedFlag = []
                        for strFlag in lsStrSearchedFlags:
                            lsESearchedFlag.append(lobstercvar.CVar.ms_lsStrFlags.index(strFlag))

                        lsECVarFlags = obj.MGetCVarFlags()

                        setMatches = set(lsECVarFlags) & set(lsESearchedFlag)

                        if (len(setMatches) > 0):
                            lsCVarAbsPath.append(strAbsPath)
                    except:
                        pass

                # if user has checked Requested checkbox
                if("Requested" in lsStrColumns):
                    strRequestedValue = str(obj.MGetCVarRequestedValue())
                    if (re.search(strSearchKeyword, strRequestedValue)):
                        lsCVarAbsPath.append(strAbsPath)

                # if user has checked Adapted checkbox
                if("Adapted" in lsStrColumns):
                    strAdaptedValue = str(obj.MGetCVarAdaptedValue())
                    if (re.search(strSearchKeyword, strAdaptedValue)):
                        lsCVarAbsPath.append(strAbsPath)

                # if user has checked Default checkbox
                if("Default" in lsStrColumns):
                    strDefaultValue = str(obj.MGetCVarDefaultValue())
                    if (re.search(strSearchKeyword, strDefaultValue)):
                        lsCVarAbsPath.append(strAbsPath)

                # if user has checked MaxLen checkbox
                if("MaxLen" in lsStrColumns):
                    try:
                        iMaxLen = obj.MGetCVarMaxLen()
                        iSearchKeyword = 0

                        iSearchKeyword = int(strSearchKeyword)
                        if (iMaxLen == iSearchKeyword):
                            lsCVarAbsPath.append(strAbsPath)
                    except:
                        pass

                # if user has checked Name Range
                if("Range" in lsStrColumns):
                    strRangeValue = str(obj.MGetCVarRange())
                    if (re.search(strSearchKeyword, strRangeValue)):
                        lsCVarAbsPath.append(strAbsPath)

                # if user has checked Min checkbox
                if("Min" in lsStrColumns):
                    try:
                        iMinValue = float(obj.MGetCVarMinValue())
                        iSearchKeyword = 0

                        iSearchKeyword = float(strSearchKeyword)
                        if (iMinValue == iSearchKeyword):
                            lsCVarAbsPath.append(strAbsPath)
                    except:
                        pass

                # if user has checked Max checkbox
                if("Max" in lsStrColumns):
                    try:
                        iMaxValue = float(obj.MGetCVarMaxValue())
                        iSearchKeyword = 0

                        iSearchKeyword = float(strSearchKeyword)
                        if (iMaxValue == iSearchKeyword):
                            lsCVarAbsPath.append(strAbsPath)
                    except:
                        pass

                # if user has checked Grain checkbox
                if("Grain" in lsStrColumns):
                    try:
                        iGrainValue = float(obj.MGetCVarGrainValue())
                        iSearchKeyword = 0

                        iSearchKeyword = float(strSearchKeyword)
                        if (iGrainValue == iSearchKeyword):
                            lsCVarAbsPath.append(strAbsPath)
                    except:
                        pass

                # if user has checked Unit checkbox
                if("Unit" in lsStrColumns):
                    strUnit = obj.MGetCVarUnit()
                    if (re.search(strSearchKeyword, str(strUnit))):
                        lsCVarAbsPath.append(strAbsPath)

                # if user has checked Width checkbox
                if("Width" in lsStrColumns):
                    iWidth = obj.MGetImageWidth()
                    if (re.search(strSearchKeyword, str(iWidth))):
                        lsCVarAbsPath.append(strAbsPath)

                # if user has checked Height checkbox
                if("Height" in lsStrColumns):
                    iHeight = obj.MGetImageHeight()
                    if (re.search(strSearchKeyword, str(iHeight))):
                        lsCVarAbsPath.append(strAbsPath)

                # if user has checked Bits checkbox
                if("Bits" in lsStrColumns):
                    iBits = obj.MGetImageBits()
                    if (re.search(strSearchKeyword, str(iBits))):
                        lsCVarAbsPath.append(strAbsPath)

                # if user has checked Root checkbox
                if("Root" in lsStrColumns):
                    strRoot = str(obj.MGetCVarRoot())
                    if (re.search(strSearchKeyword, strRoot)):
                        lsCVarAbsPath.append(strAbsPath)

                # if user has checked Filters checkbox
                if("Filters" in lsStrColumns):
                    strFilters = str(obj.MGetCVarFileters())
                    if (re.search(strSearchKeyword, strFilters)):
                        lsCVarAbsPath.append(strAbsPath)


                # if user has checked Path checkbox
                if("Path" in lsStrColumns):
                    strPath = str(obj.MGetCVarPath())
                    if (re.search(strSearchKeyword, strPath)):
                        lsCVarAbsPath.append(strAbsPath)

                # if user has checked NbOfBits checkbox
                if("NbOfBits" in lsStrColumns):
                    strBits = str(obj.MGetNbOfBits())
                    if (re.search(strSearchKeyword, strBits)):
                        lsCVarAbsPath.append(strAbsPath)

                # if user has checked HardwareAddress checkbox
                if("HardwareAddress" in lsStrColumns):
                    strAddress = str(obj.MGetCVarHardwareAddress())
                    if (re.search(strSearchKeyword, strAddress)):
                        lsCVarAbsPath.append(strAbsPath)


        return lsCVarAbsPath

    """----------------------------------------------------------------------"""

if __name__ == '__main__':
    pass
