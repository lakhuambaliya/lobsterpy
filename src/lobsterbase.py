#-------------------------------------------------------------------------------
# Name:        lobsterbase
# Purpose:     This module contains CLobsterBase class, which is the base class
#              of most of the classes in LobsterPy project
#
# Author:      lakhu
#
# Created:     03/02/2014
# Copyright:   (c) Account Prism Pvt. Ltd.
# Licence:     all_rights_reserved
#-------------------------------------------------------------------------------


#imports
import yaml
import mylogmanager
import LecroyUtil_portable as LecP
import myfile

#class-name     : CLobsterBase
#class-description : this class handles log related operations.
class CLobsterBase:

    def __init__(self, objCLogger = None):

        """
        Constructor :-

        Throws Exception : No

        Inputs :    (i) objCLogger : object of CLogger class, Used for writing logs

        Outputs :  does not return any values

        Purpose :   initialize the member variables to their default values

        """
        # initializing Logger object by receiving inputs
        if (objCLogger == None):
            self.m_objCLogger = mylogmanager.CLogger(
                                                    "c:\\temp\\temp.txt",
                                                    iBufSize = 0,
                                                    eLogMode = mylogmanager.CLogger.mC_FILELOG,
                                                    eLogLimit = mylogmanager.CLogger.mC_LOGMSGBASEDLIMIT,
                                                    iLogLimitAmount = 30
                                                   )
        # in case logger object is passed as argument, then assigning it to m_objCLogger
        else:
            self.m_objCLogger = objCLogger

        return

    """----------------------------------------------------------------------"""

    def MWhos(self, bEnableLog = False):

        """
        Public Member method :-

        Throws Exception : No

        Inputs :- (i) bEnableLog : boolean variable specifies whether to include
                                   MWhos() message in the logs

        Outputs :- (i) strObjectValue : string representing the MWhos output.

        Purpose :- This method prints a list of member variables, of type np arrays with sizes,
                   values which are int, doubles, sizes of lists, dict, tuples, and strings,
        """
        #   stored string containing whos() output in strObjectValue
        strObjectValue = LecP.whos(vars(self), bReturnAsString = True)
        #   logging in case bEnableLog is true
        if (bEnableLog == True):
            if (self.m_objCLogger != None):
                self.m_objCLogger.MLogInfo(strObjectValue)

            else:
                raise Exception("lobsterbase : object of CLogger is not available")

        return strObjectValue

    """------------------------------------------------------------------"""

    def MReadFromYaml(self, strFileNameWithExt = "c:\\temp\\dump.txt", objOfCFile = None):

        """
        public Member method :-

        Throws Exception : No

        Inputs :- (i) strFileNameWithExt :- name of file, in which the child class object was dumped.
                                            It's optional, if objOfCFile is passed.
                                            eg. obj.txt

                  (ii) objOfCFile  :- Object of CFile class, which contains handle to file, already opened.
                                      It's optional, if strFileNameWithExt is already passed.

        Outputs :- (i) self : return self object red from file

        Purpose :- This method reads the child object's information from file passed as argument and returns
                   the child class object
        """
        # show error message if both filename and object of CFile are not passed
        if ((LecP.IsEmptyOrNULLString(strFileNameWithExt) == True) and (objOfCFile == None)):
            raise Exception("lobsterbase.py : Both strFileNameWithExt and objCOfFile cannot be None")

        # if both filename and object of CFile are passed, then use object of CFile
        if ((LecP.IsEmptyOrNULLString(strFileNameWithExt) == False) and (objOfCFile != None)):
            print "lobsterbase.py : Warning :- Both strFileNameWithExt and ObjOfCFile arguments passed. Taking objOfCFile by default"

        if objOfCFile == None:
            # constructing CFile object, for the filename passed as argument
            objOfCFile = myfile.CFile(strFileName = strFileNameWithExt)

        # loading object from file and assigning its attributes to current object
        self = yaml.load(objOfCFile.MGetFileObject())

        return self

    """----------------------------------------------------------------------"""

    def MWriteYaml(self, strFileNameWithExt = None, objOfCFile = None):

        """
        Member method :-

        Throws Exception : Yes (i) when both filename and object of file are not passed

        Inputs :- (i) strFileNameWithExt :- name of file, in which the child class object was dumped.
                                            It's optional, if objOfCFile is passed.
                                            eg. obj.txt

                  (ii) objOfCFile  :- Object of CFile class, which contains handle to file, already opened.
                                      It's optional, if strFileNameWithExt is already passed.

        Outputs :- does not return any values

        Purpose :- This method writes the child class object passed as argument into file

        """
        # show error message if both filename and object of CFile are not passed
        if LecP.IsEmptyOrNULLString(strFileNameWithExt) == True and objOfCFile == None:
            raise Exception("lobsterbase : Both strFileNameWithExt and objCOfFile cannot be None")

        # if both filename and object of CFile are passed, then use object of CFile
        if LecP.IsEmptyOrNULLString(strFileNameWithExt) == False and objOfCFile != None:
            print "lobsterbase : Warning :- Both strFileNameWithExt and ObjOfCFile arguments passed. Taking objOfCFile by default"

        if objOfCFile == None:
            # constructing CFile object, for the filename passed as argument
            objOfCFile = myfile.CFile(strFileName = strFileNameWithExt, strMode = "w")

        tempLoggerObject = self.m_objCLogger

        self.m_objCLogger = None

        yaml.dump(self, objOfCFile.MGetFileObject())

        self.m_objCLogger = tempLoggerObject

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

        self.m_objCLogger = None

        return

    """----------------------------------------------------------------------"""

    @staticmethod
    def MSTestIListItem():

        """
        Tester Function :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : does not return any values

        Purpose : Testing Various methods of CLobsterBase class.

        """
        # creating object of CLobsterBase
        objCLobsterBase = CLobsterBase()
        # calling whose method
        print objCLobsterBase.MWhos(bEnableLog = True)
        #Writing object into file
        objCLobsterBase.MWriteYaml("c:\\temp\\dump.txt")
        # reading object from file
        objCLobsterBase = objCLobsterBase.MReadFromYaml("c:\\temp\\dump.txt")

        return

    """----------------------------------------------------------------------"""

if __name__ == '__main__':
    CLobsterBase.MSTestIListItem()