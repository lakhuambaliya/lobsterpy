#-------------------------------------------------------------------------------
# Name:        myfile
# Purpose:     this program contains class for handling file and its related operations
#
# Author:      Anirudh Sureka
#
# Created:     09-29-2013
# Copyright:   (c) Teledyne Lecroy Corporation
# Licence:     All rights reserved.
#-------------------------------------------------------------------------------

#imports
import LecroyUtil_portable as LecP
import os
import shutil

#class-name :- CFile
#purpose :- this file handles all the file-related operations
class CFile:
    #list of various modes supported
    ms_lsEditableFileModes = ["w", "a", "r+", "w+", "a+", "wb", "ab", "rb+", "wb+", "ab+", "r+b", "w+b", "a+b"]
    ms_lsNonEditableFileModes = ["r", "rb"]
    ms_lsstrValidFileModes = ms_lsEditableFileModes + ms_lsNonEditableFileModes

    def __init__(self, strFileNameWithCompletePath = None, strFileName = None, strDirectoryPath = None, strMode = 'r', bEnableAutoFlush = False, bEnableDebugMode = False):
        """
        Constructor :-

        Inputs      :- (i)    strFileNameWithCompletePath :- string containing complete pathname of the file to be opened
                                                               when this argument is passed, strFileName and strDirectoryPath
                                                               are not required.
                                                              eg. "c:\\temp\\check.htm".
                       (ii)   strFileName                 :- string containing the filenamewith extension. This argument is
                                                             required, when strFileNameWithCompletePath is not passed
                                                             eg. "check.htm"
                       (iii)  strDirectoryPath            :- string containing the path of the directory, containing directory.
                                                             It's required, when strFileNameWithCompletepath is not passed
                                                             eg. "c:\\temp"
                       (iv)   strMode                     :- Mode in which file have to be opened. By default, Read mode
                                                             eg. ["w", "a", "r+", "w+", "a+", "wb", "ab", "rb+", "wb+", "ab+", "r+b", "w+b", "a+b", "r", "rb"]

                       (v)    bEnableAutoFlush            :- boolean value true specifies  to flush data into file as soon as it's written
                                                             and false specifies to flush data in file, flush() when explicitly called by user

                       (vi)   bEnableDebugMode            :- boolean value specifying whether to enable debug mode for class.
                                                             Debug mode records all the method calls of the class by user class

        Outputs     :- does not return any values

        Purpose     :- initializes the data members of the class
        """

        #member variable which stores the directory path for file. eg. c:\\temp in case of c:\\temp\\check.htm
        self.m_strDirectoryPathOfFile = None
        #member variable storing only file name. eg. check.htm
        self.m_strRealFileNameWithExtension = None
        #member varialbe which stores the completepath for file. eg. c:\\temp\\check.htm
        self.m_strCompleteFilePath = None
        #the mode in which file is opened
        self.m_strFileMode = None
        #handle to the file which is opened
        self.m_fileObj = None
        #size of the file opened (in terms of bytes)
        self.m_iFileSize = 0
        #boolean value specifying whether to flush data as soon as it's written in file
        self.m_bIsAutoFlushEnabled = False
        #whether to store information about the call-stacks in the class or not
        self.m_bDebugModeEnabled = bEnableDebugMode
        #string which stores the call stacks for the class methods
        self.m_strDebugString = ""
        self.__MRecordDebugString__("init()")
        #if filename is passed then invoke the open method
        if (strFileNameWithCompletePath != None or strFileName != None):
            self.MOpenFile(strFileNameWithCompletePath, strFileName, strDirectoryPath, strMode, bEnableAutoFlush)

    """----------------------------------------------------------------------"""

    def MOpenFile(self, strFileNameWithCompletePath = None, strFileName = None, strDirectoryPath = None, strMode = 'r', bEnableAutoFlush = False):
        """
        Member Method :-

        Inputs        :- (i)    strFileNameWithCompletePath :- string containing complete pathname of the file to be opened
                                                               when this argument is passed, strFileName and strDirectoryPath
                                                               are not required.
                                                              eg. "c:\\temp\\check.htm".
                         (ii)   strFileName                 :- string containing the filenamewith extension. This argument is
                                                               required, when strFileNameWithCompletePath is not passed
                                                               eg. "check.htm"
                         (iii)  strDirectoryPath            :- string containing the path of the directory, containing directory.
                                                               It's required, when strFileNameWithCompletepath is not passed
                                                               eg. "c:\\temp"
                         (iv)   strMode                     :- Mode in which file have to be opened. By default, Read mode

                         (v)    bEnableAutoFlush            :- boolean value true specifies  to flush data into file as soon as it's written
                                                                and false specifies to flush data in file, flush() when explicitly called by user

        Outputs       :- does not return any values

        Purpose       :- This method opens the file passed to it as argument
        """
        self.__MRecordDebugString__("MOpenFile()")

        if LecP.IsEmptyOrNULLString(strFileNameWithCompletePath):
            if LecP.IsEmptyOrNULLString(strDirectoryPath) == True:
                strDirectoryPath = os.path.abspath(".")
            #if completepath of file is not passed, then check for directorypath and filename
            if self.__MValidateCompleteFileName__(strDirectoryPath, strFileName) == False:
                raise RuntimeError("CFile : CFile : Either strFileNameWithCompletePath or strFileName with strDirectoryPath have to be passed...")
            else:
                self.m_strDirectoryPathOfFile = strDirectoryPath
                self.m_strRealFileNameWithExtension = strFileName
                self.m_strCompleteFilePath = os.path.join(self.m_strDirectoryPathOfFile, self.m_strRealFileNameWithExtension)
        else:
            #in case when complete path of file is passed
            self.m_strCompleteFilePath = strFileNameWithCompletePath
            self.m_strDirectoryPathOfFile, self.m_strRealFileNameWithExtension = CFile.MSGetFileName(self.m_strCompleteFilePath, True)
            if self.__MValidateCompleteFileName__(self.m_strDirectoryPathOfFile, self.m_strRealFileNameWithExtension) == False:
                raise RuntimeError("CFile : Either Directory name or filename is invalid")

        #checking if the file open mode is valid
        if (strMode in CFile.ms_lsstrValidFileModes) == False:
            raise RuntimeError("CFile : Invalid mode passed. Valid modes are " + str(CFile.ms_lsstrValidFileModes))
        self.m_strFileMode = strMode

        #exception will be thrown by MClose() method, if none of the file is opened now
        try:
            self.MClose()
        except:
            pass

        #opening file
        self.m_fileObj = open(self.m_strCompleteFilePath, self.m_strFileMode)
        #recording the size of file(in bytes)
        self.m_iFileSize = CFile.MSGetFileSize(strCompleteFileName =  self.m_strCompleteFilePath)
        self.m_bIsAutoFlushEnabled = bEnableAutoFlush

        return

        """------------------------------------------------------------------"""

    def __MValidateCompleteFileName__(self, strDirPath, strFileName):
        """
        Member method :

        Inputs :- (i) strDirPath :- string containing the path of the directory containing filename

                  (ii) strFileName :- string containing the name of the file

        Outputs :- return boolean value True/False

        Purpose :- This method checks whether the directory-name and file-name passed to the class
                   are valid or not. If valid, return True else returns False.

                  eg. __MValidateCompleteFileName__("c:\\temp", "check.htm") --> True
                      __MValidateCompleteFileName__("c:\\temp", "") --> False
        """
        self.__MRecordDebugString__("__MValidateCompleteFileName__()")

        if LecP.IsEmptyOrNULLString(strDirPath) or LecP.IsEmptyOrNULLString(strFileName):
                return False

        return True
    """----------------------------------------------------------------------"""

    def __MRecordDebugString__(self, strMethodName):
        """
        Member Method :-

        Inputs :- (i) strMethodName :- name of method

        Outputs :- does not return any values

        Purpose :- This method records the method-name passed as argument to the stack-call
        """
        if self.m_bDebugModeEnabled == True:
            self.m_strDebugString += "CFile : " + strMethodName + " \n"

        return

        """------------------------------------------------------------------"""

    def MSetAutoFlush(self, bEnableAutoFlush = True):
        """
        Member Method :-

        Inputs  :- (i) bEnableAutoFlush :- boolean value specifying whether to turn on autoflushing

        Output :- does not return any values

        Purpose :- This method sets the autoflushing for the file

        """
        self.__MRecordDebugString__("MSetAutoFlush()")

        if self.__MIfFileObjAlive__():
            if self.__MIsFileOpenInEditMode__():
                #if any file is opened and it's in edit mode then setAutoflush true/false
                self.m_bIsAutoFlushEnabled = bEnableAutoFlush
            else:
                raise RuntimeError("CFile : Autoflush can be set for files which are opened in edit mode")
        else:
            raise RuntimeError("CFile : Either File is not opened or it's not in open state")

        return

        """------------------------------------------------------------------"""

    def __MIsFileOpenInEditMode__(self):
        """
        Member method :

        Inputs :- does not receive any inputs

        Outputs :- return boolean value True/False

        Purpose :- This method checks whether the file is opened for reading or writing purpose and
                   returns true if it's opened in write or append mode otherwise returns false
        """
        self.__MRecordDebugString__("__MIsFileOpenInEditMode__()")

        if self.__MIfFileObjAlive__():
            #if file open mode is present in list of editable file modes, then return True
            if (self.m_strFileMode in CFile.ms_lsEditableFileModes) == True:
                return True
            #if file open mode is present in list of non-editable file modes, then return False
            elif (self.m_strFileMode in CFile.ms_lsNonEditableFileModes) == True:
                return False
            else:
                raise RuntimeError("CFile : File Opened in invalid mode...")
        else:
            raise RuntimeError("CFile : File not opened or not in open state")

        """------------------------------------------------------------------"""

    def MClose(self):
        """
        Member Method :-

        Inputs        :- does not receive any inputs

        Outputs       :- does not return any values

        Purpose       :- This method closes the current file, if any opened
        """
        self.__MRecordDebugString__("MClose()")
        if self.__MIfFileObjAlive__():
            if self.__MIsFileOpenInEditMode__():
                #if file is opened in edit mode, then write any data, present buffer
                #to the file, prior to closing
                self.MFlush()
            self.m_fileObj.close()
        else:
            raise Exception("CFile : File object is None or It's already closed")

        return

    """----------------------------------------------------------------------"""

    def MFlush(self):
        """
        Member Method :-

        Inputs :- does not receive any inputs

        Outputs :- does not return any values

        Purpose :- flushes the output stream into file
        """
        self.__MRecordDebugString__("MFlush()")

        if self.__MIfFileObjAlive__():
            if self.__MIsFileOpenInEditMode__():
                #if file is opened in edit mode, then write any data, present buffer
                #to the file
                self.m_fileObj.flush()
            else:
                raise RuntimeError("CFile : MFlush() can be invoked on the files opened in the editable modes")
        else:
            raise RuntimeError("CFile : File not opened or not in open state")

        return

    """----------------------------------------------------------------------"""

    def MWrite(self, buffer, bAutoFlush = None):
        """
        Member Method :-

        Inputs :- (i) buffer :- It's the string or buffer or any other type object.
                                However it's preferred that it must be of type string.
                                if not of type string, then this method will convert it
                                into string type

                 (ii) bAutoFlush :- boolean value specifying that buffer object written to
                                    file must be flushed immediately

        Outputs:- does not return any values

        Purpose :- This method writes the object or buffer passed to it as argument
        """
        self.__MRecordDebugString__("MWrite()")
        if self.__MIfFileObjAlive__():
            if self.__MIsFileOpenInEditMode__():
                #converted buffer to string type, prior to writing it in file
                if (isinstance(buffer, str) == False):
                    buffer = str(buffer)
                self.m_fileObj.write(buffer)

                #if bAutoFlush argument is passed, then take into consideration
                #the value of bAutoFlush and not member variable self.m_bAutoFlushEnabled
                if bAutoFlush != None:
                    #if bAutoFlush is True, then flush data, as soon as you write
                    #data into file
                    if bAutoFlush == True:
                        self.MFlush()
                #if bAutoFlush argument is not passed, then take into consideration
                #the value of member variable self.m_bAutoFlushEnabled
                else:
                    if self.m_bIsAutoFlushEnabled == True:
                        self.MFlush()
            else:
                raise RuntimeError("CFile : File must be opened in edit mode for writing or appending data")
        else:
            raise RuntimeError("CFile : Either File not opened or it's not in opened state")

        return

        """------------------------------------------------------------------"""

    def __MIfFileObjAlive__(self):
        """
        Member Method :-

        Inputs : - does not receive any inputs

        Outputs :- return boolean value True/False

        Purpose :- This method checks if the file object is alive, that's whether the file is in open state
                    and returns True, if it's in opened state
        """
        self.__MRecordDebugString__("__MIfFileObjAlive__()")
        if self.m_fileObj == None or self.m_fileObj.closed == True:
            return False

        return True

    """----------------------------------------------------------------------"""

    def MClearContents(self):
        """
        Member Method :-

        Inputs :- does not receive any inputs

        Outputs :- does not return any values

        Purpose :- This method clears the contents of the file(does not delete it)
        """
        self.__MRecordDebugString__("MClearContents()")

        self.MChangeFileMode("w")

        return

        """------------------------------------------------------------------"""

    @staticmethod
    def MSGetFileSize(fileObj = None, strCompleteFileName = None):
        """
        Static Member Function :-

        Inputs                 :- (i) fileObj :- the handle to the file which is already opened.

                                  (ii) strCompleteFileName :- the complete absolute location of file
                                                    eg. "c:\\temp\\check.htm"

                                  Note :- Either fileObj is required or strCompleteFileName is required.
                                          Both are not required at the same time

        Outputs                :- returns the size of the file in terms of bytes

        Purpose                :- This method returns the size of the file passed to it as argument(in terms of bytes)
        """
        #if none of fileobject or filename is passed, then show error
        if fileObj == None and LecP.IsEmptyOrNULLString(strCompleteFileName) == True:
            raise RuntimeError("CFile : Either fileObj or strCompleteFileName is required")

        #if fileObject is passed
        if fileObj != None:
            #the file must be opened in read mode to find its size
            if fileObj.closed == False and fileObj.mode == 'r':
                return os.fstat(fileObj.fileno()).st_size
            else:
                raise RuntimeError("CFile : Either the File is opened in editable mode or it have been closed")

        #if filename is passed, then open that file to find its size
        objectOfFile = open(strCompleteFileName, "r")
        fileSize = os.fstat(objectOfFile.fileno()).st_size
        objectOfFile.close()

        return fileSize

    """----------------------------------------------------------------------"""

    @staticmethod
    def MSDoesFileExists(strAbsoluteFileName = None, strDirPath = None, strFileName = None):
        """
        Static Member  Function :-

        Inputs :- (i)   strAbsoluteFileName : - Absolution path of file. It's not required
                                            when strDirPath and strFileName are passed
                                            eg. "c:\\temp\\check.htm"

                  (ii)  strDirPath :- the directory containing the file. Not required when
                                        strAbsoluteFileName is passed
                                        eg. "c:\\temp"

                  (iii) strFileName :- the name of the file. Not required when strAbsoluteFileName
                                        is passed
                                        eg. "check.htm"

        Outputs :- returns boolean value True/False

        Purpse :- This method checks whether the file exists or not and returns True if
                  the file exists, else it returns False

        """
        #in case when absolute file name is passed
        if strAbsoluteFileName != None:
            exists = os.path.isfile(strAbsoluteFileName)
        #in case when directorypath and filenames are passed
        else:
            exists = os.path.isfile(os.path.join(strDirPath, strFileName))

        return exists

    """----------------------------------------------------------------------"""

    @staticmethod
    def MSDeleteFile(strAbsoluteFileName = None, strDirPath = None, strFileName = None):
        """
        Static Member Function :-

        Inputs :- (i)   strAbsoluteFileName : - Absolution path of file. It's not required
                                            when strDirPath and strFileName are passed
                                            eg. "c:\\temp\\check.htm"

                  (ii)  strDirPath :- the directory containing the file. Not required when
                                        strAbsoluteFileName is passed
                                        eg. "c:\\temp\\check.htm"

                  (iii) strFileName :- the name of the file. Not required when strAbsoluteFileName
                                        is passed
                                        eg. "check.htm"

        Outputs :- does not return any values

        Purpose :- This method deletes the file passed to it as argument, if it exits

        """
        #in case when complete path to file is passed as argument
        if strAbsoluteFileName == None:
            strTempFileName = os.path.join(strDirPath, strFileName)
        #in case when directory-path and filename is passed as argument
        else:
            strTempFileName = strAbsoluteFileName

        #if file exists, then remove it
        if CFile.MSDoesFileExists(strTempFileName):
            os.remove(strTempFileName)
        else:
            raise Exception("CFile : No such file exists")

        return

        """------------------------------------------------------------------"""

    @staticmethod
    def MSMoveFile(strCurrentFileLocation, strNewFileLocation):
        """
        Static Member Function :-

        Inputs :- (i) strCurrentFileLocation :- the current location of file
                                                eg. "c:\\temp\\check.htm"

                  (ii) strNewFileLocation :- the new location of file
                                                eg. "c:\\temp1\\check.htm"

        Outputs :- does not return any values

        Purpose :- This method moves the file from one location to another location
        """
        #if any of sourcelocation and destination location is missing, then show error
        if LecP.IsEmptyOrNULLString(strCurrentFileLocation) == True or LecP.IsEmptyOrNULLString(strNewFileLocation) == True:
            raise RuntimeError("CFile : Invalid source or destination file name")
        else:
            os.rename(strCurrentFileLocation, strNewFileLocation)

        return

        """------------------------------------------------------------------"""

    @staticmethod
    def MSCopyFile(strSourceFileLocation ,strDestinationFileLocation):
        """
        Static Member Function :-

        Inputs :- (i) strSourceFileLocation :- the location of the source file
                                                eg. "c:\\temp\\check.htm"

                  (ii) strDestinationFileLocation :- the location of the destination file
                                                eg. "c:\\temp1\\check.htm"

        Outputs :- does not return any values

        Purpose :- This method copy files from one location to another location
        """
        #if any of source location or destination location is missing, then show error message
        if LecP.IsEmptyOrNULLString(strSourceFileLocation) or LecP.IsEmptyOrNULLString(strDestinationFileLocation):
            raise RuntimeError("CFile : Invalid source or destination file location")
        else:
            shutil.copy(strSourceFileLocation, strDestinationFileLocation)

        return

        """------------------------------------------------------------------"""

    @staticmethod
    def MSRenameFile(strOldFileName ,strNewFileName):
        """
        Static Member Function :-

        Inputs :- (i) strOldFileName :- old name of the file
                                        eg. "c:\\temp\\check.htm"

                  (ii) strNewFileName :- new name of the file
                                        eg. "c:\\temp\\check1.htm"

        Outputs :- does not return any values

        Purpose :- This method renames the file
        """
        CFile.MSMoveFile(strOldFileName, strNewFileName)

        return

        """------------------------------------------------------------------"""

    @staticmethod
    def MSGetFileName(strAbsoluteFileName, bReturnPathOfDirContainingFile = False):
        """
        Static Member Function : -

        Inputs          : - (i) strAbsoluteFileName : - The Absolute Path of the file.
                                eg. C:\Python27\Lib\site-packages\yaml\cyaml.py

                            (ii)bReturnPathOfDirContainingFile : - boolean value specifying,
                                whether to return the path of directory containing file along
                                with the filename or filename alone have to be returned

        Output          : - (i) returns actual file-name.

        Purpose         : - This function extract the name of the file from the given
                            absolute path to the file

                            eg. MSGetFileName("c:\\temp\\check.htm") --> "check.htm"
                                MSGetFileName("c:\\temp\\check.htm", True) --> ("c:\\temp", "check.htm")
        """
        #stores the last index of slash in fileName. Default is -1
        iLastIndexOfSlash = -1
        #updating the value of iLastIndexOfSlash as "\\" or "/" are found in filename
        for iIdx, charC in enumerate(strAbsoluteFileName):
            if charC == "\\" or charC == "/":
                iLastIndexOfSlash = iIdx

        #when path of directory containing file have also to be returned
        if bReturnPathOfDirContainingFile:
            return (strAbsoluteFileName[ : iLastIndexOfSlash], strAbsoluteFileName[iLastIndexOfSlash + 1 : ])

        #when only filename with extension have to be returned
        return strAbsoluteFileName[iLastIndexOfSlash + 1 : ]

    """----------------------------------------------------------------------"""

    def MGetFileObject(self):
        """
        Member Method :-

        Inputs        :- does not receive any inputs

        Outputs       :- returns the file object or handle to the file, currently opened

        Purpose       :- This method is invoked by the users of this class, to get the handle of
                         current file opened
        """
        self.__MRecordDebugString__("MGetFileObject()")
        #if file object is alive, then return its reference or handle
        if self.__MIfFileObjAlive__() == False:
            raise RuntimeError("CFile : Reference to file object is Null")
        return self.m_fileObj

    """----------------------------------------------------------------------"""

    def MRead(self, iNoOfChars = -1):
        """
        Member Method :-

        Inputs        :- (i) iNoOfChars :- Number of bytes to read. Default is -1, implying that
                                           whole file have to be read

        Outputs       :- returns the file content in the form of string

        Purpose       :- This method is invoked to read from the file currently opened

        """
        self.__MRecordDebugString__("MRead()")
        #if no file is in open state, then show error message
        if self.__MIfFileObjAlive__() == False:
            raise RuntimeError("CFile : File not opened or it has been closed")

        #if filepointer is at the end of file, then show warning message
        if self.m_fileObj.tell() == self.m_iFileSize:
            print ("All the Bytes in the file have been read")
            return ""

        #if number of bytes to be read is non-positive, then show error message
        if iNoOfChars != -1:
            strFileContent = self.m_fileObj.read(iNoOfChars)
        else:
            strFileContent = self.m_fileObj.read()

        return strFileContent

        """------------------------------------------------------------------"""

    def MTellFilePointerPosition(self):
        """
        Member Method :-

        Inputs :- does not receive any inputs

        Outputs :- (i) iCurrentFilePointerPos :- position of current file pointer position in the file

        Purpose :- This method returns the position of file pointer in the file, if it's opened.
        """
        self.__MRecordDebugString__("MTellFilePointerPosition()")
        if not self.__MIfFileObjAlive__():
            raise RuntimeError("CFile : File not opened or it's in closed state")

        iCurrentFilePointerPos = self.m_fileObj.tell()

        return iCurrentFilePointerPos

        """------------------------------------------------------------------"""

    def MSetFilePointerPosition(self, iPositionInFile, iOffset):
        """
        Member Method :-

        Inputs :- (i) iPositionInFile :- refers to the position in file, with respect to which
                                         the file pointer have to be moved.
                                         Its possible value are :-

                                         (1) 0 - begining of file
                                         (2) 1 - current file pointer position
                                         (3) 2 - end of file

                  (ii) iOffset :- Number of units to move with reference to iPositionInfile

        Outputs :- does not return any values

        Purpose :- This method sets the file pointer to the position specified by the user
        """
        self.__MRecordDebugString__("MSetFilePointerPosition()")

        if self.__MIfFileObjAlive__() == False:
            raise RuntimeError("CFile : File not opened or it's in closed state")

        self.m_fileObj.seek(iOffset, iPositionInFile)

        return

        """------------------------------------------------------------------"""

    def __del__(self):
        """
        Destructor :-

        Inputs :- does not receive any inputs

        Outputs :- does not return any values

        Purpose :- releases the memory allocated for the member variables and closes the file
        """
        self.__MRecordDebugString__("__del__")
        if self.__MIfFileObjAlive__() == True:
            self.MClose()
        self.m_fileObj = None
        self.m_strCompleteFilePath = None
        self.m_strDirectoryPathOfFile = None
        self.m_strFileMode = None
        self.m_strRealFileNameWithExtension = None
        self.m_strDebugString = None

        """------------------------------------------------------------------"""

    def MChangeFileMode(self, strMode):
        """
        Member Method :-

        Inputs :- (i) strMode :- mode in which currently opened file have to be reopened.
                                 eg. r, w, a, r+, rb, etc.

        Outputs :- does not return any values

        Purpose :- this method changes the open mode of active file. Eg. if file is opened is in
                   'w' mode, then you can change its mode to 'r' through this method, for the
                   purpose of reading
        """
        self.__MRecordDebugString__("MChangeFileMode()")
        #checking if the new mode is valid mode
        if strMode in CFile.ms_lsstrValidFileModes:
            if self.m_strFileMode == strMode:
                return

            if self.__MIfFileObjAlive__():
                #closing the file, if it's open
                self.MClose()
            #opening the file in the new mode
            self.MOpenFile(self.m_strCompleteFilePath, strMode = strMode, bEnableAutoFlush = self.m_bIsAutoFlushEnabled)

        return

        """------------------------------------------------------------------"""

    def MSetDebugMode(self, bEnableDebugModeForClass = True, bClearPreviousCallStackInfo = False):
        """
        Member Method :-

        Inputs :- (1) bEnableDebugModeForClass :- boolean value specifying whether to
                                                  enable debug mode for the class

                  (2) bClearPreviousCallStackInfo :- boolean value specifying whether the
                                                  previous call stack information in the
                                                  debug string have to be removed or retained

        Outputs :- does not return any values

        Purpose :- This method enables/disables the debug mode for the class
        """
        self.__MRecordDebugString__("MSetDebugMode()")
        if bClearPreviousCallStackInfo == True:
            self.m_strDebugString = ""

        self.m_bDebugModeEnabled = bEnableDebugModeForClass

        return

        """------------------------------------------------------------------"""

    def MPrintDebugString(self):
        """
        Member Method :-

        Inputs :- does not receive any inputs

        Outputs :- does not return any values

        Purpose :- this method prints the value of the debug string
        """
        self.__MRecordDebugString__("MPrintDebugString()")

        print self.m_strDebugString

        return

        """------------------------------------------------------------------"""

    def MGetAbsoluteFileName(self):
        """
        Member Method :-

        Inputs :- does not receive any inputs

        Outputs :- return the currently opened file

        Purpose :- This method is used to get the filename recently opened with the help
                   of CFile object. If no file is opened, then it'll return None
        """
        return self.m_strCompleteFilePath

        """------------------------------------------------------------------"""

    def MGetMembersAsString(self):
        """
        Member Method :-

        Inputs :- does not receive any inputs

        Outputs :- does not return any values

        Purpose :- This method prints the values of the data members of the class
        """
        self.__MRecordDebugString__("MGetMembersAsString()")

        tempString = ""

        tempString +=  "m_bDebugModeEnabled              " + str(self.m_bDebugModeEnabled)
        tempString += "m_bIsAutoFlushEnabled            " + str(self.m_bIsAutoFlushEnabled)
        tempString += "m_fileObj                        " + str(self.m_fileObj)
        tempString += "m_iFileSize                      " + str(self.m_iFileSize)
        tempString += "m_strCompleteFilePath            " + str(self.m_strCompleteFilePath)
        tempString += "m_strDebugString                 " + str(self.m_strDebugString)
        tempString += "m_strDirectoryPathOfFile         " + str(self.m_strDirectoryPathOfFile)
        tempString += "m_strFileMode                    " + str(self.m_strFileMode)
        tempString += "m_strRealFileNameWithExtension   " + str(self.m_strRealFileNameWithExtension)

        return tempString

    @staticmethod
    def MSTest(strFileName = "c:\\temp\\temp.txt"):
        """
        Test Method :-

        Inputs :- (i) strFileName :- name of the file. you can pass your own name

        Outputs :- does not return any thing

        Purpose :- This method is intended to test CFile class
        """

        #first opening the file for writing purpose
        fileObj = CFile(strFileName = strFileName, strMode = "w", bEnableDebugMode = True)
        fileObj.MWrite("whenever virtue subsides, actually it's moving ahead towards its expansion\n")
        fileObj.MWrite("whenever virtue expands, it's actully moving towards its contraction", True)

        fileObj.MChangeFileMode("r")
        print "Current File-pointer position " + str(fileObj.MTellFilePointerPosition())
        print "File contents" + str(fileObj.MRead())
        print fileObj.MRead()
        print "setting file pointer to 6th position in the file"
        fileObj.MSetFilePointerPosition(0, 5)
        print "now the next two characters are '" + fileObj.MRead(2) + "' from current file position"

        fileObj.MClose()
        print "Does exits ? " + str(CFile.MSDoesFileExists(str(fileObj.MGetAbsoluteFileName())))
        print "Does exits ? " + str(CFile.MSDoesFileExists("c:\\asdf\\t.txt"))

        """
        The following given operations are test-cases for the utility methods
        of this class. These methods must have to be called - one at a time,
        so that you can clearly see their effect on the file, they are operating.
        Moreover, the filenames and paths are given according to the machine on
        which it was developed. So you may have to change the paths
        """

        strSourcePath = "c:\\temp\\check.htm"
        strDestinationPath = "c:\\work\\mangu\\ms.htm"

        print "Copying file from " + strSourcePath + " to " + strDestinationPath
        CFile.MSCopyFile(strSourcePath, strDestinationPath)

        strMoveSource = "c:\\work\\ms\\temp.htm"
        strMoveDestination = "c:\\temp\\check1.htm"

        print "Moving files from " + strMoveSource + " to " + strMoveDestination
        CFile.MSMoveFile(strMoveSource, strMoveDestination)

        strOldFileName = "c:\\temp\\check1.htm"
        strNewFileName = "c:\\temp\\checkRename.htm"

        print "renaming file from " + strMoveDestination + " to " + strNewFileName
        CFile.MSRenameFile(strOldFileName, strNewFileName)

        strFileToDelete = "c:\\temp\\check1.htm"
        print "Deleting " + strNewFileName
        CFile.MSDeleteFile(strNewFileName)

        strOldFileName = "temp.txt"
        strNewFileName =  "tempMS.txt"
        print "Renaming File"
        CFile.MSRenameFile(strOldFileName, strNewFileName)

        self.MFlushDebugString()

        """------------------------------------------------------------------"""


if __name__ == '__main__':
    CFile.MSTest(strFileName = "temp.txt")