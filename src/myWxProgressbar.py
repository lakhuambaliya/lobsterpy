#-------------------------------------------------------------------------------
# Name:        myWxProgressbar
# Purpose:     this program contains class for showing and managing progressbar
#              in any GUI Application.
#
# Author:      Anirudh Sureka
#
# Created:     09-04-2013
# Copyright:   (c) Teledyne Lecroy Corporation
# Licence:     All rights reserved.
#-------------------------------------------------------------------------------

#imports
import wx
import thread
import threading
import datetime
import os
import math
import LecroyUtil_portable as LecP
import myfile

#class-name :- CWxProgressbar
#purpose    :- this class implements Progressbar in wx toolkit. It contains various
#              other methods, which controls and defines the behaviour of progressbar.
class CWxProgressbar:

    def __init__(self, windowObj, tupPgbarLoc = (0, 0), tupPgbarSize = (120, 20), tupStatusTimeTxtLoc = (0, 0), tupStatusTimeTxtSize = (190, 30),
                 tupStaticBoxLoc = (0, 0), tupStaticBoxSize = (0, 0), lsStrTaskList = None, tupTime = (), bIsPrgBarVisible = True,
                 bIsStaticTxtVisible = True, iMaxNoOfProcessorsAvailable = -1, dGainFactor = 1.0, dExpCoefficient = 0.0, dOffsetFactor = 0.0):

        """
        Constructor : -

        Inputs : - (i)  windowObj :- window object which will contain the progressbar. Exception will be raised
                                    if it's type is not of wx.Frame

                   (ii) tupPgBarLoc : - tuple specifying the top-left corner of progressbar. By default (0, 0)

                   (iii) tupPgSize : - tuple specifying the size of progressbar. It's an optional argument

                   (iv) tupStatusTimeTxtLoc : - tuple specifying the location of statictext showing the status of progressbar.
                                            default is (0, 0).

                   (v)  tupStatusTimeTxtSize : - tuple specifying the size of the statictext showing the status of progressbar.
                                            It's an argument.

                   (vi) tupStaticBoxLoc  : - tuple specifying the location(top, left) of staticbox

                   (vii) tupStaticBoxSize : - tuple specifying the size(width, height) of staticbox

                   (viii) lsStrTaskList   :- list containing the descriptions of various tasks being active.

                   (ix) tupTime  :- tuple of form (hours, minutes, seconds), for which progressbar have to be shown.
                                     This argument is used for time-based progressbar

                   (x) bIsPrgBarVisible :- boolean value specifying, whether the progressbar have to be shown or not

                   (xi) bIsStaticTxtVisible :- boolean value specifying, whether status StaticText is visible or not

                   (xii)iMaxNoOfProcessorsAvailable :- Maximum number of processors available for computing each task in task-list.
                                                      Default is -1, which means that (N - 1) processors have to be used, where N
                                                      is the total number of processors available.

                   (xiii) dGainFactor :- double value specifying the gain factor in the equation of exponential curve

                   (xiv) dExpCoefficient :- double value specifying the exponential coefficient in the equation of
                                            exponential curve

                   (xv) dOffsetFactor :- double value specifying the offset factor

        """
        #if window object is null, then show the error message
##        if windowObj == None or isinstance(windowObj, wx.Frame) == False:
##            raise RuntimeError("CWxProgressbar:windowObj is either none or it is not of type wx.Frame")

        #checking the tuple objects passed as arguments
        self.MCheckTupleVal(tupPgbarLoc, "tupPgbarLoc")
        self.MCheckTupleVal(tupPgbarSize, "tupPgbarSize")
        self.MCheckTupleVal(tupStatusTimeTxtLoc, "tupStatusTimeTxtLoc")
        self.MCheckTupleVal(tupStatusTimeTxtSize, "tupStatusTimeTxtSize")
        self.MCheckTupleVal(tupStaticBoxLoc, "tupStaticBoxLoc")
        self.MCheckTupleVal(tupStaticBoxSize, "tupStaticBoxSize")

        #TO DO : handle vertical progressbars
        #instantiating Guague control, which is responsible for showing the progress of operation in
        #quantitative terms

        self.m_GroupControlObj = wx.StaticBox(parent = windowObj, label = "Operation status", pos = (tupStaticBoxLoc), size = (tupStaticBoxSize))
        self.m_GroupControlObj.SetBackgroundStyle(wx.BG_STYLE_SYSTEM)
        self.m_ProgressbarObj = wx.Gauge(windowObj, id = -1, pos = tupPgbarLoc, size = tupPgbarSize)
        self.m_bIsPrgbarVisible = bIsPrgBarVisible
        self.m_ProgressbarObj.Show(bIsPrgBarVisible)

        #instantiating StaticText control, which will show the status of progress bar, or the current activity being
        #processed
        self.m_StaticTxtForStatusTime = wx.StaticText(windowObj, label = "Status Text", pos = tupStatusTimeTxtLoc, size = tupStatusTimeTxtSize)
        self.m_StaticTxtForStatusTime.Show(bIsStaticTxtVisible)
        self.m_StaticTxtForStatusTime.SetBackgroundColour(wx.Color(255, 128, 0))
        self.m_bIsStatusStaticTxtVisible = bIsStaticTxtVisible

        self.MInitializeMemberVarsToDefaultVal()
        self.MSetExpCurveParams(dGainFactor, dExpCoefficient, dOffsetFactor)

        self.m_iMaxNoOfProcessorsAvailable = int(os.environ["NUMBER_OF_PROCESSORS"]) - 1
        if iMaxNoOfProcessorsAvailable >= 1:
            self.m_iMaxNoOfProcessorsAvailable = iMaxNoOfProcessorsAvailable

        if len(tupTime) == 3:
            #if tupTime is passed, and it contains exactly
            #three elements, then assign it ot m_tupTimeRemaining
            self.m_tupTimeRemaining = tupTime
            self.m_bIsTimeBasedPgbar = True

        #if time-based progressbar, then start showing the progressbar
        if self.m_bIsTimeBasedPgbar:
            self.MShowProgressBar(self.m_tupTimeRemaining)

        if lsStrTaskList != None:
            #if tasklist is of instancetype list, then assign it to member list
            if isinstance(lsStrTaskList, list):
                self.MSetTaskList(lsStrTaskList)
            else:
            #else show the error message
                raise RuntimeError("CWxProgressbar:Task list must be of type list")

    """----------------------------------------------------------------------"""

    def MInitializeMemberVarsToDefaultVal(self):
        """
        Member Method : -

        Inputs  :- does not receive any inputs

        Outputs :- does not return any values

        Purpose :- initializes the member variables of the class to their default values
        """

        #list for holding the tasks to be performed
        self.m_lsStrTasks = []

        #list for storing the time required to execute each unit of task. It's meant
        #for internal use only
        self.m_lsDTimeForEachTask = []
        #time object, which specifies the starting time, for time-based progressbar
        self.m_tmTimeStart = None
        #time object, which specifies the ending time, for time-based progressbar
        self.m_tmTimeToEnd = None
		#time object, which stores the timestamp of the start of first task in the tasklist
        self.m_tmGlobalTimeStart = None
        #current task being executed in case of sequential jobs
        #in case of parallel jobs, it's the identifier or sequence no. of job
        #which had been recently executed
        self.m_iCurrentTask = 0

        #text to be shown in statusbar. Eg. like sub-activity of current task
        self.m_strStatusTxt = ""

        #member thread object for holding the current thread displaying the progressbar
        self.m_ThreadObj = None

        #boolean variable for specifying whether the progressbar thread must continue its
        #operation or stop itself
        self.m_bExitCurrentThread = False

        self.m_lsTimeStartForEachParallelTask = []
        self.m_lsTimeEndForEachParallelTask = []

        self.m_lsDProcessorTimeRatioForTasks = []

        #stores the time, for which the progressbar have to be shown. Useful when
        #the progress bar is time-based. In case of other progressbar types, it
        #holds the hours, minutes, seconds remaining
        self.m_tupTimeRemaining = ()
        #boolean value, which specifies, whether the progressbar is time-based.
        self.m_bIsTimeBasedPgbar = False
        #boolean value specifying, whether process for which progressbar is shown
        #is aborted by the user, or not.
        self.m_bIsPrgBarAborted = False
        self.m_ProgressbarObj.SetValue(0)
        self.m_StaticTxtForStatusTime.SetBackgroundColour(wx.Color(255, 128, 0))
        self.m_dExpCoefficient = 0.0
        self.m_dOffsetFactor = 0.0
        self.m_dGainFactor = 0.0

        """------------------------------------------------------------------"""

    def MSetMaxNumOfUsableCPUs(self, iNoOfCPUs = -1):
        """
        Member Method :-

        Inputs :- (i) iNoOfCPUs :- Number of CPUs available for computing the things

        Outputs:- does not return any values

        Purpose :- This method sets the values of number of CPUs, that are used to execute tasks
                   in the task list.
        """
        if iNoOfCPUs <= 0 or iNoOfCPUs >= int(os.environ["NUMBER_OF_PROCESSORS"]):
            self.m_iMaxNoOfProcessorsAvailable = int(os.environ["NUMBER_OF_PROCESSORS"]) - 1
        else:
            self.m_iMaxNoOfProcessorsAvailable = iNoOfCPUs

        return

    """----------------------------------------------------------------------"""

    def MModifyVisibility(self, bIsPrgbarVisible = False, bIsStaticTxtVisible = False):
        """
        Member methods :

        Inputs         : (i)    bIsPrgbarVisible : boolean value specifying whether the progressbar
                                                  is visible or not

                         (ii)   bIsStaticTxtVisible : boolean value specifying whether the statictext
                                                      is visible or not

        Outputs       : does not return any values

        Purpose       : This method modifies the visibility of progressbar and status_statictext, depending
                        upon the argument passed
        """
        #showing/hiding progressbar
        self.m_ProgressbarObj.Show(bIsPrgbarVisible)
        #showing/hiding status_statictext's visibility
        self.m_StaticTxtForStatusTime.Show(bIsStaticTxtVisible)
        #in case, if status_statictext is made visible, then it's label must be none
        self.m_StaticTxtForStatusTime.SetLabel("")

        if (bIsPrgbarVisible == False and bIsStaticTxtVisible == False):
            self.m_GroupControlObj.Show(False)
        else:
            self.m_GroupControlObj.Show(True)

        return

    """----------------------------------------------------------------------"""

    def MSetTaskList(self, lsStrTask, lsDProcessorTimeRatio = None, dGainFactor = 1.0, dExpCoefficient = 0.0, dOffsetFactor = 0.0):
        """
        Member Method :

        Inputs        : (i) lsStrTask :- list of strings, containing the names of jobs
                                         to be performed

                        (ii)lsDProcessorTimeRatio :- list of values specifying the ratio of
                                                    time, each task requires to get complete.
                                                    By default none, implies each task requires
                                                    same amount of time

                        (iii) dGainFactor :- double value specifying the gain factor in the equation of exponential curve

                        (iv) dExpCoefficient :- double value specifying the exponential coefficient in the equation of
                                            exponential curve

                        (v)  dOffsetFactor :- double value specifying the offset factor

        Outputs       : does not return any values

        Purpose       : This method sets the task-list passed as argument as the list of
                        tasks to be executed
        """

        #if task-list is empty, then show error
        if lsStrTask != None and len(lsStrTask) > 0:
            iCurrentTask = 0
            #setting m_bIsPrgBarAborted variable to False, at the begining of each
            #process, which is represented by progressbar.
            self.m_bIsPrgBarAborted = False
            #setting all the member variables to their default values, so that they
            #can be used for the current tasks
            self.MInitializeMemberVarsToDefaultVal()
            self.m_lsStrTasks = lsStrTask
            #defining the range of progressbar object on the basis of no. of tasks in taks-list
            self.m_ProgressbarObj.SetRange(len(lsStrTask))
            #recording the task_start time
            self.m_tmTimeStart = datetime.datetime.now()
            self.m_tmGlobalTimeStart = self.m_tmTimeStart
            self.m_iCurrentTask = iCurrentTask
            self.MSetExpCurveParams(dGainFactor, dExpCoefficient, dOffsetFactor)
			#if list containing processor-time ratio for each task is not passed, then
			#assume that each task takes equal amount of time
            if lsDProcessorTimeRatio == None or len(lsDProcessorTimeRatio) != len(lsStrTask):
                lsDProcessorTimeRatio = []
                for strTask in lsStrTask:
                    lsDProcessorTimeRatio.append(1)
            self.m_lsDProcessorTimeRatioForTasks = lsDProcessorTimeRatio
            self.m_StaticTxtForStatusTime.SetLabel(self.MGetStatusLabel())
        else:
            raise RuntimeError("CWxProgressbar:Task List is empty")

        return

    """----------------------------------------------------------------------"""

    def MSetExpCurveParams(self, dGainFactor, dExpCoefficient, dOffsetFactor = 0.0):
        """
        Member Method :-

        Inputs :-   (i) dGainFactor :- double value specifying the gain factor in the equation of exponential curve

                    (ii) dExpCoefficient :- double value specifying the exponential coefficient in the equation of
                                        exponential curve

                    (iii)  dOffsetFactor :- double value specifying the offset factor.

                    dGainFactor, dExpCoefficient and dOffsetFactor are required, because of the variations that a
                    task may take to complete, in the last iteration, when percentage of CPU-load varies. That's,
                    the time taken to complete a task is more, when the CPU-load is high (more cores are busy), and
                    reverse is the case, when the CPU-load is less(less cores are used). For that reason, Exponential
                    curve is fitted and its equation is implemented to handle this variations, so that accurate estimate
                    of time can be given.

        Outputs :- does not return any values

        Purpose :- This method sets the value of the exponential curve equations'
                   parameters
        """

        self.m_dExpCoefficient = dExpCoefficient
        self.m_dGainFactor = dGainFactor
        self.m_dOffsetFactor = dOffsetFactor

        return

    """----------------------------------------------------------------------"""

    def MRecordParallelTaskTime(self):
        """
        Member Method :-

        Inputs  :- does not receive any inputs

        Outputs :- does not return any values

        Purpose :- This method records currrent timestamp as starting time for current task
        """

        self.m_lsTimeStartForEachParallelTask.append(datetime.datetime.now())
        self.m_lsTimeEndForEachParallelTask.append(None)

        return

    """----------------------------------------------------------------------"""

    def MGetStatusLabel(self):
        """
        Member Method :-

        Inputs :- doesn't receive any inputs

        Outputs:- return the string to be shown on the statusTxt of the progressbar

        Purpose :- This method returns the string to be shown on the progressbar statustext
        """
        #default label/text is "operation completed"
        strStatusTxt = "Operation completed"

        if len(self.m_lsStrTasks) > self.m_iCurrentTask:
            #if atleast one of the task in task-list have not been completed, then
            #change the default statustext
            strStatusTxt = ""
            #displaying the sequence of current task/total tasks. eg. 1/3
            strStatusTxt += str(self.m_iCurrentTask + 1) + "/" + str(len(self.m_lsStrTasks))
            #if user have passed information about sub-activity currently done, in current task in MUpdate method,
            #then show the sub-activity description, otherwise show the current-task name
            #eg. processing c1-vdiv-11
            strTmpTxt = self.m_strStatusTxt
            if strTmpTxt == "" or strTmpTxt == None:
                strTmpTxt ="processing " + str(self.m_lsStrTasks[self.m_iCurrentTask])
            strStatusTxt += " " + strTmpTxt
            strTmpTxt = ""
            #if its' the first task, then show "calculating time"
            #initially, when none of the task have been finished then
            #self.m_tupTimeRemaining will be (), thus its length will be 0.
            #It have to be in (hh, mm, ss) format
            if len(self.m_tupTimeRemaining) != 3:
                strTmpTxt = " Calculating time..."
            else:
                #else, show the actual time remaining
                strTmpTxt += ' ' + self.MGetTime(self.m_tupTimeRemaining) + " remaining"
            strStatusTxt += strTmpTxt
		#showing the message on statusstatictext, in case progressbar is time-based progressbar
        elif len(self.m_lsStrTasks) < 1 or self.m_lsStrTasks == None:
            strStatusTxt = self.MGetTime(self.m_tupTimeRemaining) + " remaining"

        return strStatusTxt

    """----------------------------------------------------------------------"""

    def MGetTime(self, tupTime):
        """
        Member Method :-

        Inputs  :- (i) tupTime  : - tuple containing time in the form (hours, minutes, seconds)

        Outputs :- does not return any values

        Purpose :- This method returns the string of form n hours m minutes o seconds, from the
                    time information passed to it.
                    eg. (0, 0, 1) : 1 seconds
                    eg. (0, 1, 12): 1 minutes 12 seconds
                    eg. (1, 0, 23): 1 minutes 23 seconds
        """
        strTimetxt = ""
        iHours = tupTime[0]
        iMinutes = tupTime[1]
        iSeconds = int(tupTime[2])
        if iHours > 0:
            strTimetxt += str(iHours) + ' hours '
        if iMinutes > 0:
            strTimetxt += str(iMinutes) + ' minutes '
        if iSeconds > 0:
            strTimetxt += str(iSeconds) + ' seconds'

        return strTimetxt

    """----------------------------------------------------------------------"""

    def MUpdate(self, strLabelTxt = "", bUpdatePrgBarGUI = True, bIsTimeBasedPgbar = False, bIsParallelPrgbar = False, iIdxOfCurrentParallelTask = -1):
        """
        Member Method :-

        Inputs  :- (i) strLabelTxt  : - text to be shown on the progressbar label

                   (ii) bUpdatePrgBarGUI :- boolean value specifying whether MUpdate must calculate remaining time
                                             and increment the no. of tasks completed, i.e. m_iCurrentTask
                                             It's by default True. It's set to False in case when only message
                                             have to be updated on Progressbar, without updating any other things
                                             like time-remaining or progressbar status

                   (iii) bIsTimeBasedPrgBar :- specifies whether the progressbar is timer-based

                   (iv) bIsParallelPrgBar :- specifies whether the progressbar have to be shown for parallel activities

                   (v) iIdxOfCurrentParallelTask :- specifies the index of parallel task in the task-list, which have completed
                                                      its execution and have sent the notification of it to progressbar class


        Outputs :- doesn't return any values

        Purpose :- This method updates the progressbar and statictext associated with it. Moreover, it also
                    makes the calculations regarding, the time-remaining
        """
        #if process represented by progressbar in GUI, have been aborted by the user,
        #then simply return from the method.
        if self.m_bIsPrgBarAborted == True:
            return
        #recording current time
        currentTime = datetime.datetime.now()
        if bIsTimeBasedPgbar:
            #finding the difference between the time, when progressbar started and current time
            #in terms of number of seconds
            iDifferenceInSeconds = (currentTime - self.m_tmGlobalTimeStart).seconds
            #update the progressbar based on number of seconds elapsed
            iTotalTimeInSeconds = (self.m_tmTimeToEnd - self.m_tmGlobalTimeStart).seconds
            #when 90% of the time have been elapsed and no notifications received about the
            #completion of task, then wait for that task to complete, without modifying the
            #progressbar control
            if len(self.m_lsStrTasks) > 0:
                if float(iDifferenceInSeconds) / float(iTotalTimeInSeconds) > 0.98:
                    self.m_StaticTxtForStatusTime.SetLabel(str(self.m_iCurrentTask + 1) + "/" + str(len(self.m_lsStrTasks)) + " Waiting for current task to complete...")
                    while True:
    					#if received the notification of current task completion, then exit the
    					#method
                        if self.m_bExitCurrentThread:
                            return
                        wx.Sleep(1)
                if float(iDifferenceInSeconds) / float(iTotalTimeInSeconds) < 0.9:
                    self.m_ProgressbarObj.SetValue(iDifferenceInSeconds)
            else:
                self.m_ProgressbarObj.SetValue(iDifferenceInSeconds)
            iNoOfSecondsRemaining = (self.m_tmTimeToEnd - currentTime).seconds
            #if number of seconds remaining is less than 1, then
            #exit the method
            if iNoOfSecondsRemaining < 1:
                return
            #calculating the time remaining in terms of (hours, minutes, seconds)
            self.m_tupTimeRemaining = LecP.ConvertDoubleToHMS(iNoOfSecondsRemaining, bReturnTuple = True)
            # updating the status_statictext
            self.m_StaticTxtForStatusTime.SetLabel(self.MGetStatusLabel())
        else:
			# in case, when progressbar is showing the status of parallel activities
            if bIsParallelPrgbar:
                if iIdxOfCurrentParallelTask < 0:
                    raise RuntimeError("Index of current task in the list can not be negative")
                # incrementing total number of tasks done
                self.m_iCurrentTask += 1
                # show 100% progressbar, and "Operation Complete" message,
                # when all the tasks in the tasklist are completed
                if self.m_iCurrentTask >= len(self.m_lsStrTasks):
                    self.MKillProgressbarThread()
                    self.m_ProgressbarObj.SetValue(self.m_ProgressbarObj.GetRange())
                    self.m_StaticTxtForStatusTime.SetLabel("Operation complete")
                    self.m_StaticTxtForStatusTime.SetBackgroundColour(wx.GREEN)
                    self.m_lsTimeEndForEachParallelTask[iIdxOfCurrentParallelTask] = currentTime
                    self.MPrintParallelStatistics()
                    return

                iTotalNoOfTasks = len(self.m_lsStrTasks)
                #calculating total number of iterations, based on total number of tasks and number of CPUs available
                #Formulae : iTotalNoOfTasks = ceil(tasks / usable CPUs). eg. 23 tasks and 5 usable CPUs, then
                #number of iterations will be 5
                iNoOfIterations = math.ceil(float(iTotalNoOfTasks) / float(self.m_iMaxNoOfProcessorsAvailable))
                # calculating number of tasks in the last iteration. However, we'll also get 0
                # as number of tasks in last iteration, when all the CPUs available for utitlized
                # and none of them is idle
                iNoOfTasksInLastIteration = iTotalNoOfTasks % self.m_iMaxNoOfProcessorsAvailable

                # calculating ratio of (no. of CPU used / total number of CPUs available for task execution) in last iteration
                dRatioOfCPUUseInLastIter = (float(iNoOfTasksInLastIteration) / float(self.m_iMaxNoOfProcessorsAvailable))
                # if number of tasks in last iteration is 0, i.e., all CPUs are used in the last iteration, then
                # we'll set ratioOfCPUUseInLastIter as 1.0, as CPUs are fully utilized
                if iNoOfTasksInLastIteration == 0:
                    dRatioOfCPUUseInLastIter = 1.0

                iElapsedTimeInSeconds = (currentTime - self.m_tmGlobalTimeStart).seconds

                # recording the end time for the current task
                self.m_lsTimeEndForEachParallelTask[iIdxOfCurrentParallelTask] = currentTime

                # finding the average time required to complete each task, depending on number of tasks
                # finished and time taken by them to finish their execution
                dAvgTimeInSeconds = LecP.CalculateAvgFromStartAndEndTimestampsList(self.m_lsTimeEndForEachParallelTask, self.m_lsTimeStartForEachParallelTask)

                # calculating the time required in last iteration, as percentage of time required to complete
                # one task, when CPUs are fully loaded. It's done with the help of following equation of
                # of exponential curve :
                # (a * e raise to (b * x)) + offset, where
                # a - the gain factor
                # e - the mathematical exponential constant, i.e., 2.7183
                # b - the exponential coefficent
                # x - the ratio of (number of CPUs loaded in last iteration / total number of available CPUs)
                # offset - the offset factor
                dPercentTimeRequiredForLastItr = self.m_dGainFactor * pow(math.e, (self.m_dExpCoefficient * dRatioOfCPUUseInLastIter)) + self.m_dOffsetFactor
                # calculating the actual time required for the computation of tasks in last iteration
                # depending on (avg. time taken by tasks to complete when CPU is fully loaded * percentage of average time
                # required by tasks in the last iteration)
                dTimeRequiredForLastItr = dAvgTimeInSeconds * dPercentTimeRequiredForLastItr
                # recalculating the range of progressbar, as average time required to complete one
                # task changes
                iProgressbarRange = ((dAvgTimeInSeconds) * (iNoOfIterations - 1)) + dTimeRequiredForLastItr
                # calculating time remaining in seconds
                dTimeRemaining = iProgressbarRange - iElapsedTimeInSeconds
                # if time remaining is negative or 0, i.e., there's a large variation in the time-taken by
                # each task, then time estimates shown by the progressbar will be wrong. In that case,
                # we'll show "Waiting for current task to complete" message
                if dTimeRemaining <= 0:
                    # showing the message "Waiting for current task to complete
                    self.m_StaticTxtForStatusTime.SetLabel(str(self.m_iCurrentTask + 1) + "/" + str(len(self.m_lsStrTasks)) + " Waiting for current task to complete...")
                    return
                # calculated time-remaining in (hours, minutes, seconds)
                self.m_tupTimeRemaining = LecP.ConvertDoubleToHMS(dTimeRemaining, True)
                # calling the MShowProgressBar(), to start timer-based progressbar in thread
                self.MShowProgressBar(self.m_tupTimeRemaining, iProgressbarRange = iProgressbarRange)
                # again rerecording the time end for the current-task. Initially, we have recorded the
                # the time-start, in order to calculate average time. Now, we have again recorded so that
                # the time-taken to create progressbar thread is covered.
                self.m_lsTimeEndForEachParallelTask[iIdxOfCurrentParallelTask] = datetime.datetime.now()
            else:
                """
                Summary : -
                    For taskbased progressbars, we are at present, calculating the average time required
                    to complete one task and on the basis of that we give the estimate of total time
                    remaining. If the MUpdate() is invoked with bUpdatePrgBarGUI False, then don't
                    calculate the time remaining and update the progressbar's value. But update the text
                    on status_statictext. If bUpdatePrgBarGUI is true, then check if any of the task is
                    remaining in the task list. If all have finished, then return. If any task is remaining,
                    then calculate the time-remaining and accordingly update status_statictext
                """
                self.m_strStatusTxt = strLabelTxt
                if bUpdatePrgBarGUI == False:
                    #if progressbarGUI has not to be updated, then only update the message
                    #bUpdatePrgBarGUI is false, in case when different message have to be
                    #shown for different sub-tasks  being performed in individual task
                    #without requiring to update the time remaining
                    self.m_StaticTxtForStatusTime.SetLabel(self.MGetStatusLabel())
                    return

                #updating the current task
                self.m_iCurrentTask += 1

                #if all the tasks have been completed, then show "Operation complete"
                #message and then return
                if self.m_iCurrentTask >= len(self.m_lsStrTasks):
                    self.MKillProgressbarThread()
                    self.m_ProgressbarObj.SetValue(self.m_ProgressbarObj.GetRange())
                    self.m_StaticTxtForStatusTime.SetLabel("Operation complete")
                    self.m_StaticTxtForStatusTime.SetBackgroundColour(wx.GREEN)
                    return

                self.m_tmTimeToEnd = currentTime
                timeInSecond = (self.m_tmTimeToEnd - self.m_tmTimeStart).seconds
                timeinMilliSecond = (self.m_tmTimeToEnd - self.m_tmTimeStart).microseconds / 1000

                self.m_lsDTimeForEachTask.append((timeInSecond, timeinMilliSecond))
                self.m_tmTimeStart = currentTime

                #getting the average time taken for the completion of one task
                dAvgTime = self.MGetAverageTime()
                iNoOfTasksRemaining = len(self.m_lsStrTasks) - (self.m_iCurrentTask)
				#if processor-time ratio for all the tasks is same, i.e., list containing processor-time ratio
				#for time is not passed explicitly, then use average time for each task to estimate total time
				#remaining
                if self.m_lsDProcessorTimeRatioForTasks.count(1) == len(self.m_lsDProcessorTimeRatioForTasks):
                    dTotalTimeRemainingInSeconds = dAvgTime * iNoOfTasksRemaining
                    iProgressbarRange = len(self.m_lsStrTasks) * dAvgTime
                else:
                    #calculate total time remaining
                    dTotalTimeRemainingInSeconds = 0
                    dTimeTakenForFirstTask = self.m_lsDTimeForEachTask[0][0]    #get time taken in seconds to finish first task
                    #rounding off the time(in milliseconds) to complete first task into seconds
                    dTimeTakenForFirstTask += round(self.m_lsDTimeForEachTask[0][1] / 1000.0)
                    #calculating total time remaining, on the basis of processor-time ratio passed for each task
                    for i in range(self.m_iCurrentTask, len(self.m_lsStrTasks)):
                        dTotalTimeRemainingInSeconds += self.m_lsDProcessorTimeRatioForTasks[i] * dTimeTakenForFirstTask
					#modifying the range of progressbar control, with the change in average time required for each task to complete
                    iProgressbarRange = dTotalTimeRemainingInSeconds + (dAvgTime * (len(self.m_lsStrTasks) - iNoOfTasksRemaining))
                self.m_tupTimeRemaining = LecP.ConvertDoubleToHMS(dTotalTimeRemainingInSeconds, bReturnTuple = True)
                #invoking MShowProgressBar(), which will create a thread, to show the progressbar for m_tupTimeRemaining amount of time.
                self.MShowProgressBar(self.m_tupTimeRemaining, iProgressbarRange)

        return

    """----------------------------------------------------------------------"""

    def MKillProgressbarThread(self):
        """
        Member Method :-

        Inputs        :- does not receive any inputs

        Outputs       :- does not return any values

        Purpose       :- this method kills the thread handling the progressbar updates
        """
        self.m_bExitCurrentThread = True
        if self.m_ThreadObj != None and self.m_ThreadObj.isAlive():
            self.m_ThreadObj.join()
        self.m_StaticTxtForStatusTime.SetBackgroundColour(wx.Color(255, 128, 0))

        return

    """----------------------------------------------------------------------"""

    def MRefresh(self):
        """
        Member Method :-

        Inputs :- does not receive any inputs.

        Outputs :- does not return any values

        Purpose :- This method have to be invoked when progressbar control have
                   to be refreshed, i.e., it have to be assigned to new process,
                   provided that it has previously handled a task.
        """
        #   killing the active progressbar thread, if any
        self.MKillProgressbarThread()
        #   setting the progress-value to 0.
        self.m_ProgressbarObj.SetValue(0)
        #   redrawing(updating) progressbar control
        self.m_ProgressbarObj.Layout()
        #   setting the label to empty string.
        self.m_StaticTxtForStatusTime.SetLabel("")
        self.m_StaticTxtForStatusTime.Layout()

        return

    """----------------------------------------------------------------------"""

    def MAbortOperation(self):
        """
        Member Method :-

        Inputs        :- does not receive any inputs

        Outputs       :- does not return any values

        Purpose       :- this method halts the progressbar and stop its activities, in case
                         if the task, with what it was associated has been aborted
        """
        self.m_bIsPrgBarAborted = True
        self.m_bExitCurrentThread = True
        self.m_ProgressbarObj.SetValue(0)
        self.m_StaticTxtForStatusTime.SetLabel("Operation aborted")
        self.m_StaticTxtForStatusTime.SetBackgroundColour(wx.RED)
        self.m_lsDTimeForEachTask = []
        self.m_iCurrentTask = -1
        self.m_tupTimeRemaining = ()
        self.m_strStatusTxt = ""
        #   hiding progressbar, when operation have been aborted by user.
        self.MModifyVisibility(False, False)

        return
    """----------------------------------------------------------------------"""

    def MGetAverageTime(self):
        """
        Member method :-

        Inputs        :- does not receive any inputs

        Outputs       :- does not return any values

        Purpose       :- This method returns the average time taken to complete one task
                         in the task-list, depending upon the average calculated on the time
                         taken for each task completed
        """
        iTotalMilliSeconds = 0
        iTotalSeconds = 0
        #summing up the time-taken for each task in the tasklist that have been finished
        for iSeconds, iMilliSeconds in self.m_lsDTimeForEachTask:
            iTotalSeconds += iSeconds
            iTotalMilliSeconds += iMilliSeconds

        #rounding the number of milliseconds in terms of seconds.
        iTotalSeconds += round(iTotalMilliSeconds / 1000.0)

        return iTotalSeconds / float(self.m_iCurrentTask)

    """----------------------------------------------------------------------"""

    def MShowTimeBasedProgressBar(self):
        """
        Member Method : -

        Inputs        : - does not receive any inputs

        Outputs       : - does not return any values

        Purpose       : - this method shows and updates the progress bar. It's
                          used in case of time-based progressbar. It updates the progressbar's
                          status at every 1 seconds.

                          Note :- This method is executed in thread.
        """
        #TO DO : keep locking mechanism, so that concurrency can be enforced with security
        while datetime.datetime.now() < self.m_tmTimeToEnd:
			#invoking MUpdate() at every one seconds
            wx.Sleep(1)
     		#if signal for stopping progressbar thread have been received
			#then leave the method and exit the thread
            if self.m_bExitCurrentThread == True:
                self.m_bExitCurrentThread = False
                return

            self.MUpdate(bIsTimeBasedPgbar = True)

        self.m_bExitCurrentThread = False

        self.m_StaticTxtForStatusTime.SetLabel("Operation completed")
        self.m_StaticTxtForStatusTime.SetBackgroundColour(wx.GREEN)

        return

    """----------------------------------------------------------------------"""

    def MShowProgressBar(self, tupTime, iProgressbarRange = -1):
        """
        Member method :

        Inputs        : (i) tupTime :- tuple containing the time information in (hh, mm, ss) format.

                        (ii) iProgressbarRange :- the range(maximum quantity) of progressbar control.
                                                  default is -1, implies that number of seconds, for which
                                                  progressbar control have to be shown is its range

        Outputs       : (ii) does not return any values

        Purpose       : This method accepts the time for which the progressbar have to be shown. It
                        creates a thread and execute MShowTimeBasedProgressBar in that thread
        """
        if len(tupTime) != 3:
            raise RuntimeError("CWxProgressbar:timeTup argument must be passed in (hours, minutes, seconds) format")

        iHours = tupTime[0]
        iMinutes = tupTime[1]
        iSeconds = tupTime[2]

        # if negative value is passed for either hours, minutes or seconds, then show error message
        if iHours < 0 or iMinutes < 0 or iSeconds < 0:
            raise RuntimeError("Invalid Value passed for (hh, mm, ss) for timer-based progressbar")

        # if request is made to show progressbar for 0 minutes, then show error message
        if iHours == 0 and iMinutes == 0 and iSeconds == 0:
            raise RuntimeError("Timer-based progressbar can't be shown for undefined time-period")

        if self.m_ThreadObj != None and self.m_ThreadObj.isAlive() == True:
            try:
                self.MKillProgressbarThread()
            except:
                raise RuntimeError("Progressbar thread can not be destroyed")

        # setting the range of progressbar. It's in terms of number of seconds.
        if iProgressbarRange >= 0:
			# these lines of code will be executed, when timerbased progressbar
			# have to be shown from task-based progressbar
            self.m_ProgressbarObj.SetRange(iProgressbarRange)
            self.m_tmTimeToEnd = datetime.datetime.now() + datetime.timedelta(hours = iHours, minutes = iMinutes, seconds = iSeconds)
        else:
			# these lines of code will be executed for timerbased progressbar

            # initialized all the member-variables of the class to their default values
            self.MInitializeMemberVarsToDefaultVal()
            self.m_bIsPrgBarAborted = False
            self.m_ProgressbarObj.SetRange(iSeconds + (60 * iMinutes) + (60 * 60 * iHours))
            self.m_tmGlobalTimeStart = datetime.datetime.now()
            self.m_tmTimeToEnd = self.m_tmGlobalTimeStart + datetime.timedelta(hours = iHours, minutes = iMinutes, seconds = iSeconds)

        if self.m_bIsPrgBarAborted == False:
            # created new thread object and assigned its handle to m_ThreadObj
            self.m_ThreadObj = threading.Thread(target = self.MShowTimeBasedProgressBar)
            # recorded the time-remaining in m_tupTimeRemaining
            self.m_tupTimeRemaining = (iHours, iMinutes, iSeconds)
            self.m_StaticTxtForStatusTime.SetBackgroundColour(wx.Color(255, 128, 0))
            #started the thread
            self.m_ThreadObj.start()

        return

    """----------------------------------------------------------------------"""

    def MCheckTupleVal(self, tupleObj, strParamName):
        """
        Member method :

        Inputs  :- (i) tupleObj : - object of (expected)type tuple

                   (ii) strParamName    : - name of tuple in argument list of constructor

        Outputs :- does not return any values

        Purpose :- This method checks whether tupleObj passed as argument is of type tuple.
                    and whether it's having only two elements and the values of those elements
                    must be non-negative
        """
        if tupleObj == None or (isinstance(tupleObj, tuple) == False):
            raise RuntimeError("CWxProgressbar:" + strParamName + " is either None or it is not of type tuple")
        else:
            if (len(tupleObj) != 2) or (tupleObj[0] < 0 or tupleObj[1] < 0):
                raise(strParamName+ " must contain only two elements and both must be non-negative")

        return

    """----------------------------------------------------------------------"""

    def MPrintParallelStatistics(self, strFileName = "prgbarStatistics.csv"):
        """
        Member Method :-

        Inputs  :- does not receive any inputs

        Outputs :- does not return any values

        Purpose :- prints the statistics of time-start, time-end and time-taken by each task
        """
        fileObj = myfile.CFile(strFileName = strFileName, strMode = 'a')

        fileObj.MWrite("\nStatistics of Time taken by each tasks as on " + str(datetime.datetime.now()) + "\n")
        fileObj.MWrite("\nTotal number of CPUs : " + str(os.environ["NUMBER_OF_PROCESSORS"]))
        fileObj.MWrite("\nTotal number of availabe CPUs : " + str(self.m_iMaxNoOfProcessorsAvailable))
        fileObj.MWrite("\nTotal number of tasks : " + str(len(self.m_lsStrTasks)))
        fileObj.MWrite("\n\n\n")
        #Printing Headers
        fileObj.MWrite("\nTask-name, Start-time, End-time, Total time(in seconds)")
        for i in range(0, len(self.m_lsTimeStartForEachParallelTask)):
            fileObj.MWrite("\n" + str(self.m_lsStrTasks[i]) + ', ' +  str(self.m_lsTimeStartForEachParallelTask[i]) + ', ' +
                            str(self.m_lsTimeEndForEachParallelTask[i]) + ', ' +
                            str(self.m_lsTimeEndForEachParallelTask[i] - self.m_lsTimeStartForEachParallelTask[i])
                            )

        return

    """"---------------------------------------------------------------------"""

def TmpFunction(tupSize  = (1000, 1000), sleepTime = 2):
    wx.Sleep(sleepTime)
    LecP.GiveLoadToCPU(tupSize)
    #self.MUpdate(bIsParallelPrgbar = True, iIdxOfCurrentParallelTask = int(multiprocessing.current_process().name))

class TestProgressbar(wx.App):

    def __init__(self, redirect = False):
        wx.App.__init__(self)

    def OnInit(self):
        frame = wx.Frame(None, -1, "Test_Progressbar")
        self.prgBar = CWxProgressbar(frame, (10, 20), (120, 20), (150, 20), (190, 30), (0, 0), (350, 55), iMaxNoOfProcessorsAvailable = 2)
        btn1 = wx.Button(frame, pos = (50, 150), label = "Taskbased progressbar")
        frame.Bind(wx.EVT_BUTTON, self.BtnClick1, btn1)
        btn2 = wx.Button(frame, pos = (250, 150), label = "Timebased progressbar")
        frame.Bind(wx.EVT_BUTTON, self.BtnClick2, btn2)
        btn3 = wx.Button(frame, pos = (250, 250), label = "stop progressbar thread")
        frame.Bind(wx.EVT_BUTTON, self.BtnClick3, btn3)
        btn4 = wx.Button(frame, pos=(250, 200), label = "Parallel Progressbar")
        frame.Bind(wx.EVT_BUTTON, self.BtnClick4, btn4)
        btn5 = wx.Button(frame, pos=(0, 200), label = "Abort Progressbar")
        frame.Bind(wx.EVT_BUTTON, self.BtnClick5, btn5)
        frame.Show(True)

        return True

    def WaitForOneProcessToComplete(self, iWaitNo):
        iNoOfProcessFinished = 0
        while iNoOfProcessFinished < iWaitNo:
            #wx.Sleep(1)
            for i, Job in enumerate(self.jobs):
                #print i
                if self.jobs[i].is_alive() == False and self.jobStatus[i] == False:
                    #print strJobList[i] + " finished..." + str(i)
                    #jobs.pop(i)
                    self.jobStatus[i] = True
                    #print "job " + str(i) + " ended"
                    self.prgBar.MUpdate(bIsParallelPrgbar = True, iIdxOfCurrentParallelTask = i)
                    iNoOfProcessFinished += 1
                    print "completed task " + str(i + 1)

                    if iNoOfProcessFinished >= iWaitNo:
                        return
    def BtnClick5(self, evt):
        self.prgBar.MAbortOperation()

    def TmpFunction1(self):
        import multiprocessing
        self.jobs = []
        self.jobStatus = []
        self.strJobList = ["job1", "job2", "job3", "job4", "job5", "job6", "job7", "job8", "job9", "job10"]
        iNoOfProcessors = 2
        self.prgBar.MSetTaskList(self.strJobList)
        for i in range(10):
            #if len(self.jobs) >= iNoOfProcessors:
            if self.jobStatus.count(False) >= iNoOfProcessors:
                self.WaitForOneProcessToComplete(1)
            self.prgBar.m_lsTimeStartForEachParallelTask.append(datetime.datetime.now())
            p = multiprocessing.Process(target = TmpFunction, name = str(i), args = ((300, 300), 2))
            print "submitted task " + str(i + 1)
            self.jobs.append(p)
            self.jobStatus.append(False)
            self.prgBar.m_lsTimeEndForEachParallelTask.append(None)
            p.start()
            #print str(i) + " started"

        iNoOfPendingTasks = self.jobStatus.count(False)#len(jobs)
        while iNoOfPendingTasks > 0:
            #wx.Sleep(2)
            for i, Job in enumerate(self.jobs):
                #print i
                if self.jobs[i].is_alive() == False and self.jobStatus[i] == False:
                    #print strJobList[i] + " finished..." + str(i)
                    #jobs.pop(i)
                    self.jobStatus[i] = True
                    #print "job " + str(i) + " ended"
                    self.prgBar.MUpdate(bIsParallelPrgbar = True, iIdxOfCurrentParallelTask = i)
                    iNoOfPendingTasks -= 1

    def BtnClick4(self, Evt):
        threadObj = threading.Thread(target = self.TmpFunction1)
        threadObj.start()
        #self.TmpFunction1()

    def BtnClick3(self, Evt):
        self.prgBar.MKillProgressbarThread()

    def BtnClick1(self, Evt):
        self.prgBar.MModifyVisibility(True, True)
        threading.Thread(target = self.SubmitTask).start()
        return

    def BtnClick2(self, Evt):
        self.prgBar.MShowProgressBar((0, 0, 10))
        return

    def SubmitTask(self):
        lsTasks = ["task1", "task2", "task3"]# "task4", "task5", "task6", "task7"]
        self.prgBar.MSetTaskList(lsTasks)
        for iIdx, strTask in enumerate(lsTasks):
            self.prgBar.MUpdate(bUpdatePrgBarGUI = False)
            wx.Sleep(7)
            self.prgBar.MUpdate(bUpdatePrgBarGUI = True)

        return

def main():
    TestProgressbar().MainLoop()

if __name__ == '__main__':
    main()
