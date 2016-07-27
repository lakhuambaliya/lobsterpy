#-------------------------------------------------------------------------------
# Name:        mylogmanager.py
# Purpose:     This module contains CLogger class, which handles all the log related operations
#
# Author:      Anirudh Sureka
#
# Created:     10-12-2013
# Copyright:   (c) Teledyne Lecroy 2013
# Licence:     All_Rights_Reserved
#-------------------------------------------------------------------------------


#imports
import datetime
import myfile
import inspect
import time
import multiprocessing
import threading
import numpy as np
from win32api import OutputDebugString
import LecroyUtil_portable as LecP
import myprocessmanager

class CLogEvent():
    mC_INFO = 0
    mC_WARN = 1
    mC_ERROR = 2
    mC_strEvents = ["INFO", "WARNING", "ERROR"]
    def __init__(self, iEvtId, strEvtSource, strEvtMessage = None, eEvtType = mC_ERROR, startTime = None):
        """
        Constructor :-

        Inputs :- (i) iEvtId : - Id of the event; incremental counter

                  (ii) strEvtSource :- source of the event, i.e., the name of the method where logging functions are invoked

                  (iii) strEvtMessage :- Event message

                  (iv) eEvtType :- type of event. By default error

                  (v) startTime :- time with respect to which relative time for the event have to calculated

        Outputs :- does not return any values

        Purpose :- initializes the data-members to the values passed as parameters
        """
        self.__MInitializeMembersToDefaultVal__()

        self.m_iEvtId = iEvtId
        self.m_strEvtSrcObj = strEvtSource
        self.m_strEvtMsg = strEvtMessage
        self.m_eLogEvtType = eEvtType
        #converted event-time in seconds format to timestamp object
        currentTime = LecP.cTimer.filetime_to_dt(self.m_evtDate)
        #calculating the relative time. ConvertDoubleToHMS returns HH:MM:SS. But as the millisecond resolution is
        #required, we calculated, explicitly till the millisecond resolution
        self.m_strRelativeStartTime = LecP.ConvertDoubleToHMS((currentTime - startTime).seconds, bReturnSecsAsIntegerVal = True)
        self.m_strRelativeStartTime += "." + LecP.FormatString((currentTime - startTime).microseconds, 6, '0')

        return

        """------------------------------------------------------------------"""

    def MSetEvtMsg(self, strEvtMsg):
        """
        Member Method :-

        Inputs :- (i) strEvtMsg :- The message to be logged

        Outputs :- does not return any values

        Purpose :- sets the event message
        """
        #setting the event message
        self.m_strEvtMsg = strEvtMsg

        return

        """------------------------------------------------------------------"""

    def __MInitializeMembersToDefaultVal__(self):
        """
        Member Method :-

        Inputs :- does not receive any inputs

        Outputs :- does not return any values

        Purpose :- initializes the member variables of the class to the default values
        """
        #By default, the event type is error
        self.m_eLogEvtType = CLogEvent.mC_ERROR
        #id of the event
        self.m_iEvtId = -1
        dtObj = datetime.datetime.now()
        #stores the date of event. It's the time elapsed in seconds(seconds) since january 1, 1970 and millisecond of
        #current time stamp.For more information, refer cTimer.dt_to_filetime() in Lecroy_Util_Portable file
        self.m_evtDate =  LecP.cTimer.dt_to_filetime(dtObj)
        #stores the source of this event. It's generally the name of the object and its method from where
        #the logging operations are performed
        self.m_strEvtSrcObj = None
        #the message of the log event
        self.m_strEvtMsg = ""
        #the time-relative to the start of logging. It's the time tuple (HH:MM:SS:milliseconds)
        self.m_strRelativeStartTime = None

        return

        """------------------------------------------------------------------"""

    def MGetLogTimeStamp(self):
        """
        Member Method :-

        Inputs :- does not receive any inputs

        Outputs :- returns the timestamp of the log. eg. 130278781902010000L (Unix UTC time)

        Purpose :- This method is used to get the time, when logevent has occured
        """

        return self.m_evtDate

        """------------------------------------------------------------------"""

    def MGetMembersAsString(self):
        """
        Member Method :

        Inputs :- does not receive any inputs

        Outputs :- does not return any values

        Purpose :- Returns the members as String
        """
        strTemp = ""

        # '#' is the delimiter between the columns.
        strTemp += "%-5s" % str(self.m_iEvtId) + "#" + "%-35s" %LecP.cTimer.filetime_to_dt(self.m_evtDate).strftime("%Y-%m-%d %H:%M:%S.%f") + "#" + "%-20s" %self.m_strRelativeStartTime
        strTemp += "#%-10s" % CLogEvent.mC_strEvents[self.m_eLogEvtType] + "#" + "%-40s" %str(self.m_strEvtSrcObj) + "#" + "%-50s" %self.m_strEvtMsg

        return strTemp

        """------------------------------------------------------------------"""

    def MSetRelStartTime(self, strTime):
        """
        Member Method :-

        Inputs :- (i) strTime :- string containing time in 'HH:MM:SS:milliseconds' format

        Outputs :- does not return any values

        Purpose :- This method sets the value of relative time for the event object
        """

        self.m_strRelativeStartTime = strTime

        return

        """------------------------------------------------------------------"""

    @staticmethod
    def MSGetTimeStampsAsListFromLogs(lsObjLogEvt):
        """
        Static Member Method :-

        Inputs :- (i) lsObjLogEvt :- list of Event objects

        Outputs :- list of timestamps of each logevent

        Purpose :- This method receives the list of event objects, extract the timestamp of each log and
                    store it in list and returns the list
        """
        lsUTCTimestamps = []

        for objLogEvt in lsObjLogEvt:
            lsUTCTimestamps.append(objLogEvt.m_evtDate)

        return lsUTCTimestamps

        """------------------------------------------------------------------"""
    def __del__(self):
        """
        Destructor :-

        Inputs :- does not receive any inputs

        Outputs :- does not return any values

        Purpose :- deallocates the memory allocated to its member variables

        """
        self.m_evtDate = None
        self.m_strRelativeStartTime = None
        self.m_strEvtMsg = None
        self.m_strEvtSrcObj = None

        """------------------------------------------------------------------"""

#Class-name :- CLogger
#Description :- This class handles all the logs related operations
class CLogger():
    #static constant members representing logging modes
    mC_FILELOG = 1              #represents logs to be written in file
    mC_WINDOWSLOG = 2           #represents logs to be written in windows log buffer
    mC_PARALLELPROCESSLOG = 3   #represents logs to be written in file for parallel processes running concurrently
    mC_LSVALIDLOGGINGMODES = [mC_FILELOG, mC_WINDOWSLOG, mC_PARALLELPROCESSLOG]

    mC_TIMEBASEDLIMIT = 1       #represents Limit set on logging, based on number of seconds
    mC_LOGMSGBASEDLIMIT = 2     #represents Limit set on logging, based on number messages logged
    mC_NOLIMIT = 3              #represents no limit on logging. Default option
    mC_LSVALIDLIMITMODES = [mC_TIMEBASEDLIMIT, mC_LOGMSGBASEDLIMIT, mC_NOLIMIT]

    def __init__(self, strFileNameWithExtension = None, fileObj = None, queueObj = None, mpLockObj = None, iBufSize = 0,
                eLogMode = mC_WINDOWSLOG, eLogLimit = mC_NOLIMIT, iLogLimitAmount = -1):
        """
        Constructor :-

        Inputs :- (i) strFileNameWithExtension :- name of the log file. eg. "tempLog.txt"
                                                   optional when fileObj is passed

                  (ii) fileObj :- CFile object of file opened for writing. It's optional if strFileNameWithExtension is passed

                  (iii) queueObj :- object of type multiprocessing.queue

                  (iv) mpLockObj :- object of type multiprocessing.lock

                  (v) iBufSize :- size of the buffer. It defines the number of log statements, that should be
                                    in the buffer, prior to writing them in the file

                  (vi) eLogMode :- Logging mode. It's mC_FILELOG when logging have to be done in FiLE and mC_WINDOWSLOG when logging
                                   have to done in windows log buffer

                  (vii) eLogLimit :- specifies any type of limit imposed on logging operation. It's values are
                                     (i) mC_TIMEBASEDLIMIT, (ii) mC_LOGMSGBASEDLIMIT, (iii) mC_NOLIMIT

                  (viii) iLogLimitAmount :- It's the amount, by which you want to restrict logging operation.
                                            It's in seconds if eLogLimit is mC_TIMEBASEDLIMIT and in number of
                                            logs in case of mC_LOGMSGBASEDLIMIT
        Outputs :- does not return any values

        Purpose :- initialize the member variables to their default values
        """
        #lock object. It's used in case when multiple threads tries to modify the
        #data members of the class or perform mutually exclusive operation at same time
        self.m_lockObj = multiprocessing.Lock()

        #initializing all the members to default value
        self.__MInitializeMembersToDefaultVal__()

        #setting the logging mode
        if eLogMode in CLogger.mC_LSVALIDLOGGINGMODES:
            self.m_eLogMode = eLogMode
        else:
            raise RuntimeError("mylogmanager.py : Invalid logging mode pass")

        #setting the logging limit mode
        if eLogLimit in CLogger.mC_LSVALIDLIMITMODES:
            self.m_eLogLimit = eLogLimit
            self.m_iLogLimitInMsgOrSeconds = iLogLimitAmount
        else:
            raise RuntimeError("mylogmanager.py : Invalid logging limit mode passed")

        #in case of logging in parallel environment, multiprocessing.Queue and multiprocessing.Lock object
        #must be passed as argument in constructor
        if eLogMode == CLogger.mC_PARALLELPROCESSLOG:
            if (queueObj != None and mpLockObj != None):
                self.m_queueObj = queueObj
                self.m_mpLock = mpLockObj
            else:
                raise RuntimeError("mylogmanager.py : In case of ParallelProcessing Log, multiprocessing.Queue object and multiprocessing.Lock have to be passed as argument")

        #setting the log file, if it's passed
        if eLogMode != CLogger.mC_PARALLELPROCESSLOG:
            self.__MSetLogFile__(strFileNameWithExtension, fileObj)

        #setting the buffer size
        if iBufSize > 0:
            self.m_iBufSize = iBufSize

        return

        """------------------------------------------------------------------"""

    def __MInitializeMembersToDefaultVal__(self):
        """
        protected Member Method :-

        Inputs :- does not receive an inputs

        Outputs :- does not return any values

        Purpose :- This method sets the member variables of the class to their default values
        """
        #requested and acquired lock, before modifying member variables of class
        self.m_lockObj.acquire()

        #object of CFile type. It's used, in case logging have to be done in file
        self.m_fileObj = None

        #object of multiprocess.Queue type. It's used, in case of logging in multiprocessing environments
        self.m_queueObj = None

        #object of multiprocessing.Lock type. It's used, in case of logging in multiprocessing environments
        self.m_mpLock = None

        #name of log file
        self.m_strFileNameWithExtension = ""

        #size of logevent buffer
        self.m_iBufSize = 0

        #member variables meant for assigning a unique identifier to each event
        self.m_iEvtCount = 0

        #list for storing logevent object
        self.__m_lsLogEvtBuffer__ = []

        #by default, the logging mode is windows log
        self.m_eLogMode = CLogger.mC_WINDOWSLOG

        # Type of limit imposed on logging operation
        self.m_eLogLimit = CLogger.mC_NOLIMIT

        # Maximum Number of seconds/logs, that can logged or for which logging can be done
        # In case of mC_NOLIMIT, there is not limit on logging operation
        self.m_iLogLimitInMsgOrSeconds = -1

        #member variable which records the start time, when logging have started.
        #start time is required in order to calculate the relative time for each
        #log event object
        self.m_startTime = None

        #integer value specifying number of messages logged. It's used in LOGBASEDLIMIT on logging
        self.m_iNumOfMessagesLogged = 0

        #releasing lock
        self.m_lockObj.release()

        return

        """------------------------------------------------------------------"""

    def __MSetLogFile__(self, strFileNameWithExtension, fileObj):
        """
        protected member method :-

        Inputs :- (i) strFileNameWithExtension :- name of the log file. eg. "tempLog.txt"
                                                   optional when fileObj is passed

                  (ii) fileObj :- handle to the file already opened for writing. It must be the object
                                    of CFile class defined in myfile.py module. It's optional when
                                    strFileNameWithExtension is passed

        Outputs :- boolean value True - when log file have been set successfully, False - otherwise

        Purpose :- This method sets the log file. It's invoked from either constructor or from
                    MSetLogFile() method for setting log files.

                    Note :- This method is not supposed to be invoked directly with the object of this class,
                            as its not public
        """


        # if already one file is opened for writing log files, then close it
        # before setting another file for writing log files
        self.m_lockObj.acquire()

        if (self.m_fileObj != None):
            if (self.m_fileObj.__MIfFileObjAlive__() == True):
                self.m_fileObj.MClose()
                print "Warning : mylogmanager.py : already a file was opened for writing logs"

        self.m_lockObj.release()

        if fileObj != None:
            # if CFile object is passed as argument, then acquire the lock
            # and set it as m_fileObj
            self.m_lockObj.acquire()

            self.m_fileObj = fileObj

            self.m_lockObj.release()
            # returning true indicates success of setting log file operation
            return True

        else:
            # if filename is passed, then acquire the lock and set it as log file
            if LecP.IsEmptyOrNULLString(strFileNameWithExtension) == False:
                self.m_lockObj.acquire()

                self.m_fileObj = myfile.CFile(strFileName = strFileNameWithExtension, strMode = "a")

                self.m_lockObj.release()

                return True

        #should not reach here. returning False means log file have not been set successfully
        return False

        """------------------------------------------------------------------"""

    def MSetLogFile(self, strFileNameWithExtension = None, objFile = None):
        """
        public member method :-

        Inputs :-(i) strFileNameWithExtensions :- name of the log file. eg. "tempLog.txt"
                                                   optional when objFile is passed

                 (ii) objFile :- handle to the file already opened for writing.
                                  optional when strFileNameWithExtension is passed

        Outputs :- does not return any values

        Purpose :- This method sets the log file, in case it's not passed in constructor.

                   Note :- This method has to be invoked with the object of this class instead of,
                           __MSetLogFile__ as it's public.
        """
        #invoking __MSetLogFile__ to set the log file
        bResult = self.__MSetLogFile__(strFileNameWithExtension, objFile)

        #if log file has not been set successfully, then raise RuntimeError
        if bResult == False:
            raise RuntimeError("mylogmanager.py : log file not set successfully")
        else:
            #setting the logmode to FILELOG, because, MSetLogFile() method will be
            #invoked only when FILEBASED logging is used
            self.m_eLogMode = CLogger.mC_FILELOG

        return

        """------------------------------------------------------------------"""

    def MLogWarn(self, strMsg):
        """
        Member Method :-

        Inputs :- (i) strMsg :- The message to be logged

        Outputs :- does not return any values

        Purpose :- This method logs the strMsg as warning
        """
        #got the name of the method from where MLogWarn() have been invoked

        strCallerFunctionName = LecP.GetCallerFunctionName()

        self.MLog(strMsg, strCallerFunctionName, CLogEvent.mC_WARN)

        return

        """------------------------------------------------------------------"""

    def MLogError(self, strMsg):
        """
        Member Method :-

        Inputs :- (i) strMsg :- The message to be logged

        Outputs :- does not return any values

        Purpose:- This method logs the strMsg as error
        """
        #got the name of the method from where MLogError() have been invoked
        strCallerFunctionName = LecP.GetCallerFunctionName()

        self.MLog(strMsg, strCallerFunctionName, CLogEvent.mC_ERROR)

        return

        """------------------------------------------------------------------"""

    def MLogInfo(self, strMsg):
        """
        Member Method :-

        Inputs :- (i) strMsg :- The message to be logged

        Outputs :- does not return any values

        Purpose:- This method logs the strMsg as information
        """

        #got the name of the method from where MLogInfo() have been invoked
        strCallerFunctionName = LecP.GetCallerFunctionName()

        self.MLog(strMsg, strCallerFunctionName, CLogEvent.mC_INFO)

        return

        """------------------------------------------------------------------"""

    def MLog(self, strMsg, strEvtSource, eEvtType):
        """
        public member method :-

        Inputs : - (i) strMsg :- buffer or String that have to be stored in log file

                   (ii) strEvtSource :- source of event. It's in <class>.<method>() form, where class name is
                                        is the class, whose method is performing the logging operation, and the
                                        method is the name of method of that class.

                   (iii) eEvtType :- the type of logevent. Eg. It can be warning, error, etc. Possible values
                                     are mC_ERROR, mC_WARN, mC_INFO

        Outputs :- does not return any values

        Purpose :- This class records the log statements into log file
        """
        self.m_lockObj.acquire()

        if self.m_iNumOfMessagesLogged == 0:
            # registering the startup time, when first message is logged
            self.m_startTime = datetime.datetime.now()

        self.m_lockObj.release()

        #if buffer is already full, then write its content to file or windows buffer
        if len(self.__m_lsLogEvtBuffer__) >= self.m_iBufSize:
            self.MWriteBuffer()

        #check if the logging limit have expired.
        if self.MCanLog() == False:
            return

        tempMsg = strMsg

        if str(type(strMsg)) == "<type 'list'>" or str(type(strMsg)) == "<type 'numpy.ndarray'>":
            tempMsg = ""
            #if the type of msg is list or numpy array, then iterate through each of its element
            #and if each element is of type numpy array, then write the whole numpy array with the
            #help of WriteNumpyArray function, else convert the element into string
            for iCounter in range(0, len(strMsg)):
                #if numpy array is passed, then convert it into string
                if str(type(strMsg[0])) == "<type 'numpy.ndarray'>":
                    tempMsg += LecP.WriteNumpyArray(strMsg[iCounter], fileName = None, bReturnString = True)
                    tempMsg += "\n"
                else:
                    tempMsg += str(strMsg[iCounter]) + ' '

        #acquired the lock
        self.m_lockObj.acquire()
        #incrementing event count
        self.m_iEvtCount += 1
        #created CLogEvent object for storing the log event details
        logObj = CLogEvent(self.m_iEvtCount, strEvtSource, tempMsg, eEvtType, self.m_startTime)
        #appended the CLogEvent object to list of logevents
        self.__m_lsLogEvtBuffer__.append(logObj)

        #incrementing number of messages logged
        self.m_iNumOfMessagesLogged += 1

        #released the lock
        self.m_lockObj.release()

        return

        """------------------------------------------------------------------"""

    def MClearCachedLog(self):
        """
        public member method :-

        Inputs :- does not receive any inputs

        Outputs :- does not return any values

        Purpose :- This method clears the logs present in buffer, to prevent them from being written to log file
        """
        #acquired the lock
        self.m_lockObj.acquire()
        #cleared the logevent buffer
        self.__m_lsLogEvtBuffer__ = []
        #released the lock
        self.m_lockObj.release()

        return

        """------------------------------------------------------------------"""

    def MCanLog(self):
        """
        Member Method :-

        Inputs :- does not receive any inputs

        Outputs :- true - when it's valid to log, false otherwise

        Purpose :- It's used to check, whether it's valid to log any more messages.
        """
        #in case of NOLIMIT, returns true
        if self.m_eLogLimit == CLogger.mC_NOLIMIT:
            return True

        #in case of LOGMSGBASEDLIMIT, returns false, if specified number of messages have already been
        #logged, else returns true
        elif self.m_eLogLimit == CLogger.mC_LOGMSGBASEDLIMIT:
            if self.m_iNumOfMessagesLogged >= self.m_iLogLimitInMsgOrSeconds:
                return False
            else:
                return True

        #in case of time based logging limit
        elif self.m_eLogLimit == CLogger.mC_TIMEBASEDLIMIT:
            # in case of any messages being written to buffer, then take the relative time of recent logevent object added to buffer
            # to calculate timeelapsed
            if len(self.__m_lsLogEvtBuffer__ )> 0:
                timeStampOfRecentLogEvt = LecP.cTimer.filetime_to_dt(self.__m_lsLogEvtBuffer__[len(self.__m_lsLogEvtBuffer__) - 1].m_evtDate)
            # in case, no item have been added to buffer, then take current time as reference to calculate relative time
            else:
                timeStampOfRecentLogEvt = datetime.datetime.now()

            # calculated timeelapsed
            iTimeElapsed = (timeStampOfRecentLogEvt - self.m_startTime).seconds

            if iTimeElapsed >= self.m_iLogLimitInMsgOrSeconds:
                return False
            else:
                return True

        else:
            pass #the execution should never reach here

        return False

        """------------------------------------------------------------------"""

    def MWriteBuffer(self):
        """
        Member Method :-

        Inputs :- does not receive any inputs

        Outputs :- does not return any values

        Purpose :- writes the content of buffer to the file and clears the buffer
        """
        #acquired the lock
        self.m_lockObj.acquire()
        #iterating through each logevent object in the buffer
        for iCounter in range(0, len(self.__m_lsLogEvtBuffer__)):
            #if windows log mode is enabled, write in windows buffer
            if self.m_eLogMode == CLogger.mC_WINDOWSLOG:
                OutputDebugString("%-5s" %str(self.__m_lsLogEvtBuffer__[iCounter].m_iEvtId) + " " + "%-15s" %str(self.__m_lsLogEvtBuffer__[iCounter].m_strRelativeStartTime) + " " + "%-10s" %CLogEvent.mC_strEvents[self.__m_lsLogEvtBuffer__[iCounter].m_eLogEvtType] + ' ' +  "%-15s" %self.__m_lsLogEvtBuffer__[iCounter].m_strEvtSrcObj
                                    + ' ' + "%-50s" %self.__m_lsLogEvtBuffer__[iCounter].m_strEvtMsg)
            #if file log mode is enabled, then write in file
            elif self.m_eLogMode == CLogger.mC_FILELOG:
                if self.m_fileObj != None:
                    self.m_fileObj.MWrite('\n' + self.__m_lsLogEvtBuffer__[iCounter].MGetMembersAsString())
                else:
                    raise RuntimeError("mylogmanager.py : Attempted to write to log file, prior to setting it")

            #in case of parallel process log mode
            elif self.m_eLogMode == CLogger.mC_PARALLELPROCESSLOG:
                #acquired the lock. Multiple processes will be accessing the same
                #queue object. So in order to force mutual exclusion and ensure
                #consistency of queue, lock is taken. This lock object is also shared
                #amongst multiple processes. Any process, which have to log, will take
                #this lock and write to queue
                self.m_mpLock.acquire()

                self.m_queueObj.put(self.__m_lsLogEvtBuffer__[iCounter])

                #releasing lock, so that other processes can also write their logs in queue
                self.m_mpLock.release()

        #clearing the buffer of logevents
        self.__m_lsLogEvtBuffer__ = []

        #releasing the lock
        self.m_lockObj.release()

        return

        """------------------------------------------------------------------"""

    def MDeleteCompleteLog(self, bDelCachedLog = True):
        """
        public member method :-

        Inputs :- (i) bDelCachedLog :- boolean value specifying whether to delete the logs present in buffer

        Outputs :- does not return any values

        Purpose :- This method erases the content of the log-file, if the logmode is FileLog and erases logs present in buffer, depending on
                    bDelCachedLog value
        """
        #bDelCachedLog is true, then delete the logs present in buffer, but not written to file
        if bDelCachedLog == True:
            self.MClearCachedLog()
            # set the log event count to 0. event count is set to 0 only if
            # bDelCachedLog argument is passed as true in MDeleteCompleteLog.
            # Invoking MClearCachedLog() will not reset m_iEvtCount
            self.m_iEvtCount = 0
            self.m_startTime = datetime.datetime.now()

        #if logging mode is file mode, then clear the content of log file
        #because in windows logging mode, it's not possible to clear windows log
        #buffer
        if self.m_fileObj != None and self.m_eLogMode == CLogger.mC_FILELOG:
            self.m_lockObj.acquire()
            self.m_fileObj.MClearContents()
            self.m_lockObj.release()

        return

        """------------------------------------------------------------------"""

    def MCollectParallelLogs(self, queueOfEvtObjs, objProcessManager, dTimeToPollQueue = 1.0):
        """
        Static Member Method :-

        Inputs :- (i)   queueOfEvtObjs :- object of type multiprocessing.Queue

                  (ii)  objProcessManager :- object of type CProcessManager, which manages parallel processes

                  (iii) dTimeToPollQueue :- time gap interval, at which polling have to be done at queue

        Outputs :- does not return any values

        Purpose :- Collects the logs, which are present in queueOfEvtObjs and which are written by parallel objects.
                   Sorts those logs as per their timestamp and recalculate their relative time, with reference to the
                   timestamp of first logevent object.
        """
        #list which will store the logEvt objects read from the queue
        lsOutputLogs = []

        #boolean value signalling whether to exit loop or not
        bExitLoop = False
        while True:
            try:
                #reading the logevt object from the queue.
                #here we are not making block call on get() method.
                #So, if any logevent object is present in queue, when get() is
                #invoked it'll be appended lsOutputLogs. But, if queue is empty
                #at the time of get(), then exception will be thrown
                buf = queueOfEvtObjs.get(block = False)
                #appended the logevt object to output list
                lsOutputLogs.append(buf)
            except:
                #in case of exception, checking and leaving loop, if bExitLoop flag is true or not
                if bExitLoop == True:
                    break

                #sleeping for the time provided by user
                time.sleep(dTimeToPollQueue)

                #checking if all the processes have finished and if they have, then setting bExitLoop to true
                if objProcessManager.MHaveAllProcessesFinished():
                    bExitLoop = True

        #acquired lock on logger object. Lock Acquisition is important, because from this point onwards
        #any threads which want to write logs with the help of this logger object, must be blocked, because
        #we'll have to sort the parallel logs as well as other logs(logs from main or another thread, using this
        #logger object), on the basis of their timestamp. So, if any logEvt is coming in between, then it'll not
        #be part of sorting operation. So, we have prohibited the access to logger object, by acquiring lock
        self.m_lockObj.acquire()

        #adding the extra messages, i.e., those log messages that user have logged from other thread, eg. main thread, once
        #after he have created processes, to be executed parallely
        for i in range(0, len(self.__m_lsLogEvtBuffer__)):
            lsOutputLogs.insert(i, self.__m_lsLogEvtBuffer__[i])

        #clearing buffer
        self.__m_lsLogEvtBuffer__ = []

        #getting the list of timestamp associated with each logevent object
        lsTimestamps = CLogEvent.MSGetTimeStampsAsListFromLogs(lsOutputLogs)
        #obtaining the list of indices of sorted list of timestamps
        lsSortedIndices = np.argsort(lsTimestamps).tolist()
        #storing sorted logevents objects in list of indices
        for iIdx, iVal in enumerate(lsSortedIndices):
            lsSortedIndices[iIdx] = lsOutputLogs[iVal]

        #assigning sorted list of sorted log objects to lsOutputLogs
        lsOutputLogs = lsSortedIndices

        if len(lsOutputLogs) > 0:
            # storing the timestamp of first event in the sorted list of event objects
            tempDateOfFirstEvt = LecP.cTimer.filetime_to_dt(lsOutputLogs[0].m_evtDate)

        #iterating through each event object in lsOutputLogs
        for i in range(0, len(lsOutputLogs)):
            #storing the timestamp of current event under consideration
            tempDateOfCurrentEvt = (LecP.cTimer.filetime_to_dt(lsOutputLogs[i].m_evtDate))
            #recalcuate the relative time for each event object, with reference to timestamp of first event in the sorted list
            tempResult = LecP.ConvertDoubleToHMS((tempDateOfCurrentEvt - tempDateOfFirstEvt).seconds, bReturnSecsAsIntegerVal = True)
            tempResult += "." + LecP.FormatString((tempDateOfCurrentEvt - tempDateOfFirstEvt).microseconds, 6, '0')
            #setting the relative time
            lsOutputLogs[i].MSetRelStartTime(tempResult)
            #setting the event id
            lsOutputLogs[i].m_iEvtId = i + 1

            #appended the modified log event object to buffer
            self.__m_lsLogEvtBuffer__.append(lsOutputLogs[i])

        #resetting the m_iEvtCount object, so that any next message, which is logged with this logger object
        #gets correct iEvtId
        self.m_iEvtCount = len(self.__m_lsLogEvtBuffer__)

        if len(lsOutputLogs) > 0:
            #resetting the m_startTime to the timestamp of the first event in the sorted list
            self.m_startTime = tempDateOfFirstEvt

        #releasing lock
        self.m_lockObj.release()

        #writing buffer to the file/windows buffer
        self.MWriteBuffer()

        return

        """------------------------------------------------------------------"""

    @staticmethod
    def MSCreateMultiProcessingLoggerObj(queueObj = None, mpLockObj = None, eLogLimit = mC_NOLIMIT, iLogLimitAmount = -1):
        """
        Static Method :-

        Inputs :- does not receive any inputs

        Outputs :- does not return any values

        Purpose :- This method creates and returns logger object, which can be used in multiprocessing environment
        """
        if queueObj == None:
            queueObj = multiprocessing.Queue()

        if mpLockObj == None:
            mpLockObj = multiprocessing.Lock()

        objLoggerObj = CLogger(eLogMode = CLogger.mC_PARALLELPROCESSLOG, queueObj = queueObj, mpLockObj = mpLockObj, iBufSize = 100, eLogLimit = eLogLimit, iLogLimitAmount = iLogLimitAmount)

        return objLoggerObj

        """------------------------------------------------------------------"""

    def __del__(self):
        """
        Destructor :-

        Inputs :- does not receive any inputs

        Outputs :- does not return any values

        Purpose :- deallocates the memory and other resources granted to object of this class

        Note :- However, note that destructor is not invoked when you are logging in multiple seperate processes.
                In that case, you have to explicitly invoke MWriteBuffer() to write all the messages present in
                the buffer in the file/windows buffer
        """
        #if there's any log data remaining to be written in log file or windows buffer,
        #then write it
        if self.__m_lsLogEvtBuffer__ != None and len(self.__m_lsLogEvtBuffer__) > 0:
            self.MWriteBuffer()
        #if fileobject for log file is alive, then close it
        if self.m_fileObj != None and  self.m_fileObj.__MIfFileObjAlive__() == True:
            self.m_fileObj.MClose()
            self.m_fileObj = None

        self.m_strFileNameWithExtension = None

        """------------------------------------------------------------------"""

    @staticmethod
    def MSTest1(loggerObj, strString):
        """
        Test Method :-

        Inputs :- (i) loggerObj :- Object of CLogger class

                  (ii) strString :- String that have to be logged into log file

        Outputs :- does not receive any outputs

        Purpose :- This method is run concurrently by multiple threads. This method attemps to write logger object
                passed to it as argument
        """

        for i in range(0, 1000):
            loggerObj.MLogWarn(strString + ' i = ' + str(i))

        return

        """------------------------------------------------------------------"""

    @staticmethod
    def MSTestInCaseOfParallelMethods():
        """
        Test Method :-

        Inputs :- does not receive any inputs

        Outputs :- does not return any values

        Purpose :- this method tests CLogger class. It performs the testing of CLogger
                   class, in multi-threading environment
        """
        #startTime = datetime.datetime.now()

        #creating logger object, with limits being imposed on it regarding number of log events it can log
        loggerObj = CLogger("c:\\temp\\temp.log", iBufSize = 100, eLogMode = CLogger.mC_FILELOG, eLogLimit = CLogger.mC_LOGMSGBASEDLIMIT, iLogLimitAmount = 5000)

        #creating logger object, with limits being imposed on it regarding number of seconds, till which it can perform logging
        #loggerObj = CLogger("c:\\temp\\temp.log", iBufSize = 100, eLogMode = CLogger.mC_FILELOG, eLogLimit = CLogger.mC_TIMEBASEDLIMIT, iLogLimitAmount = 2)

        #loggerObj = CLogger(iBufSize = 1, eLogMode = CLogger.mC_WINDOWSLOG)
        #perform the testing of CLogger class in case of multiple threads
        threadObj1 = threading.Thread(target = CLogger.MSTest1, args = (loggerObj, "Thread1"))
        threadObj1.start()
        print "Created thread1..."
        threadObj2 = threading.Thread(target = CLogger.MSTest1, args = (loggerObj, "Thread2"))
        threadObj2.start()
        print "Created thread2..."
        threadObj3 = threading.Thread(target = CLogger.MSTest1, args = (loggerObj, "Thread3"))
        threadObj3.start()
        print "Created thread3..."

        threadObj1.join()
        threadObj2.join()
        threadObj3.join()

        #endTime = datetime.datetime.now()
        #print "Time taken " + str((endTime - startTime).seconds) + ":" + str((endTime - startTime).microseconds)


        return

        """------------------------------------------------------------------"""

    @staticmethod
    def MSTest():
        """
        Test Method :-

        Inputs :- does not receive any inputs

        Outputs :- does not return any values

        Purpose :- this method tests CLogger class. It perform simple testing
        """
        #testing time-based logging limit
        loggerObj = CLogger("c:\\temp\\temp.log", iBufSize = 1, eLogMode = CLogger.mC_FILELOG, eLogLimit = CLogger.mC_TIMEBASEDLIMIT, iLogLimitAmount = 4)

        #testing number of log messages size-based logging
        loggerObj = CLogger("c:\\temp\\temp.log", iBufSize = 3, eLogMode = CLogger.mC_FILELOG, eLogLimit = CLogger.mC_LOGMSGBASEDLIMIT, iLogLimitAmount = 4)

        loggerObj.MLogWarn("adding two nos.")
        import time
        time.sleep(1)
        c = 1 + 2
        loggerObj.MLogInfo("Got the result")
##        loggerObj.MClearCachedLog()
##        loggerObj.MDeleteCompleteLog(False)
        time.sleep(1)
        print c
        loggerObj.MLogError("Printed the result")
        time.sleep(1)
        loggerObj.MLogWarn("The result is " + str(c))
        time.sleep(1)
        loggerObj.MLogInfo("The array is " + str(range(0, 1000)))
        time.sleep(1)

        return

        """------------------------------------------------------------------"""

    @staticmethod
    def MSTestInMultiProcessing(iNumOfProcesses = 3, iMaxWaitTimeInSeconds = 20):
        """
        Static member method :-

        Inputs :- (i) iNumOfProcesses :- Number of processes that have to be created

        Outputs :- does not return any values

        Purpose :- This method tests logging in multiprocessing environment
        """
        queue = multiprocessing.Queue()
        lock = multiprocessing.Lock()
        jobs = []
        for i in range(0, iNumOfProcesses):
            #p = multiprocessing.Process(target = TestMP, args = ("msg"  + str(i + 1), queue, lock, 1))
            p = multiprocessing.Process(target = TestMP, args = ("process - "  + str(i + 1), queue, lock, i + 1))
            jobs.append(p)
            p.start()

        manager = myprocessmanager.CProcessManager(jobs)
        #manager.MWaitForAllProcessesToComplete()

        import threading
        threadObj1 = threading.Thread(target = manager.MWaitForAllProcessesToComplete, args = (iMaxWaitTimeInSeconds, ))
        threadObj1.start()

        loggerObj = CLogger(strFileNameWithExtension = "c:\\temp\\temp.txt", eLogMode = CLogger.mC_FILELOG, iBufSize = 10)
        threadObj = threading.Thread(target = loggerObj.MCollectParallelLogs, args = (queue, manager))
        threadObj.start()

        for i in range(0, 10):
            time.sleep(1)
            print "\nlogging " + str(i)
            loggerObj.MLogInfo("Logging have started")
            print "\nlogged " + str(i)

        #loggerObj = CLogger.MSMakeLoggerObj(queue, manager, jobs)
        #loggerObj.MSetLogFile(strFileNameWithExtension = ("c:\\temp\\temp.txt"))
        #loggerObj.MWriteBuffer()

        return

        """------------------------------------------------------------------"""



def TestMP(strMsg, queueObj, lockObj, iNumberOfIterationsFactor = 1):
    """
    Static Member Method :-

    Inputs :- (i) strMsg :- Message which have to be logged

              (ii) queueObj :- object of queue type

              (iii) lockObj :- object of multiprocessing.Lock type

    Outputs :- does not return any values

    Purpose :- This method is executed in a seperate process. It simply creates a logger object
               and writes message passed as argument to it
    """
    #print "created"

    loggerObj = CLogger(queueObj = queueObj, mpLockObj = lockObj, eLogMode = CLogger.mC_PARALLELPROCESSLOG, iBufSize = 10 * iNumberOfIterationsFactor, eLogLimit = CLogger.mC_LOGMSGBASEDLIMIT, iLogLimitAmount = iNumberOfIterationsFactor * 50 + iNumberOfIterationsFactor)
    #loggerObj = CLogger(queueObj = queueObj, mpLockObj = lockObj, eLogMode = CLogger.mC_PARALLELPROCESSLOG, iBufSize = 10 * iNumberOfIterationsFactor, eLogLimit = CLogger.mC_TIMEBASEDLIMIT, iLogLimitAmount = iNumberOfIterationsFactor * 1)
    #loggerObj = CLogger(queueObj = queueObj, mpLockObj = lockObj, eLogMode = CLogger.mC_PARALLELPROCESSLOG, iBufSize = 10 * iNumberOfIterationsFactor, eLogLimit = CLogger.mC_NOLIMIT)

    #loggerObj = CLogger(queueObj = queueObj, mpLockObj = lockObj, eLogMode = CLogger.mC_PARALLELPROCESSLOG)
    import numpy

    for i in range(0, iNumberOfIterationsFactor * 100):
        LecP.GiveLoadToCPU((iNumberOfIterationsFactor * 50, iNumberOfIterationsFactor * 50))
        loggerObj.MLogError(strMsg + ' Iteration ' + str(i + 1) + ' out of ' + str(iNumberOfIterationsFactor * 100) + '#' + str(range(0, iNumberOfIterationsFactor * 100)))

    loggerObj.MWriteBuffer()

    return

    """------------------------------------------------------------------"""

if __name__ == '__main__':
    #tests logging in multithreading environment
    #CLogger.MSTestInCaseOfParallelMethods()
    #tests logging in multiprocessing environment
    #CLogger.MSTestInMultiProcessing(iNumOfProcesses = 3, iMaxWaitTimeInSeconds = 15)
    #performs simple logging in single-threaded and process environment
    CLogger.MSTest()

    pass
