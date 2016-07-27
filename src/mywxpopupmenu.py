#-------------------------------------------------------------------------------
# Name:        mywxpopupmenu.py
# Purpose:     This modules contains CWxPopumMenu class, which is a generic class
#               implementation for wx.Popupmenu.
# Author:      Kruti
#
# Created:     18/03/2014
# Copyright:   (c) Account Prism Pvt. Ltd.
# Licence:     all_rights_reserved
#-------------------------------------------------------------------------------

#   imports
import wx
import mymenu as menu

#   class-name : CWxPopupMenu
#   class-description : This class extends CMenu class and is used to create a
#                       popup menu
class CWxPopupMenu(menu.CMenu):

    def __init__(self, window, lsStrTitle, lsStrEventHandler, lsIntId = None, lsStrToolTip = None):

        """
        Constructor :-

        Throws Exception :- Yes, throws exception when

                            (i) lsStrTitle is None or an empty list

                            (ii) lsStrEventHandler is None or an empty list

                            (iii) length of lsStrTitle and lsStrEventHandler is
                                  not same

                            (iv) length of lsIntId is not same as length of
                                 lsStrTitle and lsStrEventHandler

                            (v) length of lsStrToolTip is not same as length of
                                lsStrTitle and lsStrEventHandler

        Inputs :- (i) window :- container of this class. It may be the object of
                                wx.Frame, wx.Dialog, wx.Panel or any GUI container
                                object.

                  (ii) lsStrTitle :- list of strings representing title of the
                                     menu item.
                                     eg. ["File", "Edit"]

                  (iii) lsStrEventHandler :- list of method objects, which will
                                             be acting as event handler for each
                                             menu items in the popup menu.

                  (iv) lsIntId :- list of integer, representing id of the menu
                                  items

                  (v) lsStrToolTip :- list of string, representing tool tip of
                                      the menu item
                                      eg. ["Click to open file", "Click to edit"]

        Outputs :- does not return any value

        Purpose :- It initializes the member variables to the values passed as argument
                    in constructor

        """
        #   TODO :- Tooltips are not shown on popup-menu's menu-items. So, their
        #           details can be removed from the class

        #   calling the constructor of the parent class
        menu.CMenu.__init__(self, strTitle = "Menu", menubarParent = None)

        #   raise exception, if lsStrTitle is None or an empty list
        if ((lsStrTitle == None) or (lsStrTitle == [])):
            raise Exception("mywxpopupmenu.py : lsStrTitle can neither be None nor be empty")

        #   raise exception, if lsStrEventHandler is None or an empty list
        if ((lsStrEventHandler == None) or (lsStrEventHandler == [])):
            raise Exception("mywxpopupmenu.py : lsStrEventHandler neither be None nor be empty")

        #   raise exception, if length of lsStrTitle and lsStrEventHandler is not same
        if (len(lsStrTitle) != len(lsStrEventHandler)):
            raise Exception("mywxpopupmenu.py : Number of title and number of event handlers must be same")

        #   if lsIntId is empty or None, then create ids
        if ((lsIntId == []) or (lsIntId == None)):
            lsIntId = []
            #   iterate a loop to assign values to the lsIntId
            for iIdx in range(len(lsStrTitle)):
                lsIntId.append(wx.ID_ANY)
        #   raise exception, if lsIntId contains values but number of values
        #   is not same as number of values in lsStrTitle
        else:
            if (len(lsIntId) != len(lsStrTitle)):
                raise Exception("mywxpopupmenu.py : Number of id must be equal to number of titles and event handlers")

        #   if lsStrToolTip is empty or None, then create list of tooltips, with
        #   each tooltip as empty string
        if ((lsStrToolTip == []) or (lsStrToolTip == None)):
            lsStrToolTip = []
            #   iterate a loop to assign values to the lsStrToolTip
            for iIdx in range(len(lsStrTitle)):
                lsStrToolTip.append("")
        #   raise exception, if lsStrToolTip contains values but number of values is not same as
        #   number of values in lsStrTitle
        else:
            if (len(lsStrToolTip) != len(lsStrTitle)):
                raise Exception("mywxpopupmenu.py : Number of tool tips must be equal to number of titles and event handlers")

        #   member variable, representing list of title of the menu items
        self.m_lsStrTitle = lsStrTitle

        #   member variable, representing list of id of the menu items
        self.m_lsIntId = lsIntId

        #   member variable, representing list of tool tips of the menu items
        self.m_lsStrToolTip = lsStrToolTip

        #   member variable, representing list of names of event handlers of
        #   the menu items
        self.m_lsStrEventHandler = lsStrEventHandler

        #   creating menu items
        for iIdx in range(len(self.m_lsStrTitle)):
            self.m_liCMenuItemChildMenuItemsList.append(
                                                        menu.CMenuItem(
                                                            iId = self.m_lsIntId[iIdx],
                                                            strTitle = self.m_lsStrTitle[iIdx],
                                                            strTooltip = self.m_lsStrToolTip[iIdx],
                                                            strEvtHandlerMethod = self.m_lsStrEventHandler[iIdx],
                                                            menuParentMenu = self.m_menuInstance,
                                                            frameParent = window
                                                            )
                                                    )
        return

    """----------------------------------------------------------------------"""

    def __del__(self):

        """
        Destructor :-

        Throws Exception :- No

        Inputs :- does not receive any inputs

        Outputs :- does not return any value

        Purpose :- It releases the memory of the member variables of the
                   CWxPopupMenu class and its parent class i.e. CMenu class

        """

        self.m_lsIntId = None
        self.m_lsStrEventHandler = None
        self.m_lsStrTitle = None
        self.m_lsStrToolTip = None

        menu.CMenu.__del__(self)

    """----------------------------------------------------------------------"""

#   tester class for testing mywxpopupmenu
class MyWindow(wx.Window):
    def __init__(self, parent, color):
        wx.Window.__init__(self, parent, -1)

        self.color = color

        self.SetBackgroundColour(color)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)

    def OnRightDown(self,event):
        menu = CWxPopupMenu(self, lsStrTitle = ["Item1", "Item2", "Item3"],
               lsStrEventHandler = [self.OnItem1, self.OnItem2, self.OnItem3],
               lsIntId = None, lsStrToolTip = None)
        self.PopupMenu(menu.m_menuInstance, event.GetPosition())

    def OnItem1(self, event):
        print "Item One selected in the window"

    def OnItem2(self, event):
        print "Item Two selected in the window"

    def OnItem3(self, event):
        print "Item Three selected in the window"
    """----------------------------------------------------------------------"""


class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None, -1, "Test", size=(300, 200))

        sizer = wx.GridSizer(2,2,5,5)

        sizer.Add(MyWindow(self,"blue"),1,wx.GROW)
        sizer.Add(MyWindow(self,"yellow"),1,wx.GROW)
        sizer.Add(MyWindow(self,"red"),1,wx.GROW)
        sizer.Add(MyWindow(self,"green"),1,wx.GROW)

        self.SetSizer(sizer)

        self.Show()

    """----------------------------------------------------------------------"""

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = MyFrame()
    app.SetTopWindow(frame)
    app.MainLoop()

