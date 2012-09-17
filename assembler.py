def inttohex(int_):
    if int_ >= 0:
        return ("{0:0>4s}".format(hex(int_ % (1 << 16))[2:])).upper()
    else:
        return (hex((int_ + (1 << 16)) % (1 << 16)).upper()[2:]).upper()

def inttobin(int_):
    if int_ >= 0:
        return "{0:0>16s}".format(bin(int_)[2:])
    else:
        return bin((int_ + (1 << 16)) % (1 << 16)).upper()[2:]
    
def hextobin(hex_):
    return inttobin(int(hex_, 16))

def bintohex(bin_):
    return inttohex(int(bin_, 2))

class Assemble:
    def __init__(self):
        
        self.opcodeTable = {"NEG":"000000",
                            "AND":"000001",
                            "XOR":"000010",
                            "OR":"000011",
                            "LSR":"000100",
                            "LSL":"000101",
                            "ASL":"000101",
                            "ASR":"000110",
                            "TST":"000111",
                            "ROR":"001000",
                            "ROL":"001001",
                            "HLT":"001010",
                            "MOVB":"001100",
                            "MOV":"001101",
                            "CMP":"001110",
                            "ADD":"010000",
                            "SUB":"010001",
                            "JMP":"00111110000",
                            "JZ": "00111101000",
                            "JNZ":"00111100111",
                            "JG": "00111100010",
                            "JL": "00111100001",
                            "JE": "00111101100",
                            "JNE":"00111100011",
                            "JGE":"00111101110",
                            "JLE":"00111101101"
                            }
        self.regTable = {"R0":"000",
                         "R1":"001",
                         "R2":"010",
                         "R3":"011",
                         "R4":"100",
                         "R5":"101",
                         "R6":"110",
                         "R7":"111"
                        }
        self.symbolTable = {
                          }
        self.unknownTable = {
                             }
        self.lc = 0;
        self.inst = []
    
    def run(self):
        line = self.getLine()
        try:
            while True:
                split = self.extractContents(line)
                if split.__len__() > 0: 
                    if split[0][-1] != ":":
                        split.insert(0, None)
    #                print(split)
                    self.convert(split)
#                    for inst in self.inst:
#                        print(bintohex(inst))
#                    print(self.inst)
                line = self.getLine()
        except EOFError:
            pass
        keys = self.unknownTable.keys()
#        print(self.symbolTable)
#        print(self.unknownTable)
        for key in keys:
            locs = self.unknownTable[key]
            for loc in locs:
                self.inst[int((loc)/2)] = inttobin(self.symbolTable[key])
#        print("\n\nInstructions")
#        print(self.inst)
        for inst in self.inst:
            print(bintohex(inst))
    
    def getLine(self):
        return input().upper()
#       return self.repairLine(input())
    
#    def repairLine(self, line):
#        newLine = ""
#        for char in line:
#            if char.isspace():
#                if newLine[-1] != " ":
#                    newLine += " "
#            else:
#                newLine += char.upper()
#        return newLine
    
    def extractContents(self, line):
        return line.strip().split()
    
    def convert(self, split):
        if split[0] != None:
            self.symbolTable[split[0][:-1]] = self.lc
#        print(self.symbolTable)
        
        binstring = ""
        binstring += self.opcodeTable[split[1]]
        
        jumppresent = False
        if binstring.__len__() > 6:
            jumppresent = True
            split.append(split[2])
            split[2] = ""
        
        if jumppresent == False:
            if split.__len__() > 2:
                if split[2][0] == "*":
                    binstring += self.regTable[split[2][1:][:-1]] + "01"
                else:
                    binstring += self.regTable[split[2][:-1]] + "00"
            else:
                binstring += "00000"
        
        if split[1] == "TST":
            binstring += "0" + hextobin(split[3][1:])[-4:]
            self.addInst(binstring)
            return
        
        try:
            if split.__len__() > 3:
                if split[3][0] == "#":
                    binstring += "00010"
                    self.addInst(binstring)
                    self.addInst(hextobin(split[3][1:]))
                elif split[3][0] == "*":
                    binstring += self.regTable[split[3][1:]] + "01"
                    self.addInst(binstring)
                else:
                    binstring += self.regTable[split[3]] + "00"
                    self.addInst(binstring)
            else:
                binstring += "00000"
                self.addInst(binstring)
        except KeyError:
            binstring += "00010"
            self.addInst(binstring)
            try:
                self.addInst(inttobin(self.symbolTable[split[3]]))
            except KeyError:
                try:
                    self.unknownTable[split[3]].append(self.lc)
                except KeyError:
                    self.unknownTable[split[3]] = []
                    self.unknownTable[split[3]].append(self.lc)                    
                self.addInst("")
                
    def addInst(self, inst):
#        print(hex(self.lc)[2:] + "\t: " + inst)
        self.inst.append(inst)
        self.lc += 2
                
if __name__ == '__main__':
    asm = Assemble()
    asm.run()
#    print("Done!")
