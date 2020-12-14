"""
Template for new test --- add it to the TESTALU class
def test_testname(self) :
    ias_main = IAS()
    ias_main.appendInput(address,value)
    ias_main.memory.setInstructionsMemory([40 bit instructions here])
    ias_main.fetch()
    self.assertEqual(ias_main.getStoredValue(Address of stored output),expected value)
"""



import unittest
from unittest.main import main
from IASopcodes import IAS
from bitstring import BitStream



addRoutine = ['0000000100000000001000000101000000000011','0010000100000000010000000000000000000000']
multiplicationRoutine = ['0000100100000000001000001011000000000011','0010000100000000010100000000000000000000']
divisionRoutine = ['0000000100000000001000001100000000000011','0010000100000000010100001010000000000000','0010000100000000011000000000000000000000']
subtractionRoutine = ['0000000100000000001000000110000000000011','0010000100000000010000000000000000000000']
haltroutine = ['0'*40]
vuat = ['0000100100000000001000001011000000000011','0000010100000000000100100001000000000100']
jumpRout1 = ['0000000100000000000100000101000000000010','0000111100000000001100100001000000000101','0000000000000000000000000000000000000000','0000010100000000011100100001000000000101','0000000000000000000000000000000000000000']
jumpRout2 = ['0000000100000000000100000101000000000010','0000110100000000001100100001000000000101','0000000000000000000000000000000000000000','0000010100000000011100100001000000000101','0000000000000000000000000000000000000000']
mainprogram = ['0000000100000000001000000110000000000011','0000111100000000010000000101000000000011','0000010100000000001100100001000000000001','0000000000000000000000000000000000000000','0010000100000000000100000000000000000000']


class TestALU(unittest.TestCase) :
    
    def test_sum(self) :
        """
        To check if sum is working properly
        """
        ias_sum = IAS()
        ias_sum.appendInput('000000000011', 20)
        ias_sum.appendInput('000000000010', 63)
        ias_sum.memory.setInstructionsMemory(addRoutine)
        ias_sum.fetch()
        self.assertEqual(ias_sum.getStoredValue('000000000100'),83) 


    def test_multiplication(self) :
        """
        To check if multiplication is working properly
        """
        ias_mul = IAS()
        ias_mul.appendInput('000000000011', 51)
        ias_mul.appendInput('000000000010', 3)
        ias_mul.memory.setInstructionsMemory(multiplicationRoutine)
        ias_mul.fetch()
        self.assertEqual(ias_mul.getStoredValue('000000000101'),153)

    

    def test_divide(self) :
        """
        To check if division is working properly
        """
        ias_div = IAS()
        ias_div.appendInput('000000000011', 3)
        ias_div.appendInput('000000000010', 26)
        ias_div.memory.setInstructionsMemory(divisionRoutine)
        ias_div.fetch()
        remainder = ias_div.getStoredValue('000000000101')
        quotient = ias_div.getStoredValue('000000000110')
        self.assertEqual(quotient,8)
        self.assertEqual(remainder,2)
        
    
    
    def test_leftShift(self) :
        """
        To check left shift implementation
        """
        ias_shift = IAS()
        ias_shift.appendInput('000000000010',32)
        ias_shift.decode('00000001','000000000010')
        ias_shift.decode('00010100','000000000010')
        self.assertEqual(ias_shift.getAccumulator(),64)


    
    def test_rightShift(self) :
        """
        To check right shift implementation
        """
        ias_shift = IAS()
        ias_shift.appendInput('000000000010',32)
        ias_shift.decode('00000001','000000000010')
        ias_shift.decode('00010101','000000000010')
        self.assertEqual(ias_shift.getAccumulator(),16)

    
    def test_subtraction(self) :
        """
        To check subtraction
        """
        ias_sub = IAS()
        ias_sub.appendInput('000000000011', 56)
        ias_sub.appendInput('000000000010', 35)
        ias_sub.memory.setInstructionsMemory(subtractionRoutine)
        ias_sub.instructionRoutine()
        self.assertEqual(ias_sub.getStoredValue('000000000100'),-21) 


    def test_halt(self) :
        """
        Test to check halt functionality
        """
        ias_halt = IAS()
        ias_halt.data_memory = haltroutine
        ias_halt.fetch()
        self.assertEqual(ias_halt.getAccumulator(),0)
        self.assertEqual(ias_halt.getProgramCounter(),0)
        
    
    def test_velocity(self) :
        """
        Check the working of equation v = u + at
        """
        ias_vel = IAS()
        ias_vel.appendInput('000000000001', 2)
        ias_vel.appendInput('000000000010', 3)
        ias_vel.appendInput('000000000011', 4)
        #print(ias_vel.memory.data_memory)
        ias_vel.memory.setInstructionsMemory(vuat)
        ias_vel.fetch()
        self.assertEqual(ias_vel.getStoredValue('000000000100'),14)

    
    def test_jump11(self) :
        """
        Test to check conditionaljumpleft with jump condition
        """
        ias_jump1 = IAS()
        ias_jump1.appendInput('000000000001', 1)
        ias_jump1.appendInput('000000000010', 5)
        ias_jump1.appendInput('000000000011', -1)
        ias_jump1.appendInput('000000000111',1000)
        ias_jump1.memory.setInstructionsMemory(jumpRout1)
        ias_jump1.fetch()
        self.assertEqual(ias_jump1.getStoredValue('000000000101'),1006)
        
    def test_jump12(self) :
        """
        Test to check conditionaljumpleft without jump condition
        """
        ias_jump1 = IAS()
        ias_jump1.appendInput('000000000001', 1)
        ias_jump1.appendInput('000000000010', -2)
        ias_jump1.appendInput('000000000011', -1)
        ias_jump1.appendInput('000000000111',1000)
        ias_jump1.memory.setInstructionsMemory(jumpRout1)
        ias_jump1.fetch()
        self.assertEqual(ias_jump1.getStoredValue('000000000101'),-1)


    def test_jump21(self) :
        """
        Test to check jumpleft with jump condition
        """
        ias_jump2 = IAS()
        ias_jump2.appendInput('000000000001', 1)
        ias_jump2.appendInput('000000000010', -2)
        ias_jump2.appendInput('000000000011', -1)
        ias_jump2.appendInput('000000000111',1000)
        ias_jump2.memory.setInstructionsMemory(jumpRout2)
        ias_jump2.fetch()
        self.assertEqual(ias_jump2.getStoredValue('000000000101'),999)
    

    def test_jump22(self) :
        """
        Test to check jumpleft 
        """
        ias_jump2 = IAS()
        ias_jump2.appendInput('000000000001', 1)
        ias_jump2.appendInput('000000000010', 5)
        ias_jump2.appendInput('000000000011', -1)
        ias_jump2.appendInput('000000000111',1000)
        ias_jump2.memory.setInstructionsMemory(jumpRout2)
        ias_jump2.fetch()
        self.assertEqual(ias_jump2.getStoredValue('000000000101'),1006)
        
    
    def test_maintestcase(self) :
        ias_main = IAS()
        ias_main.appendInput('000000000010',15)
        ias_main.appendInput('000000000011',5)
        ias_main.memory.setInstructionsMemory(mainprogram)
        ias_main.fetch()
        self.assertEqual(ias_main.getStoredValue('000000000001'),10)
    

    def test_maintestcase2(self) :
        ias_main = IAS()
        ias_main.appendInput('000000000010',5)
        ias_main.appendInput('000000000011',15)
        ias_main.memory.setInstructionsMemory(mainprogram)
        ias_main.fetch()
        self.assertEqual(ias_main.getStoredValue('000000000001'),20)





if __name__ == "__main__":
    unittest.main()
