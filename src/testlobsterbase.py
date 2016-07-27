#-------------------------------------------------------------------------------
# Name:        testlobsterbase
# Purpose:     This module contains tester methods for CLobsterBase class
#
# Author:      lakhu
#
# Created:     03/02/2014
# Copyright:   (c) Account Prism Pvt. Ltd.
# Licence:     all_rights_reserved
#-------------------------------------------------------------------------------

#imports
import unittest
import lobsterbase
import mylogmanager

class TestCLobsterBase(unittest.TestCase):

    def setUp(self):
        """
        Purpose :- performs all the initialization operations prior to each test-case.

        """
        # creating object of ClobsterBase
        self.m_objCLobsterBase1 = lobsterbase.CLobsterBase()

        return

    """----------------------------------------------------------------------"""

    def tearDown(self):
        """
        Purpose :- performs all finalization activities, when each test-case
                   have been ended.

        """
        #   setting member object to None
        self.m_objCLobsterBase1 = None

        return

    """----------------------------------------------------------------------"""

    def test__init__(self):

        """
        Tester Function :-

        Purpose : - Tests Constructor function of CVar class.

        """
         # creating object of ClobsterBase
        objCLobsterBase1 = lobsterbase.CLobsterBase()
        # crreating object of CLogger
        objCLogger = mylogmanager.CLogger(
                                            "c:\\temp\\temp.txt", iBufSize = 0,
                                            eLogMode = mylogmanager.CLogger.mC_FILELOG,
                                            eLogLimit = mylogmanager.CLogger.mC_LOGMSGBASEDLIMIT, iLogLimitAmount = 30
                                        )
        # creting object CLobsterBase by passing parameter
        objCLobsterBase2 = lobsterbase.CLobsterBase(objCLogger)

        return

    """----------------------------------------------------------------------"""

    def testMWhos(self):

        """
        Tester Function :-

        Purpose : - Tests MWhos() function of CVar class.

        """
        # with bEnableLog parameter
        self.m_objCLobsterBase1.MWhos(bEnableLog = True)
        # without bEnableLog parameter
        self.m_objCLobsterBase1.MWhos()

        return

    """----------------------------------------------------------------------"""

    def testMReadFromYaml(self):
        """
        Tester Function :-

        Purpose : - Tests MReadFromYaml() function of CVar class.

        """
        # Writing object into file
        self.m_objCLobsterBase1.MWriteYaml("c:\\temp\\dump.txt")
        obj = self.m_objCLobsterBase1.MReadFromYaml("c:\\temp\\dump.txt")
        #   WriteYaml() function never writes instance of logger class, so when
        #   reading it from file, will give logger object as None
        self.assertEqual(obj.m_objCLogger, None)

        return

    """----------------------------------------------------------------------"""

    def testMWriteYaml(self):
        """
        Tester Function :-

        Purpose : - Tests MWriteYaml() function of CVar class.

        """
         # Writing object into file
        self.m_objCLobsterBase1.MWriteYaml("c:\\temp\\dump.txt")
        obj = self.m_objCLobsterBase1.MReadFromYaml("c:\\temp\\dump.txt")
        self.assertEqual(obj.m_objCLogger, None)

        return

    """----------------------------------------------------------------------"""

if __name__ == '__main__':
    unittest.main()
