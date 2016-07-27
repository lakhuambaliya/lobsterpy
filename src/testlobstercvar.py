#This file was originally generated by PyScripter's unitest wizard

import unittest
import lobstercvar as cvar
import re

class TestCVar(unittest.TestCase):

    def setUp(self):

        """
        Tester Function :-

        Purpose :- performs all the initialization operations prior to each test-case.

        """
        dictTemp = {"AbsolutePath" : "XStreamDSO.Name", "Type" : "String", "Requested" : "myRequest", "Flags" : ["G"]}
        # Creating object of CVar
        self.objCVar = cvar.CVar(dictTemp)

        return

    """----------------------------------------------------------------------"""

    def tearDown(self):
        self.objCVar = None

    """----------------------------------------------------------------------"""

    def test__init__(self):

        """
        Tester Function :-

        Purpose : - Tests Constructor function of CVar class.

        """
        # Expecting Exception to be raised because of calling Constructor without type information
        self.assertRaises(Exception, cvar.CVar, {"AbsolutePath" : "XStreamDSO.Name", "Requested" : "myRequest", "Flags" : ["G"]})
        # Expecting Exception to be raised because of calling Constructor without flags information
        self.assertRaises(Exception, cvar.CVar, {"AbsolutePath" : "XStreamDSO.Name", "Type" : "String", "Requested" : "myRequest"})
        # Expecting Exception to be raised because of invoking Constructor without AbsolutePathOfCVar.
        self.assertRaises(Exception, cvar.CVar, {"Type" : "String", "Request" : "myRequested", "Flags" : ["G"]})

        return

    """----------------------------------------------------------------------"""

    def testMGetCVarName(self):

        """
        Tester Function :-

        Purpose : - Tests MGetCVarName() function of CVar class.

        """
        #   getting the name of cvar.
        strCVarName = self.objCVar.MGetCVarName()
        #   since the name of cvar is "Name", the correct code must return "Name" as the
        #   output of MGetCVarName() function.
        self.assertEqual("Name", strCVarName)

        return

    """----------------------------------------------------------------------"""

    def testMGetCVarType(self):

        """
        Tester Function :-

        Purpose : - Tests MGetCVarType() function of CVar class.

        """
        #   getting the type of cvar.
        eCVarType = self.objCVar.MGetCVarType()
        #   expecting the type of cvar to be of type String
        self.assertEqual(eCVarType, cvar.CVar.mC_STRING)

        return

    """----------------------------------------------------------------------"""

    def testMSetCVarType(self):

        """
        Tester Function :-

        Purpose : - Tests MSetCVarType() function of CVar class.

        """
        self.objCVar.MSetCVarType(self.objCVar.mC_ENUM)
        self.assertEqual(self.objCVar.MGetCVarType(), self.objCVar.mC_ENUM)

        return

    """----------------------------------------------------------------------"""

    def testMGetCVarRequestedValue(self):

        """
        Tester Function :-

        Purpose : - Tests MGetCVarRequestedValue() function of CVar class.

        """
        self.assertEqual("myRequest", self.objCVar.MGetCVarRequestedValue())

        return

    """----------------------------------------------------------------------"""

    def testMSetCVarRequestedValue(self):

        """
        Tester Function :-

        Purpose : - Tests MSetCVarRequestedValue() function of CVar class.

        """
        self.objCVar.MSetCVarRequestedValue("SimpFamily")
        self.assertEqual(self.objCVar.MGetCVarRequestedValue(), "SimpFamily")

        return

    """----------------------------------------------------------------------"""

    def testMGetCVarAdaptedValue(self):

        """
        Tester Function :-

        Purpose : - Tests MGetCVarAdaptedValue() function of CVar class.

        """
        self.objCVar.MSetCVarAdaptedValue("SimpFamily")
        self.assertEqual(self.objCVar.MGetCVarAdaptedValue(), "SimpFamily")

        return

    """----------------------------------------------------------------------"""

    def testMSetCVarAdaptedValue(self):

        """
        Tester Function :-

        Purpose : - Tests MSetCVarAdaptedValue() function of CVar class.

        """
        self.objCVar.MSetCVarAdaptedValue("MyAdapted")
        self.assertEqual(self.objCVar.MGetCVarAdaptedValue(), "MyAdapted")

        return

    """----------------------------------------------------------------------"""

    def testMGetCVarDefaultValue(self):

        """
        Tester Function :-

        Purpose : - Tests MGetCVarDefaultValue() function of CVar class.

        """
        self.objCVar.MSetCVarDefaultValue(10.00)
        self.assertEqual(self.objCVar.MGetCVarDefaultValue(), 10.00)

        return

    """----------------------------------------------------------------------"""

    def testMSetCVarDefaultValue(self):

        """
        Tester Function :-

        Purpose : - Tests MSetCVarDefaultValue() function of CVar class.

        """
        self.objCVar.MSetCVarDefaultValue(10.00)
        self.assertEqual(self.objCVar.MGetCVarDefaultValue(), 10.00)

        return

    """----------------------------------------------------------------------"""

    def testMGetCVarFlags(self):

        """
        Tester Function :-

        Purpose : - Tests MGetCVarFlags() function of CVar class.

        """
        # here in cvar for flags we ae using enum
        # if flag is "R" then value in flags will be 1
        strFlags = "RHG"
        self.objCVar.MSetCVarFlags(strFlags)
        lsECVarFlags = []
        # iterating strFlags
        for strChar in strFlags:
            # fetching the value of the flags and appending into list of cvar
            lsECVarFlags.append(self.objCVar.ms_lsStrFlags.index(strChar))

        self.assertEqual(self.objCVar.MGetCVarFlags(), lsECVarFlags)

        return

    """----------------------------------------------------------------------"""

    def testMSetCVarFlags(self):

        """
        Tester Function :-

        Purpose : - Tests MSetCVarFlags() function of CVar class.

        """

        self.testMGetCVarFlags()

        return

    """----------------------------------------------------------------------"""

    def testMGetCVarMaxLen(self):

        """
        Tester Function :-

        Purpose : - Tests MGetCVarMaxLen() function of CVar class.

        """
        self.objCVar.MSetCVarMaxLen(10)
        self.assertEqual(self.objCVar.MGetCVarMaxLen(), 10)

        return

    """----------------------------------------------------------------------"""

    def testMSetCVarMaxLen(self):

        """
        Tester Function :-

        Purpose : - Tests MSetCVarMaxLen() function of CVar class.

        """
        self.objCVar.MSetCVarMaxLen(10)
        self.assertEqual(self.objCVar.MGetCVarMaxLen(), 10)

        return

    """----------------------------------------------------------------------"""

    def testMGetCVarRange(self):

        """
        Tester Function :-

        Purpose : - Tests MGetCVarRange() function of CVar class.

        """
        lsRange = ["ON", "OFF"]
        self.objCVar.MSetCVarRange(lsRange)
        self.assertEqual(self.objCVar.MGetCVarRange(), lsRange)

        return

    """----------------------------------------------------------------------"""

    def testMSetCVarRange(self):

        """
        Tester Function :-

        Purpose : - Tests MSetCVarRange() function of CVar class.

        """
        lsRange = ["ON", "OFF"]
        self.objCVar.MSetCVarRange(lsRange)
        self.assertEqual(self.objCVar.MGetCVarRange(), lsRange)

        return

    """----------------------------------------------------------------------"""

    def testMGetCVarMinValue(self):

        """
        Tester Function :-

        Purpose : - Tests MGetCVarMinValue() function of CVar class.

        """
        self.objCVar.MSetCVarMinValue(1)
        self.assertEqual(self.objCVar.MGetCVarMinValue(), 1)

        return

    """----------------------------------------------------------------------"""

    def testMSetCVarMinValue(self):

        """
        Tester Function :-

        Purpose : - Tests MSetCVarMinValue() function of CVar class.

        """
        self.objCVar.MSetCVarMinValue(1)
        self.assertEqual(self.objCVar.MGetCVarMinValue(), 1)

        return

    """----------------------------------------------------------------------"""

    def testMGetCVarMaxValue(self):

        """
        Tester Function :-

        Purpose : - Tests MGetCVarMaxValue() function of CVar class.

        """
        self.objCVar.MSetCVarMaxValue(1)
        self.assertEqual(self.objCVar.MGetCVarMaxValue(), 1)

        return

    """----------------------------------------------------------------------"""

    def testMSetCVarMaxValue(self):

        """
        Tester Function :-

        Purpose : - Tests MSetCVarMaxValue() function of CVar class.

        """
        self.objCVar.MSetCVarMaxValue(1)
        self.assertEqual(self.objCVar.MGetCVarMaxValue(), 1)

        return

    """----------------------------------------------------------------------"""

    def testMGetCVarGrainValue(self):

        """
        Tester Function :-

        Purpose : - Tests MGetCVarGrainValue() function of CVar class.

        """
        self.objCVar.MSetCVarGrainValue(1)
        self.assertEqual(self.objCVar.MGetCVarGrainValue(), 1)

        return

    """----------------------------------------------------------------------"""

    def testMSetCVarGrainValue(self):

        """
        Tester Function :-

        Purpose : - Tests MSetCVarGrainValue() function of CVar class.

        """
        self.objCVar.MSetCVarGrainValue(10)
        self.assertEqual(self.objCVar.MGetCVarGrainValue(), 10)

        return

    """----------------------------------------------------------------------"""

    def testMGetCVarUnit(self):

        """
        Tester Function :-

        Purpose : - Tests MGetCVarUnit() function of CVar class.

        """
        self.objCVar.MSetCVarUnit("Myunit")
        self.assertEqual(self.objCVar.MGetCVarUnit(), "Myunit")

        return

    """----------------------------------------------------------------------"""

    def testMSetCVarUnit(self):

        """
        Tester Function :-

        Purpose : - Tests MSetCVarUnit() function of CVar class.

        """
        self.objCVar.MSetCVarUnit("Otherunit")
        self.assertEqual(self.objCVar.MGetCVarUnit(), "Otherunit")

        return

    """----------------------------------------------------------------------"""

    def testMGetCVarAbsolutePath(self):

        """
        Tester Function :-

        Purpose : - Tests MGetCVarAbsolutePath() function of CVar class.

        """
        # we have passed "XStreamDSO.Name" as absolute path while initiaalizing
        self.assertEqual(self.objCVar.MGetCVarAbsolutePath(), "XStreamDSO.Name")

        return

    """----------------------------------------------------------------------"""

    def testMGetParentAbsolutePath(self):

        """
        Tester Function :-

        Purpose : - Tests MGetParentAbsolutePath() function of CVar class.

        """
        self.assertEqual(self.objCVar.MGetParentAbsolutePath(), "XStreamDSO")

        return

    """----------------------------------------------------------------------"""

    def testMGetImageWidth(self):

        """
        Tester Function :-

        Purpose : - Tests MGetImageWidth() function of CVar class.

        """
        self.objCVar.MSetImageWidth(2)
        self.assertEqual(self.objCVar.MGetImageWidth(), 2)

        return

    """----------------------------------------------------------------------"""

    def testMSetImageWidth(self):

        """
        Tester Function :-

        Purpose : - Tests MSetImageWidth() function of CVar class.

        """
        self.objCVar.MSetImageWidth(2)
        self.assertEqual(self.objCVar.MGetImageWidth(), 2)

        return

    """----------------------------------------------------------------------"""

    def testMGetImageHeight(self):

        """
        Tester Function :-

        Purpose : - Tests MGetImageHeight() function of CVar class.

        """
        self.objCVar.MSetImageHeight(2)
        self.assertEqual(self.objCVar.MGetImageHeight(), 2)

        return

    """----------------------------------------------------------------------"""

    def testMSetImageHeight(self):

        """
        Tester Function :-

        Purpose : - Tests MSetImageHeight() function of CVar class.

        """
        self.objCVar.MSetImageHeight(12)
        self.assertEqual(self.objCVar.MGetImageHeight(), 12)

        return

    """----------------------------------------------------------------------"""

    def testMGetImageBits(self):

        """
        Tester Function :-

        Purpose : - Tests MGetImageBits() function of CVar class.

        """
        self.objCVar.MSetImageBits(20)
        self.assertEqual(self.objCVar.MGetImageBits(), 20)

        return

    """----------------------------------------------------------------------"""

    def testMSetImageBits(self):

        """
        Tester Function :-

        Purpose : - Tests MSetImageBits() function of CVar class.

        """
        self.objCVar.MSetImageBits(50)
        self.assertEqual(self.objCVar.MGetImageBits(), 50)

        return

    """----------------------------------------------------------------------"""

    def test__del__(self):
        pass

    """----------------------------------------------------------------------"""

if __name__ == '__main__':
    unittest.main()
