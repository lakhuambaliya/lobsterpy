#-------------------------------------------------------------------------------
# Name:        testmywxtreeitem.py
# Purpose:     This module contains tester functions for IItreeItem class.
#
# Author:      Kruti
#
# Created:     03-02-2014
# Copyright:   (c) Account Prism Pvt. Ltd.
# Licence:     all_rights_reserved
#-------------------------------------------------------------------------------

import unittest
import mywxtreeitem

#   class-name :- TestITreeItem
#   class-description :- This class tests all the methods of ITreeItem class
class TestITreeItem(unittest.TestCase):

    def setUp(self):

        """
        Purpose :- performs all the initialization operations prior to each test-case.

        """

        self.m_objITreeItem = mywxtreeitem.ITreeItem(
                                                strParentNodeNameWithFullPath = "CVarDirectory",
                                                strNodeName = "CVar", lsStrChildNodes = ["A", "B", "C"]
                                                )

        return

    """----------------------------------------------------------------------"""

    def testInit(self):

        """
        Tester Function :-

        Purpose :- Tests constructor of ITreeItem class

        """

        objITreeItem = mywxtreeitem.ITreeItem(strParentNodeNameWithFullPath = "CVarDirectory",
                    strNodeName = "CVar", lsStrChildNodes = ["A", "B", "C"])

        self.assertEqual(objITreeItem.MGetParentNodeNameWithFullPath(), "CVarDirectory")

        self.assertEqual(objITreeItem.MGetChildNodes(), ['A', 'B', 'C'])

        self.assertEqual(objITreeItem.MGetNodeName() ,"CVar")

        return
    """----------------------------------------------------------------------"""

    def tearDown(self):

        """
        Deallocates the memory of the member variables

        """

        self.m_objITreeItem = None
    """----------------------------------------------------------------------"""

    def testMGetParentNodeNameWithFullPath(self):

        """
        Tester Function :-

        Purpose : - Tests MGetParentNodeNameWithFullPath() function of ITreeItem class.

        """
        self.assertEqual(self.m_objITreeItem.MGetParentNodeNameWithFullPath(),"CVarDirectory")

        self.m_objITreeItem.MSetParentNodeNameWithFullPath("Parent.Parent Directory")
        self.assertEqual(self.m_objITreeItem.MGetParentNodeNameWithFullPath(), "Parent.Parent Directory")

        return

    """----------------------------------------------------------------------"""

    def testMSetParentNodeNameWithFullPath(self):

        """
        Tester Function :-

        Purpose : - Tests MSetParentNodeNameWithFullPath() function of ITreeItem class.

        """
        #   expects Exception, because MSetParentNodeNameWithFullPath() is invoked with integer
        #   value as argument.
        self.assertRaises(Exception, self.m_objITreeItem.MSetParentNodeNameWithFullPath, (1, ))
        #   expects Exception, because MSetParentNodeNameWithFullPath() is invoked with None
        #   value as argument.
        self.assertRaises(Exception, self.m_objITreeItem.MSetParentNodeNameWithFullPath, (None, ))
        #   expects Exception, because MSetParentNodeNameWithFullPath() is invoked with empty string
        #   value as argument.
        self.assertRaises(Exception, self.m_objITreeItem.MSetParentNodeNameWithFullPath, ("", ))

        self.m_objITreeItem.MSetParentNodeNameWithFullPath("New Parent")

        return

    """----------------------------------------------------------------------"""

    def testMGetNodeName(self):

        """
        Tester Function :-

        Purpose : - Tests MGetNodeName() function of ITreeItem class.

        """
        self.m_objITreeItem.MSetNodeName("New Node")
        self.assertEqual(self.m_objITreeItem.MGetNodeName(), "New Node")

        return

    """----------------------------------------------------------------------"""

    def testMSetNodeName(self):

        """
        Tester Function :-

        Purpose : - Tests MSetNodeName() function of ITreeItem class.

        """

        self.m_objITreeItem.MSetNodeName("New Node")
        self.assertEqual("New Node", self.m_objITreeItem.MGetNodeName())
        #   expecting Exception, because MSetNodeName is invoked with integer value
        #   as argument.
        self.assertRaises(Exception, self.m_objITreeItem.MSetParentNodeNameWithFullPath, (1, ))
        #   expecting Exception, because MSetNodeName is invoked with None value
        #   as argument.
        self.assertRaises(Exception, self.m_objITreeItem.MSetParentNodeNameWithFullPath, (None, ))
        #   expecting Exception, because MSetNodeName is invoked with empty string
        #   as argument.
        self.assertRaises(Exception, self.m_objITreeItem.MSetParentNodeNameWithFullPath, ("", ))

        return

    """----------------------------------------------------------------------"""

    def testMGetChildNodes(self):

        """
        Tester Function :-

        Purpose : - Tests MGetChildNodes() function of ITreeItem class.

        """
        self.assertEqual(self.m_objITreeItem.MGetChildNodes(), ['A', 'B', 'C'])

        return

    """----------------------------------------------------------------------"""

    def testMHasChildNodes(self):

        """
        Tester Function :-

        Purpose : - Tests MHasChildNodes() function of ITreeItem class.

        """
        #   expecting True to be output, as m_objITreeItem have been
        #   passed a list of child-nodes.
        self.assertEqual(self.m_objITreeItem.MHasChildNodes(), True)

        return

    """----------------------------------------------------------------------"""

    def testMAppendChildNode(self):

        """
        Tester Function :-

        Purpose : - Tests MAppendChildNode() function of ITreeItem class.

        """
        self.m_objITreeItem.MAppendChildNode("R")
        #   If "R" is not the part of list of childnodes of current node,
        #   then Exception will be throws and thus test-case will fail.
        self.m_objITreeItem.MGetChildNodes().index("R")

        #   expecting Exception to be raised, because MAppendChildNode() is
        #   invoked with Integer values as argument.
        self.assertRaises(Exception, self.m_objITreeItem.MAppendChildNode, (2, ))
        #   expecting Exception to be raised, because MAppendChildNode() is
        #   invoked with None value as argument.
        self.assertRaises(Exception, self.m_objITreeItem.MAppendChildNode, (None, ))
        #   expecting Exception to be raised, because MAppendChildNode() is
        #   invoked with empty string as argument.
        self.assertRaises(Exception, self.m_objITreeItem.MAppendChildNode, ("", ))

        return

    """----------------------------------------------------------------------"""

if __name__ == '__main__':
    unittest.main()
