#-------------------------------------------------------------------------------
# Name:        lobstercvar.py
# Purpose:     This class stores information about individual CVar
#
# Author:      lakhu
#
# Created:     04/02/2014
# Copyright:   (c) Account Prism Pvt. Ltd.
# Licence:     all_rights_reserved
#-------------------------------------------------------------------------------

# imports
import re
import mylogmanager
import lobsterbase
import mywxlistitem as item

# class-name        : CVar
# class-description : Stores information about individual Cvars
class CVar(item.IListItem):

    #Static constant member representing type of CVar
    mC_ACTION = 0                   # representing Action type CVar
    mC_BIT_PATTERN = 1
    mC_BOOL = 2
    mC_COLOR = 3                    # representing Bool type CVar
    mC_DOUBLE = 4                   # representing Double type CVar
    mC_DOUBLE_LOCK_STEP = 5         # representing DoubleLockStep type CVar
    mC_ENUM = 6
    mC_FILENAME = 7                 # representing Enum type CVar
    mC_IMAGE = 8
    mC_INTEGER = 9                  # representing Integer type CVar
    mC_LONG_INTEGER = 10
    mC_NAME = 11                    # representing Name type CVar
    mC_NOTIMPLE = 12                # representing Image type cvar
    mC_REGISTER = 13
    mC_SAFEARRAY = 14               # representing SafeArray type cvar
    mC_STRING = 15                  # representing String type CVar


    #Static constant member reprenting flags of CVar
    #   TODO :- Full names representing flags are not mentioned here
    #           in comments. They'll be menitioned, once they are
    #           read and deciphered from lobster vc++ project

    mC_NO_FLAG = 0          # representing No flags
    mC_R = 1                # representing Read only
    mC_H = 2                # representing Hidden only
    mC_L = 3                #
    mC_G = 4                # representing GUI flag
    mC_Y = 5                # representing Grayed
    mC_A = 6
    mC_N = 7
    mC_D = 8
    mC_P = 9
    mC_S = 10
    mC_B = 11
    mC_N = 12
    mC_W = 13
    mC_U = 14
    mC_V = 15
    mC_M = 16

    # static object of logger class. It'll be used as a logger object for all the cvars
    # throughout the application.
    ms_objCLogger = mylogmanager.CLogger(
                                            "c:\\temp\\temp.txt",
                                            iBufSize = 0,
                                            eLogMode = mylogmanager.CLogger.mC_FILELOG,
                                            eLogLimit = mylogmanager.CLogger.mC_LOGMSGBASEDLIMIT,
                                            iLogLimitAmount = 30
                                        )

     # Setting Header of ListView. Here, we're setting all the attributes,
     # associated with all the types of cvar, as listview's  column headers
    ms_lsStrHeaders = [
                        "Name", "Type", "Flags", "Requested", "Adapted",
                        "Default", "MaxLen", "Range", "Min", "Max", "Grain",
                        "Unit", "Width", "Height", "Bits", "Root", "Filters",
                        "Path", "NbOfBits", "HardwareAddress", "AbsolutePath"
                    ]

    # list containing possible different types of cvars
    ms_lsStrTypes = [
                        "Action", "BitPattern", "Bool", "Color", "Double",
                        "DoubleLockstep", "Enum", "FileName", "Image",
                        "Integer", "Long Integer", "Name", "notimpl",
                        "Register" , "SafeArray", "String"
                    ]

    # dictionary containing character as a key and value will be integer
    # eg. {"R" : 0, "H" : 1}
    ms_dictECVarFlags = {
                            "-" : mC_NO_FLAG, "" : mC_NO_FLAG, "R" : mC_R,
                            "H" : mC_H, "L" : mC_L, "G" : mC_G, "Y" : mC_Y,
                            "A" : mC_A, "N" : mC_N, "D" : mC_D, "P" : mC_P,
                            "S" : mC_S, "B" : mC_B, "N" : mC_N, "W" : mC_W,
                            "U" : mC_U, "V" : mC_V, "M" : mC_M
                        }

    # list containing multiple flags.
    ms_lsStrFlags = [
                        "", "R", "H", "L", "G", "Y", "A", "N",
                        "D", "P", "S", "B", "N", "W", "U", "V", "M"
                    ]

    #   list containing numeric cvar types
    ms_lsENumericTypes = [mC_INTEGER, mC_LONG_INTEGER, mC_DOUBLE, mC_DOUBLE_LOCK_STEP]
    #   list containing non-numeric cvar types
    ms_lsENonNumericTypes = [
                                mC_ACTION, mC_BIT_PATTERN, mC_BOOL, mC_COLOR,
                                mC_ENUM, mC_FILENAME, mC_IMAGE, mC_NAME,
                                mC_NOTIMPLE, mC_REGISTER, mC_SAFEARRAY, mC_STRING
                            ]

    def __init__(self, dictCVarAttributeAndValue = {}):

        """
        Constructor :-

        Throws Exception : No

        Inputs  :   (i) dictCVarAttributeAndValue : dictionary containing cvars attribute as a key
                                                    and atrributes value as a value
                                                    eg. {"AbsolutePath" :"XStreamDSO.Name", "Type" : "String"}

        Outputs : does not return any values.

        Purpose : initialize member variables by input parameters.

        """

        # Converting Types Value into Enum int
        # eg. if type is"String" then enum value will be 0
        strCVarType = dictCVarAttributeAndValue.get("Type")

        # raise exception if type is not valid
        if ((strCVarType == None) or (strCVarType not in CVar.ms_lsStrTypes)):
            raise Exception("CVar.py : Type is not available in list of valid types")

        eCVarType = CVar.ms_lsStrTypes.index(strCVarType)
        # setting type information
        dictCVarAttributeAndValue["Type"] = eCVarType

        # Converting flags from string to int
        # for example flag is "H" then it is converted into 2
        lsECVarFlags = []
        strCVarFlags = dictCVarAttributeAndValue.get("Flags")

        # raise exception if flag is not valis
        if (strCVarFlags == None):
            raise Exception("lobstercvar.py : flag is not available in valid list of flags")

        #   removing the whitespaces before and after the flags string
        strCVarFlags = strCVarFlags.strip()

        #   iterating through each Flag character
        for strFlag in strCVarFlags:
            #   if strFlag is '-', then converting it to "",
            #   as '-' and "" are same flags.
            if(strFlag == "-"):
                strFlag=""

            #   getting the integer representation of flag
            iFlag = CVar.ms_dictECVarFlags.get(strFlag)

            #   raising error, when integer representation for the flag couldn't be
            #   found.
            if iFlag == None:
                raise Exception("lobstercvar.py :- Invalid flag None for cvar" + dictCVarAttributeAndValue["Name"])

            lsECVarFlags.append(iFlag)

        #   setting flags
        dictCVarAttributeAndValue["Flags"] = lsECVarFlags

        # converting maxlen from string to int
        strMaxLen = dictCVarAttributeAndValue.get("MaxLen")
        #   if maxlen attribute's value is not None, then
        #   setting that attribute's value for cvar
        if (strMaxLen != None):
            iMaxLen = int(strMaxLen)
            dictCVarAttributeAndValue["MaxLen"] = iMaxLen

        # if MaxLength attribute is not None, then setting
        # that attribute's value for cvar.
        strMaxLen = dictCVarAttributeAndValue.get("MaxLength")
        if (strMaxLen != None):
            iMaxLen = int(strMaxLen)
            dictCVarAttributeAndValue["MaxLen"] = iMaxLen

        """
        ---------------------  Note  ----------------------
        FileName type of cvar have attribute "MaxLength", while
        String, Name, and Bits have attribute MaxLen. In Listview,
        the values for both these attributes for respective cvar is
        shown under 'MaxLen' header. So, for that purpose, in the
        dictionary we are maintaining only one key "MaxLen" for
        both attributes for the respective type of cvar.
        ---------------------------------------------------
        """

        # fetching name from absolute path and add into dictionary
        strAbsolutePath = dictCVarAttributeAndValue.get("AbsolutePath")

        # raise exception if absolute path is not aavailable
        if (strAbsolutePath == None or len(strAbsolutePath) <= 0):
            raise Exception("lobstercvar.py : absolute path is not available")

        #   getting parent and child values from the absolutepath
        lsStrTokensOfPath = re.split("\.", strAbsolutePath)
        strCVarName = lsStrTokensOfPath[-1]
        dictCVarAttributeAndValue["Name"] = strCVarName

        # calling parent constructor
        item.IListItem.__init__(self, dictListItemInfo = dictCVarAttributeAndValue, objCLogger = CVar.ms_objCLogger)

        return

    """----------------------------------------------------------------------"""

    def __getitem__(self, iIndex):
        """
        Member Method :-

        Inputs :- (i)   iIndex :- integer value representing index of the attribute
                                  of cvar whose value is required to be accessed

        Outputs :- returns the value of the attribute of cvar, whose index is passed
                   as argument.

        Purpose :- This method method makes cvar object as one type of sequence, which
                   can be queried for values, by passing the index. It's used in listview
                   sorting.
        """
        #   getting the header for the index passed
        strKey = CVar.ms_lsStrHeaders[iIndex]
        #   getting the dictionary of values associated with cvar
        dictionary = self.MGetItems()
        #   getting the value for the key from the dictionary
        strValue = dictionary.get(strKey)
        #   in case of 'Flags' as key, converting
        #   the list of integers to list of string
        #   and returning that string
        if(strKey == "Flags"):
            lsFlag = dictionary.get("Flags")
            strValue = ""
            #   iterating through the list
            for iFlag in lsFlag:
                #   concate the related values of the list in a string
                strValue += CVar.ms_lsStrFlags[iFlag]

        return  strValue if dictionary.get(strKey) != None else " "

    """----------------------------------------------------------------------"""

    def MGetCVarName(self):

        """
        Member Function :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : (i) strCVarName : return name of CVar as a String, eg. "MyCVar"

        Purpose : return value as a string, specifies name of CVar

        """

        strCVarName = self.__m_dictListItemInfo__.get("Name")

        return strCVarName

    """----------------------------------------------------------------------"""

    def MGetCVarType(self):

        """
        Member Function :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : (i) self.m_dictListItemInfo.get("Type") : return type of CVar as integer constant,
                                                            which will be the member of enum for constants,
                                                            defined in this class.

        Purpose : return enum type value specifies type of CVar

        """

        return self.__m_dictListItemInfo__.get("Type")

    """----------------------------------------------------------------------"""

    def MSetCVarType(self, eCVarType):

        """
        Member Function :-

        Throws Exception : No

        Inputs :  (i) eCVarType : enum type input specifies type of CVar

        Outputs : does not return any values

        Purpose : assign value to member variable by input parameter

        """

        self.__m_dictListItemInfo__["Type"] = eCVarType

        return

    """---------------------------------------------------------------------"""

    def MGetCVarRequestedValue(self):

        """
        Member Function :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : (i) self.m_dictListItemInfo.get("Requested") : return requested value of CVar
                                                                 (type will be decide at runtime)

        Purpose : return requested value of CVar

        """

        return self.__m_dictListItemInfo__.get("Requested")

    """----------------------------------------------------------------------"""

    def MSetCVarRequestedValue(self, xRequestedValue):

        """
        Member Function :-

        Throws Exception : No

        Inputs : (i) xRequestedValue : specifies requested value of CVar
                                            (type will be decide at runtime)

        Outputs : does not return any values

        Purpose : assign value to member variable by input parameter

        """

        self.__m_dictListItemInfo__["Requested"] = xRequestedValue

        return

    """----------------------------------------------------------------------"""

    def MGetCVarAdaptedValue(self):

        """
        Member Function :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : (i) self.m_dictListItemInfo.get("Adapted") : return adapted value of CVar
                                            (type will be decide at runtime)

        Purpose : return adapted value of CVar

        """

        return self.__m_dictListItemInfo__.get("Adapted")

    """----------------------------------------------------------------------"""

    def MSetCVarAdaptedValue(self, xAdaptedValue):

        """
        Member Function :-

        Throws Exception : No

        Inputs : (i) xAdaptedValue : specifies adapted value of CVar
                                            (type will be decide runtime)

        Outputs : does not return any values

        Purpose : assign adpated value to member varible

        """

        self.__m_dictListItemInfo__["Adapted"] = xAdaptedValue

        return

    """----------------------------------------------------------------------"""

    def MGetCVarDefaultValue(self):

        """
        Member Function :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : (i) self.m_dictListItemInfo.get("Default") : return default value of CVar
                                                                (type will be decide runtime)

        Purpose : return default value of CVar

        """

        return self.__m_dictListItemInfo__.get("Default")

    """----------------------------------------------------------------------"""

    def MSetCVarDefaultValue(self, xDefaultValue):

        """
        Member Function :-

        Throws Exception : No

        Inputs : (i) xDefaultValue : specifies default value of CVar

        Outputs : does not retun any values

        Purpose : assign default value to member variable by input parameter

        """

        self.__m_dictListItemInfo__["Default"] = xDefaultValue

        return

    """----------------------------------------------------------------------"""

    def MGetCVarFlags(self):

        """
        Member Function :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : (i) self.m_dictListItemInfo.get("Flags") : return list of enum CVar flags

        Purpose : return list of enum CVar flags

        """

        return self.__m_dictListItemInfo__.get("Flags")

    """----------------------------------------------------------------------"""

    def MSetCVarFlags(self, strCVarFlags):

        """
        Member Function :-

        Throws Exception : No

        Inputs : (i) strCVarFlags : String containing cvar flags. eg. "HG", "R", "GN", etc.

        Outputs : does not return any values

        Purpose : assign value to member variable by input parameter

        """
        lsECVarFlags = []
        for strFlag in strCVarFlags:
                lsECVarFlags.append(CVar.ms_dictECVarFlags.get(strFlag))

        self.__m_dictListItemInfo__["Flags"] = lsECVarFlags

        return

    """----------------------------------------------------------------------"""

    def MGetCVarMaxLen(self):

        """
        Member Function :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Ouptus : (i) self.m_dictListItemInfo.get("MaxLen") : return integer type Maximum length of CVar

        Purpose : return maximum lenth of CVar

        """

        return self.__m_dictListItemInfo__.get("MaxLen")

    """----------------------------------------------------------------------"""

    def MSetCVarMaxLen(self, iMaxLen):

        """
        Member Function :-

        Throws Exception : No

        Inputs : (i) iMaxLen : integer type specifies Maximum length of CVar

        Ouptus : does not return any values

        Purpose : assign value to member variable by input parameter

        """

        self.__m_dictListItemInfo__["MaxLen"] = iMaxLen

        return

    """----------------------------------------------------------------------"""

    def MGetCVarRange(self):

        """
        Member Function :-

        Throws Exception : No

        Inputs : deos not receive any inputs

        Outputs : (i) self.m_dictListItemInfo.get("Range") : return list of enum of CVars' range

        Purpose : return range as list of enum

        """

        return self.__m_dictListItemInfo__.get("Range")

    """----------------------------------------------------------------------"""

    def MSetCVarRange(self, lsStrCVarRange):

        """
        Member Functtion :-

        Throws Exception : No

        Inputs : (i) lsStrCVarRange : list of enum of CVars' range, eg. [OFF, ON]

        Outputs : does not return any values

        Purpose : assign value to member variable by input parameter

        """

        self.__m_dictListItemInfo__["Range"] = lsStrCVarRange

        return

    """----------------------------------------------------------------------"""

    def MGetCVarMinValue(self):

        """
        Member Function :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : (i) self.m_dictListItemInfo.get("Min") : return minimum value of CVar
                                                             (return type will be decided at runtime)

        Purpose : return min value of CVar.

        """

        return self.__m_dictListItemInfo__.get("Min")

    """----------------------------------------------------------------------"""

    def MSetCVarMinValue(self, xMinValue):

        """
        Member Function :-

        Throws Exception : No

        Inputs : (i) xMinValue : specifies minimum value of CVar
                                        (return type will be decided at runtime)

        Outputs : does not return any values

        Purpose : assign value to member variable by input parameter

        """

        self.__m_dictListItemInfo__["Min"] = xMinValue

        return

    """----------------------------------------------------------------------"""

    def MGetCVarMaxValue(self):

        """
        Member Function :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : (i) self.m_dictListItemInfo.get("Max") : return maximum value of CVar
                                                           (return type will be decided at runtime)

        Purpose : return max value of CVar.

        """

        return self.__m_dictListItemInfo__.get("Max")

    """----------------------------------------------------------------------"""

    def MSetCVarMaxValue(self, xMaxValue):

        """
        Member Function :-

        Throws Exception : No

        Inputs : (i) xMaxValue : specifies maximum value of CVar
                                        (return type will be decided at runtime)

        Outputs : does not return any values

        Purpose : assign value to member variable by input parameter

        """

        self.__m_dictListItemInfo__["Max"] = xMaxValue

        return

    """----------------------------------------------------------------------"""

    def MGetCVarGrainValue(self):

        """
        Member Function :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : (i) self.m_dictListItemInfo.get("Grain") : return grain value of CVar as unknown type
                                                              (type will be decided at runtime)

        Purpose : return grain value of CVar

        """

        return self.__m_dictListItemInfo__.get("Grain")

    """----------------------------------------------------------------------"""

    def MSetCVarGrainValue(self, xGrainValue):

        """
        Member Function :-

        Throws Exception : No

        Inputs : (i) xGrainValue : specifies grain value of CVar
                                        (type will be decided at runtime)

        Outputs : does not return any values

        Purpose : assign value to member variable by input parameter

        """

        self.__m_dictListItemInfo__["Grain"] = xGrainValue

        return

    """----------------------------------------------------------------------"""

    def MGetCVarUnit(self):

        """
        Member Function :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : (i) self.m_dictListItemInfo.get("Unit") : return string containing  Unit of CVar

        Purpose : return unit of CVar as a string

        """

        return self.__m_dictListItemInfo__.get("Unit")

    """----------------------------------------------------------------------"""

    def MSetCVarUnit(self, strUnit):

        """
        Member Function :-

        Throws Exception : No

        Inputs : (i) strUnit : string specifies Unit of CVar

        Outputs : does not return any values

        Purpose : assign value to member variable by input parameter

        """

        self.__m_dictListItemInfo__["Unit"] = strUnit

        return

    """----------------------------------------------------------------------"""

    def MSetCVarAbsolutePath(self, strCVarAbsolutePath):

        """
        Member Method :-

        Throws Exception :- No

        Inputs :- (i) strCVarAbsolutePath :- string containing the absolute path
                                             of the CVar

        Outputs :- does not return any value

        Purpose :- This method sets the absolute path of the CVar to the dictionary

        """

        self.__m_dictListItemInfo__["AbsolutePath"] = strCVarAbsolutePath

        return

    """----------------------------------------------------------------------"""

    def MGetCVarAbsolutePath(self):

        """
        Member Function :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : (i) strAbsolutePath : return string containing absolute path of CVar

        Purpose : return absolute path of CVar

        """
        strAbsolutePath = self.__m_dictListItemInfo__.get("AbsolutePath")

        return strAbsolutePath

    """----------------------------------------------------------------------"""

    def MGetParentAbsolutePath(self):

        """
        Member Function :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : (i) strParentAbsolutePath : return string containing parent's absolute path

        Purpose : assign input absolute path to member variable

        """

        strAbsolutePath = self.__m_dictListItemInfo__.get("AbsolutePath")
        # finding last occurences of dot and split using that dot
        lsTokens = strAbsolutePath.rsplit(".", 1)

        strParentAbsolutePath = lsTokens[0]

        return strParentAbsolutePath

    """----------------------------------------------------------------------"""

    def MGetImageWidth(self):

        """
        Member Function :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : (i) self.m_dictListItemInfo.get("Width") : integer number, specifies image width

        Purpose : return width of image

        """

        return self.__m_dictListItemInfo__.get("Width")

    """----------------------------------------------------------------------"""

    def MSetImageWidth(self, iImageWidth):

        """
        Member Function :-

        Throws Exception : No

        Inputs : (i) iImageWidth : integer specifies image width

        Outputs : does not return any values

        Purpose : assign received image width to member variable

        """

        self.__m_dictListItemInfo__["Width"] = iImageWidth

        return

    """----------------------------------------------------------------------"""

    def MGetImageHeight(self):

        """
        Member Function :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : (i) self.m_dictListItemInfo.get("Height") : integer number specifies image height

        Purpose : return height of image

        """

        return self.__m_dictListItemInfo__.get("Height")

    """----------------------------------------------------------------------"""

    def MSetImageHeight(self, iImageHeight):

        """
        Member Function :-

        Throws Exception : No

        Inputs : (i) iImageHeight : integer specifies image height

        Outputs : does not return any values

        Purpose : assign received image width to member variable

        """

        self.__m_dictListItemInfo__["Height"] = iImageHeight

        return

    """----------------------------------------------------------------------"""

    def MGetImageBits(self):

        """
        Member Function :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : (i) self.m_dictListItemInfo.get("Bits") : integer number specifies number of bits in image

        Purpose : return number of bits in image

        """

        return self.__m_dictListItemInfo__.get("Bits")

    """----------------------------------------------------------------------"""

    def MSetImageBits(self, iImageBits):

        """
        Member Function :-

        Throws Exception : No

        Inputs : (i) iImageBits : integer specifies number of bits in image

        Outputs : does not return any values

        Purpose : assign received image bits to member variable

        """

        self.__m_dictListItemInfo__["Bits"] = iImageBits

        return

    """----------------------------------------------------------------------"""
    def MSetCVarRoot(self, strRoot):
        """
        Member Function :-

        Throws Exception : No

        Inputs : (i) strRoot : String containing value of cvar's root ( FileName typed cvar has root its attribute)

        Outputs : does not return any values

        Purpose : set the value of root.

        """

        self.__m_dictListItemInfo__["Root"] = strRoot

        return

    """----------------------------------------------------------------------"""
    def MGetCVarRoot(self):
        """
        Member Function :-

        Throws Exception : No

        Inputs : does recieve any inputs

        Outputs : (i) self.__m_dictListItemInfo__.get("Root") : return String containing value of root attribute

        Purpose : return Root value of FileName typed cvar

        """
        return self.__m_dictListItemInfo__.get("Root")

    """----------------------------------------------------------------------"""
    def MSetCVarFileters(self, strFilters):
        """
        Member Function :

        Throws Exception : No

        Inputs : (i) strFilters : String containing value of Filters attribute of FileName typed cvar.

        Outputs : does not return any values

        Purpose : set value of Filters of FileName typed cvar.

        """
        self.__m_dictListItemInfo__["Filters"] = strFilters

        return

    """----------------------------------------------------------------------"""
    def MGetCVarFileters(self):
        """
        Member Function :

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : (i) self.__m_dictListItemInfo__.get("Filters") : return value of Filters attibute(FileName type cvar has Filters its attibute)

        Purpose : return value of Filters attribute

        """
        return self.__m_dictListItemInfo__.get("Filters")

    """----------------------------------------------------------------------"""
    def MSetCVarPath(self, strPath):
        """
        Member Function :-

        Throws Exception : No

        Inputs : (i) strPath : String containing value of Path Attribute.
                                Note : FileName typed cvar has its attribute Path.
                                        Its not a directory path of cvar

        Outputs : does not return any values

        Purpose : set the value of Path attribute of FileName typed cvar.

        """
        self.__m_dictListItemInfo__["Path"] = strPath

        return

    """----------------------------------------------------------------------"""
    def MGetCVarPath(self):
        """
        Member Function :-

        Throws Exception : No

        Inputs : does not recive any inputs

        Outputs : (i) self.__m_dictListItemInfo__.get("Path") : return String containing value of Path attribute of FileName typed cvar.

        Purpose : return value of Path attribute of FileName typed cvar.

        """
        self.MSetCVa
        return self.__m_dictListItemInfo__.get("Path")

    """----------------------------------------------------------------------"""
    def MSetNbOfBits(self, strNbOfBits):
        """
        Member Function :-

        Throws Exception : No

        Inputs : (i) strNbOfBits : String containing number of bits
                                    Note : only Register type cvar has its attribute "NbOfBits"

        Outputs : does not return any values

        Purpose : set the value of NbOfBits attribute of Register typed cvar

        """
        self.__m_dictListItemInfo__["NbOfBits"] = strNbOfBits

        return

    """----------------------------------------------------------------------"""
    def MGetNbOfBits(self):
        """
        Member Function :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : (i) self.__m_dictListItemInfo__.get("NbOfBits") : return string containing number of bits
                                                                    Note : Register type cvar has its attribute "NbOfBits"

        Purpose : return number of bits of Register type cvar

        """

        return self.__m_dictListItemInfo__.get("NbOfBits")

    """----------------------------------------------------------------------"""
    def MSetCVarHardwareAddress(self, strHardwareAddress):
        """
        Member Function :-

        Throws Exception : No

        Inputs : (i) strHardwareAddress : String containing value of hardware address
                                            Note : Register type cvar has its attribute HardwareAddress

        Outputs : does not return any values

        Purpose : set the value of hardwareAddress attribute of Register type cvar.

        """
        self.__m_dictListItemInfo__["HardwareAddress"] = strHardwareAddress

        return

    """----------------------------------------------------------------------"""
    def MGetCVarHardwareAddress(self):
        """
        Member Function :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : (i) self.__m_dictListItemInfo__.get("HardwareAddress") :
                                            return string containing value of HardwareAddress
                                            attribute of Register type cvar

        Purpose : return value of HardwareAddress atrribute of Register type cvar.

        """

        return self.__m_dictListItemInfo__.get("HardwareAddress")

    """----------------------------------------------------------------------"""



    def __del__(self):

        """
        Destructor :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : does not return any values

        Purpose : releases memory allocated for member variables

        """
        # calling parent class' destructor
        item.IListItem.__del__(self)

        return

    """----------------------------------------------------------------------"""

    def MPrintCVarDetail(self):

        """
        Member Function :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : does not return any values

        Purpose : Print the value of all member variables

        """

        # printing details
        # iterating dictionary dictListItemInfo
        for strKey in self.__m_dictListItemInfo__:
            print str(strKey) + " = " + str(self.__m_dictListItemInfo__.get(strKey))

        return

    """----------------------------------------------------------------------"""

    @staticmethod
    def MSTestCVar():

        """
        Tester Function :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : does not return any values

        Purpose : Test Constructor and functions of CVar class by different inputs

        """
        # Creating object of CVar
        objCVar = CVar({"AbsolutePath" : "XStreamDSO.Name", "Type" : "String", "Request" : "myRequest"})

        # printting details of CVar
        objCVar.MPrintCVarDetail()
        # printing logs
        objCVar.MWhos(bEnableLog = True)
        # writing object into file
        objCVar.MWriteYaml("c:\\temp\\dump.txt")

        return

    """----------------------------------------------------------------------"""

if __name__ == '__main__':
    CVar.MSTestCVar()