#-------------------------------------------------------------------------------
# Name:        mywxtreeview.py
# Purpose:     This module contains CWxTreeView class which
#               represents wx.treectrl. It's made to make wx.TreeCtrl class
#               as a generic class, which can be used in any wx-based GUI application.
#
# Author:      Kruti
#
# Created:     13/02/2014
# Copyright:   (c) Account Prism Pvt. Ltd.
# Licence:     all_rights_reserved
#-------------------------------------------------------------------------------

#   imports
import wx
import mywxtreeitem
import mywxpopupmenu as popupmenu
import lobstereventhandler as eventhandler

#   class-name : CWxTreeView
#   class-description : This class extends wx.TreeCtrl and creates a treeview.
#                       This class aims at making wx.TreeCtrl generic, so that
#                       it can be used in  any application.
class CWxTreeView(wx.TreeCtrl):

    def __init__(self, dictCVarCollection, strCurrentDirectory = None, *args, **kwargs):

        """
        Constructor :-

        Throws Exception :- No

        Inputs :- (i) dictCVarCollection :- dictionary, which contains the
                                            object of ITreeItem or IListItem

                  (ii) *args :- arbitrary number of arguments or
                                list of arguments -as positional arguments,
                                it is used to call the parent constructor or
                                function with the arguments specified by the
                                user

                  (iii) **kwargs :- keyword arguments or named arguments,
                                it is used to call the parent constructor or
                                function with the arguments specified by the
                                user

        Outputs :- does not return any value

        Purpose :- It initializes the CWxTreeView class

        """

        #   calling the constructor of the parent class
        super(CWxTreeView, self).__init__(*args, **kwargs)

        #   dictionary, which holds data for the treectrl, in a tree-like structure
        self.m_dictCVarCollection = dictCVarCollection

        #
        self.m_currentDirectory = strCurrentDirectory

        #   boolean value indicating whether a node can
        #   further collpase or not
        self.m_bCanCollapse = False

        #   creating the list of images to set as icons of the treeitem
        self.m_il = wx.ImageList(16,16)

        #   adding images to the ImageList
        self.m_fldridx = self.m_il.Add(
                                        wx.Image(r'..\res\folder_off.ico', wx.BITMAP_TYPE_ICO).ConvertToBitmap()
                                    )

        self.m_fldropenidx = self.m_il.Add(
                                            wx.Image(r'..\res\generic_folder_on.ico', wx.BITMAP_TYPE_ICO).ConvertToBitmap()
                                        )

        self.m_fldrselectedclose = self.m_il.Add(
                                            wx.Image(r'..\res\objectof.ico', wx.BITMAP_TYPE_ICO).ConvertToBitmap()
                                            )

        self.m_fldrselectedopen = self.m_il.Add(
                                            wx.Image(r'..\res\objecton.ico', wx.BITMAP_TYPE_ICO).ConvertToBitmap()
                                            )

        self.m_fldrfrequentclose = self.m_il.Add(
                                            wx.Image(r'..\res\red_fold.ico', wx.BITMAP_TYPE_ICO).ConvertToBitmap()
                                        )

        self.m_fldrfrequentopen = self.m_il.Add(
                                            wx.Image(r'..\res\automati.ico', wx.BITMAP_TYPE_ICO).ConvertToBitmap()
                                        )

        self.SetImageList(self.m_il)

        #   calling the MSetRoot() method to set the root node
        self.MSetRoot()

        return

    """----------------------------------------------------------------------"""

    def MSetRoot(self):

        """
        Member Method :-

        Throws Exception :- No

        Inputs :- does not receive any inputs

        Outputs :- does not return any value

        Purpose :- This method sets the root node of the treeview.

        """

        #   getting root node from the dictionary, which is of
        #   type ITreeItem
        objCDir = self.m_dictCVarCollection.get("Root")

        #   if object exists
        if(objCDir != None):

            #   getting the absolute path of the directory
            strRoot = self.m_dictCVarCollection.get("Root").MGetAbsolutePath()

            #   creating the root node of the treeview
            root = self.AddRoot(strRoot, data = wx.TreeItemData("Root"))

            #   setting the image of the root node when it is not open
            self.SetItemImage(root, self.m_fldridx, wx.TreeItemIcon_Normal)

            #   setting the image of the root node when it is open
            self.SetItemImage(root, self.m_fldropenidx, wx.TreeItemIcon_Expanded)

            #   specifying that root has children or not (by default True)
            self.SetItemHasChildren(root)

        else:
            raise Exception("MyTreeView.py : Root is not available")

        return

    """----------------------------------------------------------------------"""

    def MAddNode(self, item):

        """
        Member Method :-

        Throws Exception :- Yes, throws exception when
                            (i) item is not the instance of ITreeItem

        Inputs :- (i) item :- current item of the treeview

        Outputs :- does not return any value

        Purpose :- This method sets the root node of the treeview.

        """

        #   getting the text of the current treeitem
        strText = str(self.GetItemText(item))

        #   getting the data of the current treeitem
        objData = self.GetItemData(item)

        #   getting the object of ITreeItem
        objITreeItem = self.m_dictCVarCollection.get(objData.Data)

        #   checking whether obj is an instance of ITreeItem or not
        bObjIsDirectory = isinstance(objITreeItem, mywxtreeitem.ITreeItem)

        #   if obj is an instance of ITreeItem
        if(bObjIsDirectory):

            #   getting the child nodes of the current node
            lsChildNodes = objITreeItem.MGetChildNodes()

            #   if current node has child nodes
            if(lsChildNodes != None):

                #   iterating through the lsChildNodes
                for strItem in lsChildNodes:

                        #   getting the object of ITreeItem or IListItem
                        obj = self.m_dictCVarCollection.get(strItem)

                        #   getting the name of the current node
                        string =  obj.MGetNodeName()

##                        self.m_currentDirectory = obj.MGetAbsolutePath()
##
##                        print self.m_currentDirectory

                        #   creating the child node of the current node
                        child = self.AppendItem(item, str(string), data = wx.TreeItemData(obj.MGetAbsolutePath()))

                        #   checking whether the current node has child nodes or not
                        bHasChildNodes = self.m_dictCVarCollection.get(strItem).MHasChildNodes()

                        #   setting the image for the child when it is not expanded
                        self.SetItemImage(child, self.m_fldridx, wx.TreeItemIcon_Normal)

                        #   setting the image for the child when it is expanded
                        self.SetItemImage(child, self.m_fldropenidx, wx.TreeItemIcon_Expanded)

                        #   specifying that child has children or not
                        self.SetItemHasChildren(child, bHasChildNodes)

        #   if not an instance of ITreeItem
        else:
            raise Exception("MyTreeView.py : Not an instance of ITreeItem ")

        return

    """----------------------------------------------------------------------"""

    def MSetCurrentDirectory(self, strCurrentDirectory):

        self.m_currentDirectory = strCurrentDirectory
        return

    """----------------------------------------------------------------------"""

    def MGetCurrentDirectory(self):

        return self.m_currentDirectory

    """----------------------------------------------------------------------"""

if __name__ == '__main__':
    pass