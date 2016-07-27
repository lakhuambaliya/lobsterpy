#-------------------------------------------------------------------------------
# Name:        myprocessmanager.py
# Purpose:     This module contains class for handling the multiprocessing.Process type processes
#
# Author:      Anirudh Sureka
#
# Created:     10-30-2013
# Copyright:   (c) Teledyne Lecroy 2013
# Licence:     all_rights_reserved
#-------------------------------------------------------------------------------

#imports
import datetime
import time
import threading
import multiprocessing
import mylogmanager
#class-name :- CProcessManager
#purpose :- This class manages the parallel processes, running concurrently
class CProcessManager:
    mC_MAXTIMETOWAITINSECONDS = 1e9     #maximum number of seconds for which all processes will be waited for their completion
    mC_FINISHEDSTATE = False            #represents finished state of process
    mC_ACTIVESTATE = True               #represents active state of process
    def __init__(self, lsProcesses = None, objTarget = None, objMethod = None, lsTupArgs = None,
                lsStrProcessNames = None, iMaxTimeToWaitInSeconds = mC_MAXTIMETOWAITINSECONDS):
        """
        Constructor :-

        Throws Exceptions :- No

        Inputs :- (i)   lsProcesses :- list of processes

                  (ii)  objTarget :- Target object name, whose method have to be executed in seperate processes. It's None, when an
                                     indenpendent function, which does not belong to any of the classes, have to be executed in se-
                                     parate processes.

                  (iii) objMethod :- method of objTarget/independent function, which have to be executed  in seperated processes.

                  (iv)  lsTupArgs :- List of tuples contaning arguments, to be passed to objMethod.

                  (v)   lsStrProcessNames   :- list of strings, which stores the process names

                  (vi)  iMaxTimeToWaitInSeconds :- maximum number of seconds for which all processes will be waited for their completion

        Outputs :- does not return any values

        Purpose :- initializes all the member variables to default values
        """
        #   initialized all the members to their default values
        self.__MInitializeMembersToDefaultVal__()

        #   user will either pass list of prcesses, or it'll method to be executed, as well as list of input arguments
        if lsProcesses != None and len(lsProcesses) > 0:
            #   setting the list of processes and marking state of each process as
            #   active, in case user have passed the list of processes as argument.
            self.m_lsProcesses = lsProcesses
            self.m_lsProcessStatus = [CProcessManager.mC_ACTIVESTATE for processObj in lsProcesses]
        else:
            #   in case, user is not passing list of processes.
            self.m_objTarget = objTarget
            self.m_objMethod = objMethod
            self.m_lsTupArgs = lsTupArgs
            self.m_lsStrProcessNames = lsStrProcessNames

        if iMaxTimeToWaitInSeconds > 0:
            self.m_iMaxTimeInSecondsToWait = iMaxTimeToWaitInSeconds

        if (self.m_objMethod != None) and (self.m_lsTupArgs != None and len(self.m_lsTupArgs) > 0):
            self.MCreateAndManageProcesses(self.m_objTarget, self.m_objMethod, self.m_lsTupArgs, self.m_lsStrProcessNames, self.m_iMaxTimeInSecondsToWait)

        return

        """------------------------------------------------------------------"""

    def __MInitializeMembersToDefaultVal__(self):
        """
        private member method :-

        Throws Exceptions :- No

        Inputs :- does not receive any inputs

        Outputs :- does not return any values

        Purpose :- initialize all the member variables to default values
        """
        #   list for holding the process objects
        self.m_lsProcesses = []

        #   list for holding the process status
        self.m_lsProcessStatus = []

        #   list for storing the output of each processes.
        self.m_lsProcessOutputs = []

        #   list for storing the names of each processes.
        self.m_lsStrProcessNames = []

        #   integer variable which store the maximum number of seconds to wait for all process completion
        self.m_iMaxTimeInSecondsToWait = CProcessManager.mC_MAXTIMETOWAITINSECONDS

        #   target object, whose method have to be executed in seperate processes.
        self.m_objTarget = None

        #   method of target object/independent function, which have to be executed in seperate processes.
        self.m_objMethod = None

        #   list of arguments to be passed to method.
        self.m_lsTupArgs = None

        return

        """------------------------------------------------------------------"""

    def MSetProcessList(self, lsProcessObj):
        """
        public member method :-

        Throws Exceptions :- No

        Inputs :- (i) lsProcessObj :- list of process objects

        Outputs :- does not return any values

        Purpose :- sets the member process list
        """
        if len(self.m_lsProcesses) > 0 and self.MHaveAllProcessesFinished() == False:
            raise RuntimeError("myprocessmanager.py : Processmanager busy. List of processes are already managed by processmanager")

        if len(lsProcessObj) <= 0:
            raise RuntimeError("myprocessmanager.py : empty list of processes passed as argument")

        self.m_lsProcesses = lsProcessObj
        self.m_lsProcessStatus = [CProcessManager.mC_ACTIVESTATE for process in lsProcessObj]

        return

        """------------------------------------------------------------------"""

    def MCreateAndManageProcesses(self, objMethodName, lstupArgs, lsStrProcessNames = None, iWaitForMaxTimeInSeconds = 300,
                                    objLogger = None):
        """
        Member Method :-

        Inputs :- (i)

        Outputs :-

        Purpose :-
        """
        returnValue = None
        if len(self.m_lsProcesses) > 0 and self.MHaveAllProcessesFinished() == False:
            raise RuntimeError("myprocessmanager.py : Processmanager busy. List of processes are already managed by processmanager")

        self.m_lsProcesses = []
        self.m_lsProcessStatus = []

        if lsStrProcessNames == None:
            lsStrProcessNames = ["Process " + str(i + 1) for i in range(0, len(lstupArgs))]

        if objLogger != None:
            queue = multiprocessing.Queue()
            lock = multiprocessing.Lock()

        for iIdx, tupArgs in enumerate(lstupArgs):
            if objLogger:
                tupArgs += (queue, lock)
            processObj = multiprocessing.Process(target = objMethodName, name = lsStrProcessNames[iIdx], args = tupArgs)
            processObj.start()
            self.m_lsProcesses.append(processObj)
            self.m_lsProcessStatus.append(CProcessManager.mC_ACTIVESTATE)

        threadObj1 = threading.Thread(target = self.MWaitForAllProcessesToComplete, args = (iWaitForMaxTimeInSeconds, ))
        threadObj1.start()

        if objLogger:
            #loggerObj = mylogmanager.CLogger(strFileNameWithExtension = "c:\\temp\\temp.txt", eLogMode = mylogmanager.CLogger.mC_FILELOG, iBufSize = 10)
            threadObj = threading.Thread(target = objLogger.MCollectParallelLogs, args = (queue, self))
            threadObj.start()

            returnValue = objLogger

        return returnValue

        """------------------------------------------------------------------"""

    def MAppendProcess(self, subProcessObj):
        """
        public member method :-

        Throws Exceptions :- No

        Inputs :- (i) subProcessObj :- Object of type multiprocessing.Process

        Outputs :- does not return any values

        Purpose :- adds a subprocess to the list of processes to be managed
        """
        self.m_lsProcesses.append(subProcessObj)
        self.m_lsProcessStatus.append(CProcessManager.mC_ACTIVESTATE)

        return

        """------------------------------------------------------------------"""

    def MUpdateStatusOfEachProcess(self):
        """
        public member method :-

        Throws Exceptions :- No

        Inputs :- does not receive any inputs

        Outputs :- does not return any values

        Purpose :- update the status of processes as finished, whose execution have finished
        """
        #iterating through the list of processes
        for iCounter, processObj in enumerate(self.m_lsProcesses):
            #updating the status of processes, which have finished, but are recorded as active
            if processObj.is_alive() == False and self.m_lsProcessStatus[iCounter] == CProcessManager.mC_ACTIVESTATE:
                self.m_lsProcessStatus[iCounter] = CProcessManager.mC_FINISHEDSTATE

        return

        """------------------------------------------------------------------"""

    def MHaveAllProcessesFinished(self):
        """
        public member method :-

        Throws Exceptions :- No

        Inputs :- does not receive any inputs

        Outputs :- returns true if all processes in m_lsProcesses have finished, otherwise returns false

        Purpose :- checks the status of each process in m_lsProcesses and returns true, if all of them have finished
        """
        #updates the process status
        self.MUpdateStatusOfEachProcess()
        #returns true if all the processes are in finished state
        if self.m_lsProcessStatus.count(CProcessManager.mC_FINISHEDSTATE) == len(self.m_lsProcesses):
            return True

        return False

        """------------------------------------------------------------------"""

    def MHasWaitingTimeExpired(self, iCurrentNumberOfSeconds, iTargetNumberOfSeconds):
        """
        public member method :-

        Throws Exceptions :- No

        Inputs :- (i)   iCurrentNumberOfSeconds :- number of seconds elapsed

                  (ii)  iTargetNumberOfSeconds :- maximum number of seconds to wait for completion of all processes

        Outputs :- does not return any values.

        Purpose :- checks if the time to wait for have expired or not
        """

        if iCurrentNumberOfSeconds >= iTargetNumberOfSeconds:
            return True

        return False

        """------------------------------------------------------------------"""

    def MTerminate(self, bTerminateAll = False):
        """
        public member method :-

        Throws Exceptions :- No

        Inputs :- (i) bTerminateAll :- boolean value specifying whether to terminate all the processes present in process list

        Outputs :- does not return any values

        Purpose :- terminates processes
        """
        #TODO : Implementation for terminating specific process, is remaining.

        if bTerminateAll:
            #terminates all the active processes
            for iIdx, processObj in enumerate(self.m_lsProcesses):
                if self.m_lsProcessStatus[iIdx] == CProcessManager.mC_ACTIVESTATE:
                    processObj.terminate()

            #initializing all the member functions to default values
            self.__MInitializeMembersToDefaultVal__()

        return

        """------------------------------------------------------------------"""

    def MWaitForAllProcessesToComplete(self, iMaxNumberOfTimeInSeconds = 0, dTimeToSleep = 1.0):
        """
        public member method :-

        Throws Exceptions :- Yes. It throws an exception, if the time limit to wait for all processes has expired

        Inputs :- (i) iMaxNumberOfTimeInSeconds :- integer values specifying the maximum of number of time to wait for
                                                   for all subprocesses to finish. It's optional. When not passed, it's
                                                   given the default value, i.e., mC_MAXTIMETOWAITINSECONDS

        Outputs :- does not return any values.

        Purpose :- Waits for all processes to finish until time-limit passed has expired or
                   However, it throws an execption, if the time limit to wait for all processes
        """
        #set m_iMaxTimeInSecondsToWait to iMaxNumberOfTimeInSeconds, if iMaxNumberOfTimeInSeconds is not passed
        #as argument
        if iMaxNumberOfTimeInSeconds <= 0:
            iMaxNumberOfTimeInSeconds = self.m_iMaxTimeInSecondsToWait

        #recording starttime
        startTime = datetime.datetime.now()

        while True:
            #sleeping for dTimeToSleep seconds passed as argument
            time.sleep(dTimeToSleep)

            #check if all processes have finished and return, if they have finished
            if self.MHaveAllProcessesFinished() == True:
                return

            #throws exceptions, if waiting time has expired
            if self.MHasWaitingTimeExpired((datetime.datetime.now() - startTime).seconds, iMaxNumberOfTimeInSeconds):
                self.MTerminate(bTerminateAll = True)
                raise Exception("myprocessmanager.py :- Process completion wait limit has expired")

        return

        """------------------------------------------------------------------"""

    def MGetProcessAsPerState(self, bState = mC_FINISHEDSTATE):
        """
        public member method :-

        Throws Exceptions :- No

        Inputs :- (i) bState :- state of process. mC_FINISHEDSTATE for finished, mC_ACTIVESTATE for active

        Outputs :- list of  processes

        Purpose :- This method returns the list of processes which may in specific state, as per bState parameter
        """
        lsProcesses = []

        #updates the state of each process in process-list
        self.MUpdateStatusOfEachProcess()

        #appends all processes, which are in bState to lsProcesses
        for iIdx, processObj in enumerate(self.m_lsProcesses):
            if self.m_lsProcessStatus[iIdx] == bState:
                lsProcesses.append(processObj)

        return lsProcesses

        """------------------------------------------------------------------"""

    def MGetListOfFinishedProcesses(self):
        """
        public member method :-

        Throws Exceptions :- No

        Inputs :- does not receive any inputs

        Outputs :- list of active processes

        Purpose :- This method returns the list of processes which have finished execution
        """
        #gets the list of Finished processes
        lsFinishedProcesses = self.MGetProcessAsPerState(bState = CProcessManager.mC_FINISHEDSTATE)

        return lsFinishedProcesses

        """------------------------------------------------------------------"""

    def MGetListOfActiveProcesses(self):
        """
        public member method :-

        Throws Exceptions :- No

        Inputs :- does not receive any inputs

        Outputs :- list of active processes

        Purpose :- This method returns the list of processes which are active
        """
        #gets the list of finished processes
        lsActiveProcesses = self.MGetProcessAsPerState(bState = CProcessManager.mC_ACTIVESTATE)

        return lsActiveProcesses

        """------------------------------------------------------------------"""

    def MDisplayNamesOfActiveProcesses(self):
        """
        public member method :-

        Throws Exceptions :- No

        Inputs :- does not receive any inputs

        Outputs :- does not return any values

        Purpose :- This method displays the names of the processes which are currently active
        """
        lsActiveProcesses = self.MGetListOfActiveProcesses()

        for iIdx in range(0, len(lsActiveProcesses)):
            print lsActiveProcesses[iIdx].name

        return

        """------------------------------------------------------------------"""

    def MDisplayNamesOfFinishedProcesses(self):
        """
        public member method :-

        Throws Exceptions :- No

        Inputs :- does not receive any inputs

        Outputs :- does not return any values

        Purpose :- This method displays the names of the processes which are currently active
        """
        lsFinishedProcesses = self.MGetListOfFinishedProcesses()

        for iIdx in range(0, len(lsFinishedProcesses)):
            print lsFinishedProcesses[iIdx].name

        return

        """------------------------------------------------------------------"""
    @staticmethod
    def MSTest():
        """
        static member method :-

        Throws Exceptions :- No

        Inputs :- does not receive any inputs

        Outputs :- does not return any values

        Purpose :- tests CProcessManager class
        """
        manager = CProcessManager()
        manager.MCreateAndManageProcesses(objMethodName = time.sleep, lstupArgs = [(0, ), (5, ), (10, )], iWaitForMaxTimeInSeconds = 5)
        time.sleep(1)
        print "\n Following processes have finished : \n"
        manager.MDisplayNamesOfFinishedProcesses()
        print "\n Following processes are active : \n"
        manager.MDisplayNamesOfActiveProcesses()

        return

        """------------------------------------------------------------------"""

if __name__ == '__main__':
    CProcessManager.MSTest()
