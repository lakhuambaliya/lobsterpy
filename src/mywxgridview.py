#-------------------------------------------------------------------------------
# Name:        mywxgridview.py
# Purpose:     This module contains CWxGridView class, which extends wx.grid.Grid.
#              CWxGridView class is a generic class and can be used in any application
#
# Author:      Kruti
#
# Created:     11-03-2014
# Copyright:   (c) Account Prism Pvt. Ltd.
# Licence:     all_rights_reserved
#-------------------------------------------------------------------------------

#   imports
import wx
import wx.grid
import re

# class-name    : CWxGridView
# class-description : This class extends wx.grid.Grid.
class CWxGridView(wx.grid.Grid):


    #   TODO :- Although this class is considered to be generic, it's some amount
    #           of coupling with LobsterPy application. It has to be removed, in
    #           next revision. Moreover, the names of the variables, used in the
    #           class are related to LobsterPy Application. So their names also
    #           have to be changed to appropriate generic names in the application.
    def __init__(
                    self, value, parent, ID =-1,
                    pos = None, size = None,
                    style = wx.ALWAYS_SHOW_SB | wx.HSCROLL | wx.VSCROLL
                ):

        """
        Constructor :-

        Throws Exception :- No

        Inputs :-   (i) value :- adapted value of the CVar

                    (ii) parent :- parent class or window of the current class

                    (iii) pos :- a tuple, representing position of the GridView

                    (iv) size :- tuple, representing size of the GridView

                    (v) style :- style of the GridView

        Outputs :- does not return any value

        Purpose :- initializes the member variables to default values

        """

        # calling the constructor of wx.grid.Grid
        wx.grid.Grid.__init__(self, parent, style = style, pos = pos, size = size)

        #   creating a grid of 0 row and 0 column
        self.CreateGrid(0, 0)

        #   removing the gridlines of the gridview
        self.EnableGridLines(False)

        #   checking whether the input value is of type list
        if(type(value) is list):
            #   calling the method to populate the gridview
            self.MPopulateGridView(strValue = None, lsColumns = value)

        else:
            #   calling the method to populate gridview, if type of CVar is
            #   not  list
            self.MPopulateGridView(strValue = value, lsColumns = None)

        return

    """----------------------------------------------------------------------"""

    def MGetNumRowsColsAndColsValues(self):

        """
        Member Method :-

        Throws Exception :- No

        Inputs :- does not receive any inputs

        Outputs :- (i) self.m_iNumRows :- number of rows, calculated by
                                          tokenizing the input value

                    (ii) self.m_iNumCols :- number of columns, calculated by
                                            tokenizing the input value

                    (iii) self.m_lsColumns :- list of values retrieved by the
                                              columnar values.
                                              These values will be set to the
                                               cells of gridview

        Purpose :- This method is used to get the number of rows, number of columns
                   and columnar values.
                   (NOTE :- This method is used by the MOnSave() method of
                   arrayeditdialog class)

        """

        return self.m_iNumRows, self.m_iNumCols, self.m_lsColumns

    """----------------------------------------------------------------------"""

    def MPopulateGridView(self, strValue = None, lsColumns = None):

        """
        Member Method :-

        Throws Exception :- Yes, throws exception when
                            (i) both strValue and lsColumns are None

        Inputs :- (i) strValue :- input value in string format, which needs to
                                  be tokenized

                  (ii) lsColumns :- input value in list format, which does not
                                    need to be tokenized

        Outputs :- does not return any value

        Purpose :- This method is used to populate the grid view

        """

        #   raise Exception when values not passed in this method
        if((strValue == None) and (lsColumns == None)):
            raise Exception("mywxgridview.py : value can not be empty")
        #   if input value is not passed as a list format.
        #   It means the input value will be in string format,
        #   it will need to be tokenized
        if((lsColumns == []) or (lsColumns == None)):
            #   calling the MTokenize() method
            m_iNumRows, m_iNumCols, m_lsColumns = self.MTokenize(strValue,
                                                                 rowSeparator = ';',
                                                                 colSeparator = ',')

        #   if input value is passed as a list format
        else:
            #   number of columns required to create a gridview
            m_iNumCols = len(lsColumns[0])

            #   creating a variable for storing number of rows required to
            #   create a gridview
            m_iNumRows = 0

            #   calculating the total number of
            for i in range(len(lsColumns)):
                m_iNumRows += 1

            #   raise Exception when number of columns is not equal in each row
            #   iterating through the list of columns
            for i in range(len(lsColumns)):
                #   when index is greater than 0, then check equality of number of
                #   of columns in each row
                if(i>0):
                    #   checking the equality in number of columns in current row
                    #   with its preceeding row
                    if(len(lsColumns[i])!=len(lsColumns[i-1])):
                        raise Exception("mywxgridview.py : number of column must be equal in each row")

            m_lsColumns = lsColumns

        #   iterating a loop to the total number of columns
        for iIdx in range(m_iNumCols):
            #   appending the column to the gridview
            self.AppendCols()

            #   setting the labels of the columns
            self.SetColLabelValue(iIdx, str(iIdx + 1))

        #   iterating a loop to the total number of rows
        for iIdx in range(m_iNumRows):
            #   appending the row to the gridview
            self.AppendRows()
            #   iterating a loop to the total number of columns
            for i in range(m_iNumCols):
                #   defining a list from the list of column values
                ls = m_lsColumns[iIdx]
                #   assigning the value of the list to the cell of gridview
                self.SetCellValue(iIdx, i, str(ls[i]))

        #   creating member variables
        self.m_iNumRows = m_iNumRows
        self.m_iNumCols = m_iNumCols
        self.m_lsColumns = m_lsColumns

    """----------------------------------------------------------------------"""


    def MTokenize(self, strValue, rowSeparator, colSeparator):

        """
        Member Method :-

        Throws Exception :- Yes, throws exception when
                            (i) number of columns at each row differs

        Inputs :- (i) strValue :- string type of value, containing values of
                                    matrix-like object

                  (ii) rowSeparator :- separator which is used to split the strValue
                                        and will seperate the value in rows

                  (iii) colSeparator :- separator which is used to split the strValue
                                        and will seperate the strValue in columns

        Outputs :- (i) iNumRows :- integer type, representing number of rows for
                                    creating gridview

                   (ii) iNumCols :- integer type, representing number of columns
                                    for creating grieview

                   (iii) lsColumns :- list of values retrieved by the columnar
                                      values. These values will be set to the
                                      cells of gridview

        Purpose :- This method tokenizes the string passed to it as argument. This
                   string generally represents the value of matrix type object.

                   eg. a = 1, 2; 3, 4; here ";" is rowSeperator, while "," is a
                       column seperator

        """

        #   creating a list of rows by splitting the adapted value by semi colon
        lsRows = re.split(rowSeparator, strValue)

        #   creating a list of columns
        lsColumns = []

        #   iterating through the list of rows
        for iIdx, string in enumerate(lsRows):
            #   appending the values retrieved by splitting the value of lsRows
            #   by comma, to the lsColumns
            lsColumns.append(re.split(colSeparator, string))

        #   raise Exception when number of columns is not equal in each row
        #   iterating through the list of columns
        for i in range(len(lsColumns)):
            #   when index is greater than 0, then check equality of number of
            #   of columns in each row
            if(i>0):
                #   checking the equality in number of columns in current row
                #   with its preceeding row
                if(len(lsColumns[i])!=len(lsColumns[i-1])):
                    raise Exception("mywxgridview.py : number of column must be equal in each row")

        #   getting the number of rows by the length of lsRows
        iNumRows = len(lsRows)

        #   getting the number of columns by the length of first value of the
        #   lsColumns
        iNumCols = len(lsColumns[0])

        #   returning iNumRows, iNumCols, lsColumns
        return iNumRows, iNumCols, lsColumns

    """----------------------------------------------------------------------"""



#   class-name :- TestFrame
#   class-description :- This class is used to test the CWxGridView class
class TestFrame(wx.Frame):

    def __init__(self, parent):

        """
        Constructor :-

        Throws Exception :- No

        Inputs :- (i) parent :- parent class or window

        Outputs :- does not return any value

        Purpose :- It initializes the TestFrame class

        """

        #   calling the constructor of wx.Frame
        wx.Frame.__init__(self, parent, -1, "Grid", pos = (10,10),
                size= (500, 500))

        #   creating the object of CWxGridView class
        grid = CWxGridView(value = [[11,12],[13,14]], parent = self)

    """----------------------------------------------------------------------"""


if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = TestFrame(None)
    frame.Show(True)
    app.MainLoop()
