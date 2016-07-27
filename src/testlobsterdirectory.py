#-------------------------------------------------------------------------------
# Name:        testlobsterdirectory.py
# Purpose:     This module contains the tester functions for CCVarDirectory class.
#
# Author:      Kruti
#
# Created:     04-02-2014
# Copyright:   (c) Account Prism Pvt. Ltd.
# Licence:     all_rights_reserved
#-------------------------------------------------------------------------------

#   imports
import unittest
import lobsterdirectory

#   class-name :- TestCCVarDirectory
#   class-description :- This class tests all the methods of CCVarDirectory class
class TestCCVarDirectory(unittest.TestCase):

    def setUp(self):

        """

        Purpose :- performs all the initialization operations prior to each test-case.

        """
        #   creating object of CCvarDirectory, by passing all the required arguments
        self.m_objCCVarDirectory = lobsterdirectory.CCVarDirectory(
                                                                    strNodeName= "Current Node", lsStrChildDirectories = ["Child1", "Child2", "Child3"],
                                                                    strParentDirectoryName = "Parent.New Directory",
                                                                    lsStrSiblingDirectories = ["SiblingDir1", "SiblingDir2"],
                                                                    lsStrSiblingCVars = ["SiblingCVar1", "SiblingCVar2"],
                                                                    lsStrChildCVars = ["ChildCVar1", "ChildCvar2"]
                                                                )

        #   creating object of CCvarDirectory, by passing only nodename and list of child directories
        self.m_objCCVarDirectory2 = lobsterdirectory.CCVarDirectory(strNodeName = "New Node", lsStrChildDirectories = ["Child"])

        return

    """----------------------------------------------------------------------"""

    def testinit(self):

        """
        Tester Function :-

        Purpose :- Tests constructor of CCVarDirectory class

        """

        objCCVarDirectory = lobsterdirectory.CCVarDirectory(
                        "Current Node", ["Child1", "Child2", "Child3"],
                        "Parent.New Directory", ["SiblingDir1", "SiblingDir2"],
                        ["SiblingCVar1", "SiblingCVar2"],["ChildCVar1", "ChildCvar2"]
                        )

        self.assertEqual(objCCVarDirectory.MGetAbsolutePath(), "Parent.New Directory.Current Node")

        self.assertEqual(objCCVarDirectory.MGetChildCVars(), ['ChildCVar1', 'ChildCvar2'])

        self.assertEqual(objCCVarDirectory.MGetChildNodes(),["Child1", "Child2", "Child3"])

        self.assertEqual(objCCVarDirectory.MGetNodeName(), "Current Node")

        self.assertEqual(objCCVarDirectory.MGetSiblingCVars(),["SiblingCVar1", "SiblingCVar2"])

        self.assertEqual(objCCVarDirectory.MGetSiblingDirectories(), ["SiblingDir1", "SiblingDir2"])

        return

    """----------------------------------------------------------------------"""

    def tearDown(self):

        """
        Deallocates the memory of the member variables

        """

        self.m_objCCVarDirectory = None
        self.m_objCCVarDirectory2 = None

        return

    """----------------------------------------------------------------------"""

    def testMHasChildCVars(self):

        """
        Tester Function :-

        Purpose : - Tests MHasChildCVars() function of CVar class.

        """
        #   asserting that MHasChildCVars() return True for m_objCCVarDirectory
        self.assertEqual(self.m_objCCVarDirectory.MHasChildCVars(), True)
        #   asserting that MHasChildCVars() return False for m_objCCVarDirectory
        self.assertEqual(self.m_objCCVarDirectory2.MHasChildCVars(), False)

        return

    """----------------------------------------------------------------------"""

    def testMAppendChildCVar(self):

        """
        Tester Function :-

        Purpose : - Tests MAppendChildCVar() function of CVar class.

        """
        self.m_objCCVarDirectory.MAppendChildCVar("NewChildCVar")
        #   ValueError Exception will be raised, if MAppendChildCVar() has not
        #   completed successfully(i.e, NewChildCVar is not in the list of childcvars)
        self.m_objCCVarDirectory.MGetChildCVars().index("NewChildCVar")
        #   expecting Exception to be raised, because MAppendChildCVar() is invoked
        #   with integer value as argument.
        self.assertRaises(Exception, self.m_objCCVarDirectory.MAppendChildCVar, (1, ))
        #   expecting Exception to be raised, because MAppendChildCVar() is invoked
        #   with None as argument
        self.assertRaises(Exception, self.m_objCCVarDirectory.MAppendChildCVar, (None, ))
        #   expecting Exception to be raised, because MAppendChildCVar() is invoked
        #   with empty string as argument
        self.assertRaises(Exception, self.m_objCCVarDirectory.MAppendChildCVar, (None, ))

        return

    """----------------------------------------------------------------------"""

    def testMGetChildCVars(self):

        """
        Tester Function :-

        Purpose : - Tests MGetChildCVars() function of CVar class.

        """
        self.assertEqual(self.m_objCCVarDirectory.MGetChildCVars(), ['ChildCVar1', 'ChildCvar2'])
        #   asserting that MGetChildCVars() for m_objCCvarDirectory2 returns empty list
        self.assertEqual(self.m_objCCVarDirectory2.MGetChildCVars(), [])

        return

    """----------------------------------------------------------------------"""

    def testMGetSiblingDirectories(self):

        """
        Tester Function :-

        Purpose : - Tests MGetSiblingDirectories() function of CVar class.

        """
        self.assertEqual(self.m_objCCVarDirectory.MGetSiblingDirectories(), ['SiblingDir1', 'SiblingDir2'])
        #   asserting that MGetSiblingDirectories() for m_objCCvarDirectory2 returns empty list
        self.assertEqual(self.m_objCCVarDirectory2.MGetSiblingDirectories(), [])

        return

    """----------------------------------------------------------------------"""

    def testMGetSiblingCVars(self):

        """
        Tester Function :-

        Purpose : - Tests Constructor MGetSiblingCVars() of CVar class.

        """
        self.assertEqual(self.m_objCCVarDirectory.MGetSiblingCVars(), ['SiblingCVar1', 'SiblingCVar2'])
        #   asserting that MGetSiblingCVars() for m_objCCvarDirectory2 returns empty list
        self.assertEqual(self.m_objCCVarDirectory2.MGetSiblingCVars(), [])

        return

    """----------------------------------------------------------------------"""

    def testMGetAbsolutePath(self):

        """
        Tester Function :-

        Purpose : - Tests MGetAbsolutePath() function of CVar class.

        """
        #   asserting that MGetAbsolutePath() for m_objCCvarDirectory returns "Parent.New Directory.Current Node"
        self.assertEqual(self.m_objCCVarDirectory.MGetAbsolutePath(), "Parent.New Directory.Current Node")
        #   asserting that MGetAbsolutePath() for m_objCCvarDirectory1 returns "New Node"
        self.assertEqual(self.m_objCCVarDirectory2.MGetAbsolutePath(), "New Node")

        return

    """----------------------------------------------------------------------"""

if __name__ == '__main__':
    unittest.main()