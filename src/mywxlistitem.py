#-------------------------------------------------------------------------------
# Name:        mywxlistitem.py
# Purpose:     The object of this class is used as DataSource for CWxListView.
#              It's designed with an intent to make CWxListView generic, so that
#              it can be used in another applications also
#
# Author:      lakhu
#
# Created:     03/02/2014
# Copyright:   (c) Account Prism Pvt. Ltd.
# Licence:     all_rights_reserved
#-------------------------------------------------------------------------------

#imports
import lobsterbase

# class-name        : IListItem
# class-description : This class has information which will be displayed in ListView
class IListItem(lobsterbase.CLobsterBase):
    # static variable which maintains list of headers which will be used for
    # displaying header of the CWxListView. it will be empty initially. It's
    # the responsibility of the child class of IListItem to populate this list
    # with appropriate column names.
    ms_lsStrHeaders = []

    def __init__(self, dictListItemInfo = None, objCLogger = None):

        """
        Constructor :-

        Throws Exception : No

        Inputs  :- (i) dictListItemInfo  : dictionary containing list items, which
                                          will be of following type :-
                                          eg. {"SrNo" : 1, "Weight" : 20}
                                          The keys of this dictionary are actually the
                                          members of ms_lsStrHeaders.

        Outputs :- does not return any values

        Purpose :- initialize data member of the class

        """
        # calling parent constructor
        lobsterbase.CLobsterBase.__init__(self, objCLogger = objCLogger);

        # member varible which contains items to be displayed in CWxListView.
        # CWxListView class uses this dictionary to populate one row in the
        # listctrl in GUI.
        self.__m_dictListItemInfo__ = dictListItemInfo

        return

    """----------------------------------------------------------------------"""

    def MGetItems(self):

        """
        Member Function :-

        Throws Exception :- No

        Inputs  : does not receive any inputs

        Outputs : (i) return Dictionary containing list items

        Purpose : getter method for __m_dictListItemInfo__ member variable

        """
        return self.__m_dictListItemInfo__

    """----------------------------------------------------------------------"""

    def MSetItems(self, dictListItemInfo = None):

        """
        Member Function :-

        Throws Exception :- No

        Inputs  : (i) dictListItemInfo : dictionary containing list items

        Outputs : does not return any values

        Purpose : setter method for member variable __m_dictListItemInfo__.

        """
        # initialize member variable by received inputs
        self.__m_dictListItemInfo__ = dictListItemInfo

        return

    """----------------------------------------------------------------------"""

    def __del__(self):

        """
        Destructor :-

        Throws Exception : No

        Inputs  : does not receive any inputs

        Outputs : does not return any values

        Purpose : releases the memory allocated for member variables

        """
        # release memory allocated for member variable __m_dictListItemInfo__
        self.__m_dictListItemInfo__ = None
        # calling parent class' destructor
        lobsterbase.CLobsterBase.__del__(self)

        return

    """----------------------------------------------------------------------"""

    @staticmethod
    def MSTestIListItems():

        """
        Tester Function :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : does not return any values

        Purpose : test constructor and methods by different inputs

        """
        # creating object of IListItem
        objIListItem = IListItem(dictListItemInfo =  {1:"Lakhu", 2:"Kruti", 3:"mangu"})
        # testing MWhos() function with enable log
        print objIListItem.MWhos(bEnableLog = True)
        # testing MSetItems() function
        objIListItem.MSetItems(dictListItemInfo = {11:100, 22:20, 33:30})
        # testing MWriteYaml() function
        objIListItem.MWriteYaml("c:\\temp\\dump.txt")
        # testing MSetItems() function
        objIListItem.MSetItems(dictListItemInfo = {1:10, 2:20, 3:30})
        # reading object from file
        objIListItem = objIListItem.MReadFromYaml("c:\\temp\\dump.txt")
        # getting items
        print objIListItem.MGetItems()

        return

    """----------------------------------------------------------------------"""

if __name__ == '__main__':
    IListItem.MSTestIListItems()