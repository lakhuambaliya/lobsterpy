#-------------------------------------------------------------------------------
# Name:         mywxspinctrl.py
# Purpose:      This module contains CSpinCtrl class, which extends wx.SpinCtrl.
#               CSpinCtrl is a generic version of wx.SpinCtrl class which can be
#               used in any wx-based GUI application.
# Author:       lakhu
#
# Created:     14/03/2014
# Copyright:   (c) Account Prism Pvt. Ltd.
# Licence:     all_rights_reserved
#-------------------------------------------------------------------------------

#imports
import wx

# class-name    : CSpinCtrl
#class-description : this class create a spin control according to passed parameter
class CSpinCtrl(wx.SpinCtrl):

    def __init__(
                    self, objParent = None, objMethod = None, iValue = 1,
                    iLastValue = 1, iStep = 0, tupPos = None, tupSize = None,
                    iMin = 1, iMax = 100
                ):

        """
        Constructor :-

        Throws Exception : No

        Inputs :        (i)     objParent   : parent of the spin control

                        (ii)    objMethod   : method which validate the spin control values.

                        (iii)   iValue      : Initial integer value to be appear in spin control

                        (iv)    iLastValue  : latest updated value in the spin control

                        (v)     iStep       : step value which defines the how many step you want to increase or decrease

                        (vi)    tupPos      : position in gui

                        (vii)   iMin        : specifies minimum value for spin control

                        (viii)  iMax        : specifies maximum value for spin control

        Outputs :       does not return any values

        Purpose :       initializing member variable by received inputs

        """
        wx.SpinCtrl.__init__(self, parent = objParent, value = str(iValue),  pos = tupPos, size = tupSize, min =iMin, max = iMax)
        # initialize member variables by received inputs
        self.m_iStep = iStep
        self.m_iLastValue = iLastValue
        self.Bind(wx.EVT_SPINCTRL, self.MSpin)
        self.Bind(wx.EVT_TEXT, self.MSpin)
        self.m_objMethod = objMethod

        return

    """----------------------------------------------------------------------"""

    def MSpin(self, evt):

        """
        Member Function :-

        Throws Exception : No

        Inputs : (i) evt    : specifies the event by spin control

        Outputs : does not return any values

        Purpose : increase or decrease spin control value by step value

        """
        if self.m_objMethod != None:
            self.m_objMethod(self, evt)

        return

    """----------------------------------------------------------------------"""

    @staticmethod
    def OnSpin(objCSpinCtrl, event):

        """
        Static Function :

        Throws Exception : No

        Inputs :    (i) objCSpinCtrl    : specifies CSpinCtrl object which is passed through calling function
                    (ii) event  : event to be passed by spin control

        Outputs : does not return any values

        purpose : this is event handler which validate the spin control value according to its defined rules
                    eg. min value, max value, step value

        """

        #   getting the difference value before spinEvt and value after spinEvt
        iDelta = objCSpinCtrl.GetValue() - objCSpinCtrl.m_iLastValue

        #   if not change in value has taken place, then return
        if iDelta == 0:
            return

        #   if change is positive, then increment valueof m_iLastValue by
        #   the amount of m_iStep
        elif iDelta > 0:
            objCSpinCtrl.m_iLastValue += + objCSpinCtrl.m_iStep
        #   else decrement value of m_iLastValue by the amount of m_iStep
        else:
            objCSpinCtrl.m_iLastValue -= - objCSpinCtrl.m_iStep

        #   setting the modified value
        objCSpinCtrl.SetValue(objCSpinCtrl.m_iLastValue)

        return

    """----------------------------------------------------------------------"""
