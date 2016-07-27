#-------------------------------------------------------------------------------
# Name:         mywxlistview.py
# Purpose:      This module contains CListView class, which extends wx.ListCtrl.
#               It's intended to make wx.ListCtrl generic, so that it can be used
#               in any application.
#
# Author:       Kruti
#
# Created:      18-02-2014
# Copyright:    (c) Account Prism Pvt. Ltd.
# Licence:      all_rights_reserved
#-------------------------------------------------------------------------------

# imports
import wx
import wx.lib.mixins.listctrl as listmix
import decimal
import math
import lobstereventhandler
import lobstercvar
import lobsterpreferences
import mywxpopupmenu as popupmenu
import LecroyUtil_portable as LecP
import lobsterparser

# class-name    : CWxListView
# class-description : This class extends wx.ListCtrl. This class is designed to make
#                     the listview generic, so that it can be used in any application.
#                     This class extends listmix.ColumnSorterMixin, in order to provide
#                     sorting facility in the listcontrol

#   TODO :- Although this class is said to be generic, at present it's having certain
#           code for the features, that pertain to lobsterpy application, such as copy
#           cvars, edit cvars, etc. So, in future, for lobsterpy application, one class
#           will be required to be made, which will inherit this class and the functionality
#           pertaining to lobsterpy application.
class CWxListView(wx.ListCtrl, listmix.ColumnSorterMixin, listmix.TextEditMixin):

    def __init__(
                    self, parent, dictCVarCollection, numCols,
                    style = wx.LC_REPORT | wx.HSCROLL | wx.VSCROLL | wx.ALWAYS_SHOW_SB
                    | wx.BORDER_SUNKEN
                ):
        """
        Constructor :-

        Throws Exception :- No

        Inputs :- (i) parent :- parent class or window of the current class

               (ii) dictCVarCollection :- main dictionary in the application,
                                          which holds information about cvar
                                          and cvardirectories.

        Outputs :- does not return any value

        Purpose :- initializes the member variables to default values

        """

        #  calling the constuctor of wx.ListCtrl
        wx.ListCtrl.__init__(self, parent, style = style)

        #  member variable
        self.m_dictCVarCollection = dictCVarCollection

        #  binding the events for right click of listcontrol
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.MOnRightDown)

        #   it's dictionary that's used by ColumnSorterMixin class for sorting.
        self.itemDataMap = {}

        listmix.ColumnSorterMixin.__init__(self, numCols)

        listmix.TextEditMixin.__init__(self)

        #   Note :- ColumnSorterMixin class provides us sorting facility,
        #           provided that we have satisfied all the contraints and
        #           conditions that it imposes.

        #   following are the conditions and contraints for using ColumnSorterMixin
        #   class :-

        #   1)  itemDataMap dictionary must be defined in the child class, which will
        #       be populated by the items, which are currently displayed in listctrl
        #       ColumnSorterMixin class, uses this dictionary for sorting of items.
        #       Moreover, it's required that you must update this dictionary manually,
        #       whenever, the listctrl is updated with new items.

        #   2)  Constructor of ColumnSorterMixin must be invoked only after, itemDataMap
        #       have been set to any value. eg. in our case we have set it to empty
        #       dictionary {}.

        #   3)  Child class must have GetListCtrl() method defined in it as member method,
        #       which will return the listctrl

        #   4)  ColumnSorterMixin contructor invocation requires, number of columns to be
        #       provided as argument. So have to provide column count at the time of
        #       invocation of its argument

        #   5)  Last but not least. In case, when you are showing the details of any object
        #       in the listview, i.e., for eg. if you are showing student details such as
        #       rollno, marks, etc. in the listview, which are encapsulated as objects,
        #       then you have to define __getitem__() method, in that class properly, which
        #       will return the appropriate values. For more details about this, refer to
        #       cvar class.

        #   creating an image list, which will contain images of dimension 16 x 16
        self.m_lsImages = wx.ImageList(16, 16)

        a = {"m_imageUp" : "GO_UP", "m_imageDown" : "GO_DOWN"}

        #  adding images of UP and DOWN arrow to the image list
        for strKey, strValue in a.items():
            #   made the instruction to be executed in the form of string
            s = "self.%s = self.m_lsImages.Add(wx.ArtProvider_GetBitmap(wx.ART_%s,wx.ART_TOOLBAR,(16,16)))" % (strKey, strValue)
            #   executing the instruction
            exec(s)

        #   icon for favourite cvar
        self.m_objFavImg = self.m_lsImages.Add(wx.Bitmap(r'../res/star_gold_16.ico'))

        self.SetImageList(self.m_lsImages, wx.IMAGE_LIST_SMALL)

        return

    """----------------------------------------------------------------------"""

    #   this code is yet to implement
    def OpenEditor(self, col, row):
        if (col != 4):
            return
        else:
            listmix.TextEditMixin.OpenEditor(self, col, row)

        return

    """----------------------------------------------------------------------"""

    def GetSortImages(self):

        """
        Method of ColumnSorterMixin :-

        Throws Exception :- No

        Inputs :- does not receive any inputs

        Outputs :- returns a tuple of images

        Purpose :- This method is used by the ColumnSorterMixin. This method
                    puts images at the headers while sorting

        """

        return (self.m_imageUp, self.m_imageDown)

    """----------------------------------------------------------------------"""

    def GetListCtrl(self):

        """
        Member Method :-

        Throws Exception :- No

        Inputs :- does not receive any inputs

        Outputs :- returns the object of listctrl

        Purpose :- This method is used to get the listctrl on which sorting is to
                    be sorted. This method is required by ColumnSorterMixin to
                    perform sorting

        """

        return self

    """----------------------------------------------------------------------"""

    def MOnRightDown(self, event):

        """
        Member Method :-

        Throws Exception :- No

        Inputs :- (i) event :- object of wx.Event, it specifies event for which
                               the method is called

        Outputs :- does not return any value

        Purpose :- This method displays a popup menu when the user right clicks
                   on the listctrl

        """

        #   creating objcet of popup menu
        self.m_objMenu = popupmenu.CWxPopupMenu(self, lsStrTitle = ["Copy", "Edit", "Add to Favorite",
                                                                     "Add to Watch Window"],
                                                     lsStrEventHandler = [
                                                                            self.MOnCopy,
                                                                            self.MOnEdit,
                                                                            self.MOnAddToFavorite,
                                                                            self.MOnAddToWatchWindow
                                                                         ],
                                                        lsIntId = None, lsStrToolTip = None
                                                )

        self.PopupMenu(self.m_objMenu.m_menuInstance, event.GetPosition())

        return

    """----------------------------------------------------------------------"""

    def MOnCopy(self, event):

        """
        Member Method :-

        Throws Exception :- No

        Inputs :- (i) event :- object of wx.Event, it specifies for which event
                               the method is called

        Outputs :- does not return any value

        Purpose :- This method acts as a stub method which calls the method
                   of the class CEventHandler
        """

        lobstereventhandler.CEventHandler.MSOnCopy(event, self.GetParent())

        return

    """----------------------------------------------------------------------"""

    def MOnEdit(self, event):

        """
        Member Method :-

        Throws Exception :- No

        Inputs :- (i) event :- object of wx.Event, it specifies for which event
                               the method is called

        Outputs :- does not return any value

        Purpose :- This method acts as a stub method which calls the method
                   of the class CEventHandler
        """

        lobstereventhandler.CEventHandler.MSOnEdit(event, self.GetParent())

        return

    """----------------------------------------------------------------------"""

    def MOnAddToFavorite(self, event):

        """
        Member Method :-

        Throws Exception :- No

        Inputs :- (i) event :- object of wx.Event, it specifies for which event
                               the method is called

        Outputs :- does not return any value

        Purpose :- This method acts as a stub method which calls the method
                   of the class CEventHandler
        """

        lobstereventhandler.CEventHandler.MSOnAddToFavorite(event, self.GetParent())

        return

    """----------------------------------------------------------------------"""

    def MOnAddToWatchWindow(self, event):

        """
        Member Method :-

        Throws Exception :- No

        Inputs :- (i) event :- object of wx.Event, it specifies for which event
                               the method is called

        Outputs :- does not return any value

        Purpose :- This method acts as a stub method which calls the method
                   of the class CEventHandler
        """

        lobstereventhandler.CEventHandler.MSOnAddToWatchWindow(event, self.GetParent())

        return

    """----------------------------------------------------------------------"""

    def MAddHeaders(self, lsKeys):

        """
        Member Method :-

        Throws Exception :- No

        Inputs :- (i) lsKeys :- contains the list of headers

        Outputs :- does not return any value

        Purpose :- This method adds the headers to the listview

        """

        #   getting preferences
        objCPreferences = self.GetParent().m_objLobsterDataContext.MGetPreferences()
        #   getting columns, which users have specified to be shown
        lsFilteredColumn = objCPreferences.MGetFilteredColumns()

        #   iterating through the lsKeys
        for idx, strHeader in enumerate(lsKeys):
            #   setting column width to 0 by default,  so that column which
            #   user have not specified are not visible
            iColumnWidth = 0
            #   inserting column to the listview
            self.InsertColumn(idx, strHeader)
            if (idx in lsFilteredColumn):
                #   leaving extra space for columns for "Name" or "Adapted" or "AbsolutePath" value
                if(strHeader == "Name" or strHeader == "Adapted" or strHeader == "AbsolutePath"):
                    iColumnWidth = 140
                else:
                    iColumnWidth = 80

            #   setting the width of the column
            self.SetColumnWidth(idx, iColumnWidth)

        return

    """----------------------------------------------------------------------"""

    #   TODO :- Optimize this method, to selectively populate the values of attributes
    #           which are applicable for cvar
    def MPopulateValuesInListView(self, lsStrChildCVar, strDirAbsolutePath = None, bGenerateAbsPath = True):

        """
        Member Method :-

        Throws Exception :- No

        Inputs :- (i)   lsStrChildCVar :- list of cvars whose details have to be shown

                  (ii)  strDirAbsolutePath :- absolute path of the current directory

                  (iii) bGenerateAbsPath :- True if absolutepath have to be generated
                                            in the algorithm, otherwise False. Absolute
                                            path is not required to be generated, whenever
                                            search-results or favourite list cvars are shown

        Outputs :- does not return any value

        Purpose :- This method populates teh values in the listview

        """

        #   creating object to cTimer class
        timer = LecP.cTimer()

        #   calling the method to start the timer
        timer.startTimer()

        #   clearing listctrl, in order to update it
        self.ClearAll()

        #   a boolean variable, which indicates whether headers are added or not
        bAreHeadersReady = False

        #   getting the headers of the CVar and storing it in a list
        #   which is to be used as keys
        lsKeys = []

        #   iterating through the lsStrChildCVar
        for iIndex, strChild in enumerate(lsStrChildCVar):
            try:
                #   if child CVar is present
                if (strChild != ""):

                    strCVarAbsolutePath = strChild

                    #   if absolute path is to be generated explicitly
                    if (bGenerateAbsPath):
                        #   getting the absolute path of the current CVar
                        strCVarAbsolutePath = strDirAbsolutePath + "." +strChild

                    #   creating the object of CVar
                    objCVar = self.m_dictCVarCollection.get(strCVarAbsolutePath)

                    #   adding the object of CVar to the dictionary
                    self.itemDataMap[iIndex] = objCVar

                    #   if headers are not added
                    if (not(bAreHeadersReady)):
                        lsKeys = objCVar.ms_lsStrHeaders
                        #   calling the MAddHeaders() method to add the headers
                        self.MAddHeaders(lsKeys)
                        bAreHeadersReady = True

                    #   getting all the items of the CVar
                    dictValues = objCVar.__m_dictListItemInfo__

                    #   getting the specific items of the CVar, which are applicable
                    #   to that particular type of CVar
                    lsSpecificAttributes = lobsterparser.CLobsterFileParser.ms_dictTypeOfCVarAndAttributes.get(objCVar.ms_lsStrTypes[objCVar.MGetCVarType()])

                    #   inserting the value at the 0th column
                    #   SetStringItem is not applicable for 0th index.
                    #   That's why, InsertStringItem is used in this way,
                    #   outside the loop
                    self.InsertStringItem(iIndex, str(dictValues.get(lsKeys[0])))

                    strType = ""

                    #   iterating through the list
                    for i in range(1, len(lsKeys)):

                        #   if the current attribute is not applicable to
                        #   current CVar, then display an empty string in the
                        #   cell of the listview
                        if(lsKeys[i] not in lsSpecificAttributes):
                            self.SetStringItem(iIndex, i, " ")

                        #   inserting the values in the remaining columns
                        self.SetStringItem(iIndex, i, str(dictValues.get(lsKeys[i])))

                        #   if value for "Type" is being displayed
                        if (lsKeys[i] == "Type"):
                            #   fetching the string representation of "Type"
                            strType = str(objCVar.ms_lsStrTypes[dictValues.get(lsKeys[i])])
                            self.SetStringItem(iIndex, i, strType)

                        #   if value for "Flags" is being displayed
                        if (lsKeys[i] == "Flags"):
                            strFlag = objCVar.__getitem__(i)
                            self.SetStringItem(iIndex, i, strFlag)

                        #   if any value is not available for the CVar
                        if (dictValues.get(lsKeys[i]) == None):
                            #   representating None values as empty string
                            self.SetStringItem(iIndex, i, " ")

                        if (
                                (
                                    (strType == "Integer") or (strType == "DoubleLockstep") or (strType == "Double")
                                ) and
                                (
                                    (lsKeys[i] == "Requested") or (lsKeys[i] == "Adapted") or (lsKeys[i] == "Default")or
                                    (lsKeys[i] == "Min") or (lsKeys[i] == "Max") or (lsKeys[i] == "Grain")
                                )
                            ):

                            strValue = str(dictValues.get(lsKeys[i]))
                            fValue = float(strValue)

                            if (self.GetParent().m_objLobsterDataContext.MGetPreferences().MGetNumericNotation() == lobsterpreferences.CPreferences.mC_ENGINEERING_NOTATION):
                                strNotation = str(CWxListView.MSToEngineeringNotation(x = fValue, format='%.2f', si = True))
                            elif (self.GetParent().m_objLobsterDataContext.MGetPreferences().MGetNumericNotation() == lobsterpreferences.CPreferences.mC_EXPONENTIAL_NOTATION):
                                strNotation = str(CWxListView.MSToEngineeringNotation(x = fValue, format='%.2f', si = False))
                            elif (self.GetParent().m_objLobsterDataContext.MGetPreferences().MGetNumericNotation() == lobsterpreferences.CPreferences.mC_STANDARD_NOTATION):
                                if(strType == "Double"):
                                    strNotation = str('%f' % fValue)
                                else:
                                    strNotation = str(fValue)
                            self.SetStringItem(iIndex, i, strNotation)

                        #   calling the method SetItemData for the purpose of sorting
                        self.SetItemData(iIndex, iIndex)

                    #   if the CVar belongs to the list of favorite CVars, then
                    #   set the image for it
                    if strCVarAbsolutePath in self.GetParent().m_objLobsterDataContext.__m_lsStrFavoriteCVars__:
                        self.SetItemImage(iIndex, self.m_objFavImg)

                else:
                    raise Exception("None or empty string obtained " + str(strChild))
            except:
                print "Error in : " +strChild
                return

        #   refreshing list view
        self.Refresh()

        totalTime = timer.stopTimer()

        print "Total time taken : " + str(totalTime)

        return

    """----------------------------------------------------------------------"""

    @staticmethod
    def MSToEngineeringNotation( x, format='%s', si=False):
        '''
        Returns float/int value <x> formatted in a simplified engineering format -
        using an exponent that is a multiple of 3.

        format: printf-style string used to format the value before the exponent.

        si: if true, use SI suffix for exponent, e.g. k instead of e3, n instead of
        e-9 etc.

        E.g. with format='%.2f':
            1.23e-08 => 12.30e-9
                 123 => 123.00
              1230.0 => 1.23e3
          -1230000.0 => -1.23e6

        and with si=True:
              1230.0 => 1.23k
          -1230000.0 => -1.23M
        '''
        if(x == 0):
            return x

        sign = ''
        if x < 0:
            x = -x
            sign = '-'
        exp = int(math.floor(math.log10(x)))
        exp3 = exp - ( exp % 3)
        x3 = x / ( 10 ** exp3)

        if si and exp3 >= -24 and exp3 <= 24 and exp3 != 0:
            exp3_text = 'yzafpnum kMGTPEZY'[ ( exp3 - (-24)) / 3]
        elif exp3 == 0:
            exp3_text = ''
        else:
            exp3_text = 'e%s' % exp3

        return ( '%s'+format+'%s') % ( sign, x3, exp3_text)

    """----------------------------------------------------------------------"""