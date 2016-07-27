#-------------------------------------------------------------------------------
# Name:        testmywxlistitem.py
# Purpose:     This module contains tester method for testing IListItem interface(class)
#              in mywxlistitem module
#
# Author:      lakhu
#
# Created:     03/02/2014
# Copyright:   (c) Account Prism Pvt. Ltd.
# Licence:     all_rights_reserved
#-------------------------------------------------------------------------------

#   imports
import unittest
import mywxlistitem as list

class TestIListItem(unittest.TestCase):

    def setUp(self):

        """
        Purpose :- performs all the initialization operations prior to each test-case.

        """
        self.m_dictListItems = {1 : "Lakhu", 2 : "Kruti", 3 : "mangu"}
        # creating object of IListItem
        self.m_objIListItem = list.IListItem(dictListItemInfo = self.m_dictListItems)

        return

    """----------------------------------------------------------------------"""

    def tearDown(self):
        """
        Purpose :- performs all the initialization operations after the completion
                   of each test-case.

        """
        #   setting dictionary to None
        self.m_dictListItems = None
        #   setting object of IListItem to None
        self.m_objIListItem = None

        return

    """----------------------------------------------------------------------"""

    def test__init__(self):
        """
        Tester Function :-

        Purpose : - Tests Constructor of CVar class.

        """
        #   invoking IListItem constructor with dictionary as argument
        objIListItem = list.IListItem(dictListItemInfo = self.m_dictListItems)
        #   asserting that objIListItem is created successfully and it's not None
        self.assertNotEqual(objIListItem, None)
        #   invoking IListItem constructor without dictionary as argument
        objIListItem = list.IListItem()
        #   asserting that objIListItem is created successfully and it's not None
        self.assertNotEqual(objIListItem, None)

        return

    """----------------------------------------------------------------------"""

    def testMGetItems(self):

        """
        Tester Function :-

        Purpose : - Tests MGetItems() function of CVar class.

        """
        #   creating the dictionary
        tempDict1 = {1 : "Roll", 2 : "Name", 3 : "City", 4 : "Mobile"}
        #   setting it as member dictionary of self.m_objIListItem
        self.m_objIListItem.MSetItems(tempDict1)
        #   getting the member dictionary of self.m_objIListItem
        tempDict2 = self.m_objIListItem.MGetItems()
        #   asserting that tempDict1 is equal to dictionary obtained from setter method.
        self.assertEqual(tempDict1, tempDict2)

        return

    """----------------------------------------------------------------------"""

    def testMSetItems(self):

        """
        Tester Function :-

        Purpose : - Tests MSetItems() function of CVar class.

        """
        #   creating the dictionary
        tempDict1 = {1 : "Roll", 2 : "Name", 3 : "City", 4 : "Mobile"}
        #   setting it as member dictionary of self.m_objIListItem
        self.m_objIListItem.MSetItems(tempDict1)
        #   getting the member dictionary of self.m_objIListItem
        tempDict2 = self.m_objIListItem.MGetItems()
        #   asserting that tempDict1 is equal to dictionary obtained from setter method.
        self.assertEqual(tempDict1,tempDict2)

        return

    """----------------------------------------------------------------------"""
if __name__ == '__main__':
    unittest.main()