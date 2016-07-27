#-------------------------------------------------------------------------------
# Name:        lobsterconfiguration.py
# Purpose:     This module contains CSearchConfiguration class, which will contain
#              all the information related to a one instance of search operation.
#
# Author:      lakhu
#
# Created:     24/03/2014
# Copyright:   (c) Account Prism Pvt. Ltd.
# Licence:     all_rights_reserved
#-------------------------------------------------------------------------------


# imports
import lobstercvar

# class-name : CSearchConfiguration
# class-description : contains all information about one instance of search operation
class CSearchConfiguration:
    mC_MATCH_CASE = 0               #   constant specifying that search is case-sensitive
    mC_MATCH_WHOLE_WORD = 1         #   constant specifying that search must look for complete words
    mC_REG_EXPR = 2                 #   constant specifying that search keyword contains regular expression

    #   list containing valid search modes
    mC_LS_SEARCH_MODE = [mC_MATCH_CASE, mC_MATCH_WHOLE_WORD, mC_REG_EXPR]

    mC_ROOT_DIR = 0
    mC_CURRENT_DIR = 1
    mC_CURRENT_WITH_NESTED = 2
    mC_FAVORITE = 3

    mC_LS_SEARCH_DIR = [mC_ROOT_DIR, mC_CURRENT_DIR, mC_CURRENT_WITH_NESTED, mC_FAVORITE]

    mC_EQ = 0                       #   constant for equality condition
    mC_NE = 1                       #   constant for non-equality condition
    mC_LT = 2                       #   constant for less-than condition
    mC_GT = 3                       #   constant for greater than condition
    mC_LE = 4                       #   constant for less than or equal to condition
    mC_GE = 5                       #   constant for greater than or equal to condition
    mC_BETWEEN = 6                  #   constant for between condition

    #   list containing valid conditions
    mC_LS_CONDITIONS = [mC_EQ, mC_NE, mC_LT, mC_GT, mC_LE, mC_GE, mC_BETWEEN]

    #   list containing string representation of valid conditions
    mC_LS_STR_CONDITIONS = ["EQ", "NE", "LT", "GT", "LE", "GE", "BETWEEN"]

    def __init__(
                    self, strSearchKeyword = "", strSearchDirectory = "", eSearchDir = mC_CURRENT_WITH_NESTED,
                    lsESearchMode = [], dictFilterCVars = {}
                ):
        """
        Constructor :-

        Throws Exception : No

        Inputs :    (i) strSearchKeyword    : String containing search keyword

                    (ii) strSearchDirectory : String containing directory name in which user want to search

                    (iii) lsESearchMode      : list enum values indicating user want to search in which mode
                                                (match case, match whole word, or regular expression)
                    (vi) dictFilters         : dictionary contains information about filtering cvars value.


        Outputs : does not return any values

        Purpose : initializing member variables by receiving inputs.

        """
        self.m_strSearchKeyword = strSearchKeyword
        self.m_strSearchDirectory = strSearchDirectory
        self.m_lsESearchMode = lsESearchMode
        self.m_dictFilterCVars = dictFilterCVars
        self.m_eSearchDir = eSearchDir

        return

    """----------------------------------------------------------------------"""

    def MSetSearchKeyword(self, strSearchKeyword):
        """
        Member Function :

        Throws Exception : No

        Inputs : (i) strSearchKeyword : String representing search keyword

        Outputs : does not return any values

        Purpose : assigning value to member varibles by receiving inputs

        """
        self.m_strSearchKeyword = strSearchKeyword

        return

    """----------------------------------------------------------------------"""

    def MGetSearchKeyword(self):
        """
        Member Function :-

        Throws Exception : No

        Inputs : doen not receive any inputs

        Outputs : (i) self.m_strSearchKeyword : return string containing search keyword

        Purpose : getting value of search keyword

        """

        return self.m_strSearchKeyword

    """----------------------------------------------------------------------"""

    def MSetSearchDirectory(self, strSearchDirectory):
        """
        Member Function :-

        Throws Exception : No

        Inputs : (i) strSearchDirectory : string containing directory name in which user want to serch

        Outputs : does not return any values

        Purpose : assigning value to member variables

        """
        self.m_strSearchDirectory = strSearchDirectory

        return

    """----------------------------------------------------------------------"""

    def MGetSearchDirectory(self):
        """
        Member Function :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : (i) self.m_strSearchDirectory : return String containing direcoty name

        Purpose : return string containing directory name
        """

        return self.m_strSearchDirectory

    """----------------------------------------------------------------------"""
    def MSetSearchMode(self, lsESearchMode):
        """
        Member Function :-

        Throws Exception : yes when, (i) input search mode is invalid.

        Inputs : (i) lsESearchMode : list of constant representing search mode (Match case, match whole word, reg expr)

        Outputs : does not return any values

        Purpose : set the value of member variable by received inouts

        """
        if (len(lsESearchMode) != 0):
            for eMode in lsESearchMode:
                if(eMode not in CSearchConfiguration.mC_LS_SEARCH_MODE):
                    raise Exception("lobstersearchconfigurations : input mode is not in list of valid modes")

        self.m_lsESearchMode = lsESearchMode

        return

    """----------------------------------------------------------------------"""

    def MGetSearchMode(self):
        """
        Member Function :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : (i)self.m_lsESearchMode : return list of integer constant indicating search mode (match case, match whole word)

        Purpose : return search mode

        """

        return self.m_lsESearchMode

    """----------------------------------------------------------------------"""

    def MPrintCSearchConfigDetail(self):
        """
        Member Function :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : does not return any values

        Purpose : Print the value of each member variable

        """
        print "Search Keyword = " + str(self.MGetSearchKeyword())
        print "Search Mode = " + str(self.MGetSearchMode())
        print "Search Directory = " + str(self.MGetSearchDirectory())
        return

    """----------------------------------------------------------------------"""

if __name__ == '__main__':
    objCSearchConfiguration = CSearchConfiguration(
                                                    strSearchKeyword = "Hello", strSearchDirectory = "MyDir",
                                                    bSearchInFavorite = False,
                                                    lsESearchMode = [1, 2], lsEColumns = [1, 3, 5],
                                                    eCondition = CSearchConfiguration.mC_BETWEEN, xValue1 = 2, xValue2 = 8
                                                    )
    objCSearchConfiguration.MPrintCSearchConfigDetail()