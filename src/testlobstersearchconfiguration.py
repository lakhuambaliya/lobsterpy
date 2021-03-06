#This file was originally generated by PyScripter's unitest wizard

import unittest
import lobstersearchconfiguration

class TestCSearchConfiguration(unittest.TestCase):

    def setUp(self):
        """
        Tester Function :-

        Purpose :- performs all the initialization operations prior to each test-case.

        """
        self.m_objCSearchConfig = lobstersearchconfiguration.CSearchConfiguration(
                                                    strSearchKeyword = "Hello", strSearchDirectory = "MyDir",
                                                    bSearchInFavorite = True,
                                                    lsESearchMode = [1, 2], lsEColumns = [1, 3, 5],
                                                    eCondition = 2, xValue1 = 2, xValue2 = 8
                                                    )

        return

    """----------------------------------------------------------------------"""

    def test__init__(self):
        """
        Tester Function :-

        Purpose : - Tests Constructor function of CSearchConfiguration class.

        """
        objCSearchConfig = lobstersearchconfiguration.CSearchConfiguration(
                                                    strSearchKeyword = "Hello", strSearchDirectory = "MyDir",
                                                    bSearchInFavorite = True,
                                                    lsESearchMode = [1, 2], lsEColumns = [1, 3, 5],
                                                    eCondition = 2, xValue1 = 2, xValue2 = 8
                                                    )
        objCSearchConfig = lobstersearchconfiguration.CSearchConfiguration()

        return

    """----------------------------------------------------------------------"""

    def testMSetSearchKeyword(self):
        """
        Tester Function :-

        Purpose : - Tests MSetSearchKeyword() function of CSearchConfiguration class.

        """
        self.m_objCSearchConfig.MSetSearchKeyword(strSearchKeyword = "XStreamDSO")
        self.assertEqual("XStreamDSO", self.m_objCSearchConfig.MGetSearchKeyword())

        return

    """----------------------------------------------------------------------"""

    def testMGetSearchKeyWord(self):
        """
        Tester Function :-

        Purpose : - Tests MGetSearchKeyWord() function of CSearchConfiguration class.

        """
        self.m_objCSearchConfig.MSetSearchKeyword(strSearchKeyword = "")
        self.assertEqual("", self.m_objCSearchConfig.MGetSearchKeyword())

        return

    """----------------------------------------------------------------------"""

    def testMSetSearchDirectory(self):
        """
        Tester Function :-

        Purpose : - Tests MSetSearchDirectory() function of CSearchConfiguration class.

        """
        self.m_objCSearchConfig.MSetSearchDirectory(strSearchDirectory = "MyDir")
        self.assertEqual("MyDir", self.m_objCSearchConfig.MGetSearchDirectory())

        return

    """----------------------------------------------------------------------"""

    def testMGetSearchDirectory(self):
        """
        Tester Function :-

        Purpose : - Tests MGetSearchDirectory() function of CSearchConfiguration class.

        """
        self.m_objCSearchConfig.MSetSearchDirectory(strSearchDirectory = "")
        self.assertEqual("", self.m_objCSearchConfig.MGetSearchDirectory())

        return

    """----------------------------------------------------------------------"""

    def testMSetSearchFromFavorite(self):
        """
        Tester Function :-

        Purpose : - Tests MSetSearchFromFavorite() function of CSearchConfiguration class.

        """
        self.m_objCSearchConfig.MSetSearchFromFavorite(bSearchInFavorite = True)
        self.assertEqual(True, self.m_objCSearchConfig.MGetSearchFromFavorite())

        self.m_objCSearchConfig.MSetSearchFromFavorite(bSearchInFavorite = False)
        self.assertEqual(False, self.m_objCSearchConfig.MGetSearchFromFavorite())

        return

    """----------------------------------------------------------------------"""

    def testMGetSearchFromFavorite(self):
        """
        Tester Function :-

        Purpose : - Tests MGetSearchFromFavorite() function of CSearchConfiguration class.

        """
        self.m_objCSearchConfig.MSetSearchFromFavorite(bSearchInFavorite = True)
        self.assertEqual(True, self.m_objCSearchConfig.MGetSearchFromFavorite())

        self.m_objCSearchConfig.MSetSearchFromFavorite(bSearchInFavorite = False)
        self.assertEqual(False, self.m_objCSearchConfig.MGetSearchFromFavorite())

        return

    """----------------------------------------------------------------------"""

    def testMSetSearchMode(self):
        """
        Tester Function :-

        Purpose : - Tests MSetSearchMode() function of CSearchConfiguration class.

        """
        lsInput = [1,3]
        self.m_objCSearchConfig.MSetSearchMode(lsESearchMode = lsInput)
        lsOutput = self.m_objCSearchConfig.MGetSearchMode()

        for i in range(len(lsInput)):
            self.assertEqual(lsInput[i], lsOutput[i])

        self.assertRaises(Exception, self.m_objCSearchConfig.MSetSearchMode, ([1,3,5]))

        return

    """----------------------------------------------------------------------"""

    def testMGetSearchMode(self):
        """
        Tester Function :-

        Purpose : - Tests MGetSearchMode() function of CSearchConfiguration class.

        """
        lsInput = [1]
        self.m_objCSearchConfig.MSetSearchMode(lsESearchMode = lsInput)
        lsOutput = self.m_objCSearchConfig.MGetSearchMode()

        for i in range(len(lsInput)):
            self.assertEqual(lsInput[i], lsOutput[i])

        return
    """----------------------------------------------------------------------"""

    def testMSetColumnsForSearch(self):
        """
        Tester Function :-

        Purpose : - Tests MSetColumnsForSearch() function of CSearchConfiguration class.

        """
        lsInput = [1, 2, 3, 8, 10]
        self.m_objCSearchConfig.MSetColumnsForSearch(lsEColumns = lsInput)
        lsOutput = self.m_objCSearchConfig.MGetColumnsForSearch()

        for i in range(len(lsInput)):
            self.assertEqual(lsInput[i], lsOutput[i])

        return

    """----------------------------------------------------------------------"""

    def testMGetColumnsForSearch(self):
        """
        Tester Function :-

        Purpose : - Tests MGetColumnsForSearch() function of CSearchConfiguration class.

        """
        lsInput = [2, 5, 3, 6, 8]
        self.m_objCSearchConfig.MSetColumnsForSearch(lsEColumns = lsInput)
        lsOutput = self.m_objCSearchConfig.MGetColumnsForSearch()

        for i in range(len(lsInput)):
            self.assertEqual(lsInput[i], lsOutput[i])

        return

    """----------------------------------------------------------------------"""

    def testMSetCondition(self):
        """
        Tester Function :-

        Purpose : - Tests MSetCondition() function of CSearchConfiguration class.

        """
        eCondition = 3
        self.m_objCSearchConfig.MSetCondition(eCondition)
        self.assertEqual(eCondition, self.m_objCSearchConfig.MGetCondition())

        self.assertRaises(Exception, self.m_objCSearchConfig.MSetCondition, (28))

        return

    """----------------------------------------------------------------------"""

    def testMGetCondition(self):
        """
        Tester Function :-

        Purpose : - Tests MGetCondition() function of CSearchConfiguration class.

        """
        eCondition = 5
        self.m_objCSearchConfig.MSetCondition(eCondition)
        self.assertEqual(eCondition, self.m_objCSearchConfig.MGetCondition())

        self.assertRaises(Exception, self.m_objCSearchConfig.MSetCondition, (100))

        return

    """----------------------------------------------------------------------"""

    def testMSetValue1(self):
        """
        Tester Function :-

        Purpose : - Tests MSetValue1() function of CSearchConfiguration class.

        """
        xValue1 = 3
        self.m_objCSearchConfig.MSetValue1(xValue1)
        self.assertEqual(xValue1, self.m_objCSearchConfig.MGetValue1())

        return

    """----------------------------------------------------------------------"""

    def testMGetValue1(self):
        """
        Tester Function :-

        Purpose : - Tests MGetValue1() function of CSearchConfiguration class.

        """
        xValue1 = 5
        self.m_objCSearchConfig.MSetValue1(xValue1)
        self.assertEqual(xValue1, self.m_objCSearchConfig.MGetValue1())


        return

    """----------------------------------------------------------------------"""

    def testMSetValue2(self):
        """
        Tester Function :-

        Purpose : - Tests MSetValue2() function of CSearchConfiguration class.

        """
        xValue2 = 30.00
        self.m_objCSearchConfig.MSetValue2(xValue2)
        self.assertEqual(xValue2, self.m_objCSearchConfig.MGetValue2())


        return

    """----------------------------------------------------------------------"""

    def testMGetValue2(self):
        """
        Tester Function :-

        Purpose : - Tests MGetValue2() function of CSearchConfiguration class.

        """
        xValue2 = 100.001
        self.m_objCSearchConfig.MSetValue2(xValue2)
        self.assertEqual(xValue2, self.m_objCSearchConfig.MGetValue2())

        return

    """----------------------------------------------------------------------"""

if __name__ == '__main__':
    unittest.main()
