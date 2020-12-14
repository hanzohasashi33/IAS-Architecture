# implementation of the ias architecture.

from bitstring import BitStream



class Memory :
    """
    Memory class for the IAS Architecture
    """

    def __init__(self):
        self.instructions_memory = []
        self.data_memory = [BitStream(int=0,length=40)] * 1000
    
    def setDataMemory(self,elDM) :
        self.data_memory = elDM

    def getDataMemory(self) :
        return self.data_memory

    def setInstructionsMemory(self,elIM) :
        self.instructions_memory = elIM

    def getInstructionsMemory(self) :
        return self.instructions_memory





class IAS :
    '''
    Implement the IAS computer (fetch the instruction, decode and execute) 
    Implement any assembly program of your choice to test the design
    '''
    def __init__(self) -> None :
        '''
        constructor for : 
        memory, Accumualtor, ProgramCounter, MultiplierQuotient, MBR, MAR, IR and IBR.
        '''
        self.memory = Memory()
        self.__PC  = 0                                              #Program counter   
        self.__AC  = BitStream(int=0, length=40)                    #Accumulator         Employed to hold temporarily operands and results of ALU operations.  
        self.__MQ  = BitStream(int=0, length=40)                    #Multiplier Quotient Employed to hold temporarily operands and results of ALU operations.
        self.__MBR = BitStream(int=0, length=40)                    #Contains a word to be stored in memory or sent to the I/O unit, or is used to receive a word from memory or from the I/O unit.
        self.__IR  = BitStream(int=0, length=8)                     #Contains the 8-bit opcode instruction being executed.
        self.__MAR = BitStream(int=0, length=12)                    #Specifies the address in memory of the word to be written from or read into the MBR.
        self.__IBR = ""                                             #Instruction Buffer.

        
        # the below dictionary contains all the operations of the IAS operator with their meanings.
        # the design is implented in such a way that the opcode gets decoded and compsred with the dictionary.
        # if the opcode matches a key-pair value the corresponding function gets implemented.

        
        self.operations = {
            '00000001': self.load,                           #00000001 LOAD M(X) Transfer M(X) to the accumulator
            '00001010': self.loadToAC,                       #00001010 LOAD MQ Transfer contents of register MQ to the accumulator AC
            '00001001': self.loadToMQ,                       #00001001 LOAD MQ,M(X) Transfer contents of memory location X to MQ 
            '00000010': self.loadNegative,                   #00000010 LOAD -M(X) Transfer -M(X) to the accumulator
            '00000011': self.loadAbsolute,                   #00000011 LOAD |M(X)| Transfer absolute value of M(X) to the accumulator
            '00100001': self.store,                          #00100001 STOR M(X) Transfer contents of accumulator to memory location X
            '00000100': self.loadNegativeAbsolute,           #00000100 LOAD -|M(X)| Transfer -|M(X)| to the accumulator
            '00000101': self.add,                            #00000101 ADDM(X) Add M(X) to AC; put the result in AC
            '00000111': self.addAbsolute,                    #00000111 ADD |M(X)| Add |M(X)| to AC; put the result in AC
            '00000110': self.sub,                            #00000110 SUB M(X) Subtract M(X) from AC; put the result in AC
            '00001000': self.subAbsolute,                    #00001000 SUB |M(X)| Subtract |M(X)| from AC; put the remainder in AC
            '00001011': self.multiply,                       #00001011 MUL M(X) Multiply M(X) by MQ; put most significant bits of resultin AC, put least significant bits in MQ
            '00001100': self.divide,                         #00001100 DIV M(X) Divide AC by M(X); put the quotient in MQ and the remainder in AC
            '00001001': self.loadToMQ,                       #LOAD MQ,M(X) Transfer contents of memory location X to MQ
            '00001010': self.loadToAC,                       #LOAD MQ Transfer contents of address MQ to the accumulator AC
            '00001101': self.jumpLeftInstruction,            #00001101 JUMP M(X,0:19) Take next instruction from left half of M(X)
            '00001110': self.jumpRightInstruction,           #00001110 JUMP M(X,20:39) Take next instruction from right half of M(X)
            '00001111': self.conditionalJumpLeft,            #JUMP+M(X,0:19) If number in the accumulator is nonnegative, take next instruction from left half of M(X)
            '00010000': self.conditionalJumpRight,           #JUMP+M(X,20:39) If number in the accumulator is nonnegative , take next instruction from right half of M(X)
            '00010100': self.leftShift,                      #00010100 LSH Multiply accumulator by 2; i.e., shift left one bit position
            '00010101': self.rightShift,                     #00010101 RSH Divide accumulator by 2; i.e., shift right one position
            '00010010': self.storeLeft,                      #00010010 STOR M(X,8:19) Replace left address field at M(X) by 12 rightmost bits of AC
            '00010011': self.storeRight,                     #00010011 STOR M(X,28:39) Replace right address field at M(X) by 12 rightmost bits of AC
            '00000000': self.halt,                           #00000000 HALT Halt all the ongoing operations
        }


    def appendInstructions(self,inputInstruction) :
        """
        gets the relative parameters from 40 bit instruction and then calls the instruction method to decode it and execute the corresponding method.
        """
        self.memory.instructions_memory.append(inputInstruction)    #adds it to the memory
        leftOpCode = inputInstruction[:8]                    
        rightOpCode = inputInstruction[20:28]
        leftAddress = inputInstruction[8:20]
        rightAddress = inputInstruction[28:]
        self.__MBR = inputInstruction[:]
        self.__IR = leftOpCode
        self.__MAR = leftAddress
        self.__IBR = inputInstruction[20:]
        self.decode(inputInstruction[:8],inputInstruction[8:20])
        self.__IR = rightOpCode
        self.__MAR = rightAddress
        self.decode(inputInstruction[20:28],inputInstruction[28:])
        self.__PC += 1                                         #increment program counter after instruction is done.
    


    def fetch(self) :
        """
        Executes the fetch cycle of the IAS implementation wrt the PC and calls the corresponding execute.
        Done wrt to program counter.
        """
        flag = 1
        while self.__PC < len(self.memory.instructions_memory):
            self.__MAR = self.__PC 
            self.__MBR = self.memory.instructions_memory[self.__MAR]    
            self.__PC += 1                          #increment program counter after instruction is done.
            #print(self.__PC)
            leftOpCode = self.memory.instructions_memory[self.__MAR][:8]                    
            rightOpCode = self.memory.instructions_memory[self.__MAR][20:28]    
            leftAddress = self.memory.instructions_memory[self.__MAR][8:20]    
            rightAddress = self.memory.instructions_memory[self.__MAR][28:]    
            #self.__IBR = self.__MBR[20:]

            
            #Both LHs and RHS there
            if self.__IBR == "" :
                self.__IBR = self.__MBR[20:]
                self.__IR = self.__MBR[:8]
                self.__MAR = self.__MBR[8:20]
                #print(self.__IBR,self.__IR,self.__MAR)
                #print(type(self.__IR),type(self.__MAR),type(self.__IBR))
                # self.__IR = self.__IBR[0:8]
                # self.__MAR = self.__IBR[8:]
                # self.__IBR = ""
                # print(self.__IBR,self.__IR,self.__MAR)
                # self.decode(self.__IR,self.__MAR)
                self.decode(self.__IR,self.__MAR)
                #print(self.__AC.int)
            
            #only RHS there
            if self.__IBR != "" :
                self.__IR = self.__IBR[0:8]
                self.__MAR = self.__IBR[8:]
                #print(type(self.__IR),type(self.__MAR))
                #print(self.__IR,self.__MAR)
                #print(self.__IBR,self.__IR,self.__MAR)
                #print(type(self.__IR),type(self.__MAR))
                self.decode(self.__IR,self.__MAR)
                self.__IBR = ""
                #print(self.__AC.int)
            



    def instructionRoutine(self) :
        """
        Instructions exexuted wrt to elements in instructions_memory size
        """
        for inputInstruction in self.memory.instructions_memory :
            leftOpCode = inputInstruction[:8]                    
            rightOpCode = inputInstruction[20:28]
            leftAddress = inputInstruction[8:20]
            rightAddress = inputInstruction[28:]
            self.__MBR = inputInstruction[:]
            self.__IR = leftOpCode
            self.__MAR = leftAddress
            self.decode(inputInstruction[:8],inputInstruction[8:20])
            self.__IR = rightOpCode
            self.__MAR = rightAddress
            self.decode(inputInstruction[20:28],inputInstruction[28:])
            self.__PC += 1                                         #increment program counter after instruction is done.
    
    
    def getStoredValue(self,address) :
        """
        Returns element stored at given address
        """
        return self.memory.data_memory[int(address,2)].int
    

    def appendInput(self,address,value) :
        """
        append one single input to the data_memory in a specific position
        """
        self.memory.data_memory[int(address,2)] = BitStream(int=value, length=40)        

    
    def input(self,address,value) :
        self.memory.data_memory[int(address,2)] = BitStream(int=value, length=40)


    
    def decode(self,opcode,address) :
        """
        method to decode 
        """
        #self.operations[opcode](int(address,2))
        #self.operations[opcode](address.int)
        self.operations.get(opcode, lambda: 'Invalid')(int(address,2))

    
    def loadToAC(self,address) :
        """
        Transfer contents of register MQ to the accumulator AC
        """
        self.__AC = self.__MQ

    
    def loadToMQ(self,address) :
        """
        Transfer contents of memory location X to MQ
        """
        self.__MQ = self.memory.data_memory[address]


    def load(self,address) :
        """
        Transfer M(X) to the accumulator
        """
        self.__AC = BitStream(int=self.memory.data_memory[address].int,length=40)


    def store(self,address) :
        """
        Transfer contents of accumulator to memory location X
        """
        self.memory.data_memory[address] = BitStream(int=self.__AC.int,length=40)     

    

    def loadNegative(self,address) :
        """
        LOAD -M(X) Transfer -M(X) to the accumulator
        """
        self.__AC = BitStream(int = -self.memory.data_memory[address].int,length=40)

    
    def loadAbsolute(self,address) :
        """
        LOAD |M(X)| Transfer absolute value of M(X) to the accumulator
        """
        self.__AC = BitStream(int = abs(self.memory.data_memory[address].int),length=40)

    
    def loadNegativeAbsolute(self,address) :
        """
        Transfer -|M(X)| to the accumulator
        """
        self.AC = BitStream(int = -abs(self.memory.data_memory[address].int),length=40)


    def add(self,address) :
        """
        Add M(X) to AC; put the result in AC
        """
        self.__AC = BitStream(int=self.__AC.int + self.memory.data_memory[address].int, length=40)

    
    def addAbsolute(self,address) :
        """
        Add |M(X)| to AC; put the result in AC
        """
        self.__AC = BitStream(int = abs(self.memory.data_memory[address].int) + self.__AC.int,length=40)


    def sub(self,address) :
        """
        Subtract M(X) from AC; put the result in AC
        """
        self.__AC = BitStream(int=self.__AC.int - self.memory.data_memory[address].int, length=40)


    def subAbsolute(self, address) : 
        """
        Subtract |M(X)| from AC; put the remainder in AC
        """
        self.__AC = BitStream(int = self.__AC.int - abs(self.memory.data_memory[address].int) ,length=40)


    def multiply(self, address) :
        """
        Multiply M(X) by MQ; put most significant bits of result in AC, put least significant bits in MQ
        """
        res = BitStream(int=self.__MQ.int * self.memory.data_memory[address].int, length=80)
        self.__AC = BitStream(int=res[40:80].int, length=40)
        self.__MQ = BitStream(int=res[0:39].int, length=40)


    def divide(self, address) :
        """
        Divide AC by M(X); put the quotient in MQ and the remainder in AC
        """
        quotient =  BitStream(int=(self.__AC.int // self.memory.data_memory[address].int), length=40)
        remainder = BitStream(int=(self.__AC.int % self.memory.data_memory[address].int), length=40)
        self.__MQ = quotient
        self.__AC = remainder

    
    def jumpLeftInstruction(self, address) :
        """
        Take next instruction from left half of M(X)
        """
        #self.decode(self.memory.instructions_memory[address][0:8],(self.memory.instructions_memory[address][8:20]))
        self.__IBR = ""
        self.__PC = address


    def jumpRightInstruction(self, address): 
        """
        Take next instruction from right half of M(X)
        """
        self.decode(self.memory.instructions_memory[address][20:28],(self.memory.instructions_memory[address][28:]))
        self.__PC = address + 1


    def conditionalJumpLeft(self,address) :
        if(self.__AC.int >= 0) :
            #self.decode(self.memory.instructions_memory[address][0:8],(self.memory.instructions_memory[address][8:20]))
            self.__IBR = ""
            self.__PC = address


    def conditionalJumpRight(self,address) :
        if(self.__AC.int >= 0) :
            self.decode(self.memory.instructions_memory[address][20:28],(self.memory.instructions_memory[address][28:]))
            self.__PC = address + 1

    
    def leftShift(self, address) : 
        """
        Multiply accumulator by 2; i.e., shift left one bit position
        """
        self.__AC <<= 1


    def rightShift(self, address) :
        """
        Divide accumulator by 2; i.e., shift right one position
        """ 
        self.__AC >>= 1


    def storeLeft(self, address) :   
        """
        Replace left address field at M(X) by 12 rightmost bits of AC
        """
        self.memory.instructions_memory[address][8:20] = self.__AC[28:]


    def storeRight(self, address) : 
        """
        Replace right address field at M(X) by 12 rightmost bits of AC
        """
        self.memory.instructions_memory[address][28:] = self.__AC[28:]

    
    def getAccumulator(self) :
        """
        getter for accumulator
        """
        return self.__AC.int


    def setAccumulator(self,value) :
        """
        setter to set the value of accumulator
        USE WITH CAUTION
        ONLY FOR TEST PURPOSES
        """
        self.__AC = BitStream(int = value,length=40)

    
    def getMultiplierQuotient(self) :
        """
        getter for multiplier quotient
        """
        return self.__MQ.int


    def setMultiplierQuotient(self,value) :
        """
        setter for multiplier quotient
        USE WITH CAUTION
        ONLY FOR TEST PURPOSES
        """
        self.__MQ = BitStream(int = value,length=40)

    
    def getProgramCounter(self) :
        """
        getter for program counter.
        """
        return self.__PC

    
    def halt(self, address) :
        """
        Halt all the ongoing operations
        """
        self.__AC = BitStream(int=0, length=40) 
        self.__MQ = BitStream(int=0, length=40) 
        self.__PC = len(self.memory.instructions_memory) + 63            # I like 63(Roll number) hence the number.Basically used to break loop
        self.__IBR = "" 
        self.__IR = BitStream(int=0, length=8) 
        self.__MAR = BitStream(int=0, length=12) 
        self.__MBR = BitStream(int=0, length=20) 
        




if __name__ == "__main__":
    pass 
