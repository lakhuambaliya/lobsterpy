#-------------------------------------------------------------------------------
# Name:        lobsterdirectory.py
# Purpose:     This module contains CCVarDirectory class, which represents directory
#              while stores CVars.
#
# Author:      Kruti
#
# Created:     04-02-2014
# Copyright:   (c) Account Prism Pvt. Ltd.
# Licence:     all_rights_reserved
#-------------------------------------------------------------------------------

#   imports
import LecroyUtil_portable as LecP
import mywxtreeitem as Node

#   class-name :- CCVarDirectory
#   class-description : This class extends ITreeItem class and stores information
#                       about CVarDirectory in which cvars are contained
class CCVarDirectory(Node.ITreeItem):

    def __init__(
                    self, strNodeName = None, lsStrChildDirectories = None, strParentDirectoryName = None,
                    lsStrSiblingDirectories = None, lsStrSiblingCVars = None, lsStrChildCVars = None
                ):

        """
        Constructor :-

        Throws Exception :- No

        Inputs :- (i) strNodeName : string type, name of the node or directory.
                                    eg. "EnableBWFilter"

                  (ii) lsStrChildDirectories : list of strings, which contains names of
                                                the child directories of current directory.
                                                eg. ["C4", "C3", "C2", "C1"]

                  (iii) strParentDirectoryName : string type, contains name of the
                                                parent directory with full path of current directory.
                                                eg.Parent.EnableBWFilter

                  (iv) lsStrSiblingDirectories : list of strings, which contains names of
                                                the sibling directories of current directory.
                                                eg. ["C4", "C3", "C2", "C1"]

                  (v) lsStrSiblingCVars : list of strings, contains names of sibling CVars of current directory.
                                                eg. ["EnableIFFTFilter"]

                  (vi) lsStrChildCVars : list of strings, contains names of the child CVars of current directory.
                                                eg. ["EnableIRRTFilter"].

        Outputs :- Does not return any value

        Purpose :-  Initializes its member variables to the values passed.

        """

        #   calling constructor of the parent class ITreeItem to initialize its member variables
        Node.ITreeItem.__init__(self, strParentDirectoryName, strNodeName, lsStrChildDirectories)

        #   member variable which contains list of names of sibling directories
        self.__m_lsStrSiblingDirectories__ = lsStrSiblingDirectories
        #   if lsStrSiblingDirectories is None, then initializing __m_lsStrSiblingDirectories by [].
        if (lsStrSiblingDirectories == None):
            self.__m_lsStrSiblingDirectories__ = []

        #   member variable which contains list of names of sibling CVars
        self.__m_lsStrSiblingCVars__ = lsStrSiblingCVars
        if (lsStrSiblingCVars == None):
            self.__m_lsStrSiblingCVars__ = []

        #   member variables which contains list of names of child CVars
        self.__m_lsStrChildCVars__ = lsStrChildCVars
        if (lsStrChildCVars == None):
            self.__m_lsStrChildCVars__ = []

        #   integer value, which represents the overall number of cvars, that are
        #   descendents of this cvar directory object.
        self.iNumberOfDecendantsCvars = 0

        return

    """----------------------------------------------------------------------"""

    def MHasChildCVars(self):

        """
        Member Function :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : (i) bHasChildCVars : returns true if current directory has
                                        child cvars otherwise returns false

        Purpose : This function is used to check whether current directory
                 has child cvars or not.

        """

        bHasChildCVars = True

        # if m_lsStrChildNodes does not have any child, then set bHasChildCVars to False
        if ((self.__m_lsStrChildCVars__ == None) or (len(self.__m_lsStrChildCVars__) == 0)):
            bHasChildCVars = False

        return bHasChildCVars

    """----------------------------------------------------------------------"""


    def MAppendChildCVar(self, strChildCVar = None) :

        """
        Member Function :-

        Throws Exception : Yes, throws exception when
                        (i)     strChildCVar is not of type string

                        (ii)    strChildCVar is empty or null string

        Inputs : (i) strChildCVar : String containing name of child Cvar.
                                    eg. "EnableIFFTFilter"

        Outputs : does not return any value

        Purpose : This method appends the strChildCVar to the list of child cvars
                  of current directory, only if it already doesn't contain any
                  cvar by that name
                  Note :- Don't use this method for adding sub-directories of current
                          CVarDirectory. For adding child directories, use MAppendChildNode()
                          method, defined in the ITreeItem, which is the parent class of
                          current directory.

        """

        # checking that strChildCVar must be of type string and it must not be empty
        if(not isinstance(strChildCVar, str) and LecP.IsEmptyOrNULLString(strChildCVar)):
            raise Exception("CDirectory.py : strChildCVar can neither be non-string parameter nor be empty/null string")

        # appends the child CVars to list of childs, only if
        # any cvar by that name is not the part of children of
        # current directory.
        if(strChildCVar not in self.__m_lsStrChildCVars__):
            self.__m_lsStrChildCVars__.append(strChildCVar)

        return

    """----------------------------------------------------------------------"""

    def MGetChildCVars(self):

        """
        Member Function :-

        Throws Exception :  No

        Inputs : does not receive any inputs

        Outputs : (i) self.__m_lsStrChildCVars__ : list of string containing names of child CVars

        Purpose : This method returns list of names of child CVar

        """

        return self.__m_lsStrChildCVars__

    """----------------------------------------------------------------------"""

    def MGetSiblingDirectories(self):

        """
        Member Function :-

        Throws Exception : No.

        Inputs : does not receive any input

        Outputs : (i) self.__m_lsStrSiblingDirectories__ : list of string, containing
                                                            names of the sibling directories
                                                            of the current CVarDirectory.

        Purpose : This method returns the list of names of sibling directories
                  of the current CVarDirectory.

        """

        return self.__m_lsStrSiblingDirectories__

    """----------------------------------------------------------------------"""

    def MGetSiblingCVars(self):

        """
        Member Function :-

        Throws Exception : No

        Inputs : It does not receive any values

        Outputs : (i) self.__m_lsStrSiblingCVars__ : list of string containing
                                                     names of the sibling CVars
                                                     of current CVarDirectory.

        Purpose : This method returns the list of the sibling CVars of current
                 CVarDirectory.

        """

        return self.__m_lsStrSiblingCVars__

    """----------------------------------------------------------------------"""

    def MGetAbsolutePath(self):

        """
        Member Function :-

        Throws Exception : No

        Inputs : does not receive any input

        Outputs : (i) strAbsolutePath : string type, which contains absolute path of the current directory

        Purpose : This method returns absolute path of the current directory

        """

        strAbsolutePath = None

        # if the node has a parent directory then its absolute path name will start from its parent directory
        strAbsolutePath = str(self.MGetParentNodeNameWithFullPath()) + "." + str(self.MGetNodeName())

        # if the node does not have parent directory then its absolute path will start from its own name
        if((self.MGetParentNodeNameWithFullPath() == None) or(self.MGetParentNodeNameWithFullPath() == '')):
            strAbsolutePath = self.MGetNodeName()

        return strAbsolutePath

    """------------------------------------------------------------------"""

    def MIncreaseNumberOfDecendantsCvars(self):

        """
        Member Function :-

        Inputs :- does not return any inputs

        Outputs :- does not return any values

        Purpose :- This method increments the number of descendent cvars of current
                    cvar directory by 1
        """

        self.iNumberOfDecendantsCvars += 1

        return

    """------------------------------------------------------------------"""

    def __del__(self):

        """
        Destructor :-

        Throws Exception : No

        Inputs : does not receive any input

        Outputs : does not return any value

        Purpose : It releases the memory of the member variables of the
                  CDirectory class and its parent class ItreeItem
        """

        self.__m_lsStrChildCVars__ = None
        self.__m_lsStrSiblingCVars__ = None
        self.__m_lsStrSiblingDirectories__ = None

        #   invoking the destructor of parent class.
        Node.ITreeItem.__del__(self)

    """----------------------------------------------------------------------"""

    #   TODO For Mangu :- not able to review MSTesterFunction() tester method, as test-cases
    #                     are already reviewed. Will review this method, whenever get time
    @staticmethod
    def MSTesterFunction():

        """
        Static Tester Function :-

        Inputs : does not receive any input

        Outputs : does not return any value

        Purpose : This method tests all the methods of CCVarDirectory class

        """

        try:
            objCCVarDirectory = CCVarDirectory(
                        "Current Node", ["Child1", "Child2", "Child3"],
                        "Parent.New Directory", ["SiblingDir1", "SiblingDir2"],
                        ["SiblingCVar1", "SiblingCVar2"],["ChildCVar1", "ChildCvar2"]
                        )
            print "Successfully executed"

        except:
            print "Fail"

        b = objCCVarDirectory.MHasChildCVars()

        print "Has children : " + str(b)

        try:
            print str(objCCVarDirectory.MGetChildCVars())
            print "Successfully executed"

        except:
            print "Fail"

        try:
            print str(objCCVarDirectory.MGetAbsolutePath())
            print "Successfully executed"

        except:
            print "Fail"

        try:
            print str(objCCVarDirectory.MGetSiblingDirectories())
            print "Successfully executed"

        except:
            print "Fail"

        try:
            print str(objCCVarDirectory.MGetSiblingCVars())
            print "Successfully executed"

        except:
            print "Fail"

        try:
            objCCVarDirectory2 = CCVarDirectory(
                                "New Node", ["Child"], None,
                                None, None, None
                                )
            print "Successfully executed"

        except:
            print "Fail"

        try:
            print str(objCCVarDirectory2.MGetAbsolutePath())
            print "Successfully executed"

        except:
            print "Fail"

        try:
            print str(objCCVarDirectory2.MGetParentNodeNameWithFullPath())
            print "Successfully executed"

        except:
            print "Fail"

        try:
            print str(objCCVarDirectory2.MGetSiblingDirectories())
            print "Successfully executed"

        except:
            print "Fail"

        try:
            print str(objCCVarDirectory2.MGetSiblingCVars())
            print "Successfully executed"

        except:
            print "Fail"

        try:
            print str(objCCVarDirectory2.MGetSiblingCVars())
            print "Successfully executed"

        except:
            print "Fail"

        try:
            print str(objCCVarDirectory2.MGetChildCVars())
            print "Successfully executed"

        except:
            print "Fail"

        try:
            print str(objCCVarDirectory2.MSetParentNodeNameWithFullPath("New Parent"))
            print "Successfully executed"

        except:
            print "Fail"

        try:
            print "Absolute path is : " + str(objCCVarDirectory2.MGetAbsolutePath())
            print "Successfully executed"

        except:
            print "Fail"

        try:
            #   abnormal input
            print str(objCCVarDirectory2.MSetParentNodeNameWithFullPath())
            print "Successfully executed"

        except:
            print "Fail"

        try:
            #   abnormal input
            print str(objCCVarDirectory2.MSetParentNodeNameWithFullPath(1))
            print "Successfully executed"

        except:
            print "Fail"

        return

    """----------------------------------------------------------------------"""

if __name__ == '__main__':
    CCVarDirectory.MSTesterFunction()
