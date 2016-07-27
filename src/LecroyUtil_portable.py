#-------------------------------------------------------------------------------
# Name:        LecroyUtil_portable.py
# Purpose:     Set of helper library functions which make day to day tasks easier.  This library
#              has functions for math operations, DSP operations, File IO, Scope setups, CVAR control etc.
#			   Also any function that is added here should be compatible with Portable Python
#
# Author:      Anirudh Sureka
#
# Created:     2/10/2011
# Copyright:   (c) LeCroy Corp. 2011
# Licence:     all rights reserved.
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# imports

import numpy as np
import numpy.linalg
import matplotlib.pyplot as plt
import time as ti
import win32com.client as win32
import string as st
import math,winsound,os,cmath,shutil,zipfile,re,subprocess
import scipy as sp
import scipy.signal as signal
import sys
import fnmatch,glob
import smtplib    # Import smtplib for the actual email sending function
import pkg_resources #knowing the version of python module or library
import inspect
import win32api, win32con
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
from datetime import datetime, timedelta, tzinfo
from calendar import timegm
import wx
#import pyPdf

'''#####################################################################################################
    General stuff
#####################################################################################################'''
EPOCH_AS_FILETIME = 116444736000000000  # January 1, 1970 as MS file time
HUNDREDS_OF_NANOSECONDS = 10000000
ZERO = timedelta(0)
HOUR = timedelta(hours=1)

class UTC(tzinfo):
    """UTC"""
    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO

utc = UTC()

class cTimer():
      def __init__(self):
          self.startTime = ti.time()
      def getCurrentTime(self):
          return ti.time()
      def getCurrentTimeStr(self):
          return GetCurrentTime();
      def startTimer(self):
          self.startTime = ti.time();
      def stopTimer(self):
          currentTime = ti.time();
          diffTime = dict(double=1.0, string="")
          diffTime['double'] = currentTime - self.startTime
          diffTime['string'] = ConvertDoubleToHMS(diffTime['double'])
          return diffTime;

      @staticmethod
      def dt_to_filetime(dt):
        """Converts a datetime to Microsoft filetime format. If the object is
        time zone-naive, it is forced to UTC before conversion.

        >>> "%.0f" % dt_to_filetime(datetime(2009, 7, 25, 23, 0))
        '128930364000000000'

        >>> "%.0f" % dt_to_filetime(datetime(1970, 1, 1, 0, 0, tzinfo=utc))
        '116444736000000000'

        >>> "%.0f" % dt_to_filetime(datetime(1970, 1, 1, 0, 0))
        '116444736000000000'

        >>> dt_to_filetime(datetime(2009, 7, 25, 23, 0, 0, 100))
        128930364000001000L
        """
        if (dt.tzinfo is None) or (dt.tzinfo.utcoffset(dt) is None):
            dt = dt.replace(tzinfo=utc)
        ft = EPOCH_AS_FILETIME + (timegm(dt.timetuple()) * HUNDREDS_OF_NANOSECONDS)
        return ft + (dt.microsecond * 10)

      @staticmethod
      def filetime_to_dt(ft):
        """Converts a Microsoft filetime number to a Python datetime. The new
        datetime object is time zone-naive but is equivalent to tzinfo=utc.

        >>> filetime_to_dt(116444736000000000)
        datetime.datetime(1970, 1, 1, 0, 0)

        >>> filetime_to_dt(128930364000000000)
        datetime.datetime(2009, 7, 25, 23, 0)

        >>> filetime_to_dt(128930364000001000)
        datetime.datetime(2009, 7, 25, 23, 0, 0, 100)
        """
        # Get seconds and remainder in terms of Unix epoch
        (s, ns100) = divmod(ft - EPOCH_AS_FILETIME, HUNDREDS_OF_NANOSECONDS)
        # Convert to datetime object
        dt = datetime.utcfromtimestamp(s)
        # Add remainder in as microseconds. Python 3.2 requires an integer
        dt = dt.replace(microsecond=(ns100 // 10))
        return dt

      @staticmethod
      # converts the lec time stamp to file time long integer
      def LecTimeStampToFileTime(lecTime):
        Jan1st2000 = 125911584000000000;
        fileTime = Jan1st2000 + long(lecTime)/long(100);        # as lecTime is 1ns resolution
        return fileTime

      @staticmethod
      # converts lec time stamp to a string like "2012-08-18 17:47:52.393992"
      def LecTimeStampToTimeStr(lecTime):
        dt_str = filetime_to_dt(LecTimeStampToFileTime(lecTime));
        return dt_str

      @staticmethod
      # compares lecroy time stamps and finds if they are within the differential asked for
      def IsWithin(timeDifferentialInSeconds, LecTimeStamp1, LecTimeStamp2):
        difference = abs(LecTimeStamp1 - LecTimeStamp2)/1e9                # convert it into seconds
        if difference < timeDifferentialInSeconds:
           return True
        else:
             return False

      @staticmethod
      # compares lecroy time stamps and finds if they are within the differential asked for
      def IsWithinPythonTimeStamp(timeDifferentialInSeconds, PyTimeStamp1, PyTimeStamp2):
        difference = abs(PyTimeStamp1 - PyTimeStamp2)
        if difference < timeDifferentialInSeconds:
           return True
        else:
             return False

      # to convert lecTimeStamp for comparison follow the below steps:
      # 1)

def ConvertDoubleToHMS(dTime, bReturnTuple = False, bReturnSecsAsIntegerVal = False):
    '''---------------------------------------------------------
    Converts the double value in Hour, Mins, Seconds numbers '''
    hours = int(dTime/3600.0)
    mins = int((dTime%3600)/60.0)
    # in case seconds do not have to be returned as integer value
    if not bReturnSecsAsIntegerVal:
        secs = ((dTime%3600)%60.0)
    # in case seconds have to be returned as integer value
    else:
        secs = ((dTime%3600)%60)

    if bReturnTuple:
        return(hours, mins, secs)

    return str(hours) + ":" + str(mins) + ":" + str(secs)


def CalculateAvgFromStartAndEndTimestampsList(lsTimeEnd, lsTimeStart):
    """
    Function :-

    Inputs   :- (i) lsTimeStart :- list containing the timestamps, when task started

                (ii)lsTimeEnd   :- list containing the timestamps, when task finished

    Outputs  :- Average of time taken to complete one task

    Purpose  :- This method calculates the time required to complete each task, calculate
                the average time and returns it
    """
    # integer variable, which stores the number of tasks finished in tasklists
    iTotalNoOfTasksFinished = 0
    # list which stores time in [seconds, milliseconds] format
    iTotalTime = [0, 0]

    # iterating through the time list for tasks
    for iCounter in range(0, len(lsTimeEnd)):
        # if start time and end time for the task is not None, then
        # it implies that task have completed. So, use that tasks
        # statistics for calculating average time for one task
        if lsTimeStart[iCounter] != None and lsTimeEnd[iCounter] != None:
            # getting the time taken by the task to complete, in seconds
            timeInSecond = (lsTimeEnd[iCounter] - lsTimeStart[iCounter]).seconds
            # getting the time taken by the task to complete, in millisecond
            timeInMillSeconds = (lsTimeEnd[iCounter] - lsTimeStart[iCounter]).microseconds / 1000.0

            iTotalTime[0] += timeInSecond
            iTotalTime[1] += timeInMillSeconds

            # incrementing the total number of tasks finished
            iTotalNoOfTasksFinished += 1

    # calculating total time in seconds
    iTotalTimeInSeconds = iTotalTime[0] + round(iTotalTime[1] / 1000.0)
    # calculating average time
    dAvgTimeInSeconds = float(iTotalTimeInSeconds) / float(iTotalNoOfTasksFinished)

    return dAvgTimeInSeconds

    """----------------------------------------------------------------------"""

def GetCurrentTime():
    '''---------------------------------------------------------
    get current time string Eg: Sat, 27 Nov 2010 04:35:00 +0000 '''
    timeStr = ti.strftime("%a, %d %b %Y %H:%M:%S +0000", ti.localtime())
    return timeStr

# can be used to convert time str printed in file to a time double used for comparison
# eg: ConvertTimeStrToTimeStamp("Sat, 18 Aug 2012 17:47:54 +0000")
# eg: ConvertTimeStrToTimeStamp("2012-08-18 17:47:54.393992",r"%Y-%m-%d %H:%M:%S.%f")  << results from lecTimeStamp functions
def ConvertTimeStrToTimeStamp(timeStr,formatStr = r"%a, %d %b %Y %H:%M:%S +0000"):
    tiStruct = ti.strptime(timeStr,formatStr)
    timeStamp = ti.mktime(tiStruct)
    return timeStamp

def GetCurrentTimeStamp():
    '''---------------------------------------------------------
    returns a double timestamp value related to current time '''
    return ti.time();

def ConvertDoubleToTimeStr(dTimeStamp = ti.time()):
    '''---------------------------------------------------------
    converts the input double to a time string'''
    return ti.ctime(dTimeStamp);

def GetClock():
    '''---------------------------------------------------------
    clock time elapsed in seconds after 1st call.  Has micro seconds precision'''
    return ti.clock()

def Sleep(SecondsToSleep = 0.5):
    '''---------------------------------------------------------
    Sleeps the execution for given no. of seconds.  Can be subseconds too. '''
    iters= SecondsToSleep/60.0
    remainder = SecondsToSleep%60.0
    ti.sleep(remainder)
    for i in np.arange(1, iters + 1, 1):
        ti.sleep(60.0)
    print str(i) + " of " + str(iters) + " minutes complete."
    return

def Beep(N=1):
    '''---------------------------------------------------------
    Plays a beep sound. '''
    #winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
    #winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
    for i in np.arange(0,N,1):
        winsound.MessageBeep()
        ti.sleep(1)
        winsound.MessageBeep()
    return;

def StopPYCFiles(val = True):
	'''---------------------------------------------------------
	StopPYCFiles(val = True):
    Stops the script from producing a .PYC byte code file. '''
	sys.dont_write_bytecode = True
	# PYTHONDONTWRITEBYTECODE is the enviorment variable
	return

def SampleToCallCmdPrompt():
    ''' ----------------------------------------------------------
	Call exe with arguments in separate cmd prompt.
	TODO: add arguments for exe name and input arguments '''
    os.system("calc.exe");
    return;

def DebugPrint(a,debug = False):
    ''' ----------------------------------------------------------
    Call this function to print in debug mode only. '''

    if debug == True:
       print a
    return;

def GenerateColorList():
    ''' ----------------------------------------------------------
    This function generates a list of high contrast colors which can be used for plotting. '''
    strColorList = ('Red','Green','Black','Blue','Fuchsia','GreenYellow','Aqua','Tan','HotPink','Khaki','Purple','Coral','SpringGreen','Teal','SkyBlue','Goldenrod','Maroon','DarkRed','MediumVioletRed','Orange','DarkKhaki','DarkViolet','DarkGreen','Navy','Peru');
    return strColorList;

'''#####################################################################################################
    Other instrument oven, sine gen, step gen stuff
#####################################################################################################'''
''' Sets the Engg ovens or the downstairs production oven temperature once connected via USB to GPIB '''


def ConvertIntoDBM(Vdiv = 50.0, NoOfDivisions = 6.0):
    '''---------------------------------------------------------
    convert amplitude in vdiv and NoOfDivisions big into dBm '''
    val = math.pow((NoOfDivisions*Vdiv/2.0/math.sqrt(2.0)),2.0)
    amplInDBM = 10.0*np.log10(val/50.0/0.001)        #convert divisions into dBm
    return amplInDBM


##def SineSweep( freqV, sigGenGPIB = "GPIB::05", ScopeIP = "127.0.0.1"):
##    '''---------------------------------------------------------
##    given freq Vector does a sine sweep using Anritsu generator.
##    Note: P3 should have the sdev setup. Also the generator Ampl is set '''
##    app = win32.DispatchEx('LeCroy.XStreamDSO', ScopeIP )
##    j = 0;
##    sdevData = np.arange(0.0,np.size(freqV),1.0)
##    for f in freqV:
##        SetSineGenFreq(GPIB = sigGenGPIB, FreqInMHz = f)
##        SingleForceAcquisition(ScopeIP)
##        StopAcquiring(ScopeIP)
##
##        sdevData[j] = app.Measure.P3.last.Result.Value
##        j += 1
##
##    return sdevData;

'''#####################################################################################################
    Scope Compensation stuff
#####################################################################################################'''
def ReadFIRDS(fileName):
    '''---------------------------------------------------------
    Reads the cached_xx.txt file format from given filename, returns fir, Fs.
    Only reads the fir filter'''
    d = LoadTxtFix(fileName)
    Fs = d[0]
    stages = d[1]
    Fs = d[2]
    N = d[3]                 # no. of taps in fir filter
    fir = d[4:4+int(N)]           # fir taps

    return fir,Fs


def ReadDS(fileName):
    # This function reads a DS file stored by the scope
    # 'IsSOS' is '1' if file has a second order system, '0' if would read an FIR stage & if '2', it has SOS + FIR stages
    # It returns IsSOS, sampling freq, numerator & denominator polynomials, and sos.

    d = LoadTxtFix(fileName)

    sos = np.array([])
    IsSOSstagePresent = False
    IsFIRpresent = False
    IsSOS = 0
    numWhole = 1
    denoWhole = 1

    Fs = d[0]
    stages = int(d[1])

    j = 2

    for s in np.arange(stages):
        Fs_stage = d[j]; j += 1

        N_numerator = d[j]; j += 1
        num = d[j:j + int(N_numerator)]; j += N_numerator

        N_denominator = d[j]; j += 1
        deno = d[j:j + int(N_denominator)]; j += N_denominator

        # SOS stage is present---------------------------
        if N_numerator <= 3 and N_denominator <= 3:
            IsSOSstagePresent = True

            # Making numerator and denominator of length '3'
            if N_numerator < 3:
                num = np.append(num, np.zeros(3 - len(num)))
            if N_denominator < 3:
                deno = np.append(deno, np.zeros(3 - len(deno)))
            # Creating an sos matrix------------------------
            sos = np.append(sos, np.append(num, deno))
            continue

        # FIR stage is present---------------------------
        if N_denominator == 1.0:
            IsFIRpresent = True

        numWhole = np.convolve(numWhole, num)
        denoWhole = np.convolve(denoWhole, deno)

    if (IsSOSstagePresent == True):
        IsSOS = 1

    if (IsFIRpresent == True):
        IsSOS = 0

    if (IsSOSstagePresent == True) and (IsFIRpresent == True):
        IsSOS = 2

    return IsSOS, Fs, numWhole, denoWhole, sos

def ReadDF():
	#TODO: complete this'''
    return;

def ReadHiZ():
	#TODO: complete this'''
    return;

def ReadADCpaths(fn, plotFig = False, figureNo=53433, titleStr = 'Fn ReadADCPaths'):
    # this function reads the raw interleave data file; can be used to read any matrix data
    with open(fn) as f:
        r, c = [int(x) for x in f.readline().split(' ')] # read first line
        data = []
        for line in f: # read rest of lines
            data.append([float(x) for x in line.split(' ')])
        d = np.array(data)
    if plotFig:
       f = d[:,0]
       magIndx = np.arange(1,c,2)
       phaseIndx = magIndx+1
       plt.figure(figureNo); plt.clf();
       plt.subplot(211)
       plt.plot(f,d[:,1::2]); plt.grid('on'); plt.title(titleStr+':magnitude response');
       plt.xlabel('GHz'); plt.ylabel('dB')
       plt.subplot(212)
       plt.plot(f,d[:,2::2]); plt.grid('on'); plt.title('phase response')
       plt.xlabel('GHz'); plt.ylabel('deg')
       plt.tight_layout()

    return d, c

    """----------------------------------------------------------------------"""


def ReadPSPLFile(filename,makePositive):
    step = []
    if(DoesFileExist(filename)):
        fileObj = open(filename,"r")
        fileStr = fileObj.read()
        N    = FindNumberAfterString(r"Points:        ", fileStr)
        T    = FindNumberAfterString(r"XInc:        ", fileStr)
        fs = 1.0/T/1.0e9
        fileStrline = re.split(r'\n',fileStr)
        step = map(float,fileStrline[10:-1])
        step = np.array(step)
        if makePositive:
            step = -step

    return step

def ReadCachedComp_txt(fileName, debug = False):
    '''---------------------------------------------------------
    Reads the cached_comp_40p0.txt file format from given filename, returns sos, Fs'''
    d = LoadTxtFix(fileName)
    Fs = d[0]
    stages = d[1]
    j = 2
    sos = np.zeros((stages,6))         # first 3 elements of each row are numerator, last 3 are denominator
    for s in np.arange(stages):
        Fs = d[j];
        j += 1
        NumSize = int(d[j]);
        j += 1
        Num = d[j:j+NumSize];
        j += NumSize
        DenoSize = int(d[j])
        j += 1
        Deno = d[j:j+DenoSize];
        j += DenoSize

        sos[s,0:NumSize] = Num
        sos[s,3:DenoSize+3] = Deno

    return sos,Fs

def ReadCachedGD_txt(fileName, debug = False):
    '''---------------------------------------------------------
    Reads the cached_gd_40p0_3.txt file format from given filename, returns sos, Fs'''
    d = LoadTxtFix(fileName)
    power = d[0]
    ver = d[1]
    Fs = d[2]
    stages = d[3]
    j = 4
    sos = np.zeros((stages,6))         # first 3 elements of each row are numerator, last 3 are denominator
    for s in np.arange(stages):
        Fs = d[j];
        j += 1
        NumSize = int(d[j]);
        j += 1
        Num = d[j:j+NumSize];
        j += NumSize
        DenoSize = int(d[j])
        j += 1
        Deno = d[j:j+DenoSize];
        j += DenoSize

        sos[s,0:NumSize] = Num
        sos[s,3:DenoSize+3] = Deno

    return sos,Fs

# reads the temperature log file written during phase tests for DBI, which has values for all chips
# returns the array of strings with column headers, data matrix
# eg:Indx	Time				OvenSetTemp	BoardTemp	HAD1	HAD2	HAD3	HAD4	MSH1	MSH2	MSH3	MSH4	ClockTemp	TimeLOR	SR	OvenActualTemp	MFLOCoef0	CMFLOCoef1	HFLOCoef0	HFLOCoef1	ClkRef	BrdRef
#0	Sat, 18 Aug 2012 17:47:54 +0000	5		48.8		78.16	78.16	84.88	76.48	71.2	73.84	76.48	71.44	52.16		0.0	80.0	0.0		0.0		0.0		0.0		0.0	0.0	35.0
#1	Sat, 18 Aug 2012 17:48:53 +0000	5		44.72		72.4	75.76	82.96	70.96	65.68	69.04	70.48	65.68	52.16		0.0	80.0	0.0		0.0		0.0		0.0		0.0	0.0	22.8
def ReadTemperatureLog(fileName, NoOfCols = 22):
    # this function reads the raw interleave data file; can be used to read any matrix data
    with open(fileName) as f:
        strHeader = f.readline().split('\n')
        strHeaderPerCol = strHeader[0].split('\t')
        strHeaderPerColCopy = strHeaderPerCol
        for h in strHeaderPerColCopy:
            if h == '':
               strHeaderPerCol.remove('')

        data = np.zeros([1,NoOfCols])
        r = 0
        for line in f: # read rest of lines
            y = line.split('\n')
            dataStr = y[0].split('\t')
            c = 0
            for s in dataStr:
                if is_number(s):
                   data[r][c] = float(s)
                   c = c+1
                elif s == r'':
                     doNothing = 1;
                else:
                     data[r][c] = ConvertTimeStrToTimeStamp(s)
                     c = c+1
            r = r+1
            zeroRow = np.zeros([1,NoOfCols])
            data = np.vstack([data,zeroRow])
        return strHeaderPerCol,data

        """------------------------------------------------------------------"""

#   TODO :- this function is not fully functional. It works on files of specific types. Make it more
#   general. eg. before applying it to any file, remove all (i or j) from file in  complex nos in that file, using find and replace
def LoadTxtComplex(strFileName):
    """
    Utility Function :-

    Inputs :- (i) strFileName :- name of the file

    Outputs :- (i) npaReturnVal :- numpy array consisting of complex values

    Purpose :- This method reads complex values from the file, passed as argument,
               and return those values, in the form of numpy arrays.

               Note :- This method requires values to be <val1><space><val2> form.
                        eg. 2.34543423 4.324534344
                            where 2.34543423 is real value
                                  4.324534344 is complex value
    """
    npaStrVal = r = np.loadtxt(strFileName, delimiter = '\n',dtype = str)
    npaStrVal1 = map(str.split, npaStrVal)
    npaReturnVal = np.array([])
    for strVal in npaStrVal1:
        npaReturnVal = np.append(npaReturnVal, complex(float(strVal[0]), float(strVal[1])))

    return npaReturnVal

    """----------------------------------------------------------------------"""

def LoadTxtFixInt(fileName):
    '''---------------------------------------------------------
    Reads int from given filename, returns single array with all numbers'''
    r = np.loadtxt(fileName,delimiter = ' ',dtype=str)
    try:
        int(r[-1])
        deleteFlag = False
    except ValueError:
        deleteFlag = True

    if deleteFlag:
        r = np.delete(r,-1)

    r = list(map(int, r))
    r = np.array(r)
    return r

def LoadTxtFix(fileName):
    '''---------------------------------------------------------
    Reads doubles from given filename, returns single array with all numbers'''
    r = np.loadtxt(fileName,delimiter = ' ',dtype=str)
    try:
        float(r[-1])
        deleteFlag = False
    except ValueError:
        deleteFlag = True

    if deleteFlag:
        r = np.delete(r,-1)

    r = list(map(float, r))
    r = np.array(r)
    return r

def ReadStep_txt(fileName = r'\Step3.txt', debug = False):
    '''---------------------------------------------------------
    Reads the Step3.txt file format from given filename, returns time, step, rt, Fs '''
    d = LoadTxtFix(fileName)
    rt = d[0]
    N = d[1]
    time = d[2::2]
    step = d[3::2]

    Fs = 1.0/(time[1] - time[0])

    if debug == True:
       plt.figure(1222);plt.clf(); plt.plot(time,step); plt.grid('on'); plt.title('Fn ReadStep_txt:' + str(fileName));

    return time,step,rt,Fs

def WriteStep_txt(time,step,rt,fileName):
    '''---------------------------------------------------------
    Writes the Step3.txt file format '''
    N = len(time)
    strData = str(rt)
    strData += " " + str(N)
    for i in np.arange(N):
        strData += " " + str(time[i])
        strData += " " + str(step[i])
    AppendToFile(fileName, strData)
    return

def ReadResponse(fileName, debug = False):
    # function reads a file with N,x,y,x,y format data in it.

    r = LoadTxtFix(fileName)
    x = r[1::2]
    y = r[2::2]

    if debug == True:
       plt.figure(1221); plt.clf();plt.plot(x,Powerlog(y)); plt.grid('on'); plt.title('Fn ReadResponse:' + str(fileName));

    return x,y

def WriteResponseTxt(f,H,fileName):
    # function writes a file which is in the response.txt format

    N = len(f)
    strData = str(int(N))
    for i in np.arange(N):
        strData += " " + str(f[i])
        strData += " " + str(H[i])
    AppendToFile(fileName, strData)
    return

def WriteNumpyArray(x, fileName, formatStr = r'%15.15e', delimiter = r' ', delimiter_complex = r' ', bReturnString = False):
    # this function writes the numpy array in given format to a given filename
    # Eg:  WriteNumpyArray(x = firLPF, fileName = r"C:\work\Supriya\firLPF.txt")

    N = len(x)
    xStr = ""
    for i in np.arange(N):
        if x.conjugate == x.all():                            # x.conjugate == x.all() x.imag.all() == np.zeros([])
            xStr += str(formatStr%x[i]) + delimiter
        else:
            xStr += str(formatStr%x[i].real) + delimiter_complex + str(formatStr%x[i].imag) + '\n'

    if bReturnString == True:
        return xStr

    AppendToFile(fileName, xStr)

    return

def WriteCachedGDFilt_txt(p,v,Fs,fir,fileName):
    # function writes a file which is in the cashedgdfilt.txt format
    if DoesFileExist(fileName):     # delete the current file if exist
        DeleteFile(fileName)

    N = len(fir)
    stages = 1
    strData = str(str("%15.15e" %p )) +  " "  + str("%15.15e" %v ) +  " "  + str("%15.15e" %Fs ) +  " "  + str(int(stages)) +  " "  + str("%15.15e" %Fs )
    strData += " " + str(int(N))

    for i in np.arange(N):
        strData += " " + str(fir[i])

    NdenoCoeffs = 1
    denoCoeffs = 1.0

    strData += " " + str(int(NdenoCoeffs))
    strData += " " + str("%15.15e" %denoCoeffs )
    AppendToFile(fileName, strData)
    return

def DelCompensationPlotFiles(direcTree):
    '''---------------------------------------------------------
    # Deletes all the plot generated debug files from the scopes folder'''
    pattern = ('sr*.txt','shape*.txt','noise*.txt','low*.txt','Lin*.txt','impl*.txt','IFFT*.txt','high*.txt','hfe*.txt','gd*.txt','final*.txt','comp*.txt','chan*.txt','crf*.txt','rf*.txt');
    DelTreeFilePattern(pattern, direcTree);
    return;

'''#####################################################################################################
    Scope specific stuff
#####################################################################################################'''
def DevCode(ScopeIP = "127.0.0.1"):
    '''---------------------------------------------------------
    enters the dev code to the scope '''
    app = win32.DispatchEx('LeCroy.XStreamDSO', ScopeIP )
    app.Utility.Service.ServiceAccessCode = 22872201
    return

def OpenCompenstorDialog(Ch, DBIMode = 0, ScopeIP = "127.0.0.1"):
    ''' opens the compensator dialog box for respective scope channel'''
    app = win32.DispatchEx('LeCroy.XStreamDSO', ScopeIP )
    app.Utility.Service.ServiceAccessCode = 22872201

    if DBIMode == 1:
       if Ch == 2:
          app.MauiKernel.Processing.Processors("C2BWQuadruplerCompensator").ExpertMode.ActNow()
       elif Ch == 3:
          app.MauiKernel.Processing.Processors("C3BWQuadruplerCompensator").ExpertMode.ActNow()
       else:
            print "Error: Can't have any other channel than 2 or 3 for DBI."
    else:
       if Ch == 1:
          app.MauiKernel.Processing.Processors("C1Compensator").ExpertMode.ActNow()
       elif Ch == 2:
          app.MauiKernel.Processing.Processors("C2Compensator").ExpertMode.ActNow()
       elif Ch == 3:
          app.MauiKernel.Processing.Processors("C3Compensator").ExpertMode.ActNow()
       elif Ch == 4:
          app.MauiKernel.Processing.Processors("C4Compensator").ExpertMode.ActNow()

    return

def StopAcquiring(ScopeIP = "127.0.0.1"):
    '''---------------------------------------------------------
    Stop scope acquisition '''
    app = win32.DispatchEx('LeCroy.XStreamDSO', ScopeIP )
    app.Acquisition.Stop.ActNow()
    return

def AutoTrigger(ScopeIP = "127.0.0.1"):
    ''' sets the scope to auto trigger '''
    app = win32.DispatchEx('LeCroy.XStreamDSO', ScopeIP )
    app.SetAutoTriggerMode.ActNow()
    return

def SingleForceAcquisition(ScopeIP = "127.0.0.1"):
    '''---------------------------------------------------------
    Single scope acquisition '''
    app = win32.DispatchEx('LeCroy.XStreamDSO', ScopeIP )
    app.Acquisition.Arm.ActNow()
    Sleep(0.1)
    app.Acquisition.ForceTrigger.ActNow()
    return

def DoApproxNAcquisitions(ScopeIP = "127.0.0.1", N = 1, Source = "C1"):
    '''---------------------------------------------------------
    Does Approximately N scope acquisitions. Does NOT do anything to the trigger '''
    app = win32.DispatchEx('LeCroy.XStreamDSO', ScopeIP )
    start = app.MauiKernel.Acquisition.Boards("EagleAcqBoard").Channels(Source).ProcessingCompleteCount()
    final = start + N
    while (True):
          currentCount = app.MauiKernel.Acquisition.Boards("EagleAcqBoard").Channels(Source).ProcessingCompleteCount()
          if(currentCount > final):
              return
          Sleep(1.0)

def DoNAcquisitions(ScopeIP = "127.0.0.1", N = 1, Source = "C1", SleepBetwAcq = 0.2):
    '''---------------------------------------------------------
    Does N scope acquisitions. Uses Stop and Single Trigger '''
    app = win32.DispatchEx('LeCroy.XStreamDSO', ScopeIP )
    app.Acquisition.Stop.ActNow()
    start = app.MauiKernel.Acquisition.Boards("EagleAcqBoard").Channels(Source).ProcessingCompleteCount()
    print start
    final = start + N - 1
    print final
    while (True):
          currentCount = app.MauiKernel.Acquisition.Boards("EagleAcqBoard").Channels(Source).ProcessingCompleteCount()
          print currentCount
          app.Acquisition.Arm.ActNow()
          Sleep(SleepBetwAcq)
          if(currentCount >= final):
              return

def CalcTriggerToVclkTime(TdcCoarseCount, TdcFineCount, TdcOffset, TdcStretchFactor, TdcPeriod):
    '''---------------------------------------------------------
    returns the trigger to Vclk time, useful to make adjustments to waveform location whne triggering, for phase calculation.
    '''
    dTriggerToVClkTime = (np.double(TdcFineCount - TdcOffset)/TdcStretchFactor + TdcCoarseCount) * TdcPeriod
    return dTriggerToVClkTime

def SetForceSameADC(ScopeIP = "127.0.0.1", Val = True):
    '''---------------------------------------------------------
    Sets First data from same ADC '''
    app = win32.DispatchEx('LeCroy.XStreamDSO', ScopeIP )
    app.MauiKernel.Acquisition.Boards("EagleAcqBoard").Horizontal.FirstDataFromSameAdc = True
    return

def GetTDCCoarseAndFineValue(ScopeIP = "127.0.0.1"):
    '''---------------------------------------------------------
    returns the TDCfine and TDCcoarse values from the output pins of the acqboard '''
    app = win32.DispatchEx('LeCroy.XStreamDSO', ScopeIP )
    tdcFine = app.MauiKernel.Acquisition.Boards("EagleAcqBoard").Outputs("TdcFine").Result.Value
    tdcCoarse = app.MauiKernel.Acquisition.Boards("EagleAcqBoard").Outputs("TdcCoarse").Result.Value
    return tdcFine, tdcCoarse

def ADSOCmd(cmd):
    ''' converts a cvar path to Active DSO acceptable cmd.
    Eg: cmd = 'app.SaveRecall.Setup.PanelDir = "c:\\test"'   converts to
        adsoCmdStr = 'VBS \'app.SaveRecall.Setup.PanelDir = "c:\\test"\''       '''
    first = "VBS '";
    third = "'";
    adsoCmdStr = "{0}{1}{2}".format(first,cmd,third);
    return adsoCmdStr;

def ADSOQuery(cmd):
    ''' converts a cvar path to Active DSO acceptable query.
    Eg: cmd = 'app.InstrumentFamily'   converts to
        adsoCmdStr = 'VBS ? \' return = app.InstrumentFamily\''       '''
    first = "VBS? 'return = ";
    third = "'";
    adsoCmdStr = "{0}{1}{2}".format(first,cmd,third);
    print adsoCmdStr
    return adsoCmdStr;

def ActiveDSO(Address = "IP:127.0.0.1"):
    '''---------------------------------------------------------
    Instantiate Active DSO
    TODO: make helper functions to wrap the cmds for remote execution '''
    dso = win32.DispatchEx('LeCroy.ActiveDSOCtrl.1')
    dso.MakeConnection(Address)
    dso.WriteString("*IDN?",True)
    response = dso.ReadString(1e6)
    print response

    return dso


##def SaveWaveform(ScopeIP = "127.0.0.1", Source = "C1", FileName = "Wfrm.txt", WaveFormat = "ASCII", SubFormat = "TimeAmplitude", Delimiter = "Space", SaveDir = "D:\\Waveforms" ):
##    '''---------------------------------------------------------
##    Saves waveform files usign scope's save waveform '''
##    app = win32.DispatchEx('LeCroy.XStreamDSO', ScopeIP )
##
##    app.SaveRecall.Waveform.SaveTo = "File"
##    app.SaveRecall.Waveform.SaveSource = Source
##    app.SaveRecall.Waveform.WaveFormat = WaveFormat
##    app.SaveRecall.Waveform.SubFormat = SubFormat
##    app.SaveRecall.Waveform.Delimiter = Delimiter
##    app.SaveRecall.Waveform.WaveformDir = SaveDir
##    app.SaveRecall.Waveform.TraceTitle = st.rstrip(FileName,".txt")
##
##    app.SaveRecall.Waveform.DoSave.ActNow()
##    return

##def GetWaveform(ScopeIP = "127.0.0.1", Source = "C1", Npts = -1, debug = 0):
##    '''---------------------------------------------------------
##    Get float array from scope channel waveform '''
##    app = win32.DispatchEx('LeCroy.XStreamDSO', ScopeIP )
##
##    numSamples = app.Acquisition.Channels(Source).Out.Result.Samples
##    print numSamples
##    if (Npts == -1):
##        N = numSamples
##    else:
##        N = Npts
##
##    waveform = app.Acquisition.Channels(Source).Out.Result.DataArray
##
##    if (debug == 1):
##       plt.plot(waveform)
##
##    return waveform

##def GetMathWaveform(ScopeIP = "127.0.0.1", Source = "F1", Npts = -1, debug = 0):
##    '''---------------------------------------------------------
##    Get float array from scope math waveform '''
##    app = win32.DispatchEx('LeCroy.XStreamDSO', ScopeIP )
##
##    numSamples = app.Math.Functions(Source).Out.Result.Samples
##    print numSamples
##    if (Npts == -1):
##        N = numSamples
##    else:
##        N = Npts
##
##    waveform = app.Math.Functions(Source).Out.Result.DataArray
##
##    if (debug == 1):
##       plt.plot(waveform)
##
##    return waveform

##def ClearSweeps(ScopeIP = "127.0.0.1"):
##    '''-----------------------------------------------------------
##    Does a global clear sweeps'''
##    app = win32.DispatchEx('LeCroy.XStreamDSO', ScopeIP )
##
##    app.Acquisition.ClearSweeps.ActNow()
##    app.Measure.ClearSweeps.ActNow()
##    app.Math.ClearSweeps.ActNow()
##    #app.SDA2.ClearSweeps.ActNow()
##    return

##def RecallSetupFromFile(setupFileName, directory, ScopeIP = "127.0.0.1"):
##    '''-----------------------------------------------------------
##    Recall a setup file from particular directory'''
##    app = win32.DispatchEx('LeCroy.XStreamDSO', ScopeIP )
##    app.SaveRecall.Setup.PanelFilename = setupFileName
##    app.SaveRecall.Setup.PanelDir = directory
##    Sleep(0.5);
##    app.SaveRecall.Setup.DoRecallPanel.ActNow()
##    return;
##
##def SetScopeChannelForSineSweep(ch = "C3", Vdiv = 0.100, Input = "A", DBIMode = "", ScopeIP = "127.0.0.1"):
##    '''-----------------------------------------------------------
##    Setup the scope channel, sdev and freq parameters- used for sine sweep
##    Input = A, B, BHBW;
##    DBIMode = HBW,MBW,"";
##    '''
##    app = win32.DispatchEx('LeCroy.XStreamDSO', ScopeIP )
##    app.SaveRecall.Setup.DoRecallDefaultPanel.ActNow()
##
##    # Set DBI mode
##    if (DBIMode == "HBW"):
##        app.Acquisition.Horizontal.Dbi3Mode = 2
##    elif (DBIMode == "MBW"):
##        app.Acquisition.Horizontal.Dbi3Mode = 1
##    else:
##        app.Acquisition.Horizontal.Dbi3Mode = 0
##
##
##    # Set Input A vs B
##    if (Input == "A"):
##        app.Acquisition.C3.ActiveInput = 0
##    elif (Input == "B"):
##        app.Acquisition.C3.ActiveInput = 1
##    elif (Input == "BHBW"):
##        app.Acquisition.C3.ActiveInput = 2
##
##
##    # Set the required channel on
##    app.Acquisition.C1.View = 0
##    app.Acquisition.C2.View = 0
##    app.Acquisition.C3.View = 0
##    app.Acquisition.C4.View = 0
##    if (ch == "C3"):
##        app.Acquisition.C3.View = 1
##        app.Acquisition.C3.VerScale = Vdiv
##        app.Acquisition.C3.VerScaleVariable = 1
##    elif (ch == "C2"):
##        app.Acquisition.C2.View = 1
##        app.Acquisition.C2.VerScale = Vdiv
##        app.Acquisition.C3.VerScaleVariable = 1
##    elif (ch == "C1"):
##        app.Acquisition.C1.View = 1
##        app.Acquisition.C1.VerScale = Vdiv
##        app.Acquisition.C3.VerScaleVariable = 1
##    else:
##        app.Acquisition.C4.View = 1
##        app.Acquisition.C4.VerScale = Vdiv
##        app.Acquisition.C3.VerScaleVariable = 1
##
##
##    # set the time scale
##    app.Acquisition.Horizontal.HorScale = 100e-9
##
##    # setup freq on P2 on given channel as source
##    app.Measure.P1.View = 0
##    app.Measure.P2.Source1 = ch
##    app.Measure.P2.View = 1
##    app.Measure.ShowMeasure = 1
##    app.Measure.ViewP2 = 1
##    app.Measure.P2.ParamEngine = "Frequency"
##
##    # setup Sdev on P3 on given channel as source
##    app.Measure.P3.Source1 = ch
##    app.Measure.P3.View = 1
##    app.Measure.ShowMeasure = 1
##    app.Measure.ViewP3 = 1
##    app.Measure.P3.ParamEngine = "StandardDeviation"
##
##    return;

##def LogCurrentTemperature(filename, ScopeIP = "127.0.0.1"):
##    '''-----------------------------------------------------------
##    Logs board,ADC,MSH,clkmodule temperatures in a log file'''
##    app = win32.DispatchEx('LeCroy.XStreamDSO', ScopeIP )
##
##    DevCode(ScopeIP)
##    timeStr = GetCurrentTime()
##    hadC1 = app.MauiKernel.Acquisition.Boards("EagleAcqBoard").HealthMonitor.HADCH1
##    hadC2 = app.MauiKernel.Acquisition.Boards("EagleAcqBoard").HealthMonitor.HADCH2
##    hadC3 = app.MauiKernel.Acquisition.Boards("EagleAcqBoard").HealthMonitor.HADCH3
##    hadC4 = app.MauiKernel.Acquisition.Boards("EagleAcqBoard").HealthMonitor.HADCH4
##    boardTemp = app.MauiKernel.Acquisition.Boards("EagleAcqBoard").HealthMonitor.BoardTemp
##
##    mshC1 = app.MauiKernel.Acquisition.Boards("EagleAcqBoard").HealthMonitor.MSHCH1
##    mshC2 = app.MauiKernel.Acquisition.Boards("EagleAcqBoard").HealthMonitor.MSHCH2
##    mshC3 = app.MauiKernel.Acquisition.Boards("EagleAcqBoard").HealthMonitor.MSHCH3
##    mshC4 = app.MauiKernel.Acquisition.Boards("EagleAcqBoard").HealthMonitor.MSHCH4
##
##    clkModule = app.MauiKernel.Acquisition.Boards("EagleAcqBoard").HealthMonitor.ClkStatus
##
##    string = timeStr + " "
##    string += str(boardTemp) + " "
##    string += str(clkModule) + " "
##    string += str(hadC1) + " "
##    string += str(hadC2) + " "
##    string += str(hadC3) + " "
##    string += str(hadC4) + " "
##    string += str(mshC1) + " "
##    string += str(mshC2) + " "
##    string += str(mshC3) + " "
##    string += str(mshC4) + " "
##    AppendToFile(fileName = filename, stringToAppend = string)
##
##    return;
##
##def SaveImage(directory, filename, fileFormat = "PNG", ColorScheme = "Std", printArea = "DSOWindow", ScopeIP = "127.0.0.1" ):
##    ''' saves the scope image '''
##    app = win32.DispatchEx('LeCroy.XStreamDSO', ScopeIP )
##    app.HardCopy.Directory = directory
##    app.HardCopy.ImageFileFormat = fileFormat
##    app.HardCopy.HardcopyArea = printArea
##    app.HardCopy.UseColor = ColorScheme
##    app.HardCopy.Destination = "File"
##    app.HardCopy.FileName = filename
##
##    app.HardCopy.Print.ActNow()
##    return;
##
##def MakeSdevMeasurement(Vdiv = 0.05, Ch = 1, Input = r"A", Coupling = r"DC50", Fs = 40.0, ScopeIP = "127.0.0.1"):
##    ''' Sdev for noise measurement for given scope channel.
##    INCOMPLETE
##    '''
##    app = win32.DispatchEx('LeCroy.XStreamDSO', ScopeIP )
##
##    app.SaveRecall.Setup.DoRecallDefaultPanelWithTriggerModeAuto.ActNow()
##
##    if Input == r"A":
##       Input = r"InputA"
##    else:
##        Input = r"InputB"
##
##    app.Acquisition.C3.View = True
##    app.Acquisition.C4.View = True
##
##    return;

# find cvar(s) on specified object (or hierarchy) whose names (or types) match the specified expression.
# returns an array of strings (automation paths starting at specified object) or objects.
# takes optional arguments:
# infoLevel controls the amount of info printed (0 => name only [default], 1 => name+value,
# 2 => name+type+value, 3 => full signature).
# iRecurseLevels == 0 means no recursion.
# iRecurseLevels == -1 means "infinite" recursion (i.e. until no child objects found).
# Otherwise, iRecurseLevels specifies the number of levels in hierarchy to recurse.
# returnType arg is optional (defaults to 0, which returns a list of strings containing the cvar
# paths). if set to 1, returns cvar objects in the list. if set to 2, returns list of 2-element lists,
# so caller may get the path and the cvar object.
# bEcho if true prints each name to stdout as it is found (default is False).
#
# examples:
# 1. return string paths of all cvars under app hierarchy with full info level (full signature).
# findCvars(app, ".*", 3, -1)
# 2. return string paths of all cvars under app hierarchy which are register cvars (return name only).
# findCvars(app, "(re.search(r\"reg\", cvar.Type, re.IGNORECASE) != None)", 0, -1)
# 3. return string paths of all cvars directly on app object which are string cvars with CVARFLAGS_none (0).
# findCvars(app, "((re.search(r\"string\", cvar.Type, re.IGNORECASE) != None) & (cvar.Flags == 0))")
# 4. return string paths of all cvars under acq object whose full names (from acquisition) do match verscale on a channel.
# findCvars(acq, "verscale", 0, -1)
# 5. return string paths of all cvars under acq object whose full names (from acquisition) do not match verscale on a channel.
# findCvars(acq, "(re.search(r\"c\d+\.verscale\", fullname, re.IGNORECASE) is None)", 0, -1)
# 6. same as prev, except return cvar objects instead of string paths.
# findCvars(acq, "(re.search(r\"c\d+\.verscale\", fullname, re.IGNORECASE) is None)", 0, -1, 1)
# 7. same as prev, except return PathObjPair objects which hold the cvar object and string path.
# findCvars(acq, "(re.search(r\"c\d+\.verscale\", fullname, re.IGNORECASE) is None)", 0, -1, 2)
#
def findCvars(obj, matchExp = "", infoLevel = 0, recurseLevels = 0, returnType = 0, bEcho = False, prefix = ""):

    # check matchExp input arg to see if it will be handled as a regexp or eval expression.
    if (type(matchExp) == str):

        # if matchExp is a string, then check for special keywords "cvar, fullname, fullnameremote" which indicates
        # to evaluate the string expression rather than using as a regexp.
        if (re.search(r"\W+(cvar|fullname|fullnameremote)\W+", matchExp, re.IGNORECASE) is None):

            # if empty string, then default to match all
            if (len(matchExp) == 0):
                matchExp = ".*"

            # convert to a regex object, since it's more efficient
            matchExp = re.compile(matchExp, re.IGNORECASE)


    retList = list()

    try:

        bIsCvarBag = False
        try:
            strNameAuto = obj.NameAutomation
            bIsCvarBag = len(strNameAuto) > 0
        except AttributeError:
            bIsCvarBag = False

        prefix += obj.name + "."

        if bIsCvarBag:

            for item in enumerate(obj):

                cvar = item[1]

                fullname = prefix + cvar.Name
                fullnameremote = prefix + cvar.NameRemote

                #TODO: add support for "eval/exec" matching?
                bMatches = False
                bMatchesRemote = False
                if (type(matchExp) == str):

                    # matchExp is a string, so evaluate it as an expression (advanced/flexible mode)
                    bMatches = eval(matchExp)

                else:

                    # matchExp is a regex, so try to match against cvar name(s)
                    if re.search(matchExp, fullname):
                        bMatches = True
                    elif re.search(matchExp, fullnameremote):
                        bMatchesRemote = True

                if bMatches | bMatchesRemote:

                    strOut = fullname
                    if bMatchesRemote:
                        strOut = fullnameremote

                    # append to strOut according to infoLevel
                    if infoLevel >= 3:
                        strOut += ": " + cvar.Signature
                    elif infoLevel > 0:
                        cvarType = cvar.Type
                        if infoLevel == 2:
                            # append cvar type
                            strOut += ":" + cvarType

                        # append value
                        if (cvarType == "Action") | (cvarType == "Object") |(cvarType == "Image"):
                            strOut += " = { can't print value for this type }"
                        else:
                            #TODO: add better formatting for Double or Integer cvarType

                            strOut += " = " + cvar.GetAdaptedValueStringAutomation()

                    # append to return list depending on returnType
                    if (returnType == 0):
                        # return string
                        retList.append(strOut)
                    elif (returnType == 1):
                        # return cvar object
                        retList.append(cvar)
                    else:
                        # return list containing strOut and cvar object
                        retList.append(list((strOut, cvar)))

                    if bEcho:
                        print(strOut)
                        if len(strOut) > 80:
                            print("**************************************************")


        if (recurseLevels > 0) | (recurseLevels == -1) | (recurseLevels == -2):

            enumChildObjects = None

            if bIsCvarBag:
                enumChildObjects = enumerate(obj.Objects) #check if parent
            else:
                enumChildObjects = enumerate(obj) # if collection

            for item in enumChildObjects:

                childRecurseLevels = recurseLevels
                if childRecurseLevels > 0:
                    childRecurseLevels -= 1

                childObj = item[1]
                recurse = True

                #TODO: add support for recurseLevels == -2

                if recurse:

                    retList.extend(findCvars(childObj, matchExp, infoLevel, childRecurseLevels, returnType, bEcho, prefix))

    except:
        # nothing to do
        pass

    return retList

# call findCvars with bEcho==true, so cvars are displayed to stdout as they are found.
def printCvars(obj, matchExp = "", infoLevel = 0, recurseLevels = 0):

    listCvars = findCvars(obj, matchExp, infoLevel, recurseLevels, 0, True)
    print(str(len(listCvars)) + " cvar(s) found.")

##def SaveAllBTD(scopeIP = "127.0.0.1",force = False):
##    '''---------------------------------------------------------
##    this function saves all BTD to the scopes calibration folder  '''
##    app = win32.DispatchEx('LeCroy.XStreamDSO', scopeIP)
##    btd = app.MauiKernel.Acquisition.Boards("EagleAcqBoard").Calibration.Btd
##    if force:
##        btd.SaveAllBtd.ActNow()
##    else:
##        userInput = raw_input("Do you want to save ALL BTD ? Enter y OR n");
##        if userInput == 'y':
##            btd.SaveAllBtd.ActNow()
##        else:
##            print("coefficients NOT saving to BTD");
##    return;
##
##def SaveAllFLASH(scopeIP = "127.0.0.1", BoardId = 0, force = False):
##    '''---------------------------------------------------------
##    this function saves the calibration folder to flash   '''
##    app = win32.DispatchEx('LeCroy.XStreamDSO', scopeIP)
##    if force:
##        app.Acquisition.BTDMgr.BoardId = BoardId
##        app.Acquisition.BTDMgr.SaveToFlash.ActNow()
##    else:
##        userInput = raw_input("Do you want to save cablibration to FLASH ? Enter y OR n");
##        if userInput == 'y':
##            app.Acquisition.BTDMgr.BoardId = BoardId
##            app.Acquisition.BTDMgr.SaveToFlash.ActNow()
##        else:
##            print("Data NOT writing to FLASH");
##
##    return;


'''#####################################################################################################
    General Math stuff
#####################################################################################################'''
def Size(x):
    '''---------------------------------------------------------
    size : returns the size of rows, columns of any dimensional matrix'''
    dim = x.ndim
    sizes = np.zeros((dim+1))
    for d  in np.arange(dim):
        sizes[d] = x.shape[d]
    sizes[dim] = 1.0

    return sizes;

def Rows(x):
    sizes = Size(x)
    if (len(sizes) > 0):
       return sizes[0];
    else:
         return 0;

def Cols(x):
    sizes = Size(x)
    if(len(sizes) > 1):
                  return sizes[1];
    else:
         return 0;

def flipud(x):
    # returns numpy vector flipped upside down
    return x[::-1]

def MakeColVector(x):
    # only works for vectors
    if(Cols(x) > 1):
               x = x.T
    return x

def MakeRowVector(x):
    # only works for vectors
    if(Rows(x) > 1):
               x = x.T
    return x

def VectorToString(v,spacer = " "):
    # converts a vector of numbers into string separated by spacers
    outputStr = ""
    for i in np.arange(Rows(MakeColVector(v))):
        outputStr = AppendString(outputStr, v[i], spacer)
    return outputStr;

def AppendString(oriStr, value, spacer = " "):
    # appends the value to oriStr with a space in between
    if oriStr == "":
       return str(value);
    else:
         return oriStr + spacer + str(value)

def Cat(x,y):
    # column wise concatenate, rows should be same for both matrices
    if(IsEmpty(x)):
                   return y
    if(IsEmpty(y)):
                   return x

    z = np.column_stack((x,y))
    return z

def Stack(x,y):
    # row wise stack the matrices, cols should be same
    if(IsEmpty(x)):
                   return y
    if(IsEmpty(y)):
                   return x

    z = np.vstack((x,y))
    return z;

def Powerlog(x):
    '''---------------------------------------------------------
    Powerlog '''
    y = 20.0*np.log10(np.abs(x))
    return y

def gcd(num1, num2):
    '''---------------------------------------------------------
    Greatest common divisor: GCD'''
    if num1 > num2:
        for i in range(1,num2+1):
            if num2 % i == 0:
                if num1 % i == 0:
                    result = i
        return result

    elif num2 > num1:
        for i in range(1,num1+1):
            if num1 % i == 0:
                if num2 % i == 0:
                    result = i
        return result

    else:
        result = num1*num2/num1
        return result

def lcm(num1, num2):
    '''---------------------------------------------------------
    the function to calculate the LCM '''
    result = num1*num2/gcd(num1,num2)
    return result

def MaxMinAvgStdev(a):
    '''-----------------------------------------------------------------------------
    returns an array in the format of x[0] = max; x[1] = min ; x[2] = mean;
    x[3] = standard deviation for given vector'''
    x = np.arange(4.0)
    x[0] = np.max(a)
    x[1] = np.min(a)
    x[2] = np.mean(a)
    x[3] = np.std(a)
    return x

def MMASForMat(MatA):
    '''-----------------------------------------------------------------------------
    takes a matrix (will find the max min avg and sdev of each row in the matrix)
    returns a matrix with 4 cols and the number of rows in the given matrix'''
    dim = MatA.shape[0];

    MatRet = np.zeros(shape=(dim,4.0))
    for i in np.arange(dim):
        MatRet[i] = MaxMinAvgStdev(MatA[i])
    return MatRet

def RandMat(rows, cols, minval = 0, maxval = 1, NvsU = "N", stdev = 1, mean = 0):
    '''-----------------------------------------------------------------------------
    returns a random matrix fitting the specifications: if you want a normal
    distribution, you need only give specifications for rows, cols, stdev, mean and "N";
    if you want a uniform distribution, you give specifications for rows, cols, minval, maxval and "U" '''

    if NvsU=="N":
        MatRet = np.random.randn(rows,cols)*stdev + mean
    else:
        MatRet = np.random.rand(rows,cols)*(maxval-minval) + minval
    return MatRet

def integrate(x):
    '''---------------------------------------------------------
    # Function to integrate array x '''
    y = np.cumsum(x)
    return y

    """----------------------------------------------------------------------"""

def Sort(npaArrayToBeSorted, npaTargetArray):
    """
    Utility Function :-

    Inputs :- (i)   npaArrayToBeSorted :- numpy x (independent) array

              (ii)  npaTargetArray :- numpy y (dependent) array

    Outputs :- (i)  sorted numpy x (independent) array
               (ii) sorted numpy y (dependent) array

    Purpose :- This method sorts numpy x array in ascending order and accordingly modifies the numpy y array
    """
    if npaArrayToBeSorted == None or npaTargetArray == None:
        raise RuntimeError("LecroyUtil_portable.py :- npaArrayToBeSorted and npaTargetArray can not be None")

    if npaArrayToBeSorted.shape != npaTargetArray.shape:
        raise RuntimeError("LecroyUtil_portable.py :- both npaArrayToBeSorted and npaTargetArray must have same shape")

    npaIndependentArray = npaArrayToBeSorted
    #   obtained the indices of sorted array
    npaSortedIndices = np.argsort(npaIndependentArray)
    #   actually sorting the independent array
    npaIndependentArray.sort()
    #   adjusting the dependent array, as per the changs in independent array
    npaDependentArray = npaTargetArray.take(npaSortedIndices)

    #   returning independent and dependent array
    return npaIndependentArray, npaDependentArray

    """------------------------------------------------------------------"""

def IsXInBetWeenN1N2(x, n1, n2):
    """
    Utility Function :-

    Inputs :- (i)   x :- x value

              (ii)  n1 :- lower limit of range

              (iii) n2 :- upper limit of range

    Outputs :- This method checks whether the number x is with in range (n1, n2) or (n2, n1) not including n1 and n2

    Purpose :- This method returns True, if x lies with in the range (n1, n2) or (n2, n1), else returns False
    """
    bReturnValue = True

    if (n1 > n2):
        if (n1 > x) and (x > n2):
            bReturnValue = True
        else:
            bReturnValue = False
    else:
        if (n1 < x) and (x < n2):
            bReturnValue = True
        else:
            bReturnValue = False

    return bReturnValue

    """------------------------------------------------------------------"""

def CalcYForXInLinEq(dSlope, dIntercept, dxOry, bCalculateY = True):
    """
    Utility Function :-

    Inputs :- (i)   dSlope :- slope of line

              (ii)  dIntercept :- intercept of line equation

              (iii) dxOry :- double value. It can be x or y. It'll be regarded as
                             x val, when bCalculateY is True and as y val, when
                             bCalculateY is False.

              (iv)  bCalculateY :- boolean value. True specifies calculate Y for given X.
                                                  False specifies calculate X for given Y

    Purpose :- This method calculates x for given y or y for given x based on bCalculateY argument, on the
                basis of slope and intercept parameter of equation of line
    """
    dOutputxory = 0.0
    if bCalculateY:
        #   y = intercept + (slope * x)
        dOutputxory = dIntercept + (dSlope * dxOry)
    else:
        #   x = (y - intercept) / slope
        dOutputxory = (dxOry - dIntercept) / dSlope

    return dOutputxory

    """------------------------------------------------------------------"""

def GetLineEquation(tupDPoint1, tupDPoint2):
    """
    Utility Function :-

    Inputs :- (i)   tupDPoint1 :- tuple containing point 1, i.e., (x1, y1)

              (ii)  tupDPoint2 :- tuple containing point 2, i.e., (x2, y2)

    Outputs :-(i)   dSlope :- slope of the line

              (ii)  dIntercept :- intercept of the line

    Purpose :- This method calculates the equation of line and returns its slope and intercept
    """
    dSlope = 0.0
    dIntercept = 0.0

    #   calculated the slope (endYVal - startYVal) / (endXVal - startXval)
    #`  The equation of line is yVal = intercept + slope * xVal
    dSlope = float(tupDPoint2[1] - tupDPoint1[1]) / float(tupDPoint2[0] - tupDPoint1[0])

    #   calculated intercept (yVal - (slope * xVal))
    dIntercept = tupDPoint1[1] - (dSlope * tupDPoint1[0])

    return dSlope, dIntercept

    """------------------------------------------------------------------"""
def IsEven(iNo):
    """
    Utility Function :-

    Inputs:  1) iNo: number

    Output: True if number is even, else False

    Purpose: checks whether passed number is even or odd
    """
    bReturnVal = False
    #check a number is even or not by modulo operator %
    if((iNo % 2) == 0):
        bReturnVal = True

    return bReturnVal

    """----------------------------------------------------------------------"""
def Linspace(dStart, dInterval, iNumberOfPts):
    """
    Utility Function :-

    Inputs :- (i)   dStart :- start value

              (ii)  dInterval :- interval value or step value

              (iii) iNumberOfPts :- number of samples or points

    Outputs :- numpy array of size iNumberOfPts.

    Purpose :- returns the vector of numbers, with dStart as its first element, difference between
               adjacent element in vector as dInterval and iNumberOfPts as size.
    """
    npaVector = np.linspace(dStart, dStart + (dInterval * iNumberOfPts), iNumberOfPts, endpoint = False)

    return npaVector

    """----------------------------------------------------------------------"""

'''#####################################################################################################
    DSP stuff
#####################################################################################################'''
def GetHalfSpectrumSize(N):
    '''---------------------------------------------------------
    Returns length of the positive spectrum and Nyquist present
    function NHalf, bNyquistPresent = GetHalfSpectrumSize(N)
    inputs:
           N: size of input time domain signal array
    output:
           Nhalf: size of the positive spectrum only
           bNyquistPresent: returns if nyquist frequency is present or not'''

    if (iN%2):
        bNyquistPresent = False
        iNHalf = math.floor(iN/2)+1
    else:
        bNyquistPresent = True
        iNHalf = iN/2 + 1

    return iNHalf, bNyquistPresent

def GetHalfSpectrum(npaF, npaH):
    '''---------------------------------------------------------
    Returns the positive complex spectrum and its frequency
    function  npaFHalf, npaHHalf = GetHalfSpectrum(npaF, npaH)
    inputs:
           npaF: numpy array containing +ve and -ve Frequency
           npaH: numpy array containing +ve and -ve complex spectrum
    output:
           npaFHalf: numpy array containing only +ve frequencies
           npaHHalf: numpy array containing only -ve frequencies'''

    N = np.size(npaF)
    NHalf, NyquistPresent = GetHalfSpectrumSize(N)

    npaFHalf = npaF[0:NHalf]
    npaHHalf = npaH[0:NHalf]

    return npaFHalf, npaHHalf

def GetFullSpectrum(npaFHalf, npaHHalf, bNyquistPresent):
    if bNyquistPresent == False:
       npaF = np.concatenate(npaFHalf,npaFHalf[1::-1])
       npaH = np.concatenate(npaH,npaH[1::-1])
    else:
         npaF = np.concatenate(npaFHalf,npaFHalf[1::-1])
         npaH = np.concatenate(npaH,npaH[1::-1])

    """----------------------------------------------------------------------"""

def Levin(npaA, npaB):
    """
    Utility Function :-

    Inputs :- (i)   npaA :- numpy X array

              (ii)  npaB :- numpy Y array

    Outputs :- (i)  npaX :- solution of Ax = b problem.

    Purpose :- It's used to perform the inverse of a positive definite hermitian toeplitz matrix
    """
    npaA = npaA.reshape(npaA.size, 1)
    npaB = npaB.reshape(npaB.size, 1)
    iLength = npaA.size
    npaT = None
    npaX = None
    if (str(type(npaA[1, 0])) == "<type 'numpy.complex128'>") and (str(type(npaB[1, 0])) == "<type 'numpy.complex128'>"):
        npaT = np.zeros((iLength, 1), dtype = "complex")
        npaX = np.zeros((iLength, 1), dtype = "complex")
    else:
        npaT = np.zeros((iLength, 1))
        npaX = np.zeros((iLength, 1))
    npaT[0, 0] = 1
    alpha = npaA[0]

    if alpha == 0:
        raise RuntimeError("LecroyUtil_portable.py :- alpha is zero.")

    npaX[0, 0] = npaB[0, 0] / npaA[0, 0]

    for i in range(0, iLength - 1):
        k = -(np.dot(npaA.take(np.arange(i + 1, 0, -1)).conj(), npaT[:i + 1, 0])) / alpha
        dResult = (k * np.flipud(npaT[:i + 2, 0].conjugate()))
        npaT[:i + 2, 0] += dResult
        alpha *= (1 - (abs(k) ** 2))

        if alpha == 0:
            raise RuntimeError("LecroyUtil_portable.py :- alpha is zero.")

        k = (npaB[i + 1] - np.dot(npaA.take(np.arange(i + 1, 0, -1)).conj(), npaX[:i + 1, 0])) / alpha
        dResult = k * np.flipud(npaT[: i + 2, 0].conjugate())
        npaX[: i + 2, 0] += dResult

    return npaX

    """----------------------------------------------------------------------"""

#   TODO :- check for complex inputs
def LSLevin(N, npaOm, npaD, npaW):
    """
    Utility Function :-

    Inputs :- (i)   N :-

              (ii)  npaOm :-

              (iii) npaD :-

              (iv)  npaW :-

    Outputs :-

    Purpose :- implementation of ls Levin algorithm
    """
    npaOm = npaOm.reshape(npaOm.size, 1)
    npaD = npaD.reshape(npaD.size, 1)
    npaW = npaW.reshape(npaW.size, 1)
    iLength = npaOm.size

    if iLength <= 0:
        raise RuntimeError("LecroyUtil_portable.py : iLength is zero.")

    npaReal = npaD.real
    npaImag = npaD.imag
    npaA = np.zeros((N, 1))
    npaB = np.zeros((N, 1))
    npaDVec = npaD.copy()
    npaEVec = np.ones((iLength, 1))
    e1 = np.exp(1j * npaOm)

    for i in range(0, N):
        npaA[i] = np.dot(npaW.transpose(), npaEVec.real)
        npaB[i] = np.dot(npaW.transpose(), npaDVec.real)
        npaEVec = npaEVec * e1
        npaDVec = npaDVec * e1

    npaA = npaA / iLength
    npaB = npaB / iLength
    npaX = Levin(npaA, npaB)

    return npaX

    """----------------------------------------------------------------------"""

def Fftf(y,fs,returnFullSpectrum = 0,Normalize = 0,debug = 0):
    '''---------------------------------------------------------
    Calculates the fft of given waveform
    function  [Y,f] = fftf(y,fs,returnFullSpectrum,Normalize);
    This function takes in data in y, sampling rate in fs and
    returns the freq. pts in f and the spectrum from 0 to fs/2 in Y
       returnFullSpectrum = 1 then we return the +ve and then -ve part of
                            the spectrum in Y and f
       Normalize = 1, would divide the spectrum with 1/N where N = len(y)'''

    N = np.size(y)
    NHalf, NyquistPresent = GetHalfSpectrumSize(N)

    # calculate the freq. values
    f = np.fft.fftfreq(N,1.0/fs)

    # calculate the FFT
    Y = np.fft.fft(y);

    if (Normalize == 1):
        Y = Y/N

    if (returnFullSpectrum == 0):
        f = f[0:NHalf]
        Y = Y[0:NHalf]

    if (NyquistPresent == 1):
        f[-1] = -f[-1]

    if (debug == 1):
        plt.figure(2)
        plt.plot(f,Powerlog(Y))
        plt.draw()

    return Y,f

def NForFullCycle(Fs_Num,Fs_Den,Ref_Num,Ref_Den):
    '''---------------------------------------------------------
    returns the no. of points needed for full cycle of sinewave '''
    N = lcm(Ref_Num*Fs_Den, Ref_Den*Fs_Num)/(Ref_Num*Fs_Den);
    N = int(N)
    return N

def FreqIndxInFFT(Fs_Num,Fs_Den,Ref_Num,Ref_Den,N):
    '''---------------------------------------------------------
    returns the index of a particular frequency in a frequency vector '''
    indx = Ref_Num*float(N)*Fs_Den/(Ref_Den*Fs_Num)
    indx = int(indx)
    return indx

def Angle(X):
    '''---------------------------------------------------------
    returns the angle in Radians given input complex vector '''
    ang = np.angle(X)
    return ang

def AngleInDeg(ang, mod = 0):
    '''---------------------------------------------------------
    returns the angle in Degrees given input of angles in radians
    if mod = 1, then a value between 0.0-360.0 returned'''
    angInDeg = ang*180.0/math.pi

    if(mod == 1):
        angInDeg = angInDeg%360.0

    return angInDeg

def AngleInDegToTime(ang,Fin):
    '''---------------------------------------------------------
    returns the time in ns for a given angle in Degrees for an input freq '''
    T = 1.0/Fin
    return ang*T/360.0

def GrpDelayFromH(H,f,timeDelay = 0.0):
    '''---------------------------------------------------------
    calculates the group delay for a given input spectrum H and
    frequency vector, adjusts for a time delay of the step '''
    # timeDelay = 0.0 for general case, if we want to add delay then its any value.

    constant = 2.0*np.pi*timeDelay*1J
    H *= np.exp(constant*f)
    unwrappedPhaseData = np.unwrap(Angle(H))
    unwrappedPhase = unwrappedPhaseData.copy()
    for i in np.arange(len(H)):
        unwrappedPhase[i] = unwrappedPhaseData[i]

    dOmega = 2.0*np.pi*(f[1] - f[0])
    gd = - np.diff(unwrappedPhase.T)/dOmega
    gd = np.append(gd,gd[-1])
    gd = gd.T

    return gd,unwrappedPhase

def StepBaseAndTop(step):
    """
    Utility Method :-

    Inputs :- (i) step

    Outputs :- top, bottom of the steps

    Purpose :- It calculates the top and bottom values for the step passed to it as argument.
    """
    Nbins = 128
    counts,centers = np.histogram(step,bins = Nbins)
    indx = np.argmax(counts[0:Nbins/2])
    bottom = centers[indx]

    indx = np.argmax(counts[Nbins/2:])
    top = centers[indx+Nbins/2]

    return top, bottom

    """----------------------------------------------------------------------"""

def ROP(step,Fs, Calc1090 = True):
    '''---------------------------------------------------------
    calculates the steps risetime overshoot and preshoot values '''
    step = step - np.min(step)
    top, bottom = StepBaseAndTop(step)
    amplitude = top - bottom

    Overshoot = 100.0*abs(np.max(step) - top)/amplitude
    Preshoot = 100.0*abs(np.min(step) - bottom)/amplitude

    if Calc1090 == True:
       thresLo = amplitude*0.1
       thresHi = amplitude*0.9
    else:
       thresLo = amplitude*0.2
       thresHi = amplitude*0.8

    timeStartIndx = 0; timeEndIndx = 0

    MaxIndx = np.argmax(step)
    MinIndx = np.argmin(step)
    for i in range(MinIndx,MaxIndx,1):
        if(step[i-1] <= thresLo) and (step[i] >= thresLo):
                     timeStartIndx = (thresLo-step[i-1]) / (step[i] - step[i-1]) + i - 1
                     break

    startIndx = i
    for i in range(startIndx,MaxIndx,1):
        if(step[i-1] <= thresHi) and (step[i] >= thresHi):
                     timeEndIndx = (thresHi-step[i-1]) / (step[i] - step[i-1]) + i - 1
                     break

    rt = (timeEndIndx - timeStartIndx)/Fs

    return rt,Overshoot,Preshoot

    """----------------------------------------------------------------------"""

def AlignSteps(lsnpaSteps, lsnpaTimeVector, lsFs, lsStrLegends = None, bDrawPlt = False, iFigNum = 9440):
    """
    Utility Function :-

    Inputs :- (i) lspnaSteps :- list of numpy arrays representing step values

              (ii) lsnpaTimeVector :- list of time numpy arrays

              (iii)lsFs :- list containing sampling rates

              (iv) lsStrLegends :- list of strings to be displayed as legends on the traces

              (v) bDrawPlt :- boolean value specifying, whether to draw plot

              (vi) iFigNum :- figure number for the plot

    Outputs :- (i) lsnpaTempTimeVector :- list of aligned time numpy arrays

               (ii) lsnpaTempSteps :- list of aligned numpy arrays

    Purpose :- Align all the step delays, such that the rising edges are on top of each other
    """
    #list which stores the step delays for each step vector
    lsDStepDelays = []

    #variable which stores the value of maximum stepdelay
    maxStepDelay = 0.0

    #output list of aligned numpy array of steps
    lsnpaTempSteps = []
    #output list of aligned numpy array of time
    lsnpaTempTimeVector = []

    for iCounter in range(0, len(lsnpaSteps)):
        #calculating step delay
        stepDelay = StepDelay(lsnpaSteps[iCounter], lsFs[iCounter])

        if iCounter == 0:
            maxStepDelay = stepDelay

        if stepDelay > maxStepDelay:
            maxStepDelay = stepDelay
        #appending the step delay for the plot in the list
        lsDStepDelays.append(stepDelay)

    for iCounter in range(0, len(lsnpaSteps)):
        #in case of step with maximum step delay, don't do any calculations
        if lsDStepDelays[iCounter] == maxStepDelay:
            lsnpaTempTimeVector.append(lsnpaTimeVector[iCounter])
            lsnpaTempSteps.append(lsnpaSteps[iCounter])
            continue

        #calculating the number of points to be base padded
        dPaddingPtsCnt = (maxStepDelay - lsDStepDelays[iCounter]) * lsFs[iCounter]

        #calculating the value of top and bottom
        iTopValue, iBaseValue = StepBaseAndTop(lsnpaSteps[iCounter])

        #creating the numpy array, of dPaddingPtsCnt elements
        #and populating all its values will be base value
        npaBaseValues = numpy.ones(dPaddingPtsCnt)*iBaseValue

        #padding the numpy array containing base values at the begining of the step array
        lsnpaTempSteps.append(numpy.append(npaBaseValues, lsnpaSteps[iCounter]))

        #calculating the end time. As base padding is done, new time points have to be added
        #So for that calculating the final time point
        dEndVal = ((1.0 / lsFs[iCounter]) * (dPaddingPtsCnt)) + numpy.max(lsnpaTimeVector[iCounter])
        #created a numpy array starting from the first element of time, to the dEndVal, and each value in
        #array differs by (1 / lsFs[iCounter]) value
        lsnpaTempTimeVector.append(numpy.arange(lsnpaTimeVector[iCounter][0], dEndVal, (1.0 / lsFs[iCounter])))

    if bDrawPlt:
        plt.figure(iFigNum)
        if lsStrLegends == None:
            lsStrLegends = []
            lsStrLegends += ("Trace " + str(i) for i in range(0, len(lsnpaTempSteps)))
        for iCounter in range(0, len(lsnpaTempSteps)):
            plt.plot(lsnpaTempTimeVector[iCounter], lsnpaTempSteps[iCounter], label = lsStrLegends[iCounter], marker = "x")
            plt.legend(loc = "lower right")
            plt.grid(True)

    return lsnpaTempTimeVector, lsnpaTempSteps

    """----------------------------------------------------------------------"""

def ScaleSteps(lsnpaSteps, lsnpaTimeVector, iNewAmplitude = 1, dStaggerX = 0.0, dStaggerY = 0.0,  lsStrLegends = None, bDrawPlt = False, iFigNum = 4564):
    """
    Utility function :-

    Inputs :- (i) lsnpaSteps :- list of numpy arrays representing step values

              (ii) lsnpaTimeVector :- list of numpy arrays representing time

              (iii) iNewAmplitude :- represent the point where all the step plots must be scaled to.

              (iv) dStaggerX :- represents the value, by which each trace have to be moved either left or right, when compared
                                with its predecessor trace

              (v) dStaggerY :- represents the value, by which each trace have to be moved either top or bottom, when compared with
                                its predecessor trace

              (vi) lsStrLegends :- list of strings to be displayed as legends on the traces

              (vii) bDrawPlt :- boolean value specifying, whether to draw plot or not

              (viii) iFigNum :- Figure number of the plot

    Outputs :- (i) lsnpaTempTimeVector :- list of scaled time numpy arrays

               (ii) lsnpaTempSteps :- list of scaled numpy arrays

    Purpose :- scales the steps to iNewAmplitude, passed as argument
    """
    #output list of scaled numpy array of steps
    lsnpaTempSteps = []
    #output list of scaled numpy array of time
    lsnpaTempTimeVector = []

    for iCounter in range(0, len(lsnpaSteps)):
        #getting step top and bottom values
        top, bottom = StepBaseAndTop(lsnpaSteps[iCounter])
        #calculating amplitude
        amplitude = top - bottom
        #setting the offset of the step to 0
        lsnpaTempSteps.append(lsnpaSteps[iCounter] - bottom)
        #scaling the plot to iNewAmplitude passed as argument
        lsnpaTempSteps[iCounter] *= (iNewAmplitude / amplitude)
        #adding stagger value to the y-axis cordinates
        lsnpaTempSteps[iCounter] += (iCounter * dStaggerY)
        #adding stagger value to the x-axis cordinates
        lsnpaTempTimeVector.append(lsnpaTimeVector[iCounter] + (iCounter * dStaggerX))

    if bDrawPlt:
        plt.figure(iFigNum)
        if lsStrLegends == None:
            lsStrLegends = []
            lsStrLegends += ("Trace " + str(i) for i in range(0, len(lsnpaTempSteps)))

        for iCounter in range(0, len(lsnpaTempSteps)):
            plt.plot(lsnpaTempTimeVector[iCounter], lsnpaTempSteps[iCounter], label = lsStrLegends[iCounter], marker = "x")
            plt.legend(loc = "lower right")
            plt.grid(True)

    return lsnpaTempTimeVector, lsnpaTempSteps

    """----------------------------------------------------------------------"""

def CheckFreqResponse(npaX, npaY, npaXLimit, npaYHiLimit, npaYLowLimit, bPlot = False, iFigNum = 23453445, iSubPlotNum = 111):
    """
    Utility Function

    Inputs :- (i)   npaX :- numpy array of frequency

              (ii)  npaY :- numpy array of response

              (iii) npaXLimit :- numpy array containing frequencies for which limit values are given

              (iv)  npaYHiLimit :- numpy array containing higher limit response values

              (v)   npaYLowLimit :- numpy array containing lower limit response values

              (vi) bPlot :- boolean value specifying whether to draw plot or not

              (vii) iFigNum :- Figure number of plot

              (viii)iSubPlotNum :- Subplot number

    Outputs :- True if limits are not violated else returns False, npaLimitViolationVector :- numpy array of
                points which violates limit. It's of (freq, response) value form

    Purpose :- check input vector against limits
    """
    #   raise error, if frequency vector is empty
    if len(npaX) <= 0:
        raise RuntimeError("Frequency numpy array must not be empty")

    #   raise error, if frequency vector and response vector are not unequal shape
    if npaX.shape != npaY.shape:
        raise RuntimeError("Both frequency and response numpy arrays must be of same shape")

    #   raise error, if limit frequency vector is empty
    if len(npaXLimit) <= 0:
        raise RuntimeError("Limit frequency numpy array must not be empty")

    #   raise error, if limit frequency vector and high limit response vector are of unequal shape
    if npaXLimit.shape != npaYHiLimit.shape:
        raise RuntimeError("Both limit frequency array and high limit response array must have same shape")

    #   raise error, if limit frequency vector and low limit response vector are of unequal shape
    if npaXLimit.shape != npaYLowLimit.shape:
        raise RuntimeError("Both limit frequency array and low limit response array must have same shape")

    #   found the interpolation function for low limit response vector
    lowLimitInterpolationFunc = sp.interpolate.interp1d(npaXLimit, npaYLowLimit, kind = "zero")

    #   found the interpolation function for high limit response vector
    highLimitInterpolationFunc = sp.interpolate.interp1d(npaXLimit, npaYHiLimit, kind = "zero")

    #   recalculated new higher and lower limits at each point, with the help of
    #   interpolation functions obtained
    npaNewHiLimit = highLimitInterpolationFunc(npaX)
    npaNewLowLimit = lowLimitInterpolationFunc(npaX)
    #   numpy array, which will store the (freq, res) points, which violates limits
    #   By default, it's size is equal to number of frequency points
    npaLimitViolationVector = np.zeros((len(npaX), 2))

    #   integer value which store the number of points violating the limits criteria
    iNumberOfElements = 0
    #   iterating through each element of response vector
    for iIdx, dVal in enumerate(npaY):
        if (npaNewLowLimit[iIdx] > npaNewHiLimit[iIdx]):
            raise RuntimeError("Interpolated lower limit is higher that interpolated higher limit")
        #   if response vector element, do not lies between the limits, then add it
        #   to the limits violation vector
        if (dVal >= npaNewHiLimit[iIdx] or dVal <= npaNewLowLimit[iIdx]):
            npaLimitViolationVector[iNumberOfElements] = [npaX[iIdx], dVal]
            iNumberOfElements += 1

    #   chopping only first iNumberOfElements from limit violation vector and reassigning it to itself
    npaLimitViolationVector = npaLimitViolationVector[:iNumberOfElements]
    bLimitsViolated = False

    if iNumberOfElements > 0:
        bLimitsViolated = True

    if bPlot:
        plt.figure(iFigNum)
        plt.subplot(iSubPlotNum)
        plt.plot(npaX, npaNewHiLimit, marker = "x", label = "Hight limit")
        plt.plot(npaX, npaNewLowLimit, marker = "s", label = "Low limit")
        plt.plot(npaX, npaY, marker = "o", label = "Original response")
        plt.plot(npaLimitViolationVector[:, 0], npaLimitViolationVector[:, 1], "y d", label = "Limit violating points")
        plt.legend(loc = "best")
        plt.grid(True)
        strTitle = "Fn CheckFreqResponse -"
        if bLimitsViolated:
            strTitle += " Fail"
        else:
            strTitle += " Pass"

        plt.title(strTitle)

    return not(bLimitsViolated), npaLimitViolationVector

    """------------------------------------------------------------------"""

def StepResponse(iN, iFsin, iFsfilter, npaFirFilter, npaLowImageRejFilter, npaInputStep = None, bPlot = False, iFigNum = 32434254):
    """
    Utility Function :-

    Inputs :- (i)   iN :- size of step

              (ii)  iFsin :- Sampling frequency

              (iii) iFsfilter :- Sampling frequency of fir

              (iv)  npaFirFilter :- numpy array of fir filter

              (v)   npaLowImageRejFilter :- numpy array of low pass filter

              (vi) npaInputStep :- incase user want to send in the input step itself to be used, this
                                step is not filtered via the lowImageRejFilter

              (vii)  bPlot :- boolean value specifying whether to show plot

              (viii) iFigNum :- figure number

    Outputs :- (i) npaFinal :- final filtered step

    Purpose :- This method calculates the low pass filter and actual filter passed to it as argument and return
                final filter
    """
    if npaInputStep == None:
        #   creating ideal step
        npaIdealStep = np.zeros(iN)
        npaIdealStep[(iN / 2):] = 1

        #   plotting ideal filter, if plotting is enabled
        if bPlot:
            plt.figure(iFigNum)
            plt.subplot(131)
            plt.plot(npaIdealStep, marker = "s")
            plt.axis([0, iN, -2, 2])
            plt.grid(True)
            plt.title("Fn StepResponse : Ideal step")

        #   passing ideal step through lowpass filter
        npaOut = Filter(npaLowImageRejFilter, 1, npaIdealStep)
    else:
        npaOut = npaInputStep

    #   plotting resulting low pass filtered step, if plotting is enabled
    if bPlot:
        plt.subplot(132)
        plt.plot(npaOut, marker = "x")
        plt.axis([0, iN, -2, 2])
        plt.grid(True)
        plt.title("Fn StepResponse : Lowpass filtered step")

    #   calculate oversampling rate
    iPolyFactor = (iFsin / iFsfilter)
    #   numpy array which will store final actally filtered step
    npaFinal = np.zeros((len(npaOut), 1))
    for i in np.arange(0, iPolyFactor, 1):                                                                           # Filtering through FIR or IIR filter
        npaTemp = Filter(npaFirFilter, 1, npaOut[i::iPolyFactor]);
        npaFinal[i::iPolyFactor] = npaTemp.reshape(Rows(npaTemp), 1)
    #   plotting final step, if plotting is enabled
    if bPlot:
        plt.subplot(133)
        plt.plot(npaFinal, marker = "d")
        plt.axis([0, iN, -2, 2])
        plt.grid(True)
        plt.title("Fn StepResponse : Actual filtered step")

    #   return final actually filtered step
    return npaFinal

    """----------------------------------------------------------------------"""

def Freq(iNoFullSpec, dFs, bNyquistPresent):
    """
    Utility Function :-

    Inputs:  1) iNoFullSpec: number of points in full spectrum freq

             2) dFs: sample rate

             3) bNyquistPresent: asks for nyquist freq to be included

    Outputs: return vector of positive spectrum frequencies

    Purpose: Calculate Frequency vector
    """
    #in case when Nyquist is present
    if bNyquistPresent:
        if(not IsEven(iNoFullSpec)):
            #if iNoFullSpec is not even then increment it by 1
            iNoFullSpec += 1
        npaVector = np.arange(0, (iNoFullSpec / 2) + 1, dtype = 'float')
    #in case when Nyquist is not present
    else:
        if(IsEven(iNoFullSpec)):
            #if iNoFullSpec is even then increment it by 1
            iNoFullSpec += 1
        npaVector = np.arange(0, ((iNoFullSpec - 1) / 2) + 1, dtype='float')

    dScale = float(dFs) / float(iNoFullSpec)
    npaVector = npaVector * dScale

    return npaVector
    """----------------------------------------------------------------------"""

##def GrpDelayOfFilter(npaNum, npaDeno, f, Fs, debug = False):
##    """
##    Utility Function :-
##
##    Inputs :- (i)   npaNum :- numpy array containing numerator part of coefficient
##
##              (ii)  npaDeno :- numpy array containing denominator part of coefficient
##
##              (iii) f :- numpy array of filter
##
##              (iv)  Fs :- sampling frequency
##
##              (v)   debug :- boolean value specifying, whether this function is invoked from debug mode
##
##    Outputs :- group delay
##
##    Purpose :- This function calculates the group delay for the filter passed as argument
##    """
##    #   calculating response
##    H = Freqz(npaNum, npaDeno, f, Fs, debug = debug)
##
##    #   calculating groud delay
##    gd, unwrappedPhase = GrpDelayFromH(H, f)
##
##    return gd
##
##    """----------------------------------------------------------------------"""

def Spec(npaNum, npaDeno, f, Fs, bIsSOS = False, bPlotFig = False, iFigNum = 141124, bClearFigure = True):
    """
    Utility Function :-

    Inputs :- (i)   npaNum :- numpy array containing numerator part of coefficient

              (ii)  npaDeno :- numpy array containing denominator part of coefficient

              (iii) f :- numpy array of filter

              (iv)  Fs :- sampling frequency

              (v)   bIsSOS :- True if filter is for second order system

              (vi)  bPlotFig :- True if plot have to be shown, else False

              (vii) iFigNum :- figure number

              (viii)bClearFigure :- True if the plot have to be cleared, otherwise False

    Outputs :-  (f, H)
              Note :- at present it's not returning gd. But in future, after GrpDelayOfFilter problem
                      is solved, it'll return gd.

    Purpose :- This method plots the filter passed as argument and return response and group-delay of filter.
    """
    if(len(f) == 1):
        f = Freq(2 * f, fs, True)

    f = MakeColVector(f)

    #   ask sir, from where to get gd, if bIsSOS is True, as Freqzsos is not returning group delay
    if (bIsSOS):
        sos = npaNum
        H = Freqzsos(sos, f, Fs)

    else:
        H = Freqz(npaNum, npaDeno, f, Fs)
        #   these lines will be uncommented, after GrpDelayOfFilter problem is solved. Till then
        #   we'll return None as Group delay
        ##gd = GrpDelayOfFilter(npaNum, npaDeno, f, Fs)

    ##gd = gd / Fs
    gd = None

    if(bPlotFig):
        plt.figure(iFigNum);
        if (bClearFigure):
            plt.clf()

        plt.subplot(211)
        plt.plot(f, Powerlog(h))
        plt.grid(True)
        plt.title('Spec: Mag Resp')
        plt.subplot(212)
##        plt.plot(f, gd)
        plt.grid(True)
        plt.title('GD in ns')

    return f, H

    """----------------------------------------------------------------------"""

def ChangeFilterSampleRate(npaNum, npaDeno, iOldFs, iNewFs, iM, bIsSOS, bPlot = False, iFigNum = 657667, bClearFigure = True):
    """
    Utility Function :-

    Inputs :- (i)   npaNum :- numpy array of numerators of filter coefficients.

              (ii)  npaDeno :- numpy array of denominators of filter coefficients

              (iii) iOldFs :- current sampling frequency of filter

              (iv)  iNewFs :- new sampling frequency of filter

              (v)   iM :- size of the new filter, to be returned

              (vi)  bIsSOS :- True if original filter is a second order system

              (vii) bPlot :- True if plot have to be shown

              (viii)iFigNum :- figure number

              (ix)  bClearFigure :- True if plot have to be cleared prior to any of the plotting operation

    Outputs :- (i) npaNewFilter :- numpy array of new filter

    Purpose :- This method accepts filter, changes it sampling rate and return the modified FIR filter
    """
    #   numpy array, for storing new filter
    npaNewFilter = None
    #   if OldFs and NewFs are same, then return npaNum
    if iOldFs == iNewFs:
        npaNewFilter = npaNum
    else:
        newF = Freq(iM, iNewFs, True)
        bigF = Linspace(0, newF[1] / 4.0, (2 * iM) + 4)
        fold = Freq(iM, iOldFs, True)

    if bIsSOS:
        H1 = Freqzsos(npaNum, fold, iOldFs)
        H2 = Freqzsos(npaNum, newF, iOldFs)
    else:
        H1 = Freqz(npaNum, npaDeno, fold, iOldFs)
        H2 = Freqz(npaNum, npaDeno, newF, iOldFs)

    delay = (2 * math.pi - Angle(H2[-1])) / (2 * math.pi * newF[-1])

    H2 *= np.exp(1j * 2 * math.pi * newF * delay)
    H2[-1] = H2[-1].real

    bUseButter = False

    if bUseButter:
        [bb, ab] = signal.butter(16, 2 * 8 / iNewFs)
        hb = Freqz(bb, ab, newF, iNewFs)

        H2 = abs(hb) * H2
    else:
        if iNewFs > iOldFs:
            indx = np.where(newF > iOldFs / 2)
            H2[indx] = 0.0001

    npaNewFilter = idft(H2, newF, iNewFs)

    if bPlot:
        S = Spec(npaNewFilter, 1, bigF, iNewFs, bIsSOS, False)
        plt.figure(iFigNum)

        if (bClearFigure):
            plt.clf()
        plt.subplot(311)
        plt.plot(fold, Powerlog(H1), label = "ori")
        plt.grid(True)
        plt.hold(True)
        plt.plot(S[0], Powerlog(S[1]), "r--x", label = "new filter")
        plt.title('ChangeFilterSampleRate: Mag. Resp Different SampleRates')

        plt.subplot(312)
        ##plt.plot(S[0], S[2])
        plt.grid(True)
        plt.title('New Filter Group Delay');

        plt.subplot(313)
        plt.plot(npaNewFilter)
        plt.grid(True)
        plt.title('New Filter filter taps')

    return npaNewFilter

    """----------------------------------------------------------------------"""

def NormalizeStep(step):
    '''---------------------------------------------------------
    Normalizes the step to go from 0 to 1.0 '''
    top = np.mean(step[-5:])
    step /= top
    return step


def StepDelay(step,Fs):
    '''---------------------------------------------------------
    calculates the step delay for a given input step, returns the time in seconds. '''
    counts,centers = np.histogram(step,bins = 128)
    indx = np.argmax(counts[0:64])
    bottom = centers[indx]

    indx = np.argmax(counts[64:])
    top = centers[indx+64]

    threshold = (top + bottom)/2.0
    for i in np.arange(1,len(step)):
        if ((step[i-1] < threshold) and (step[i] >= threshold)):
           timeIndx = (threshold - step[i-1])/(step[i] - step[i-1]) + i - 1
           delay = timeIndx/Fs
           return delay
    return 0.0

def GetFreqVector(N = 512, Fs = 1.0, fullUnitCircle = 0):
    '''---------------------------------------------------------
    returns a frequency vector of given size and sample rate '''
    if (fullUnitCircle == 1):
       f = np.fft.fftfreq(N,1.0/Fs)
    else:
       f = np.fft.fftfreq(2*N,1.0/Fs)
       NHalf = N + 1
       f = f[0:NHalf]
       f[-1] = -f[-1]

    # The following code will make sure f is a vector instead of a tuple with only one element
    fnew = np.ones((len(f),1))
    for i in np.arange(len(f)):
        fnew[i] = f[i]
    return fnew

def GrpDelayFromStep(step,f,Fs,win=0.0,debug = 0):
    '''---------------------------------------------------------
    returns input spectrum H, GD for an input step '''
    stepdelay = StepDelay(step,Fs)
    impl = np.diff(step)*Fs
    impl = np.append(impl,impl[-1])

    omega,H = signal.freqz(impl,1,2.0*np.pi*f/Fs)
    GD,unwrappedPhase = GrpDelayFromH(H,f,timeDelay = stepdelay)
    return H,GD,unwrappedPhase

def Freqz(b,a,f,Fs,debug = False):
    omega,H = signal.freqz(b,a,2.0*np.pi*f/Fs)
    return H

def Freqzsos(sos,f,Fs,debug = False):
    '''---------------------------------------------------------
    Freqzsos(sos,f,Fs,debug = False):
    Calculates the frequency response of the Second order system.
    sos = '''
    stages = Rows(sos)
    H = np.ones((len(f),1))
    print Size(H)
    for s in np.arange(stages):
        Num = sos[s,0:3]
        Deno = sos[s,3:]
        Hs = Freqz(Num,Deno,f,Fs)
        H = H*Hs

    return H;

def Filter(b,a,x,Fs_filter = 1.0, Fs_data = 1.0):
    if (Fs_filter == Fs_data):
       y = signal.lfilter(b,a,x)
    elif(Fs_data%Fs_filter != 0):
                           raise NameError('Fn Filter: Data sample rate is not integer upsample of filter sample rate.')
    else:
         upsampleFactor = Fs_data/Fs_filter
         y = np.zeros((1,len(x)))
         for u in np.arange(upsampleFactor):
             x_u = x[u::u]
             y_u = Filter(b,a,x_u)
             y[u::u] = y_u
    return y

def Impulse(N = 512, center = 0):
    '''---------------------------------------------------------
    # returns an Ideal impulse of 1 followed by zeros of required size'''
    impl = np.zeros((N,1))
    if center == 0:
       impl[0] = 1.0
    else:
         impl[N/2] = 1.0
    return impl

def IdealStep(N = 512):
    '''---------------------------------------------------------
    # returns an ideal step of required size'''
    z = np.zeros((N/2,1))
    o = np.ones((N/2,1))
    x = Stack(z,o)
    return x

def PowerCurve(x,p,v):
    '''---------------------------------------------------------
    # Function to generate a powercurve for axis array x '''

    xp = x**p
    x2p = xp*xp
    n = np.sum(xp)
    d = np.sum(x2p)
    A = n/d
    y = v*A*(xp)

    return y

def idft(X, freq, Fs):
    '''---------------------------------------------------------
    # Function to calculate inverse fft for X '''
    if (len(np.nonzero(freq == Fs/2 )[0]) > 0):
        NyquistFreqPresent = 1
    else:
        NyquistFreqPresent = 0

    indx = np.nonzero(freq <= Fs/2)[0]
    X = X[indx].copy()

    if(NyquistFreqPresent):
        tt = np.flipud(X[1:-1])
        tt = tt.conj()
        Xfull = np.hstack((X, tt))
    else:
        tt = np.flipud(X[1:])
        tt = tt.conj()
        Xfull = np.hstack((X, tt))

    x = np.fft.ifft(Xfull)


    maxImagValue = np.abs(x.imag).max()
    if(maxImagValue > 1e-2):
        print('result which should be real vector has high imaginary values!')

    x = x.real

    return x

def PolyphaseFilter(filt, x, polyFactor):

    """
    Input :
            (i) filt :- a 1 col (if FIR) or 2 col (if IIR, 1st col = numerator 2nd cold = denominator)
                or 6 col matrix (if SOS, 1st to 3rd col = numerator, 4th to 6th col = denominator)
            (ii) x :- input signal to be filtered
            (iii) polyFactor :- polyphase filtering factor

    Output: returns filtered signal.

    Purpose : Does normal and polyphase filtering for FIR, IIR or SOS filters.

    """
    columns = Cols(filt)
    if(columns == 1):    # filter is FIR
        b = filt
        a = 1
        isSOS = False
    elif(columns == 2):   # filter is IIR with 1st col. as numerator and 2nd col. as denominator
        b = filt[:,0]
        a = filt[:,1]
        isSOS = False
    elif(columns == 6):   # filter is SOS with first 3 cols of numerator and next 3 cols of denom
        isSOS = True
    else:
        raise NameError('Fn PolyphaseFilter: Input filter "filt" columns not as per expectations.')

    final = np.zeros((len(x),1))
    for i in np.arange(0,polyFactor,1):
        if isSOS:
            out = x[i::polyFactor]
            for r in np.arange(0, Rows(filt), 1):
                out = Filter(filt[0:3, r], filt[3:, r], out)
        else:
            out = Filter(b,a,x[i::polyFactor]);
        final[i::polyFactor]= out.reshape(Rows(out),1)
    return final

'''#####################################################################################################
    File writing, string processing stuff
#####################################################################################################'''
#TO DO:-   to be removed
def RemoveDirectory(direc):
    '''---------------------------------------------------------
    # removes a directory and sub-direc under it (empty or full)'''
    shutil.rmtree(direc)
    return

#TO DO:- to be removed
def CopyDirectory(source,dest):
    '''---------------------------------------------------------
    # copies the source directory (will all its contents) to the destination.
    NOTE: make sure that the dest does not exist!!'''
    shutil.copytree(source,dest)
    return;

#TO DO:- to be removed
def CreateDirectory(direc):
    '''---------------------------------------------------------
    # creates a directory if its necessary to create one. Note creates the whole tree
    ONLY takes directory path; no file names included '''
    if not os.path.exists(direc):
       os.makedirs(direc)
    return;

#TO DO :- to be removed
def DelTreeFilePattern(pattern, directory):
    '''---------------------------------------------------------
    # searches the directory tree and deletes the files that match the pattern.
    # NOTE: pattern is a tuple.  So a list of strings can be sent to delete multiple files
    # eg: DelTreeFilePattern(('step*.txt','resp*.txt'),r'c:\temp')          '''

    for patternSelected in pattern:
		f = FindAllFilesInDirTree(rootPath = directory, filePattern = patternSelected)
		for fileN in f:
			DeleteFile(fileN);
    return;

#TO DO : to be removed
def DeleteFile(fileName):
    '''---------------------------------------------------------
    Deletes a file if its present. fileName can be with path'''
    if os.path.isfile(fileName):
       os.remove(fileName);
    return;

#TO DO : to be removed
def DoesFolderExist(direc):
    '''---------------------------------------------------------
    # returns true if the folder exists else returns false '''
    if os.path.exists(direc):
       return True;
    else:
         return False;

#TO Do : to be removed
def DoesFileExist(filenameWithPath):
    '''---------------------------------------------------------
    # returns true if the file exists else returns false '''
    exists = os.path.isfile(filenameWithPath)
    return exists

def GetElementInsideFileInDirTree(rootPath = r'c:\temp', filePattern = '*.*', lineNo = 0,elementNo = 0):
    f = FindAllFilesInDirTree(rootPath,filePattern)
    for fileN in f:
        for line in open(fileN).readlines():
            data = line.split()
            print data[3]
            return;

#TO DO :- to be removed
def FindAllFilesInDirTree(rootPath = r'c:\temp', filePattern = '*.*'):
    '''---------------------------------------------------------
    # returns an array of full-paths for the file found in the directory tree'''
    strPaths = []
    for path, dirs, files in os.walk(os.path.abspath(rootPath)):
       for filename in fnmatch.filter(files, filePattern):
            strPaths.append(os.path.join(path, filename))

    return strPaths

#TO DO :- to be removed
def FindAllFilesInDir(filePattern = 'c:\\temp\\*\\*.*'):
    '''---------------------------------------------------------
    # returns an array of full-paths for the files found in the directory using glob
    Eg: FindAllFilesInDir("c:\\temp\\calibration\\compensation\\a\\c?\\*\\step[0-9].txt")'''
    strPaths = []
    for filename in glob.glob(filePattern):
        strPaths.append(filename)

    return strPaths

# To be removed
def RenameFiles(directory, inputSearchTerm, inputNamePart, outputNamePart):
    '''----------------------------------------------------------
    # renames given files it finds in the directory
    directory - searches this directory eg: r'c:\temp'
    inputSearchTerm - used for searching files to be renamed eg: r'In*.txt'
    inputNamePart - file name part which needs to be replaced eg: r'In'
    outputNamePart - file name with which it would be replaced eg: r'Out'  '''
    strPaths =FindAllFilesInDirTree(rootPath = directory, filePattern = inputSearchTerm)
    for fileName in strPaths:
        newFileName = fileName.replace(inputNamePart, outputNamePart)
        os.rename(fileName, newFileName)
    return

def SaveMatrixToFile(fileName, data, fmt = '%.16e', delimiter =' '):
    '''---------------------------------------------------------
    # saves a data matrix into a file, without the starting and ending brackets'''
    np.savetxt(fileName, data, fmt=fmt, delimiter=delimiter)
    return;

def ReadMatrixFromFile(fileName, delimiter = ' '):
    '''---------------------------------------------------------
    # Read matrix from file saved using saveMatrixToFile function'''
    data = LoadTxtFix(fileName)
    return data
#    N = np.loadtxt(fileName,delimiter = delimiter,usecols = (0,1))
#    cols = np.arange(0,2*int(N[0]) + 1,1)
#    read_data = np.loadtxt(fileName,delimiter = delimiter,usecols = (cols))
#    return read_data

def StringToFloatArray(inputStr,delimiter = ','):
    '''---------------------------------------------------------
    returns a float array given an input string '''
    y = inputStr.replace('(','')
    y = y.replace(')\n','')
    y = y.replace(')','')
    y = [float(i) for i in y.split(delimiter)]
    return y

def AppendToFile(fileName = "c:\\temp\\Pytmp.txt", stringToAppend = "", switch = 'a+'):
    '''---------------------------------------------------------
    Appends string to given file'''
    f = open(fileName, switch)
    f.write(stringToAppend)
    f.write("\n")
    f.close()

#TO Do :- to be removed
def ReadFile(fileName = "c:\\temp\\Pytmp.txt"):
    '''---------------------------------------------------------
    returns string from given file'''
    f = open(fileName,'r')
    x = f.read()
    f.close()
    return x

def Zip(direcToZip, fileName = ""):
    '''---------------------------------------------------------
    Zips a directory.  Gives it the same name as the directory and places it besides the original.
    Own filename with path can also be given.
    Eg: Zip(r"c:\temp",r"c:\tem.zip")'''
    if len(fileName) == 0:
       fileName = direcToZip + ".zip"

    # if the file already exists, delete the zip file
    DeleteFile(fileName)
    file = zipfile.ZipFile(fileName,"w")
    fileArray = FindAllFilesInDirTree(rootPath=direcToZip, filePattern=r"*.*");
    for name in fileArray:
        file.write(name, os.path.relpath(name,start=direcToZip), zipfile.ZIP_DEFLATED)
    file.close()
    return;

def Unzip(fileName, direcToUnzip = ""):
    '''---------------------------------------------------------
    UnZips a zip file.  Gives it the same name as the file and places it besides the original.
    Own directory can be given where the unzipped directory is placed.
    Eg: Unzip(r"c:\temp.zip",r"c:\temp")'''
    if len(direcToUnzip) == 0:
       direcToUnzip = os.path.splitext(fileName)
       direcToUnzip = direcToUnzip[0]

    # if the folder already exists, delete it
    DelTreeFilePattern(r"*.*", direcToUnzip)
    zipF = zipfile.ZipFile(fileName,'r')

    # If the output location does not yet exist, create it
    #
    if not os.path.isdir(direcToUnzip):
        os.makedirs(direcToUnzip)

    for each in zipF.namelist():
        # Check to see if the item was written to the zip file with an
        # archive name that includes a parent directory. If it does, create
        # the parent folder in the output workspace and then write the file,
        # otherwise, just write the file to the workspace.
        #
        if not each.endswith('/'):
            root, name = os.path.split(each)
            directory = os.path.normpath(os.path.join(direcToUnzip, root))
            if not os.path.isdir(directory):
                os.makedirs(directory)
            file(os.path.join(directory, name), 'wb').write(zipF.read(each))

    return

def MergePdf(InputFileNameList, strOutputFileName, deleteInputFiles = True):
    '''-----------------------------------------------------------------------------
    Function can me used to merge multiple input pdf files into a single output file which
    is overwritten.
        InputFileNameList = ["x.pdf","y.pdf"]
        strOutputFileName = "output.pdf"
        deleteInputFiles will delete the input pdf files; BUG: cant delete input files as opened by another process
    '''
    output = pyPdf.PdfFileWriter()
    inputStreamBuffer = []
    # for each input file
    for f in InputFileNameList:
        f += '.pdf'
        input1 = pyPdf.PdfFileReader(file(f, "rb"))
        #print "%s " % str(f) + "has %s pages." % input1.getNumPages()

        # add page one by one from each input file to output file
        for p in np.arange(input1.getNumPages()):
            output.addPage(input1.getPage(p))

    # finally, write output file
    outputStream = file(strOutputFileName, "wb")
    output.write(outputStream)
    outputStream.close()

    # BUG with delete files
##    # delete files
##    if deleteInputFiles:
##       for f in InputFileNameList:
##           inputStream = file(f, "rb")
##           inputStream.close()
##           DeleteFile(f)

    return;

def CreatePyreportCmd(strOutputFileName, strPyScriptToRun, strArgumentForScript):
    '''-----------------------------------------------------------------------------
    Function can me used to create command line argument for pdf report creation.
        strOutputFileName = "output.pdf"
        strPyScriptToRun = "xyz.py"
        strArgumentForScript = arguments needed for the above script to run "-a 'xyz' -b 20"
    '''
    outStr = 'pyreport.py -n -t pdf -o %s' % strOutputFileName
    outStr += ' -a "%s"' % strArgumentForScript
    outStr += ' %s' % strPyScriptToRun
    return outStr;


def CompareFileTimeStamps(arr):
    '''-----------------------------------------------------------------------------
    takes an array of two file names and compares the timestamps.'''
    if os.path.exists(arr[0]) & os.path.exists(arr[1]):
        time1 = os.path.getmtime(arr[0]);
        time2 = os.path.getmtime(arr[1]);
        if time1 < time2:
            return 1 #returns 1 if  the first path in array is modified earlier
        if time1 > time2:
            return -1 #return -1 if the first path in array is modified later
        else:
            return 0 #if equal
    else:
        print "File doesn't exist"

def approx_equal(a, b, tol):
    '''-----------------------------------------------------------------------------
    float comparison.'''
    result = abs(a-b) < tol
    return result

def is_number(s):
    '''-----------------------------------------------------------------------------
    check whether it is numbers.'''
    try:
        float(s)
        return True
    except ValueError:
        return False

def Send_Email(send_from, send_to, subject, text, files=[], server="sendout.lecroy.net"):
    '''----------------------------------------------------------------------------
    Send email:  send_from : abc@lecroy.com
                 send_to : [xyz@lecroy.com abc@lecroy.com]
                 subject : r'This is the subject line'
                 text : r'This is the body of text of the email'
                 files : [temp.txt my.jpg ]; list of file names to attach to the email
    '''
    assert type(send_to)==list
    assert type(files)==list

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    text += '\n\n\nThis email has been sent from a Python script.'
    msg.attach( MIMEText(text) )

    for f in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(f,"rb").read() )
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)

    smtp = smtplib.SMTP(server)
    smtp.sendmail(send_from, send_to, msg.as_string())
    print "\nEmail sent."
    smtp.close()
    return;

def NetworkLogin(networkPath,username,passwrd):
    '''----------------------------------------------------------------------------
    NetworkLogin:  login to a networkPath
                   networkPath : r'\\newyork_svr1\users'
                   username: r'lecroy\nymfg'
                   passwrd: r'stopthenthink'
    '''
    winCMD = 'NET USE ' + networkPath + ' /User:' + username + ' ' + passwrd
    subprocess.Popen(winCMD, stdout=subprocess.PIPE, shell=True)
    return;

def FindNumberAfterString(str, longSourceStr):
    '''---------------------------------------------------------
    # Function to search over longSourceStr and find the number after the matched str
    eg. open a file, a line is as the following:
        ChannelCompensator.SelfTestLowLimitGain01 = -0.5
        Use str as "ChannelCompensator.SelfTestLowLimitGain01 = ", longSourceStr as the
        read out file, this function will give a result of float "-0.5"
    # input:
        str --- string before the number interested;
        longSourceStr --- the long string which contains the str, usually the file read out;
    # output:
        num --- float type of the number after the string    '''

    Obj = re.search('(?<='+str+')[-]*\d+[\.\d+]*', longSourceStr)
    num = float(Obj.group(0))
    return num

# Note: Please be really carefull about r'' vs ''  ie. raw string vs non-raw string
def FindNumberAfterString2(searchStr, Str):

    """
    Input :
            (i) searchStr :- The string to be searched.
            (ii) Str :- The parent string in which the string will be searched.

    Output: Number after the string.

    Purpose : This function is used to search over long Source String and find the number after the matched string.

    E.g: N = FindNumberAfterString2(Str = 'Points:		2000\nCount:		4096\nXInc:		5.e-12', searchStr = r'\sPoints:\s(.*)')

    """

    Obj = re.search(searchStr, Str, re.I)
    if Obj is not None:
        return Obj.group(1)

    return -1


def AskUserExit(msg):
    # ask the user to exit
    print " "
    userInput = raw_input(msg + "Press y if you want to exit or simply close the window.\n");
    if userInput == 'y':
        exit();

def whos(z1321z, bReturnAsString = False, strObjectName = None):
    ''' This function prints a list locals np arrays with sizes, values which are int, doubles, lists, dict.
    No string is displayed.
    Inputs:  vars()'''

    tempString = "\n"

    strTabSeperator = ""
    if bReturnAsString == True:
        strTabSeperator = "\t\t"

    if IsEmptyOrNULLString(strObjectName) == True:
        tempString += strTabSeperator + '------------whos started----------------'
    else:
        tempString += strTabSeperator + '------------' + strObjectName + ' whos started----------------'

    #z1321z = vars()
    for k in z1321z.keys():
        varType = str(type(z1321z[k]))
        if varType == "<type 'numpy.ndarray'>":
            if z1321z[k].shape[0] <= 5 and z1321z[k].shape[1] <= 10:
                tempString += "\n" + strTabSeperator + 'NAME:' + str(k) + '\t' + 'RxC:' + str(z1321z[k].shape) + '\tVALUE:' + str(z1321z[k]) + '\t\t\tTYPE:' + str(z1321z[k].dtype.name)
            else:
                tempString += "\n" + strTabSeperator + 'NAME:' + str(k) + '\t' + 'RxC:' + str(z1321z[k].shape) + '\t\t\tTYPE:' + str(z1321z[k].dtype.name)
        elif varType == "<type 'list'>" or varType == "<type 'str'>" or varType == "<type 'tuple'>":
            if len(z1321z[k]) <= 10:
                tempString += "\n" + strTabSeperator + 'NAME:' + str(k) + '\t' + 'RxC:' + str(len(z1321z[k])) + "x1" + '\tVALUE:' + str(z1321z[k]) + '\t\t\tTYPE:' + str(varType)
            else:
                tempString += "\n" + strTabSeperator + 'NAME:' + str(k) + '\t' + 'RxC:' + str(len(z1321z[k])) + "x1" + '\t\t\tTYPE:' + str(varType)

        elif varType == "<type 'module'>" or varType == "<type 'function'>" or varType == "<type 'classobj'>" or varType == "<type 'NoneType'>":
             junk = 1;       # dont do anything

        elif varType[0:8] == "<class '" or varType == "<netref class '__builtin__.module'>":
             junk = 1;       # dont do anything

        elif varType == "<type 'dict'>":
             if str(k) != 'z1321z' and str(k) != '__builtins__':
                tempString += "\n" + strTabSeperator + 'NAME:' + str(k) + '\t' + 'VALUE:' + str(z1321z[k]) + '\t\t\tTYPE:'  + str(varType)
        else:
             tempString += "\n" + strTabSeperator + 'NAME:' + str(k) + '\t' + 'VALUE:' + str(z1321z[k]) + '\t\t\tTYPE:' + str(varType)

    tempString += '\n' + strTabSeperator + '----------------------------------------'

    if bReturnAsString:
        return tempString

    print tempString

    return;

    """----------------------------------------------------------------------"""

def GetCallerFunctionName():
    """
    Utility Function :-

    Inputs :- does not receive any inputs

    Outputs :- returns <module-name>.<class-name>.<methodname>() eg. __main__.CBase.MLog()

    Purpose :- returns the name of the caller function of the function, who have called this function
    """
    stack = inspect.stack()
    try:
        the_class = stack[2][0].f_locals["self"].__class__
    except:
        the_class = "No-Class"
    the_method = stack[2][0].f_code.co_name

    strTemp = "{}.{}()".format(str(the_class), the_method)

    return strTemp

    """----------------------------------------------------------------------"""

def saveAndLoadBin():
    np.savez('test', x=x, y=y);   # saves a test.npz file with variables names x and y in it
    v = np.load('test.npz');
    v.files                 # lists the variables read out
    v['x']                  # to get data of variable x
    v['y']                  # to get data of variable y


def find(array,val,tol = 0.0):
    '''---------------------------------------------------------
    # returns an array of index values where array == val '''
    indxArr = np.int_([])
    valArr = np.array([])
    if tol == 0.0:
        for i in np.arange(np.size(array)):
            if val == array[i]:
               indxArr = np.append(indxArr,np.int(i));
               valArr = np.append(valArr,array[i])
    else:
        for i in np.arange(np.size(array)):
            if np.abs(val-array[i]) < tol:
               indxArr = np.append(indxArr,np.int(i));
               valArr = np.append(valArr,array[i])
    return indxArr,valArr

def getLibraryVersion(strLibraryName):
    """
    Function :-

    Inputs   :- (i) strLibrarName :- name of the python third-party library

    Output   :- returns the version of library

    Purpose  :- This method helps to get information about the version of any python library,
                provided that egg file of that library is present.
    """
    try:
        return pkg_resources.get_distribution(strLibraryName).version
    except:
        print "LecroyUtil_Portable : Either egg file is missing or it doesn't contain version information for package %s", strLibraryName
        return None
    """----------------------------------------------------------------------"""

def GetVersionOfImportantLib():
    """
    Utility function :

    Inputs :-  does not receive any inputs

    Outputs :- does not return any values

    Purpose :- This method prints versions of important libraries such as yaml, numpy, scipy, matplotlib, py2exe, wxPython, etc.
    """
    liStrImpLibs = ["numpy", "scipy", "pyYaml", "matplotlib", "py2exe", "wxPython", "pp"]

    for strLibName in liStrImpLibs:
        strVersion = getLibraryVersion(strLibName)
        if strVersion != None:
            print strLibName + " : " + strVersion

    return

    """----------------------------------------------------------------------"""

def GiveLoadToCPU(tupSize = (6000, 6000)):
    """
    Function :-

    Inputs   :- (i) tupSize :- tuple containing the size of array

    Outputs  :- No outputs

    Purpose  :- This function is meant to give load to cpu for certain amount of time.
                It is mainly used for testing purpose
    """
    m = np.random.randint(10000, size = tupSize)
    i = np.linalg.inv(m)

    return i

    """----------------------------------------------------------------------"""

def Copy(strValue):

    dataObj = wx.TextDataObject()
    dataObj.SetText(strValue)
    if wx.TheClipboard.Open():
        wx.TheClipboard.SetData(dataObj)
        wx.TheClipboard.Close()
    else:
        wx.MessageBox("Unable to open the clipboard", "Error")
    """----------------------------------------------------------------------"""




def IsEmptyOrNULLString(strVal):
    """
    Utility Function :

    Inputs           : (i) strVal :- String which have to be checked. eg. Sachin

    Outputs          : boolean value - True/False

    Purpose          : This method checks the string passed to it as argument, if it's empty or not
                       eg. IsEmptyString("sachin") --> False
                           IsEmptyString("") --> True
                           IsEmptyString("   ") --> True
                           IsEmptyString(None) --> True
    """
    #if the length of the trimmed string is less than 1, return True
    if strVal == None or len(strVal.replace(' ', '')) <= 0:
        return True

    return False

    """----------------------------------------------------------------------"""

def FormatString(strStringToFormat, iFieldSize = 10, strPaddingChar = '*'):

    if strStringToFormat == None:
        strStringToFormat = ""

    if iFieldSize < 0:
        objMethodToInvoke = str(strStringToFormat).ljust
    else:
        objMethodToInvoke = str(strStringToFormat).rjust

    return objMethodToInvoke(abs(iFieldSize), strPaddingChar)

    """----------------------------------------------------------------------"""

def ClickMouseAtXY(tupPointXY = (30, 30)):
    """
    """
    win32api.SetCursorPos(tupPointXY)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, tupPointXY[0], tupPointXY[1], 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, tupPointXY[0], tupPointXY[1], 0, 0)

    return

    """----------------------------------------------------------------------"""

def TestClickMouseAtXY():
    """
    """
    ClickMouseAtXY()
    ClickMouseAtXY((10, 10))

    return

    """----------------------------------------------------------------------"""

def TestArray(lsStrFileNames = None, lsStrLegends = None, iFigNum = 33245432,
                bClearFig = True, iSubPlotNo = 111, strPltTitle = None,
                bSavePlot = False, strImgFileName = "Figure1.png"):
    """
    Tester Function :-

    Inputs :- (i)   lsStrFileNames :- list of file names, which contains array.

              (ii)  lsStrLegends :- list of legends to be given to plots

              (iii) iFigNum :- Figure number

              (iv)  bClearFig :- True, if figure have to be cleared, else False

              (v)   iSubPlotNo :- Subplot number in which plot have to be drawn

              (vi)  strPltTitle :- title of the plot

              (vii) bSavePlot :- True if plot figure have to be saved as png file, else False

              (viii)strImgFileName :- name by which figure have to be saved on disk.

    outputs :- does not return any values

    Purpose :- This method is used to read mathpack's Arrays from list of filenames
               passed as argument, and plots them
    """
    if lsStrFileNames == None or len(lsStrFileNames) < 0:
        raise RuntimeError("LecroyUtil_portable.py :- At least one filename have to be passed")

    if (lsStrLegends == None) or (len(lsStrFileNames) > len(lsStrLegends)):
        lsStrLegends = []
        for strFileName in lsStrFileNames:
            lsStrLegends.append(strFileName)

    if IsEmptyOrNULLString(strPltTitle):
        strPltTitle = "Array test plot"

    plt.figure(iFigNum, figsize = (14, 10))

    if bClearFig:
        plt.clf()

    plt.subplot(iSubPlotNo)
    for iIdx, strFileName in enumerate(lsStrFileNames):
        npaArray = LoadTxtFix(strFileName)
        npaArray = npaArray[1:]
        plt.plot(npaArray, label = lsStrLegends[iIdx] + " size : " + str(len(npaArray) / 1000.0) + "K elements", marker = "x")

    plt.grid(True)
    plt.legend()
    plt.title(strPltTitle)

    if bSavePlot:
        plt.savefig(strImgFileName)

    return

    """----------------------------------------------------------------------"""

def TestINTArray(strSize = "1.0KB_"):
    """
    Tester Function :-

    Inputs :- (i)   strSize :- size of array. eg. "10.0KB_", "100.0KB_", etc.

    Outputs :- does not return any values

    Purpose :- invokes TestArray for integer type.
    """
    strRootDir = "C:\\work\\webzinc\\mauisoft\\main\\components\\processing\\CompensationFilterSvr\\mathpackTester\\x64\\Release"
    lsStrArrayModes = ["UOP", "OP", "IPP"]
    lsStrLegends = ["OperandArray1", "OperandArray2", "ResultArray"]
    iSubPlotNos = [311, 312, 313]
    strImageFileName = os.path.join(strRootDir, strSize + "ADD_IPP32s.png")
    bSavePlot = False
    for iIdx, strArrayMode in enumerate(lsStrArrayModes):
        lsStrFileNames = [
            os.path.join(strRootDir, strSize + strArrayMode + '_ADD_OPD1ARRAY_Ipp32s.txt'),
            os.path.join(strRootDir, strSize + strArrayMode + '_ADD_OPD2ARRAY_Ipp32s.txt'),
            os.path.join(strRootDir, strSize + strArrayMode + '_ADD_RESULTARRAY_Ipp32s.txt')
        ]

        if (len(lsStrArrayModes) - iIdx) == 1:
            bSavePlot = True

        TestArray(lsStrFileNames, lsStrLegends, iSubPlotNo = iSubPlotNos[iIdx], strPltTitle = strArrayMode + " Integer Array",
                    bClearFig = False, bSavePlot = bSavePlot, strImgFileName = strImageFileName)


    return

    """----------------------------------------------------------------------"""

def TestDOUBLEArray(strSize = "1.0KB_"):
    """
    Tester Function :-

    Inputs :- (i) strSize :- size of array. eg. "10.0KB_", "100.0KB_", etc.

    Outputs :- does not return any values

    Purpose ;- invokes TestArray for double type.
    """
    strRootDir = "C:\\work\\webzinc\\mauisoft\\main\\components\\processing\\CompensationFilterSvr\\mathpackTester\\x64\\Release"

    lsStrArrayModes = ["UOP", "OP", "IPP"]
    lsStrLegends = ["OperandArray1", "OperandArray2", "ResultArray"]
    iSubPlotNos = [311, 312, 313]
    strImageFileName = os.path.join(strRootDir, strSize + "ADD_IPP64f.png")
    bSavePlot = False
    for iIdx, strArrayMode in enumerate(lsStrArrayModes):
        lsStrFileNames = [
            os.path.join(strRootDir, strSize + strArrayMode + '_ADD_OPD1ARRAY_Ipp64f.txt'),
            os.path.join(strRootDir, strSize + strArrayMode + '_ADD_OPD2ARRAY_Ipp64f.txt'),
            os.path.join(strRootDir, strSize + strArrayMode + '_ADD_RESULTARRAY_Ipp64f.txt')
        ]

        if (len(lsStrArrayModes) - iIdx) == 1:
            bSavePlot = True

        TestArray(lsStrFileNames, lsStrLegends, iSubPlotNo = iSubPlotNos[iIdx], strPltTitle = strArrayMode + " Ipp64f Array",
                    bClearFig = False, bSavePlot = bSavePlot, strImgFileName = strImageFileName)

    return

    """----------------------------------------------------------------------"""

def TestScaleSteps():
    """
    Tester Function :-

    Inputs :- does not receive any inputs

    Outputs :- does not return any values

    Purpose :- tests scalesteps() function
    """
    strCalibrationDirPath = "C:\\LeCroy\\XStream\\Calibration\\"
    t1, step1, b, F1 = ReadStep_txt(strCalibrationDirPath + "DHOCompensation\\A\\C1\\10mV\\step3.txt", False)
    t2, step2, b, Fs2 = ReadStep_txt(strCalibrationDirPath + "DHOCompensation\\A\\C1\\11mV\\step3.txt", False)
    t8, step8, b, Fs8 = ReadStep_txt(strCalibrationDirPath + "DHOCompensation\\A\\C1\\500mV\\step3.txt", False)

    plt.figure(3254)
    plt.plot(t1, step1, label = "Step1", marker = "x")
    plt.plot(t2, step2, label = "Step2", marker = "x")
    plt.plot(t8, step8, label = "Step3", marker = "x")
    plt.legend(loc = "lower right")
    plt.grid(True)
    scaledArrayX, scaledArrayY = ScaleSteps([step1, step2, step8], [t1, t2, t8], dStaggerX = 0.1, dStaggerY = 0.1, bDrawPlt = True, lsStrLegends = ["Step1", "Step2", "Step8"], iNewAmplitude = 1.5)

    """----------------------------------------------------------------------"""

def TestAlignSteps():
    """
    Tester Function :-

    Inputs :- does not receive any arguments as input

    Outputs :- does not return any values

    Purpose :- tests AlignSteps() function
    """
    strCalibrationDirPath = "C:\\LeCroy\\XStream\\Calibration\\"
    t2, step2, b, Fs2 = ReadStep_txt(strCalibrationDirPath + "DHOCompensation\\A\\C1\\11mV\\step3.txt", False)
    t8, step8, b, Fs8 = ReadStep_txt(strCalibrationDirPath + "DHOCompensation\\A\\C1\\20mV\\step3.txt", False)
    t8 = numpy.arange(0, ((1.0 / Fs8) * (500 + 1)) + numpy.max(t8), (1.0 / Fs8))
    step8 = numpy.append(numpy.zeros(500), step8)
    plt.figure(3254)
    plt.plot(t2, step2, label = "Step1", marker = "x")
    plt.plot(t8, step8, label = "Step2", marker = "x")
    plt.legend(loc = "lower right")
    plt.grid(True)

    AlignSteps([step2, step8], [t2, t8], [Fs2, Fs8], bDrawPlt = True, lsStrLegends = ["Step1", "Step2", "Step8"])

    """----------------------------------------------------------------------"""

def TestCheckFreqResponse():
    """
    Tester Function :-

    Inputs :- does not receive any arguments as input

    Outputs :- does not return any values

    Purpose :- tests CheckFreqResponse() function
    """
    a = ReadResponse("C:\\LeCroy\\XStream\\Calibration\\Compensation\\A\\C1\\10mV\\response.txt", True)
    npaFreqLimit = np.array([0, 1.5e10, 2.5e10, 3.5e10, 4.5e10])

    #limit values for which violation takes place
    npaLowLimit= np.array([-3, -5, -7.5, -30, -30])
    npaHighLimit = np.array([3, 0, -5, -5, -30])
    #limit values for which violation donot take place
    #npaLowLimit= np.array([-4, -7.5, -12, -30, -30])
    #npaHighLimit = np.array([3, 0, -3, -5, -30])
    bResult, npaViolationVector = CheckFreqResponse(a[0], Powerlog(a[1]), npaFreqLimit, npaHighLimit, npaLowLimit, True)
    print bResult

    """----------------------------------------------------------------------"""

def TestStepResponse():
    """
    Tester Function :-

    Inputs :- does not receive any arguments as input

    Outputs :- does not return any values

    Purpose :- tests CheckFreqResponse() function
    """
    npaLowImageFilter = LoadTxtFix("F:\\lowImageRejFir_100.txt")
    npaFirfilter = LoadTxtFix("F:\\fir_20.txt")
    npaOutputStep = StepResponse(10000, 100, 20, npaFirfilter, npaLowImageFilter, True)

    return

    """----------------------------------------------------------------------"""

def TestChangeFilterSamplingRate():
    """
    Tester Function :-

    Inputs :- does not receive any inputs

    Outputs :- does not return any values

    Purpose :- This method tests ChangeFilterSampleRate() function
    """
    b, a = signal.butter(6, 0.3)
    npaNewFilter = ChangeFilterSampleRate(b, a, 10, 20, 512, False, True)
    plt.figure(124323)
    plt.plot(npaNewFilter)
    plt.show()

    return

    """----------------------------------------------------------------------"""

def TestLevin():
    """
    Tester Function :-

    Inputs :- does not receive any inputs

    Outputs :- does not return any values

    Purpose :- Tests Levin() utility function, by providing sample input(real and complex) data
    """
    #   testing Levin() for real data
    a = np.array([ 81.8497,   18.2839,  -14.0382,   11.0083,   -4.9673])
    b = np.array([ 82.3671,   19.0593,  -14.6875,    8.6317,   -4.1692])
    """
    The correct output for above input is given below. This output matches will the output
    generated by Levin() written in matlab, when provided with the same input, given above :-
    [[ 1.01541528]
     [-0.00531546]
     [ 0.00820849]
     [-0.03864443]
     [ 0.02144162]]
    """
    a = a.reshape(5, 1)
    b = b.reshape(5, 1)
    a = a[:4]
    b = b[:4]
    print "testing Levin() for real data"
    npaX = Levin(a, b)
    print npaX

    #   testing Levin() for complex data
    a = np.array([ 81.8497 + 42.1j,   18.2839 + 42.2j,  -14.0382 + 42.3j,   11.0083 + 42.4j,   -4.9673 + 42.5j])
    b = np.array([ 82.3671 + 42.1j,   19.0593 + 42.2j,  -14.6875 + 42.3j,    8.6317 + 42.4j,   -4.1692 + 42.5j])
    """
    The correct output for above input :-
     [[-0.73552432+0.08100898j]
     [-1.13603496-0.3269801j ]
     [-0.94584945-0.80578462j]
     [-0.30522111-1.27905458j]
     [ 0.55590224-1.18686668j]]z
    """
    a = a.reshape(5, 1)
    b = b.reshape(5, 1)
    a = a[:5]
    b = b[:5]
    print "testing Levin() for complex  data"
    npaX = Levin(a, b)
    print npaX

    return

    """----------------------------------------------------------------------"""

def TestLSLevin():
    """
    Tester Function :-

    Inputs :- does not receive any inputs

    Outputs :- does no return any values

    Purpose :- tests LSLevin() function
    """
    N = 300
    npaOm = LoadTxtFix("c:\\temp\\om.txt")
    npaD = LoadTxtComplex("c:\\temp\\D.txt")
    npaW = LoadTxtFix("c:\\temp\\W.txt")
    npaX = LSLevin(N, npaOm, npaD, npaW)
    npaX = npaX.reshape((npaX.size))
    bIsMatlabFilePresent = True

    if bIsMatlabFilePresent:
        #   Note :- for the remaining part of function to work, matlabLSLevin.txt must be present
        #           which contains the output of LSLevin function in matlab.
        matlabOutput = LoadTxtFix("c:\\temp\\matlablslevin.txt")
        plt.figure(354454465)
        plt.plot(matlabOutput - npaX)
        plt.title("Difference between matlab and python output")
        plt.grid("on")
        plt.show()

    print npaX

    return

    """----------------------------------------------------------------------"""

def TestLoadTxtComplex():
    """
    Utility Function :-

    Inputs :- does not receive any inputs

    Outputs :- does not return any values

    Purpose :- Tests LoadTxtComplex() Utility function.
    """
    npaComplexArray = LoadTxtComplex("c:\\temp\\d.txt")

    print npaComplexArray

    return
    """----------------------------------------------------------------------"""

def TestMiscUtilFunctions():
    """
    Tester Function :-

    Inputs :- does not receive any inputs.

    Outputs :- does not return any values.

    Purpose :- tests various miscellaneous functions, such as Sort, linspace, Freq, etc.
    """
    print "Sorted output is " + str(Sort(np.array([4, 32, 1]), np.array([65, 23, 100])))
    print "Does 1 lie between -1 & 10 ? " + str(IsXInBetWeenN1N2(1, -1, 10))
    print CalcYForXInLinEq(10.23324, -10, 2)
    print "Line Equation is " + str(GetLineEquation((0, 1), (10, 2.5)))
    print "IsEven(21) " + str(IsEven(21))
    print "Freq :- " + str(Freq(10, 12, True))
    print "Linspace(5, -2, 10) = " + str(Linspace(5, -2, 10))

    return

    """----------------------------------------------------------------------"""

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
##   RenameFiles(directory = r'H:\mauisoft\main\Components\processing\DecompressorFDSvr', inputSearchTerm = r'DecompressorFD*.*', inputNamePart = r'DecompressorFDSystemCvars', outputNamePart = r'DecompressorFDCvars')
##   headers, data = ReadTemperatureLog()
   #sos,Fs = ReadCachedGD_txt(fileName = r'C:\LeCroy\XStream\Calibration\LCRYSIM00000\DHOCompensation\C3\50mV\cached_gd_160p0_3.txt', debug = False)
   #IsSOS, Fs, numWhole, denoWhole, sos = ReadDS(r'C:\LeCroy\XStream\Calibration\LCRYSIM00000\DHOCompensation\C3\50mV\cached_gd_160p0_3.txt');
   #MergePdf(['xyz.pdf','xyz2.pdf'], 'output.pdf')
   #z = 1;
   f = Freq(5, 1, False)
   a = cTimer.filetime_to_dt(130275496643590000L)
   print a.timetuple()
   print type(a)
   #GetVersionOfImportantLib()
   #TestLevin()
   #TestLSLevin()
   #TestLoadTxtComplex()
   #ClickMouseAtXY()
   #TestMiscUtilFunctions()
   TestCheckFreqResponse()
   #TestStepResponse()
   #TestChangeFilterSamplingRate()
   #TestINTArray("1.000KB_")
   #TestDOUBLEArray("1.000KB_")
   pass