#-------------------------------------------------------------------------------
# Name:        lobsterdatacontext
# Purpose:      This class houses all the data of application, which includes, CVar and CVarDirectory
#               info, Preferences, etc.
#
# Author:      lakhu
#
# Created:     05/02/2014
# Copyright:   (c) Account Prism Pvt. Ltd.
# Licence:     all_rights_reserved
#-------------------------------------------------------------------------------

# imports
import lobstercvar as cvar
import lobsterdirectory as cdirectory
import lobsterbase
import lobsterparser
import lobsterpreferences

# class-name         : CDataContext
# class-description  : This class stores information about Cvars, CVarDirecotories, WatchWindow variables and Preferences
class CDataContext(lobsterbase.CLobsterBase):

    def __init__(
                    self, dictCVarCollection = None, lsStrFavoriteCVars = None,
                    lsStrFrequentDirectories = None, lsStrWatchWindowCVars = None,
                    objCPreferences = None, strCurrentWorkingDirectory = None
                ):

        """
        Constructor :-

        Throws Exception : No

        Inputs :    (i) dictCVarCollection : dictionary type, which contains whole
                                            path of Cvar or CDirectoy as a key and
                                            object of CVar or CDirecoty as value.

                                            eg. dictCVarCollection = {"XStreamDSO.Name" : m_objCVarName}

                                            Note :- This dictionary houses all the cvars and cvardirectories
                                                    in the application.

                    (ii) lsStrFavoriteCVars : list containing string typed favorite cvars

                    (iii) lsStrFrequentDirectories : list containing string typed frequent directories.

                    (iv) lsStrWatchWindowCVars : list of names of CVar with complete path, which are added to
                                                 watch window by the user
                                                 eg. "XStreamDSO.SamplingRate"

                    (v) objCPreferences : object of type CPreferences, which represents the preferences of user.

                    (vi) strCurrentWorkingDirectory : String containing name of current working directory

        Outputs : does not return any values

        Purpose : initializes member variables by received inputs

        """

        lobsterbase.CLobsterBase.__init__(self)

        self.m_dictCVarCollection = {}

        #   reading the list of favorite CVars from the file
        try:
           self.__m_lsStrFavoriteCVars__ = self.MReadFromYaml("favoriteCVars.txt")
        except:
            #   if the file does not have any favorite CVars in it,
            #   then make the list of favorite CVars an empty list
            self.__m_lsStrFavoriteCVars__ = []

        # creating list frequent directories ( contains only ablosute path)
        self.__m_lsStrFrequentDirectories__ = lsStrFrequentDirectories

        #   reading the list of watch window CVars from the file
        try:
            self.__m_lsStrWatchWindowCVars__ = self.MReadFromYaml("watchWindowCVars.txt")
        except:
            #   if the file does not have any watch window CVars in it,
            #   then make the list of watch window CVars an empty list
            self.__m_lsStrWatchWindowCVars__ = []

        try:
            self.__m_objCPreferences__ = self.MReadFromYaml("preferences.txt")
        except:
            self.__m_objCPreferences__ = lobsterpreferences.CPreferences(lsIFilteredColumns = [0, 1, 2, 3, 20])

        # defining searchconfiguration object
        self.__m_objCSearchConfiguration__ = None

        # assigning string containing current directory full name  to member variable
        self.__m_strCurrentWorkingDirectory__ = strCurrentWorkingDirectory

        # This dictionary contains two dictionaries,
        # e.g. self.m_dictSeparated = { "Type" : {   }, "Alphabets" : {   } }
        # Two child seperate dictionaries are maintained, in order to help
        # in reducing search space in the search algorithm
        self.m_dictSeparated = {}

        # if dictCVarCollection is not passed then we need to load data here
        if(dictCVarCollection == None):
            self.MLoad(bReadFromFile = True)

        else:
            self.m_dictCVarCollection = dictCVarCollection

        return

    """----------------------------------------------------------------------"""

    def WriteYaml(self, strFileNameWithExt = None):
        """
        Member Function :-

        Throws Exception : No

        Inputs :    (i) strFileNameWithExt : String containing name with absilute path and extension of file

        Outputs : does not return any values

        Purpose : reading data context object from file

        """
        # defining dictionary for cvars
        self.m_dictCVarCollection = None
        # Writing data context object to file
        self.MWriteYaml("c:\\temp\\datacontext.txt", self)

        return

    """----------------------------------------------------------------------"""

    def MLoad(self, bReadFromFile = True):

        """
        Member Function :-

        Throws Exception : No

        Inputs : (i) bReadFromFile : boolean variable specifies whether application
                                        load data from file or MAUI application

        Outputs : does not return any values

        Purpose : load all cvar from file or MAUI application

        """
        # creating object of lobsterparser, lobsterparser is used for reading and parsing cvars from file
        objCLobsterParser = lobsterparser.CLobsterFileParser("150000lines.txt")

        self.m_dictCVarCollection, self.m_dictSeparated = objCLobsterParser.MGetDictCollection()

        return

    """----------------------------------------------------------------------"""

    def MSetFavoriteCVars(self, lsStrFavoriteCVars):

        """
        Member Method :-

        Throws Exception :- No

        Inputs :- (i) lsStrFavoriteCVars :- list of strings containing the
                                            absolute path of the favorite CVars

        Outputs :- does not return any value

        Purpose :- This method sets the list of favorite CVars

        """

        self.__m_lsStrFavoriteCVars__ = lsStrFavoriteCVars

        return

    """----------------------------------------------------------------------"""

    def MGetFavoriteCVars(self):

        """
        Member Method :-

        Throws Exception :- No

        Inputs :- does not receive any inputs

        Outputs :- (i)self.__m_lsStrFavoriteCVars__ :- list of strings
                                                       containing the
                                                       absolute path of the
                                                       favorite CVars

        Purpose :- This method returns the list of favorite CVars

        """

        return self.__m_lsStrFavoriteCVars__

    """----------------------------------------------------------------------"""

    def MSetFrequentDirectories(self, lsStrFrequentDirectories):

        """
        Member Method :-

        Throws Exception :- No

        Inputs :- (i) lsStrFrequentDirectories :- list of strings containing the
                                            absolute path of the frequent directories

        Outputs :- does not return any value

        Purpose :- This method sets the list of favorite CVars

        """

        self.__m_lsStrFrequentDirectories__ = lsStrFrequentDirectories

    """----------------------------------------------------------------------"""

    def MGetFrequentDirectories(self):

        """
        Member Method :-

        Throws Exception :- No

        Inputs :- does not receive any inputs

        Outputs :- (i)self.__m_lsStrFrequentDirectories__ :- list of strings
                                                       containing the
                                                       absolute path of the
                                                       frequent directories

        Purpose :- This method returns the list of favorite CVars

        """

        return self.__m_lsStrFrequentDirectories__

    """----------------------------------------------------------------------"""

    def MIsDirectory(self, strCVarDirNameWithCompletePath = None):

        """
        Member Function :-

        Throws Exception : No

        Inputs : (i) strCVarDirNameWithCompletePath : String containing path of CVar or CDirectory

        Outputs : return True if strCVarDirNameWithCompletePath is of type CVarDirectory,
                    else returns False.

        Purpose : checking whether CVarDirectory name passed as argument, is CVarDirectory or not.

        """

        bIsDirectory = False
        # fetching object from m_dictCVarCollection
        obj = self.m_dictCVarCollection.get(strCVarDirNameWithCompletePath)
        # Checkeing whether fetched object is of type CCVarDirectory or not
        if(isinstance(obj, cdirectory.CCVarDirectory)):
            bIsDirectory = True

        return bIsDirectory

    """----------------------------------------------------------------------"""

    def MIsCVar(self, strCVarNameWithCompletePath = None):

        """
        Member Function :-

        Throws Exception : No

        Inputs : (i) strCVarNameWithCompletePath : String containing path of CVar or CDirectory

        Outputs : return true if strCVarNameWithCompletePath is of type CVar,
                    otherwise returns False.

        Purpose : checking whether CVarName passed as argument is of CVar type or not.

        """

        bIsCVar = False
        # fetching object from m_dictCVarCollection
        obj = self.m_dictCVarCollection.get(strCVarNameWithCompletePath)
        # Checkeing whether fetched object is of type CVar or not
        if(isinstance(obj, cvar.CVar)):
            bIsCVar = True

        return bIsCVar

    """----------------------------------------------------------------------"""

    def MGetPreferences(self):

        """
        Member Function :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : (i) __m_objCPreferences__ : return CPreferences object contains preferences of user

        Purpose : return preference which is set by user

        """

        return self.__m_objCPreferences__

    """----------------------------------------------------------------------"""

    def MSetPreferences(self, objCPreferences):

        """
        Member Function :-

        Throws Exception : No

        Inputs : (i) objCPreferences : CPreferences object, set by user

        Outputs : does not return any values

        Purpose : assign preferences to member variable by input parameter

        """

        self.__m_objCPreferences__ = objCPreferences

        return

    """----------------------------------------------------------------------"""

    def MGetWatchWindowCVars(self):

        """
        Member Function :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : (i) __m_lsStrWatchWindowCVars__ : list watch window variables

        Purpose : return list of watch window variables

        """

        return self.__m_lsStrWatchWindowCVars__

    """----------------------------------------------------------------------"""

    def MSetWatchWindowCVars(self, lsStrWatchWindowCVars):

        """
        Member Function :-

        Throws Exception : No

        Inputs : (i) lsStrWatchWindowCVars : specifies list of watch window variable as a string

        Outputs : does not return any value

        Purpose : assign list of watch window variable to member variable

        """

        self.__m_lsStrWatchWindowCVars__ = lsStrWatchWindowCVars

        return

    """----------------------------------------------------------------------"""

    def __del__(self):

        """
        Destructor :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : does not return any values

        Purpose : releases memory allocated for member variables

        """

        self.m_dictCVarCollection = None
        self.__m_lsStrWatchWindowCVars__ = None
        self.__m_objCPreferences__ = None
        self.__m_strCurrentWorkingDirectory__ = None
        self.__m_lsStrFavoriteCVars__ = None
        self.__m_lsStrFrequentDirectories__ = None

        return

    """----------------------------------------------------------------------"""

    @staticmethod
    def MSTestCDataContext():

        """
        Tester Function :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : does not return any values

        Purpose : Testing multiple functions of CDataContext

        """

        # defining dictionary, which contains cvars and directories
        dictCVarCollection = {}

        # Creating object of CVar
        objCVar1 = cvar.CVar(
                        strParentWithPath = "XStreamDSO.ScopeIdentify",
                        strCVarName = "SimHSTrigVersion", eCVarType = cvar.CVar.mC_INTEGER, xRequestedValue = 0, xAdaptedValue = 0,
                        xDefaultValue = 0, xMinValue = 0, xMaxValue = 255, xGrainValue = 1, strCVarUnit = "", lsECVarFlags = [cvar.CVar.mC_G]
                        )

        # fetching absolute path
        strCVarAbsolutePath = objCVar1.MGetCVarAbsolutePath()
        # adding item into dictionay
        dictCVarCollection[strCVarAbsolutePath] = objCVar1

        # Creating object of CVar
        objCVar2 = cvar.CVar(
                        strParentWithPath = "XStreamDSO.ExecutivesCollection.ScanHisto.Histogram", strCVarName = "ValuesBeforeFindScale",
                        eCVarType = cvar.CVar.mC_INTEGER, xRequestedValue = 100, xAdaptedValue = 100, xDefaultValue = 100, xMinValue = 20, xMaxValue = 20000,
                        xGrainValue = 1, strCVarUnit = "", lsECVarFlags = [cvar.CVar.mC_H]
                        )
        # fetching absolute path
        strCVarAbsolutePath = objCVar2.MGetCVarAbsolutePath()
        # adding item into dictionay
        dictCVarCollection[strCVarAbsolutePath] = objCVar2

        # Creating object of CVar
        objCVar3 = cvar.CVar(
                        strParentWithPath = "XStreamDSO", strCVarName = "Name",
                        eCVarType = cvar.CVar.mC_NAME, xRequestedValue = "XStreamDSO|XStreamDSO|XSTREAMDSO", xAdaptedValue = "XStreamDSO|XStreamDSO|XSTREAMDSO",
                         xDefaultValue = "XStreamDSO|XStreamDSO|XSTREAMDSO", iCVarMaxLen = -1, lsECVarFlags = [cvar.CVar.mC_H]
                        )
        # fetching absolute path
        strCVarAbsolutePath = objCVar3.MGetCVarAbsolutePath()
        # adding item into dictionay
        dictCVarCollection[strCVarAbsolutePath] = objCVar3

        # creating object of CVarDirectory
        objCVarDirectory = cdirectory.CCVarDirectory(
                                                    strNodeName = "Simulator", lsStrChildDirectories = ["Channels.C4"],
                                                    strParentDirectoryName = "XStreamDSO.InternalCollection.Acquisition.Simulator",
                                                    lsStrChildCVars = ["Mfe670BGainOffsetCurve"]
                                                    )
        # fetching absolute path
        strCVarAbsolutePath = objCVarDirectory.MGetAbsolutePath()

        # adding item into dictionay
        dictCVarCollection[strCVarAbsolutePath] = objCVarDirectory

        # creating object of CDataContext
        objCDataContext = CDataContext()
        print objCDataContext.m_dictCVarCollection

        return

    """----------------------------------------------------------------------"""

if __name__ == '__main__':
    CDataContext.MSTestCDataContext()