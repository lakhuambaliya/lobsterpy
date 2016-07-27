#-------------------------------------------------------------------------------
# Name:        mymenu.py
# Purpose:     This module contains the classes that handles the menubar, menu and menuitems in GUI
#
# Author:      Anirudh Sureka
#
# Created:     09/03/2013
# Copyright:   (c) Teledyne Lecroy 2013
# Licence:     all rights reserved.
#-------------------------------------------------------------------------------

#imports for the module
import  wx;

#Class name :- CMenuItem
#Description :- This class represent a MenuItem that is appended to particular menu

"""-----------------------------------------------------------------------------"""

class CMenuItem():

    """
    Constructor:

    Input :
            (i) iId:- unique menuitem identifier
            (ii) strTitle :- menuTitle
            (iii) strTooltip :- tooltip that appears when mouse is hovered upon the menu
            (iv) strEvtHandlerMethod :- the method which is responsible for handling the event of this class
            (v)  menuParentMenu :- the parent menu of this CMenuItem object
            (vi) frameParent :- represents the window or frame container in which all menus and menuitems are appended

    Output: does not return anything

    Purpose : initializes the data members of CMenuItem class and bind the method with this MenuItem that is to be
              invoked when any event is triggered through that menu item

    """

    def __init__(self, iId, strTitle, strTooltip, strEvtHandlerMethod, menuParentMenu, frameParent):

            #menuItemInstance is an member varible of CMenuItem class , which is of type MenuItem
            #we have appended the menuItemInstance menuItem to mnuParentMenu object

            self.m_menuitemInstance = menuParentMenu.Append(iId, strTitle, strTooltip)

            #bounded the eventhandler method with this menuItem object,which will be invoked on the
            #click event of this menuitem

            frameParent.Bind(wx.EVT_MENU, strEvtHandlerMethod, self.m_menuitemInstance)


"""-----------------------------------------------------------------------------"""


#Class name :- CMenu
#Description :- This class represent a Menu that is appended to the menubar

class CMenu():

    """
    Constructor:

    Input :
            (i) strTitle = Title that appears on the menu
            (ii) menubarParent= the menubar to whom this menu has to be appended
            (iii) liCMenuItemMenuItems = the list which holds the object of CMenuItem class (i.e. its menuitems), that
             are appended to this menu. This arguement is Optional.

    Output : does not return anything

    Purpose : provides title to the menu, append this menu to its parentmenubar and
              provides the list of menuItems that are added under this menu, if liCMenuItemMenuItems arguement is provided

    """

    def __init__(self, strTitle, menubarParent, liCMenuItemMenuItems = []):

        #m_menuInstance is an instance variable of this class of type Menu
        self.m_menuInstance = wx.Menu( )

        if(menubarParent != None):

            #appended this menu object to its parent menubar object
            menubarParent.Append(self.m_menuInstance ,strTitle)

        #appended the list of menuitems that are appended to this menu.
        self.m_liCMenuItemChildMenuItemsList = liCMenuItemMenuItems

    """-----------------------------------------------------------------------------"""

    def __del__(self):

        """
        Destructor :-

        Throws Exception :- No

        Inputs :- does not receive any inputs

        Outputs :- does not return any value

        Purpose :- It releases the memory of the member variables of the CMenu
                    class

        """

        self.m_menuInstance = None
        self.m_liCMenuItemChildMenuItemsList = None



#Class name :- CMenuBar
#Description :- This class represent the menubar

class CMenuBar():

    """
    Constructor:

    Input :
            (i) liCMenuChildMenus = the list which contains the list of menus that are appended to this menubar object

    Output :
            does not return anything

    purpose :
            initializes the members of this class and add the list of menus that are appended to this menubar
    """

    def __init__(self, liCMenuChildMenus = []):

        #m_menubarInstance is the member variable of the class of type wx.Menubar
        self.m_menubarInstance = wx.MenuBar()

        #m_liCMenuChildMenuList is the member list which contains the menus that have to be appended to his menubar
        self.m_liCMenuChildMenuList = liCMenuChildMenus

"""-----------------------------------------------------------------------------"""

if __name__ == '__main__':
    pass