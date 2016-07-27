#-------------------------------------------------------------------------------
# Name:        mywxtreeitem.py
# Purpose:      This class represents a single node in the treeview. This class
#               is designed to make a generic treeview(which extends wx.TreeCtrl).
#               This class is used as a input node to that treeview class.
#
# Author:      Kruti
#
# Created:     03-02-2014
# Copyright:   (c) Account Prism Pvt. Ltd.
# Licence:     all_rights_reserved
#-------------------------------------------------------------------------------


# imports
import LecroyUtil_portable as LecP
import lobsterbase

# class-name : ITreeItem
# class-description : This class represents each node, to be added to generic treeview class
class ITreeItem(lobsterbase.CLobsterBase):

    def __init__(self, strParentNodeNameWithFullPath = None, strNodeName = None, lsStrChildNodes = None):

        """
        Constructor :-

        Throws Exception : No

        Inputs :-   (i) strParentNodeNameWithFullPath :- string type, name of the
                                                        parent node with full path.
                                                        eg.Parent.Enable,
                                                           Parent/Enable

                    (ii) strNodeName :- string type, name of the node. eg. "EnableBWFilter"

                    (iii) lsStrChildNodes :- list of strings, contains the list of names of child nodes

        Outputs :- does not return any value

        Purpose :- Initializes the member variables by received parameters

        """

        #   member variable, which stores the name of node, with complete path
        self.m_strParentNodeNameWithFullPath = strParentNodeNameWithFullPath
        #   member variable, which stores the name of the node.
        self.m_strNodeName = strNodeName
        #   member variable, which stores the name of the child nodes
        self.m_lsStrChildNodes = lsStrChildNodes

        return

    """----------------------------------------------------------------------"""

    def MGetParentNodeNameWithFullPath(self):

        """
        Member Function :-

        Throws Exception :- No

        Inputs :- does not receive any input

        Outputs :- (i) self.m_strParentNodeNameWithFullPath :- string type, contains
                     name of the parent node of current node with full path
                     eg."Parent.EnableBWFilter", "Parent/EnableBWFilter"

        Purpose :- returns the name of the parent node of the current node with
                   full path

        """

        return self.m_strParentNodeNameWithFullPath

    """----------------------------------------------------------------------"""

    def MSetParentNodeNameWithFullPath(self, strParentNodeNameWithFullPath):

        """
        Member Function :-

        Throws Exception :- Yes, throws exception when
                        (i)     strParentNodeNameWithFullPath is not of type string

                        (ii)    strParentNodeNameWithFullPath is empty/null

        Inputs :- (i) strParentNodeNameWithFullPath : string type, string type,
                                                    contains name of the parent
                                                    node with full path.
                                                    eg.Parent.EnableBWFilter.

        Outputs :- does not return any value

        Purpose :- This method sets the name of the parent node of the
                   current node

        """

        #   raising exceptions, when strParentNodeNameWithFullPath is empty or null string
        if(type(strParentNodeNameWithFullPath) is not str or LecP.IsEmptyOrNULLString(strParentNodeNameWithFullPath)):
            raise Exception("ITreeItem.py : strParentNodeNameWithFullPath can neither be non-string parameter nor be empty/null string")

        self.m_strParentNodeNameWithFullPath = strParentNodeNameWithFullPath

        return

    """----------------------------------------------------------------------"""

    def MGetNodeName(self) :

        """
        Member Function :-

        Throws Exception : No

        Inputs :- does not receive any value

        Outputs :- (i) self.m_strNodeName :- string type, contains the name of the node. eg. "EnableBWFilter"

        Purpose :- returns the name of the node

        """

        return self.m_strNodeName

    """----------------------------------------------------------------------"""

    def MSetNodeName(self, strNodeName):

        """
        Member Function :-

        Throws Exception : Yes, throws exception when
                          (i)   strNodeName is not of type string

                          (ii)  strNodeName is empty/null string

        Inputs :- (i) strNodeName :- string type, contains the name of the node to be set

        Outputs :- does not return any value

        Purpose :- This method sets the name of the node.

        """

        # if type of strNodeName is not string
        if (type(strNodeName) is not str or LecP.IsEmptyOrNULLString(strNodeName)):
            raise Exception("ITreeItem.py : strNodeName can neither be non-string parameter nor be empty/null string")

        self.m_strNodeName = strNodeName

        return

    """------------------------------------------------------------------"""

    def MGetChildNodes(self):

        """
        Member Function :-

        Throws Exception : No

        Inputs :- does not receive any input

        Outputs :- (i) self.m_lsStrChildNodes :- list of string, contains the names of the child nodes

        Purpose :- This method returns the list of the names of child nodes

        """

        return self.m_lsStrChildNodes

    """----------------------------------------------------------------------"""

    def MHasChildNodes(self):

        """
        Member Function :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : (i) bHasChildNodes : returns true if it has child nodes otherwise returns false

        Purpose : This function is used to check whether a node has child nodes or not.

        """

        bHasChildNodes = True

        # if m_lsStrChildNodes does not have any child
        if((self.m_lsStrChildNodes == None) or (len(self.m_lsStrChildNodes) == 0)):
            bHasChildNodes = False

        return bHasChildNodes

    """----------------------------------------------------------------------"""

    def MAppendChildNode(self, strChildNode):

        """
        Member Function :-

        Throws Exception : Yes, throws exception when
                          (i)   strChildNode is not of type string

                          (ii)  strChildNode is empty/null string

        Inputs :- (i) strChildNode :- string containing name of child node

        Outputs :- does not return any value

        Purpose :- This method appends the child node (i.e. a child directory to
                    the current node and not the child CVar item/ file item.) to the list of
                    child nodes of current node.

        """

        #   raising exception, when strChildNode is empty or null string or it's not of type string
        if(type(strChildNode) is not str or LecP.IsEmptyOrNULLString(strChildNode)):
            raise Exception("ITreeItem.py : strNodeName can neither be non-string parameter nor be empty/null string")

        #   appending the child node to the list of child nodes only if give child node
        #   is not the part of list of child nodes of this node
        if(strChildNode not in self.m_lsStrChildNodes):
            self.m_lsStrChildNodes.append(strChildNode)

        return

    """------------------------------------------------------------------"""

    def __del__(self):

        """
        Destructor :-

        Throws Exception : No

        Inputs : deos not receive any inputs

        Outputs : does not return any values

        Purpose : release memory allocated for member variables

        """

        self.m_strParentNodeNameWithFullPath = None
        self.m_strNodeName = None
        self.m_lsStrChildNodes = None

        #   invoking parent class constructor
        lobsterbase.CLobsterBase.__del__(self)

    """------------------------------------------------------------------"""

    #   TODO For Mangu :- not able to review MSTestMethod() tester method, as test-cases
    #                     are already reviewed. Will review this method, whenever get time
    @staticmethod
    def MSTestMethod():

        """
        Static Tester Function :-

        Inputs :- does not receive any input

        Outputs :- does not return any value

        Purpose :- This method tests all the methods of ITreeItem

        """

        objCLobsterBase = lobsterbase.CLobsterBase()

        objITreeItem = ITreeItem(strParentNodeNameWithFullPath = "CVarDirectory",
                    strNodeName = "CVar", lsStrChildNodes = ["A", "B", "C"])

        try:
            objITreeItem.MSetParentNodeNameWithFullPath("Parent.Parent Directory")
            print
        except:
            print "Fail"


        print objITreeItem.MGetParentNodeNameWithFullPath()
        try :
            #   in case of normal input
            objITreeItem.MSetNodeName("New Node")
            print "Name of the node is : " + str(objITreeItem.MGetNodeName())   # output : Name of the node is : New Node
        except:
            print "Fail"

        try :
            #   in case of abnormal input
            objITreeItem.MSetNodeName(1)
            print "Name of the node is : " + str(objITreeItem.MGetNodeName())

        except:
            print "Fail"

        try:
            #   in case of normal input
            objITreeItem.MAppendChildNode("R")
            print "Child nodes are : " + str(objITreeItem.MGetChildNodes()) # output : Child nodes are : ['A', 'B', 'C', 'R']

        except:
            print "Fail"

        try:
            #   in case of normal input
            objITreeItem.MAppendChildNode("Q")
            print "Child nodes are : " + str(objITreeItem.MGetChildNodes()) # output : Child nodes are : ['A', 'B', 'C', 'R', 'Q']

        except:
            print "Fail"

        try:
            #   in case of normal input
            objITreeItem.MAppendChildNode("1")
            print "Child nodes are : " + str(objITreeItem.MGetChildNodes()) # output : Child nodes are : ['A', 'B', 'C', 'R', 'Q', '1']

        except:
            print "Fail"

        try:
            #   In case of abnormal input
            objITreeItem.MAppendChildNode("a")    # Exception : MSetNodeName() accepts only string as argument

        except:
            print "Fail"

        try:
            objITreeItem.MAppendChildNode(2)    # Exception : MSetNodeName() accepts only string as argument

        except :
            print "Fail"

        return

        """------------------------------------------------------------------"""

if __name__ == '__main__':
    ITreeItem.MSTestMethod()