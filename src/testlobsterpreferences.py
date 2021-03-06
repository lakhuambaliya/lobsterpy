#This file was originally generated by PyScripter's unitest wizard

import unittest
import lobsterpreferences

class TestCPreferences(unittest.TestCase):

    def setUp(self):
        """
        Tester Function :-

        Purpose :- performs all the initialization operations prior to each test-case.

        """
        self.m_objPref = lobsterpreferences.CPreferences(
                                        eAppMode = 1, eNumericNotation = 0,
                                         iWatchWindowRefreshTime = 12, iSearchHistorySize = 0 ,
                                         lsIFilteredColumns = [2, 4], lsEPlots = [3] )

        return

    """----------------------------------------------------------------------"""
    def tearDown(self):

        """
        Deallocates the memory of the member variables

        """

        self.m_objPref = None

        return

    """----------------------------------------------------------------------"""
    def test__init__(self):
        """
        Tester Function :-

        Purpose : - Tests Constructor function of CPreferences class.

        """

        self.m_objPref = lobsterpreferences.CPreferences(
                                        eAppMode = 1, eNumericNotation = 0,
                                         iWatchWindowRefreshTime = 12, iSearchHistorySize = 0 ,
                                         lsIFilteredColumns = [2, 4], lsEPlots = [3] )


        self.m_objPref = lobsterpreferences.CPreferences()

        return

    """----------------------------------------------------------------------"""

    def testMSetAppMode(self):
        """
        Tester Function :-

        Purpose : - Tests MSetAppMode() function of CPreferences class.

        """
        self.m_objPref.MSetAppMode(eAppMode = lobsterpreferences.CPreferences.mC_STANDARD_APPMODE)
        self.assertEqual(lobsterpreferences.CPreferences.mC_STANDARD_APPMODE, self.m_objPref.MGetAppMode())

        self.m_objPref.MSetAppMode(eAppMode = lobsterpreferences.CPreferences.mC_FREQUENT_APPMODE)
        self.assertEqual(lobsterpreferences.CPreferences.mC_FREQUENT_APPMODE, self.m_objPref.MGetAppMode())

        #   expecting exception to be raised as 23 is not a valid application
        self.assertRaises(Exception, self.m_objPref.MSetAppMode, 23)

        return

    """----------------------------------------------------------------------"""

    def testMGetAppMode(self):
        """
        Tester Function :-

        Purpose : - Tests MGetAppMode() function of CPreferences class.

        """
        self.m_objPref.MSetAppMode(eAppMode = lobsterpreferences.CPreferences.mC_STANDARD_APPMODE)
        self.assertEqual(lobsterpreferences.CPreferences.mC_STANDARD_APPMODE, self.m_objPref.MGetAppMode())

        self.m_objPref.MSetAppMode(eAppMode = lobsterpreferences.CPreferences.mC_FREQUENT_APPMODE)
        self.assertEqual(lobsterpreferences.CPreferences.mC_FREQUENT_APPMODE, self.m_objPref.MGetAppMode())

        return

    """----------------------------------------------------------------------"""

    def testMSetNumericNotation(self):
        """
        Tester Function :-

        Purpose : - Tests MSetNumericNotation() function of CPreferences class.

        """
        self.m_objPref.MSetNumericNotation(eNotation = lobsterpreferences.CPreferences.mC_STANDARD_NOTATION)
        self.assertEqual(lobsterpreferences.CPreferences.mC_STANDARD_NOTATION, self.m_objPref.MGetNumericNotation())

        self.m_objPref.MSetNumericNotation(eNotation = lobsterpreferences.CPreferences.mC_ENGINEERING_NOTATION)
        self.assertEqual(lobsterpreferences.CPreferences.mC_ENGINEERING_NOTATION, self.m_objPref.MGetNumericNotation())

        #   Expecting exception to be raised, as 23 is not a valid numericnotation
        #   option
        self.assertRaises(Exception, self.m_objPref.MSetNumericNotation, 23)

        return

    """----------------------------------------------------------------------"""

    def testMGetNumericNotation(self):
        """
        Tester Function :-

        Purpose : - Tests MGetNumericNotation() function of CPreferences class.

        """
        self.m_objPref.MSetNumericNotation(eNotation = lobsterpreferences.CPreferences.mC_STANDARD_NOTATION)
        self.assertEqual(lobsterpreferences.CPreferences.mC_STANDARD_NOTATION, self.m_objPref.MGetNumericNotation())

        self.m_objPref.MSetNumericNotation(eNotation = lobsterpreferences.CPreferences.mC_ENGINEERING_NOTATION)
        self.assertEqual(lobsterpreferences.CPreferences.mC_ENGINEERING_NOTATION, self.m_objPref.MGetNumericNotation())

        return

    """----------------------------------------------------------------------"""

    def testMGetHistorySize(self):
        """
        Tester Function :-

        Purpose : - Tests MGetHistorySize() function of CPreferences class.

        """
        self.m_objPref.MSetHistorySize(iSearchHistorySize = 1)
        self.assertEqual(1, self.m_objPref.MGetHistorySize())

        self.m_objPref.MSetHistorySize(iSearchHistorySize = 10)
        self.assertEqual(10, self.m_objPref.MGetHistorySize())

        #   expecting exception to be raised, as history size can not be negative
        self.assertRaises(Exception, self.m_objPref.MSetHistorySize, -12)

        return

    """----------------------------------------------------------------------"""

    def MGetHistorySize(self):
        """
        Tester Function :-

        Purpose : - Tests MGetRememberNumberOfSearched() function of CPreferences class.

        """
        self.m_objPref.MSetHistorySize(iSearchHistorySize = 1)
        self.assertEqual(1, self.m_objPref.MGetHistorySize())

        self.m_objPref.MSetHistorySize(iSearchHistorySize = 10)
        self.assertEqual(10, self.m_objPref.MGetHistorySize())

        return

    """----------------------------------------------------------------------"""

    def testMSetWatchWindowRefreshTime(self):
        """
        Tester Function :-

        Purpose: - Tests MSetWatchWindowRefreshTime() function of CPreferences class.

        """
        self.m_objPref.MSetWatchWindowRefreshTime(iWatchWindowRefreshTime = 12)
        self.assertEqual(12, self.m_objPref.MGetWatchWindowRefreshTime())

        self.m_objPref.MSetWatchWindowRefreshTime(iWatchWindowRefreshTime = 72)
        self.assertEqual(72, self.m_objPref.MGetWatchWindowRefreshTime())

        #   expecting exception to be raised, as watch window refresh time
        #   can not be negative
        self.assertRaises(Exception, self.m_objPref.MSetWatchWindowRefreshTime, -12)

        return

    """----------------------------------------------------------------------"""

    def testMGetWatchWindowRefreshTime(self):
        """

        Tester Function :-

        Purpose : - Tests MGetWatchWindowRefreshTime() function of CPreferences class.

        """
        self.m_objPref.MSetWatchWindowRefreshTime(iWatchWindowRefreshTime = 12)
        self.assertEqual(12, self.m_objPref.MGetWatchWindowRefreshTime())

        self.m_objPref.MSetWatchWindowRefreshTime(iWatchWindowRefreshTime = 72)
        self.assertEqual(72, self.m_objPref.MGetWatchWindowRefreshTime())

        return

    """----------------------------------------------------------------------"""

    def testMSetFilteredColumns(self):
        """
        Tester Function :-

        Purpose : - Tests MSetFilteredColumns() function of CPreferences class.

        """
        lsInput = [2, 4, 5, 6, 10]
        self.m_objPref.MSetFilteredColumns(lsIFilteredColumns = lsInput)
        lsOutput = self.m_objPref.MGetFilteredColumns()

        # iterating each element of input list and compare with each element of output list
        for iColumnIndex in range(len(lsInput)):
            iInput = lsInput[iColumnIndex]
            iOutput = lsOutput[iColumnIndex]
            self.assertEqual(iInput, iOutput)

        self.assertRaises(Exception, self.m_objPref.MSetFilteredColumns, None)

        return

    """----------------------------------------------------------------------"""

    def testMGetFilteredColumns(self):
        """
        Tester Function :-

        Purpose : - Tests MGetFilteredColumns() function of CPreferences class.

        """
        lsInput = [3, 5, 8, 9]
        self.m_objPref.MSetFilteredColumns(lsIFilteredColumns = lsInput)
        lsOutput = self.m_objPref.MGetFilteredColumns()

        # iterating each element of input list and compare with each element of output list
        for iColumnIndex in range(len(lsInput)):
            iInput = lsInput[iColumnIndex]
            iOutput = lsOutput[iColumnIndex]
            self.assertEqual(iInput, iOutput)

        return

    """----------------------------------------------------------------------"""

    def testMSetPlots(self):
        """
        Tester Function :-

        Purpose : - Tests MSetPlots() function of CPreferences class.

        """
        lsInput = [0, 1]

        self.m_objPref.MSetPlots(lsEPlots = lsInput)
        lsOutput = self.m_objPref.MGetPlots()
        # iterating each element of input list and compare with each element of output list
        for iColumnIndex in range(len(lsInput)):
            iInput = lsInput[iColumnIndex]
            iOutput = lsOutput[iColumnIndex]
            self.assertEqual(iInput, iOutput)

        self.assertRaises(Exception, self.m_objPref.MSetPlots, [2, 34])

        return

    """----------------------------------------------------------------------"""

    def testMGetPlots(self):
        """
        Tester Function :-

        Purpose : - Tests MGetPlots() function of CPreferences class.

        """
        lsInput = [False, True, True]

        self.m_objPref.MSetPlots(lsEPlots = lsInput)
        lsOutput = self.m_objPref.MGetPlots()
        # iterating each element of input list and compare with each element of output list
        for iColumnIndex in range(len(lsInput)):
            iInput = lsInput[iColumnIndex]
            iOutput = lsOutput[iColumnIndex]
            self.assertEqual(iInput, iOutput)

        return

    """----------------------------------------------------------------------"""
    def testMSetCopyPref(self):
        """
        Tester Function :-

        Purpose : - Tests MSetCopyPref() function of CPreferences class.

        """
        lsECopyPref = [1, 2, 3]

        self.m_objPref.MSetCopyPref(lsECopyPref)
        lsOutput = self.m_objPref.MGetCopyPref()
        # iterating each element of input list and compare with each element of output list
        for iColumnIndex in range(len(lsECopyPref)):
            iInput = lsECopyPref[iColumnIndex]
            iOutput = lsOutput[iColumnIndex]
            self.assertEqual(iInput, iOutput)

        return

    """----------------------------------------------------------------------"""
    def testMGetCopyPref(self):
        """
        Tester Function :-

        Purpose : - Tests MSetCopyPref() function of CPreferences class.

        """
        lsECopyPref = [6, 8, 9, 0]

        self.m_objPref.MSetCopyPref(lsECopyPref)
        lsOutput = self.m_objPref.MGetCopyPref()
        # iterating each element of input list and compare with each element of output list
        for iColumnIndex in range(len(lsECopyPref)):
            iInput = lsECopyPref[iColumnIndex]
            iOutput = lsOutput[iColumnIndex]
            self.assertEqual(iInput, iOutput)

        return

    """----------------------------------------------------------------------"""

if __name__ == '__main__':
    unittest.main()
