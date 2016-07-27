#-------------------------------------------------------------------------------
# Name:         lobsterpreferences.py
# Purpose:      This module contains CPreferences class, which contains all the
#               preferences related to application.
#
# Author:      lakhu
#
# Created:     16/03/2014
# Copyright:   (c) Account Prism Pvt. Ltd.
# Licence:     all_rights_reserved
#-------------------------------------------------------------------------------

#imports section
import lobsterbase
# class-name        : CPreferences
# class-description : this class stores all the information about preferences configuration
class CPreferences(lobsterbase.CLobsterBase):

    # Application Modes
    mC_STANDARD_APPMODE = 0     #   represents standard application mode
    mC_FREQUENT_APPMODE = 1     #   represents frequent application mode

    # list containing valid application modes
    mC_LS_APPMODES = [mC_STANDARD_APPMODE, mC_FREQUENT_APPMODE]

    # Numeric Notations
    mC_STANDARD_NOTATION = 0    #   standard notation
    mC_ENGINEERING_NOTATION = 1 #   engineering notation
    mC_EXPONENTIAL_NOTATION = 2

    # list containing valid numeric notiations
    mC_LS_NUMERICNOTATION = [mC_STANDARD_NOTATION, mC_ENGINEERING_NOTATION, mC_EXPONENTIAL_NOTATION]

    # plots
    mC_PLOT_X = 0               #   represents plotting w.r.t. x-axis only
    mC_PLOT_Y = 1               #   represents plotting w.r.t. y-axis only
    mC_PLOT_XY = 2              #   represents plotting w.r.t. xy axis.

    # list of valid plot types
    mC_LS_PLOTS = [mC_PLOT_X, mC_PLOT_Y, mC_PLOT_XY]

    mC_COPY_PATH = 0            #   specifies that only path have to copied,
                                #   when copy operation is performed
    mC_COPY_VALUE = 1           #   specifies that only value have to be copied,
                                #   when copy operation is performed

    #   list which stores possible options avaiable for copy operation
    mC_LS_COPY_PREF = [mC_COPY_PATH, mC_COPY_VALUE]

    def __init__(
                    self, eAppMode = 1, eNumericNotation = 1, iWatchWindowRefreshTime = 1,
                    iSearchHistorySize = 1, lsIFilteredColumns = [], lsEPlots = [],
                    lsECopyPref = []
                ):

        """
        Constructor :-

        Throws Exception : No

        Inputs :    (i)   eAppMode  : integer constant representing mode of app

                    (ii)  eNumericNotation  : integer constant representing numeric notation

                    (iii) iWatchWindowRefreshTime   : integer number representing
                                                      time durarion in seconds
                                                      to refresh the value of
                                                      cvar in watch window

                    (iv)  iHistorySize : integer value representing the number of
                                         latest searchconfigurations to be remembered

                    (v)   lsIFilteredColumns : List containing indices of columns to
                                               be shown in the listview

                    (vi)  lsEPlots : list of enum which represents which
                                     type of plots user want to see(i.e., x, y, xy)

                    (vii) lsECopyPref : list of enum constants represents copy
                                        preferences
                                        ( whether user want to copy only path,
                                        only value or both)

        Outputs :   does not return any values

        Purpose :   initialize member data by received inputs

        """
        #   calling parent class constructor
        lobsterbase.CLobsterBase.__init__(self);

        # defining App Mode
        self.MSetAppMode(eAppMode)

        # define which kind of numeric notation is to be applied
        self.MSetNumericNotation(eNumericNotation)

        # if search history is enable then how many latest searching to be shown
        self.MSetHistorySize(iSearchHistorySize)

        # define that allow filter column or not..if not then by default all column would be displayed
        self.MSetFilteredColumns(lsIFilteredColumns)

        # time in seconds in which application will bw refreshed its seetings and other things
        self.MSetWatchWindowRefreshTime(iWatchWindowRefreshTime)

        # if plot is enable then which plots user want to see. eg. (i) x plot, (ii) y plot, (ii) both x&y plots
        self.MSetPlots(lsEPlots)

        # define which copy preferences user wanted.
        self.MSetCopyPref(lsECopyPref)

        return

    """----------------------------------------------------------------------"""

    def MSetAppMode(self, eAppMode):

        """
        Member Function :-

        Throws Exception : Yes, when (i) value of eAppMode is not present in
                                         list of appModes.

        Inputs : (i) eAppMode : integer value represent mode of application
                                it's mC_STANDARD_APPMODE for standard mode and
                                mC_FREQUENT_APPMODE for Frequent mode

        Outputs : does not return any values

        Purpose : assign mode to member variable by received inputs

        """
        #   raising exception ,when eAppMode is not present in the list of valid
        #   appModes.
        if (eAppMode not in CPreferences.mC_LS_APPMODES):
            raise Exception("lobsterpreferences.py : invalid app mode received...")

        self.m_eAppMode = eAppMode

        return

    """----------------------------------------------------------------------"""

    def MGetAppMode(self):

        """
        Member Function :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : (i) self.eAppMode : return integer representing App Mode

        Purpose : return Application mode as integer

        """

        return self.m_eAppMode

    """----------------------------------------------------------------------"""

    def MSetNumericNotation(self, eNotation):

        """
        Member Function :-

        Throws Exception : yes, when (i) value of eNotation is not present in list of
                                         valid notations.

        Inputs : (i) eNotation : integer representing Numeric Notation. It can
                                 be any one of mC_STANDARD_NOTATION,
                                 mC_ENGINEERING_NOTATION or mC_EXPONENTIAL_NOTATION

        Outputs : does not return any values

        Purpose : assign received notation to member variable

        """
        #   raising exception, when eNotation is not in list of numericnotiations
        if (eNotation not in CPreferences.mC_LS_NUMERICNOTATION):
            raise Exception("lobsterpreferences : invalid numeric notation received")

        self.m_eNumericNotation = eNotation

        return

    """----------------------------------------------------------------------"""

    def MGetNumericNotation(self):

        """
        Member Function :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : (i) self.eNumericNotation : return numeric notation

        Purpose : return numeric notation to be displayed to user

        """

        return self.m_eNumericNotation

    """----------------------------------------------------------------------"""

    def MSetHistorySize(self, iSearchHistorySize):

        """
        Member Function :-

        Throws Exception : yes, when (i) value of iSearchHistorySize is negative

        Inputs : (i) iSearchHistorySize : integer representing search-history size

        Outputs : does not return any values

        Purpose : setting the value of member variable, m_iSearchHistorySize.

        """
        #   raising exception, when iSearchHistorySize is negative
        if (iSearchHistorySize < 0):
            raise Exception("lobsterpreferences : negative search history size received...")

        self.m_iSearchHistorySize = iSearchHistorySize

        return

    """----------------------------------------------------------------------"""

    def MGetHistorySize(self):

        """
        Member Function :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : (i) self.m_iSearchHistorySize : return integer representing number
                                                  of searched variables are availabe to user

        Purpose : return value that specifies number of latest searched variables available to user

        """

        return self.m_iSearchHistorySize

    """----------------------------------------------------------------------"""

    def MSetWatchWindowRefreshTime(self, iWatchWindowRefreshTime):

        """
        Member Function :-

        Throws Exception : yes, when (i) value of input parameter iWatchWindowRefreshTime is negative

        Inputs : (i) iWatchWindowRefreshTime : integer representing elpased time in seconds,
                                               on the expiration of which, values of cvars
                                               in watch-window have to be queried.

        Outputs : does not return any values

        Purpose : applying preferences for refresh the application in given time

        """
        #   raising exception, when iWatchWindowRefreshTime is negative.
        if (iWatchWindowRefreshTime <= 0):
            raise Exception("lobsterpreferences : Refresh time of watch window never negative...")

        self.m_iWatchWindowRefreshTime = iWatchWindowRefreshTime

        return

    """----------------------------------------------------------------------"""

    def MGetWatchWindowRefreshTime(self):

        """
        Member Function :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : (i) self.iWatchWindowRefreshTime : watch window refersh time

        Purpose : return refresh time of the application

        """

        return self.m_iWatchWindowRefreshTime

    """----------------------------------------------------------------------"""

    def MSetFilteredColumns(self, lsIFilteredColumns):

        """
        Member Function :-

        Throws Exception : yes, when (i) input parameter is None

        Inputs : (i) lsIFilteredColumns : list of integer number representing columns to be filtered

        Outputs : does not return any values

        Purpose : applying preferences for which columns to be filtered

        """
        #   raising exception, when lsIFilteredColumns in None
        if (lsIFilteredColumns == None):
            raise Exception("lobsterpreferences : input parameter of MSetFilteredColumn should not be None...")

        self.m_lsIFilteredColumns= lsIFilteredColumns

        return

    """----------------------------------------------------------------------"""
    def MGetFilteredColumns(self):

        """
        Member Function :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : (i) self.lsIFilteredColumns : return list of integer number representing columns which have to
                                                be shown in list-view

        Purpose : return columns to be filtered as list of integer

        """

        return self.m_lsIFilteredColumns

    """----------------------------------------------------------------------"""

    def MSetPlots(self, lsEPlots):

        """
        Member Function :-

        Throws Exception : yes

        Inputs : (i) lsEPlots : list of integer specifies plots to be available
                                to user(0 = x plot, 1 = y plot, 2 = both x&y plots)

        Outputs : does not return any values

        Purpose : applying preferences for which plots user want to see

        """
        for iPlotType in lsEPlots:
            if iPlotType not in CPreferences.mC_LS_PLOTS:
                raise Exception("lobsterpreferencs.py : - Invalid plot type passed " + str(iPlotType) + " in " + str(lsEPlots))

        self.m_lsEPlots = lsEPlots

        return

    """----------------------------------------------------------------------"""

    def MGetPlots(self):

        """
        Member Function :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : (i) self.lsEPlots : return list of integer specifies plots to
                                     be available to user(0 = x plot,
                                     1 = y plot, 2 = both x&y plots)

        Purpose : return preference that which plots user want to see

        """

        return self.m_lsEPlots

    """----------------------------------------------------------------------"""

    def MSetCopyPref(self, lsECopyPref):

        """
        Member Function :-

        Throws Exception : No

        Inputs : (i) lsECopyPref : list of integer specifies copy preferences

        Outputs : does not return any values

        Purpose : applying preferences for whether user want to copy only path, value or both

        """
        for iCopyOption in lsECopyPref:
            if iCopyOption not in CPreferences.mC_LS_COPY_PREF:
                raise Exception("lobsterpreferences.py :- Invalid copy option " + str(iCopyOption) + " passed in " + str(lsECopyPref))

        self.m_lsECopyPref = lsECopyPref

        return

    """----------------------------------------------------------------------"""

    def MGetCopyPref(self):

        """
        Member Function :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : (i) self.m_lsECopyPref : return list containing copy preferences

        Purpose : applying preferences for whether user want to copy only path, value or both

        """

        return self.m_lsECopyPref

    """----------------------------------------------------------------------"""

    def __del__(self):

        """
        Destructor :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : does not return any values

        Purpose : releases memory allocated for member variables

        """
        self.m_lsIFilteredColumns = None
        self.m_lsEPlots = None
        self.m_lsECopyPref = None

        return

    """----------------------------------------------------------------------"""

    def MPrintPreferences(self):

        """
        Member Function :-

        Throws Exception : No

        Inputs : does not receive any inputs

        Outputs : does not return outputs

        Purpose : this method print the details of preferences

        """
        print "App Mode = " + str(self.MGetAppMode())
        print "Numeric Notation = " + str(self.MGetNumericNotation())
        print "History for No. of Columns = " + str(self.MGetHistorySize())
        print "Filtered Columns = " + str(self.MGetFilteredColumns())
        print "Plots = " + str(self.MGetPlots())
        print "Refresh Time = " + str(self.MGetWatchWindowRefreshTime())
        print "Copy options = " + str(self.MGetCopyPref())

    """----------------------------------------------------------------------"""

if __name__ == '__main__':
    objPref = CPreferences(eAppMode = 1, eNumericNotation = 0, iWatchWindowRefreshTime = 5, iSearchHistorySize = 12, lsIFilteredColumns = [2, 4, 6, 7], lsEPlots = [False, True, True] )
    objPref.MPrintPreferences()

