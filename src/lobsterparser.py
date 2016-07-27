#-------------------------------------------------------------------------------
# Name:        lobsterFileParser
# Purpose:     This module contains class, which will read cvars from file and loads them
#               into application. This class contains algorithm/logic for parsing the file,
#               tokenizing them appropriately and instantiating cvar and cvardirectory
#               objects from them.
#
# Author:      lakhu
#
# Created:     10/02/2014
# Copyright:   (c) Account Prism Pvt. Ltd.
# Licence:     all_rights_reserved
#-------------------------------------------------------------------------------


# imports
import re
import lobstercvar as cvar
import lobsterdirectory as directory

#class-name         : CLobsterFileParser
#class-description  : read cvars from file, tokenize it and populate CDataContext
class CLobsterFileParser:

    # dictionary containing, CVar type as key and list of its attribute name as its values
    # eg. {"Action" : ["AbsolutePath", "Type", "Flags"],
    #       "SafeArray" : ["AbsolutePath", "Type", "Request", "Adapt", "Default", "Range", "Flags"]
    #       }
    ms_dictTypeOfCVarAndAttributes = {
                                        #   attributes applicable for "Action" type of cvar
                                        "Action" : ["AbsolutePath", "Type", "Flags"],
                                        #   attributes applicable for "SafeArray" type of cvar
                                        "SafeArray" : ["AbsolutePath", "Type", "Requested", "Adapted", "Default", "Range", "Flags"],
                                        #   attributes applicable for "String" type of cvar
                                        "String" : ["AbsolutePath", "Type", "Requested", "Adapted", "Default" ,"MaxLen", "Flags"],
                                        #   attributes applicable for "Name" type of cvar
                                        "Name" : ["AbsolutePath", "Type", "Requested", "Adapted", "Default" ,"MaxLen", "Flags"],
                                        #   attributes applicable for "Enum" type of cvar
                                        "Enum" : ["AbsolutePath", "Type", "Requested", "Adapted", "Default", "Flags", "Range"],
                                        #   attributes applicable for "Bool" type of cvar
                                        "Bool" : ["AbsolutePath", "Type", "Requested", "Adapted", "Default", "Flags", "Range"],
                                        #   attributes applicable for "Integer" type of cvar
                                        "Integer" : ["AbsolutePath", "Type", "Requested", "Adapted", "Default", "Min", "Max", "Grain", "Unit", "Flags"],
                                        #   attributes applicable for "Double" type of cvar
                                        "Double" : ["AbsolutePath", "Type", "Requested", "Adapted", "Default", "Min", "Max", "Grain", "Unit", "Flags"],
                                        #   attributes applicable for "DoubleLockstep" type of cvar
                                        "DoubleLockstep" : ["AbsolutePath", "Type", "Requested", "Adapted", "Default", "Min", "Max", "Grain", "Unit", "Flags"],
                                        #   attributes applicable for "Image" type of cvar
                                        "Image" : ["AbsolutePath", "Type", "Adapted", "Flags", "Width", "Height", "Bits"],
                                        # attributes applicable for "Color" type of cvar
                                        "Color" : ["AbsolutePath", "Type", "Adapted", "Default", "Flags", "Range"],
                                        # attributes applicable for "FileName" type of cvar
                                        "FileName" : ["AbsolutePath", "Type", "Adapted", "Default", "Flags", "Range", "MaxLength", "Root", "Filters", "Path"],
                                        # attribute applicable for "notimpl" cvar
                                        "notimpl" :["AbsolutePath", "Type"],
                                        # attribute applicable for "Long Integer" cvar
                                        "Long Integer" : ["AbsolutePath", "Type", "Requested", "Adapted", "Default", "Min", "Max", "Grain", "Unit", "Flags"],
                                        # attribute applicable for "BitPattern" cvar
                                        "BitPattern" : ["AbsolutePath", "Type", "Requested", "Adapted", "Default", "MaxLen", "Flags"],
                                        # attribute applicable for "Register" cvar
                                        "Register" : ["AbsolutePath", "Type", "Adapted", "Default", "Flags", "NbOfBits", "HardwareAddress"]
                                      }

    def __init__(self, strFileName = "c:\\temp\\temp.txt"):

        """
        Constructor :-

        Throws Exception : No

        Inputs :    (i) strFileName : string containing file name, which stores info. about cvars.
                                        eg. "c:\\temp\\temp.txt"

        Outputs : does not return any values

        Purpose : initialize member variable by parameters received as input

        """
        #   filename, from which parsing have to be done
        self.m_strFileName = strFileName

        #   dictionary, which contains the cvar objects. It'll contain
        #   information in following format : {cvar-name(with absolute path) : cvarObject}
        #   eg. {"XStreamDSO.Name" : objCVarName}
        self.m_dictCVarCollection = {}
        #   dictionary, which contains the directory objects. This dictionary also
        #   stores the information in the same format, as m_dictCVarCollection.
        #   Note :- We are maitaining two dictionaries. But, finally after the load
        #           operation of cvars from file have completed, both these dictionaries
        #           are merged and returned as a single dictionary.

        # defining dictionary for for cvar
        self.m_dictDirCollection = {}


        self.m_dictSeaparated = {
                                    "Type" : {
                                        "Action" : {},
                                        "SafeArray" : {},
                                        "String" : {},
                                        "Name" : {},
                                        "Enum" : {},
                                        "Bool" : {},
                                        "Integer" : {},
                                        "Double" : {},
                                        "DoubleLockstep" : {},
                                        "Image" : {},
                                        "Color" : {},
                                        "FileName" : {},
                                        "notimpl" :{},
                                        "Long Integer" : {},
                                        "BitPattern" : {},
                                        "Register" : {}
                                        },

                                    "Alphabets" : {
                                        "A" : {},
                                        "B" : {},
                                        "C" : {},
                                        "D" : {},
                                        "E" : {},
                                        "F" : {},
                                        "G" : {},
                                        "H" : {},
                                        "I" : {},
                                        "J" : {},
                                        "K" : {},
                                        "L" : {},
                                        "M" : {},
                                        "N" : {},
                                        "O" : {},
                                        "P" : {},
                                        "Q" : {},
                                        "R" : {},
                                        "S" : {},
                                        "T" : {},
                                        "U" : {},
                                        "V" : {},
                                        "W" : {},
                                        "X" : {},
                                        "Y" : {},
                                        "Z" : {}
                                    }
                                }

        return

    """----------------------------------------------------------------------"""

    def MReadAndPopulateCVar(self, strRegExprDelim = ": |,"):

        """
        Member Function :-

        Throws Exception :- Yes (i) when file name with absolute path is not passed or filename passed does not exists.

        Inputs : (i) strRegExprDelim : string containing characters, which have to be used as delimiters.
                                        (delimeter is used to tokenize the String). Here ": |," is passed, which means
                                        that string will be tokenized with respect to either ': ' or wrt. to ','. If
                                        any of these two delimiters are found in source string, then string will be
                                        tokenized.

        Outputs : does not return any values.

        Purpose : This method reads CVar information from file, tokenizes it, instantiates cvar
                    objects and populate them in m_dictCVarCollection.
        """

        # check whether file name is passed or not, if not passed then raise exception
        if (self.m_strFileName == None):
            raise Exception("lobsterparser.py :- File name is not passed.")

        # open file in reading mode
        objFile = open(self.m_strFileName, "r")

        iLine = 0
        # reading file line by line
        for strLine in objFile:
            #print iLine
            #iLine += 1
            #   removing "\n" at the end of each line
            strLine = strLine[0 : -1]
            # tokenize line by delimeter ": " and ",".
            # Note :- Tokenizing takes place in two phase :- (i) Phase 1, (ii) Phase 2
            #         (i) Phase1 :- Here we are tokenizing string containing CVar information
            #                       using strRegExprDelim as delimiter, which is generally ": |,".
            #                       Here, the purpose is to find the type of CVar.
            #         (ii) Phase2 :- Here we are tokenzing string containing CVar information
            #                        using the attributes as delimiter. And since at that time,
            #                        we are having type of cvar info. with us, we parses the
            #                        values of cvars, which are related to that specific type
            #                        of cvar only. eg. For Double and Integer type only, we
            #                        will try to look for "Min-Val" and "Max-Val" attributes' values.
            #                        We get the information about the attributes applicable for the
            #                        particular type of cvar, with the help of the static dictionary
            #                        maintained, in this class.

            #   First phase of tokenization to know type information
            lsTokens = re.split(strRegExprDelim, strLine)

            #   if only two tokens are generated due to re.split, then
            #   it'll be the case of cvars which are not implemented
            if (len(lsTokens) == 2):
                if(lsTokens[1] == "notimpl"):
                    #   processing the directory information of current cvar read from file
                    #   lsAttributeValues[0] contains the name with absolutepath of cvar. eg. XStreamDSO.TouchScreenEnabled.
                    self.MPopulateDirectories(lsTokens[0])

                    lsNotimplValues = CLobsterFileParser.ms_dictTypeOfCVarAndAttributes.get(lsTokens[1])

                    dictCVarAttributeAndValue = {}
                    # iterating list of attribute
                    # Note : This code is written according to file format

                    for iCounter in range(0, len(lsNotimplValues)):
                        dictCVarAttributeAndValue[lsNotimplValues[iCounter]] = lsTokens[iCounter]
                    dictCVarAttributeAndValue["Flags"] = ""

                    objCVar = cvar.CVar(dictCVarAttributeAndValue = dictCVarAttributeAndValue)
                    self.m_dictCVarCollection[lsTokens[0]] = objCVar

                continue
            else:
                # token at position 2 will be value of type attribute
                strType = lsTokens[2]

                #   string which contains the attributes of cvar as delimiters.
                strAttribDelims = ": Type,|,Request,|,Adapt,|,Default,|,MaxLen,|,Flags,|,Range,|,Min,|,Max,|,Grain,|,Unit,|,Width,|,Height,|,Bits,|,MaxLength,|,Root,|,Filters,|,Path,|,NbOfBits,|,HardwareAddress,"

                #   second phase of tokenization, to know the attributes values, which are
                #   applicable to cvar of specific type
                lsAttributeValues = re.split(strAttribDelims, strLine)

                if (lsAttributeValues[0] in self.m_dictCVarCollection):
                    continue

                #   processing the directory information of current cvar read from file
                #   lsAttributeValues[0] contains the name with absolutepath of cvar. eg. XStreamDSO.TouchScreenEnabled.
                self.MPopulateDirectories(lsAttributeValues[0])

                # getting list of attributes value. eg. if type is "Action" then list will be ["AbsolutePath", "Type", "Flags"]
                lsAttributes = CLobsterFileParser.ms_dictTypeOfCVarAndAttributes.get(strType)
                # dictionary containing attribute of cvar as key and value will be actual value of cvar's attribute
                # eg. {"AbsolutePath" : "XStreamDSO.Name", "Type" : "String"}
                dictCVarAttributeAndValue = {}
                # iterating list of attribute
                # Note : This code is written according to file format
                try:
                    for iCounter in range(0, len(lsAttributes)):
                        dictCVarAttributeAndValue[lsAttributes[iCounter]] = lsAttributeValues[iCounter]
                except:
                    return

                # creating object of cvar
                objCVar = cvar.CVar(dictCVarAttributeAndValue = dictCVarAttributeAndValue)
                self.m_dictCVarCollection[lsAttributeValues[0]] = objCVar
                self.m_dictSeaparated.get("Type").get(strType)[lsAttributeValues[0]] = objCVar

                lsStrTokens = re.split("\.", lsAttributeValues[0])
                strName = lsStrTokens[len(lsStrTokens)-1]
                strFirstChar = strName[0].upper()
                self.m_dictSeaparated.get("Alphabets").get(strFirstChar)[lsAttributeValues[0]] = objCVar
        return

    """----------------------------------------------------------------------"""

    def MPopulateDirectories(self, strAbsPath = None):

        """
        Member Function :-

        Throws Exception : Yes, (i) when input parameter strAbsPath is an empty string
                                    or it's None

        Inputs : (i) strAbsPath : string specifies the absolute path of cvar
                                (using this absolute path, we get information about cvar's
                                 directory, and accordingly, we creates the object of cvar
                                 directory, if it doesn't exits.)
                                eg. "XStreamDSO.ScopeIdentify.SimFamily"

        Outputs : does not return any values

        Purpose : This method gets information about the directory of cvar passed as
                   argument, and accordingly, instantiates CVarDirectory object and
                   add that object to m_dictDictCollection.

        """
        if (strAbsPath == None or len(strAbsPath) <= 0):
            raise Exception("lobsterparser.py : input parameter strAbsPath is not received")

        # splitting absolute path by dot and separating each token. In "\.", "\" is
        # just a escape character, because '.' have special meaning. To override that
        # escape character('\') is used'
        # eg. if absolute path is "XStreamDSO.EyeDr.SignalInput.EDrIn.Zoom.ZoomGauge"
        # then list will be [XStreamDSO, EyeDr, SignalInput, EDrIn, Zoom, ZoomGauge]
        lsStrPathTokens = re.split("\.", strAbsPath)

        # define number of token fetched from absolute path
        iPathLen = len(lsStrPathTokens)

        # string which contains the absolute path of current cvardirectory
        strAbsolutePath = None
        # string which contains the fullname with path of the parent directory of given cvardirectory
        strParentNodeWithpath = None
        # string which contains the name of the child cvar of cvardirectory under process
        strChildCVar = None
        # string which contains the name of the child cvardirectory of cvardirectory under process
        strChildDir = None

        # iterating each token except last token
        for iCount in range(0, iPathLen - 1):
            # specifying delimeter for separating parent and child directories.
            # delimeter will be current token or current token with dots
            strCurrentDirectory = lsStrPathTokens[iCount]

            # There are 3 phases :  (i) Token can be a first token :
            #                       (ii) Token cane be last second token
            #                       (ii) Token can be a in between token

            # if current node is first node then it will not have parent
            if (iCount == 0):
                strDelim = strCurrentDirectory + '.'
                lsStrParentChild = re.split(strDelim, strAbsPath)
                # setting absolute path for root cvardirectory
                strAbsolutePath = strCurrentDirectory

                strCurrentNode = strCurrentDirectory
                # setting parent of root cvardirectory to None as it does not
                # have any parent cvardirectory
                strParentNodeWithpath = None
                # if iPathLen is greater than 2, ie., A.B.C, then B is regarded as
                # childcvar directory of A, instead of child cvar of A
                if(iPathLen > 2):
                    strChildDir = strCurrentNode + "." + re.split("\.", lsStrParentChild[1])[0]
                    strChildCVar = None
                # in case of A.B, then make B as child cvar of A
                else:
                    strChildDir = None
                    strChildCVar = lsStrPathTokens[1]

            # if  current token is last second token then it will not have any child directory
            elif (iCount == iPathLen - 2):
                # setting delimiter
                strDelim = '.' + strCurrentDirectory
                # getting the details of parent and child for the absolute path passed
                lsStrParentChild = re.split(strDelim, strAbsPath)
                # setting parent
                strParentNodeWithpath = lsStrParentChild[0]
                # setting the name of current cvardirectory
                strCurrentNode = strCurrentDirectory
                # setting the absolute path of the current cvar directory
                strAbsolutePath = strParentNodeWithpath + "." + strCurrentDirectory
                # eg . in case of A.B.C.D, then D have to considered as child cvar of
                # C.
                strChildDir = None
                strChildCVar = lsStrPathTokens[iPathLen - 1]

            # in case if it is in between token
            else:
                # preparing delimiter
                strDelim = '.' + strCurrentDirectory + '.'
                # getting parent and child details about current cvardirectory
                lsStrParentChild = re.split(strDelim, strAbsPath)
                # setting parent node
                strParentNodeWithpath = lsStrParentChild[0]
                # setting name of current cvardirectory
                strCurrentNode = strCurrentDirectory
                # setting the absolute path of current cvardirectory
                strAbsolutePath = strParentNodeWithpath + "." + strCurrentDirectory
                # setting the child cvar directory of current cvardirectory.
                # eg. A.B.C.D, then C is child cvardirectory of B.
                strChildDir = strParentNodeWithpath + "." + strCurrentNode + "." +re.split("\.", lsStrParentChild[1])[0]
                strChildCVar = None

            # checking whether dictionary contains strAbsolutePath,
            # (i)   if no then make new object of CCVarDirectory,
            # (ii)  if yes then fetch that object of CCVarDirectory and add child
            objDir = None
            if (strAbsolutePath not in self.m_dictDirCollection):
                lsStrChildCVars = []
                lsStrChildDirectories = []

                if (strChildCVar != None):
                    lsStrChildCVars = [strChildCVar]

                if(strChildDir != None):
                    lsStrChildDirectories = [strChildDir]

                # creating new object of CCVarDirectory
                objDir = directory.CCVarDirectory(
                                                    strNodeName = strCurrentNode, lsStrChildDirectories = lsStrChildDirectories,
                                                    lsStrChildCVars = lsStrChildCVars, strParentDirectoryName = strParentNodeWithpath)

                # appending object of CCVarDirectory into dictionary if it does not have this object already
                self.m_dictDirCollection[strAbsolutePath] = objDir

            else:
                # fetching object of CCVarDirectory from dictionary
                objDir = self.m_dictDirCollection.get(strAbsolutePath)

                # Appending Child directory to list of child directory
                if((strChildDir != None) and (strChildDir not in objDir.MGetChildNodes())):
                        objDir.MAppendChildNode(strChildDir)

                # Appending Child CVar to list of child CVar
                if((strChildCVar != None) and (strChildCVar not in objDir.MGetChildCVars())):
                    objDir.MAppendChildCVar(str(strChildCVar))

            objDir.MIncreaseNumberOfDecendantsCvars()

        return

    """----------------------------------------------------------------------"""

    def MGetDictCollection(self):

        """
        Member Function :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : (i) m_dictCVarCollection : return dictionary containing collection of CVars and CvarDirectories

        Purpose : return combined dictionary of CVar Collection and CvarDirectory Collection

        """

        # calling MReadAndPopulateCVar() function
        self.MReadAndPopulateCVar(strRegExprDelim = ": |,")

        # adding m_dictDirCollection to m_dictCVarCollection
        self.m_dictCVarCollection.update(self.m_dictDirCollection)

        return self.m_dictCVarCollection, self.m_dictSeaparated

    """----------------------------------------------------------------------"""

    def __del__(self):

        """
        Destructor :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : does not return any values

        Purpose : releases memory allocated for member variables

        """
        self.m_strFileName = None
        self.m_dictCVarCollection = None
        self.m_dictDirCollection = None

        return

    """----------------------------------------------------------------------"""

    @staticmethod
    def MSTestLobsterParser():

        """
        Tester Function :-

        Throws Exxception : No

        Inputs : does not receive any inputs

        Outputs : does not return any values

        Purpose :

        """
        objCLobsterFileParser = CLobsterFileParser(strFileName = "demo.txt")
        dictTemp = objCLobsterFileParser.MGetDictCollection()

        for strKey in dictTemp:
            obj = dictTemp.get(strKey)
            # if fetched object is of CCVarDirectory
            if(isinstance(obj, directory.CCVarDirectory)):
                print "-------------------------------------------"
                print "Path = " + obj.MGetAbsolutePath()
                print "Name = " + obj.MGetNodeName()
                print "Parent = " + str(obj.MGetParentNodeNameWithFullPath())
                print "Child Dirs = " + str(obj.MGetChildNodes())
                print "Child CVars = " + str(obj.MGetChildCVars())
                print "-------------------------------------------"
            # # if fetched object is of CVar
            if(isinstance(obj, cvar.CVar)):
#                obj.MPrintCVarDetail()
                print "-------------------------------------------"
                print "Path = " + obj.MGetCVarAbsolutePath()
                print "Name = " + obj.MGetCVarName()
                print "Parent = " + obj.MGetParentAbsolutePath()
                print "Type = " + str(obj.MGetCVarType())
                print "Requested = " + str(obj.MGetCVarRequestedValue())
                print "Adapted = " + str(obj.MGetCVarAdaptedValue())
                print "Default = " + str(obj.MGetCVarDefaultValue())
                print "MaxLen = " + str(obj.MGetCVarMaxLen())
                print "Flags = " + str(obj.MGetCVarFlags())
                print "Range = " + str(obj.MGetCVarRange())
                print "Min = " + str(obj.MGetCVarMinValue())
                print "Max = " + str(obj.MGetCVarMaxValue())
                print "Grain = " + str(obj.MGetCVarGrainValue())
                print "Unit = " + str(obj.MGetCVarUnit())
                print "Height = " + str(obj.MGetImageHeight())
                print "Width = " + str(obj.MGetImageWidth())
                print "Bits = " + str(obj.MGetImageBits())
                print "-------------------------------------------"

        return

    """----------------------------------------------------------------------"""

if __name__ == '__main__':
        CLobsterFileParser.MSTestLobsterPsarser()