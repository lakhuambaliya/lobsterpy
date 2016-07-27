#-------------------------------------------------------------------------------
# Name:        lobstersearchmanager
# Purpose:      it contains the functionality of searching
#
# Author:      lakhu
#
# Created:     30/04/2014
# Copyright:   (c) Account Prism Pvt. Ltd.
# Licence:     all_rights_reserved
#-------------------------------------------------------------------------------

import lobsterdatacontext
import lobstercvar
import lobsterdirectory
import re
import lobstersearchconfiguration
import LecroyUtil_portable as Lec_P

# class-name        : CSearchManager
# class-desctions   : this class contains all the search functionalities

class CSearchManager():

    ms_dictTypeAndAttribute = {
                                        "Action" :          ["Name", "Type", "Flags"],
                                        "SafeArray" :       ["Name", "Type", "Flags", "Adapted"],
                                        "String" :          ["Name", "Type", "Flags", "Adapted"],
                                        "Name" :            ["Name", "Type", "Flags", "Adapted"],
                                        "Enum" :            ["Name", "Type", "Flags", "Adapted"],
                                        "Bool" :            ["Name", "Type", "Flags", "Adapted"],
                                        "Integer" :         ["Name", "Type", "Flags", "Adapted"],
                                        "Double" :          ["Name", "Type", "Flags", "Adapted"],
                                        "DoubleLockstep" :  ["Name", "Type", "Flags", "Adapted"],
                                        "Image" :           ["Name", "Type", "Flags", "Adapted", "Bits"],
                                        "Color" :           ["Name", "Type", "Flags", "Adapted"],
                                        "FileName" :        ["Name", "Type", "Flags", "Adapted", "Root", "Filters", "Path"],
                                        "notimpl" :         ["Name", "Type"],
                                        "Long Integer" :    ["Name", "Type", "Flags", "Adapted"],
                                        "BitPattern" :      ["Name", "Type", "Flags", "Adapted"],
                                        "Register" :        ["Name", "Type", "Flags", "Adapted", "NbOfBits", "HardwareAddress"],
                                        "AllTypes"  :        ["Name", "Type", "Flags", "Adapted", "Root", "Filters", "Path", "Bits", "NbOfBits", "HardwareAddress"]
                                    }
    def __init__(self):
        pass
    """----------------------------------------------------------------------"""
    @staticmethod
    def MSSearch(objCSearchConfigurations, objCDataContext):
        """
        Static Function :-

        Inputs :    (i)  objCSearchConfigurations   : object of CSearchConfiguration
                    (ii) objCDataContext            : object of CDataContext

        Outputs : (i) lsSearchResults : list containing string absolute path of searched cvars

        purpose : this function serches cvars according to user's choices of attributes.

        """
        # fetching timer object for calculating duration of searching cvars
        objTimer = Lec_P.cTimer()
        objTimer.startTimer()

        # declaring list which will contains absolute path of searched cvars
        lsSearchResults = []

        # fetching search keyword from object of CSearchConfiguration.
        strSearchKeyWord = objCSearchConfigurations.m_strSearchKeyword
        # fetching dictionary of user's choices from object of CSearchConfiguration
        dictFilterCVars = objCSearchConfigurations.m_dictFilterCVars
        # fetching directory as enum from object of CSearchConfiguration
        eSearchDir = objCSearchConfigurations.m_eSearchDir
        lsESearchMode = objCSearchConfigurations.m_lsESearchMode
        # fetching dictionary from data context in which we will search
        dictSearchSpace = objCDataContext.m_dictCVarCollection

        # if user's choice of direcory is Root Directory
        if (eSearchDir == lobstersearchconfiguration.CSearchConfiguration.mC_ROOT_DIR):
            # if search mode is "Match Whole word" and user has selected more than zero types
            if(
                lobstersearchconfiguration.CSearchConfiguration.mC_MATCH_WHOLE_WORD in lsESearchMode and
                (dictFilterCVars.get("Type") != None and len(dictFilterCVars.get("Type")) > 0)
                ):
                        # fetching first character from search keyword string and converting into capital letters.
                        # converting into Upper letter because we have maitained dictioanry which has key in capital letters
                        strFirstChar = strSearchKeyWord[0].upper()
                        # fetching dictionary which has key same as first character of search keyword
                        dictSearchSpace = objCDataContext.m_dictSeparated.get("Alphabets").get(str(strFirstChar))
                        # fetching length of dictionary which contains all cvars which starts with <<strFirstChar>>
                        iLengthMatchWholeWord = len(dictSearchSpace)

                        iLengthTypeDict = 0
                        # calculating number of cvars after aading user's choices of type dictionaries
                        for iType in dictFilterCVars.get("Type"):
                            strType = lobstercvar.CVar.ms_lsStrTypes[iType]
                            iLengthTypeDict += len(objCDataContext.m_dictSeparated.get("Type").get(str(strType)))

                        # number of Cvar in dictioanry <strFirstChr> is less than number of cvars in type dictionary
                        # here we are comparing lenght of dictionary and go for searching in small dictionary
                        # for example :
                        # User enters serchkeyword "Instrument" and he/she has selected Type as Integer and String.
                        # it will calculate number of cvars in dictionary "I" (because "Instrument" starts with "I")
                        # and also calculate number of cvars in combined dictionary of "Integer" and "String"
                        # after calculating number of cvar in both case it will decide in which dictionary we go for searching
                        if(iLengthMatchWholeWord < iLengthTypeDict):
                            dictSearchSpace = objCDataContext.m_dictSeparated.get("Alphabets").get(str(strFirstChar))
                        else:
                            dictSearchSpace = {}
                            for iType in dictFilterCVars.get("Type"):
                                strType = lobstercvar.CVar.ms_lsStrTypes[iType]
                                dictSearchSpace.update(objCDataContext.m_dictSeparated.get("Type").get(str(strType)))

            else:
                dictSearchSpace = {}
                # if user has selected match whole word
                if (lobstersearchconfiguration.CSearchConfiguration.mC_MATCH_WHOLE_WORD in lsESearchMode):
                    # converting into upper case because we have maintained dictionarie's key as capital letter
                    strFirstChar = strSearchKeyWord[0].upper()
                    dictSearchSpace = objCDataContext.m_dictSeparated.get("Alphabets").get(str(strFirstChar))
                elif (dictFilterCVars.get("Type") != None and len(dictFilterCVars.get("Type")) > 0):
                    for eType in dictFilterCVars.get("Type"):
                        dictSearchSpace.update(objCDataContext.m_dictSeparated.get("Type").get(lobstercvar.CVar.ms_lsStrTypes[eType]))
                else:
                    dictSearchSpace = objCDataContext.m_dictCVarCollection

        elif (eSearchDir == lobstersearchconfiguration.CSearchConfiguration.mC_CURRENT_DIR):
            objDir = objCDataContext.m_dictCVarCollection.get(objCDataContext.__m_strCurrentWorkingDirectory__)
            if (isinstance(objDir, lobsterdirectory.CCVarDirectory)):
                lsChildCVars = objDir.MGetChildCVars()
                dictSearchSpace = {}
                for strChildPath in lsChildCVars:
                    strAbsPath = objDir.MGetAbsolutePath() + "." + strChildPath
                    dictSearchSpace[strAbsPath] = objCDataContext.m_dictCVarCollection.get(strAbsPath)
            else:
                raise Exception("lobstersearchmanager : Path not found in Dictionary")

        elif (eSearchDir == lobstersearchconfiguration.CSearchConfiguration.mC_FAVORITE):
            lsChildCVars = objCDataContext.__m_lsStrFavoriteCVars__
            dictSearchSpace = {}
            for strChildPath in lsChildCVars:
                dictSearchSpace[strChildPath] = objCDataContext.m_dictCVarCollection.get(strChildPath)

        setUnionList = CSearchManager.MSUnionAttributes(objCSearchConfigurations.m_dictFilterCVars.get("Type"))

        for strPath, objCVar in dictSearchSpace.items():
            if(isinstance(objCVar, lobsterdirectory.CCVarDirectory)):
                continue
            bAllConditionSatisfied = True
            for strAttribute in setUnionList:
                if (strAttribute in objCSearchConfigurations.m_dictFilterCVars):

                    if (((strAttribute == "Adapted")  and
                        (objCVar.MGetCVarType() == lobstercvar.CVar.mC_INTEGER or
                        objCVar.MGetCVarType() == lobstercvar.CVar.mC_DOUBLE or
                        objCVar.MGetCVarType() == lobstercvar.CVar.mC_DOUBLE_LOCK_STEP)) or
                        (strAttribute == "Bits" or strAttribute == "NbOfBits")):

                        lsAdaptedOperatorsAndValus = objCSearchConfigurations.m_dictFilterCVars.get(strAttribute)
                        try:
                            fAdaptedValue = float(objCVar.MGetCVarAdaptedValue())
                            fAdaptedValue1 = float(lsAdaptedOperatorsAndValus[1])
                        except:
                            bAllConditionSatisfied = False
                            break
                        if not objCVar.MGetCVarType() in objCSearchConfigurations.m_dictFilterCVars.get("Type"):
                            continue

                        if (lsAdaptedOperatorsAndValus[0] == "EQ"):
                            if (fAdaptedValue != fAdaptedValue1):
                                #lsSearchResults.append(strPath)
                                bAllConditionSatisfied = False
                                break
                        elif (lsAdaptedOperatorsAndValus[0] == "NE"):
                            if (fAdaptedValue == fAdaptedValue1):
                                #lsSearchResults.append(strPath)
                                bAllConditionSatisfied = False
                                break
                        elif (lsAdaptedOperatorsAndValus[0] == "LT"):
                            if (fAdaptedValue >= fAdaptedValue1):
                                #lsSearchResults.append(strPath)
                                bAllConditionSatisfied = False
                                break
                        elif (lsAdaptedOperatorsAndValus[0] == "GT"):
                            if (fAdaptedValue <= fAdaptedValue1):
                                #lsSearchResults.append(strPath)
                                bAllConditionSatisfied = False
                                break
                        elif (lsAdaptedOperatorsAndValus[0] == "LE"):
                            if (fAdaptedValue > fAdaptedValue1):
                                #lsSearchResults.append(strPath)
                                bAllConditionSatisfied = False
                                break
                        elif (lsAdaptedOperatorsAndValus[0] == "GE"):
                            if (fAdaptedValue < fAdaptedValue1):
                                #lsSearchResults.append(strPath)
                                bAllConditionSatisfied = False
                                break
                        elif (lsAdaptedOperatorsAndValus[0] == "BETWEEN"):
                            try:
                                fAdaptedValue2 = float(lsAdaptedOperatorsAndValus[2])
                            except:
                                bAllConditionSatisfied = False
                                break
                            if (fAdaptedValue > fAdaptedValue2 or fAdaptedValue < fAdaptedValue1):
                                #lsSearchResults.append(strPath)
                                bAllConditionSatisfied = False
                                break

                    elif (strAttribute == "Type" or strAttribute == "Flags"):
                        lsEValues = objCSearchConfigurations.m_dictFilterCVars.get(strAttribute)
                        if(strAttribute == "Type"):
                            if (objCVar.MGetCVarType() not in lsEValues):
                                #lsSearchResults.append(strPath)
                                bAllConditionSatisfied = False
                                break

                        elif (strAttribute == "Flags"):
                            bFlagExist = False
                            for eFlag in lsEValues:
                                if (eFlag in objCVar.MGetCVarFlags()):
                                    #lsSearchResults.append(strPath)
                                    bFlagExist = True
                                    break
                            if (bFlagExist == False):
                                bAllConditionSatisfied = False
                                break

                    else:
                        xValue = str(objCVar.__m_dictListItemInfo__.get(strAttribute))
                        strAttrValue = objCSearchConfigurations.m_dictFilterCVars.get(strAttribute)

                        if (strAttribute == "Name"):
                            strAttrValue = strSearchKeyWord

                        # match case and dont match whole word
                        if (lobstersearchconfiguration.CSearchConfiguration.mC_MATCH_CASE in lsESearchMode and lobstersearchconfiguration.CSearchConfiguration.mC_MATCH_WHOLE_WORD not in lsESearchMode):
                            if (not strAttrValue in str(xValue)):
                                #lsSearchResults.append(strPath)
                                bAllConditionSatisfied = False
                                break

                        # match whole word and dont match case
                        if (lobstersearchconfiguration.CSearchConfiguration.mC_MATCH_CASE not in lsESearchMode and lobstersearchconfiguration.CSearchConfiguration.mC_MATCH_WHOLE_WORD in lsESearchMode):
                            strLowerValue = xValue.lower()
                            strLowerSearchKeyword = strAttrValue.lower()
                            if (strLowerSearchKeyword != strLowerValue):
                                #lsSearchResults.append(strPath)
                                bAllConditionSatisfied = False
                                break

                        # match case and match whole word
                        if (lobstersearchconfiguration.CSearchConfiguration.mC_MATCH_CASE in lsESearchMode and lobstersearchconfiguration.CSearchConfiguration.mC_MATCH_WHOLE_WORD in lsESearchMode):
                            if (strAttrValue != str(xValue)):
                                #lsSearchResults.append(strPath)
                                bAllConditionSatisfied = False
                                break

                        if (lobstersearchconfiguration.CSearchConfiguration.mC_MATCH_CASE not in lsESearchMode and lobstersearchconfiguration.CSearchConfiguration.mC_MATCH_WHOLE_WORD not in lsESearchMode):
                            if (lobstersearchconfiguration.CSearchConfiguration.mC_REG_EXPR in lsESearchMode):
                                pass
                            else:
                                strLowerValue = xValue.lower()
                                strLowerSearchKeyword = strAttrValue.lower()
                                if (strLowerSearchKeyword not in strLowerValue):
                                    #lsSearchResults.append(strPath)
                                    bAllConditionSatisfied = False
                                    break
            if (bAllConditionSatisfied == True):
                lsSearchResults.append(strPath)
        print objTimer.stopTimer()

        return lsSearchResults

    """----------------------------------------------------------------------"""
    @staticmethod
    def MSUnionAttributes(lsTypes):
        setUnionList = set()
        if (lsTypes == None):
            setUnionList = CSearchManager.ms_dictTypeAndAttribute.get("AllTypes")
        else:
            for eType in lsTypes:
                    strType = lobstercvar.CVar.ms_lsStrTypes[eType]
                    setUsersAttribute = set(CSearchManager.ms_dictTypeAndAttribute.get(strType))
                    setUnionList = setUnionList.union(setUsersAttribute)
        return setUnionList

    """----------------------------------------------------------------------"""
