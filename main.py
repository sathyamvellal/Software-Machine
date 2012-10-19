#!/usr/bin/python3.2

import sys
from PyQt4 import QtGui, QtCore
from gui import Ui_Form

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

class PyASM(QtGui.QMainWindow):
    
    def __init__(self):
        super(PyASM, self).__init__()
        self.ui = Ui_Form(); self.ui.setupUi(self)
        self.ui.step.clicked.connect(self.run)
        self.ui.run.clicked.connect(self.runFull)
        self.initSIM()
        self.ui.memory.verticalHeader().setVisible(False)
        self.ui.memory.setRowCount(32768)
        self.newItem = QtGui.QTableWidgetItem
        self.setWindowTitle('Software Machine v1.3')
        
        openFile = QtGui.QAction('&Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.triggered.connect(self.loadProgramFromFile)
        refreshProgram = QtGui.QAction('&Refresh', self)
        refreshProgram.setShortcut('Ctrl+R')
        refreshProgram.triggered.connect(self.loadInstructions)
        aboutProgram = QtGui.QAction('&About', self)
        aboutProgram.triggered.connect(self.aboutProgram)
        exitAction = QtGui.QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(QtGui.qApp.quit)
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Menu')
        fileMenu.addAction(openFile)
        fileMenu.addAction(refreshProgram)
        fileMenu.addAction(exitAction)
        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction(aboutProgram)
        
        stepButton = QtGui.QAction(self)
        stepButton.setShortcut('F11')
        stepButton.triggered.connect(self.run)
        self.ui.step.addAction(stepButton)
        runButton = QtGui.QAction(self)
        runButton.setShortcut('F5')
        runButton.triggered.connect(self.runFull)
        self.ui.run.addAction(runButton)
        
        self.running = "on"
        
        row = 0
        i = 0
        for row in range(0, 32768):
            #self.ui.table.setItem(row, 0, QtGui.QTableWidgetItem(str(row)))
            self.ui.memory.setItem(row, 0, self.newItem(inttohex(i)))
            self.ui.memory.setItem(row, 1, self.newItem("0000"))
            self.ui.memory.item(row, 0).setFlags(QtCore.Qt.ItemIsSelectable)
            i += 2
        self.updateUI()
        #self.ui.instructions.setReadOnly(True)
        self.show()
    
    def updateUI(self):
        self.ui.r0.setText("r0:     " + self.regbank["000"])
        self.ui.r1.setText("r1:     " + self.regbank["001"])
        self.ui.r2.setText("r2:     " + self.regbank["010"])
        self.ui.r3.setText("r3:     " + self.regbank["011"])
        self.ui.r4.setText("r4:     " + self.regbank["100"])
        self.ui.r5.setText("r5:     " + self.regbank["101"])
        self.ui.r6.setText("r6:     " + self.regbank["110"])
        self.ui.r7.setText("r7:     " + self.regbank["111"])
        self.regbank["pc"] = inttohex(2 * self.pc)
        self.ui.pc.setText("pc:     " + self.regbank["pc"])
        self.ui.sp.setText("sp:     " + self.regbank["sp"])
        tmp = hextobin(self.regbank["flags"])
        self.ui.flags.setText("Flags:\n" + "Z" + tmp[-16] + 
                              ", E" + tmp[-15] + 
                              ", G" + tmp[-14] +
                              ", L" + tmp[-13])
        
    def initSIM(self):
        # Initialize the backend requirements of the SIM
        #self.memory = ["00"] * 65536
        self.instructionTable = {"000000":self.instruction_NEG,
                                 "000001":self.instruction_AND,
                                 "000010":self.instruction_XOR,
                                 "000011":self.instruction_OR,
                                 "000100":self.instruction_LSR,
                                 "000101":self.instruction_LSL,
                                 "000110":self.instruction_ASR,
                                 "000111":self.instruction_TST,
                                 "001000":self.instruction_ROR,
                                 "001001":self.instruction_ROL,
                                 "001010":self.instruction_HLT,
                                 "001011":None,
                                 "001100":self.instruction_MOVB,
                                 "001101":self.instruction_MOV,
                                 "001110":self.instruction_CMP,
                                 "001111":self.instruction_JMP,
                                 "010000":self.instruction_ADD,
                                 "010001":self.instruction_SUB,
                                 "010010":self.instruction_PUSH,
                                 "010011":self.instruction_POP,
                                 "010100":self.instruction_CALL,
                                 "010101":self.instruction_RET
                                 }
        self.regbank = {"000":"0000",
                        "001":"0000",
                        "010":"0000",
                        "011":"0000",
                        "100":"0000",
                        "101":"0000",
                        "110":"0000",
                        "111":"0000",
                        "flags":"0000",
                        "pc":"0000",
                        "sp":"FFFE"
                        }
        self.pc = 0
        self.prevpc = 0
        self.initialPC = 0
        self.initialLoadAddress = 0
        
    def loadProgramFromFile(self):
        file = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '.')
        file = open(file, 'r')
        self.ui.instructions.setText(file.read())
        file.close()
        addr, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Enter starting address to place instructions (default : 0000)')
        if not ok or addr == "":
            addr = "0000"
        addr = int(addr, 16)
        tmp, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Enter value of PC (default : 0000)')
        if not ok or tmp == "":
            tmp = "0000"
        self.pc = int(int(tmp, 16)/2)
        self.initialPC = self.pc
        self.initialLoadAddress = addr
        self.loadInstructions()
        
    def loadInstructions(self):
        self.regbank["000"] = "0000"
        self.regbank["001"] = "0000"
        self.regbank["010"] = "0000"
        self.regbank["011"] = "0000"
        self.regbank["100"] = "0000"
        self.regbank["101"] = "0000"
        self.regbank["110"] = "0000"
        self.regbank["111"] = "0000"
        self.regbank["flags"] = "0000"
        self.regbank["pc"] = "0000"
        sp, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Enter value of start of Stack (default : FFFE)')
        if not ok or sp == "":
            self.regbank["sp"] = "FFFE"
        else:
            self.regbank["sp"] = sp
        
        self.pc = self.initialPC
        i = self.initialLoadAddress
        
        instructions = self.ui.instructions.toPlainText().split("\n")
        for inst in instructions:
            if inst != "":
                self.setWord(i, inst)
                #self.ui.memory.item(int(i / 2), 1).setFlags(QtCore.Qt.ItemIsSelectable)
                i += 2
        self.updateUI()
        self.defaultColor = self.ui.memory.item(0, 0).background()
        self.running = "on"
        self.previnst = ""
    
    def run(self):
        if self.running == "on" and self.pc < 32768:
            if self.previnst != "":
                self.ui.memory.item(self.prevpc-1, 1).setBackground(self.defaultColor)
                if self.previnst[-2:] == "10" or self.previnst[-2:] == "11" or self.previnst[-7:-5] == "10" or self.previnst[-7:-5] == "11":
                    self.ui.memory.item(self.prevpc-2, 1).setBackground(self.defaultColor)
            inst = hextobin(self.nextInstruction())
            self.simulateInstruction(inst)
            self.updateUI()
            self.previnst = inst
            #print("run successful!")
            
    def runFull(self):
        while self.running == "on" and self.pc < 32768:
            self.run()
        
    def nextInstruction(self):
        inst = self.ui.memory.item(self.pc, 1).text()
        self.ui.memory.item(self.pc, 1).setBackground(QtGui.QBrush(QtGui.QColor(0, 255, 255)))
        self.pc += 1
        self.prevpc = self.pc
        return inst
        # boundary conditions to be added
        
    def simulateInstruction(self, inst):            
        self.instructionTable[inst[-16:-10]](inst)
    
    # ------------------------- NEG ------------------------- #
    def instruction_NEG(self, inst):
        #print("NEG")
        src1 = self.getOperandOneWord(inst)
        self.setDestinationWord(inst, ~src1)
        #print("NEG Executed")
    
    # ------------------------- AND ------------------------- #    
    def instruction_AND(self, inst):
        #print("AND")
        src1 = self.getOperandOneWord(inst)
        src2 = self.getOperandTwoWord(inst)
        self.setDestinationWord(inst, src1 & src2)
        #print("AND Executed")
    
    # ------------------------- XOR ------------------------- #
    def instruction_XOR(self, inst):
        #print("XOR")
        src1 = self.getOperandOneWord(inst)
        src2 = self.getOperandTwoWord(inst)
        self.setDestinationWord(inst, src1 ^ src2)
        #print()
    
    # ------------------------- ORR ------------------------- #
    def instruction_OR(self, inst):
        #print("OR")
        src1 = self.getOperandOneWord(inst)
        src2 = self.getOperandTwoWord(inst)
        self.setDestinationWord(inst, src1 | src2)
        #print("OR Executed")
    
    # ------------------------- LSR ------------------------- # 
    def instruction_LSR(self, inst):
        #print("LSR")
        src1 = self.getOperandOneWord(inst)
        src2 = self.getOperandTwoWord(inst)
        self.setDestinationWord(inst, src2 >> src1)
        #print("LSR Executed")
    
    # ------------------------- LSL ------------------------- #    
    def instruction_LSL(self, inst):
        #print("LSL")
        src1 = self.getOperandOneWord(inst)
        src2 = self.getOperandTwoWord(inst)
        self.setDestinationWord(inst, src2 << src1)
        #print("LSL Executed")
    
    # ------------------------- ASR ------------------------- #
    def instruction_ASR(self, inst):
        #print("ASR")
        src1 = self.getOperandOneWord(inst)
        src2 = self.getOperandTwoWord(inst)
        if src2 > 32767:
            src2 -= 65536
        self.setDestinationWord(inst, src2 >> src1)
        #print("ASR Executed")
    
    # ------------------------- TST ------------------------- #
    def instruction_TST(self, inst):
        #print("TST")
        if inst[-7:-5] == "00":
            src = int(self.regbank[inst[-10:-7]], 16)
        elif inst[-7:-5] == "01":
            src = int(self.getWord(int(self.regbank[inst[-10:-5]], 16)), 16)
            
        bit = 2**(int(inst[-4:], 2))
        #print(inttobin(src))
        #print(inttobin(bit))
        if bit & src == 0:
            tmp = "1000000000000000"
            #print("Zero")
        else:
            tmp = "0000000000000000"
            #print("Not Zero")
            
        self.regbank["flags"] = bintohex(tmp)
        #print("TST Executed")
    
    # ------------------------- ROR ------------------------- #
    def instruction_ROR(self, inst):
        #print("LRR")
        src1 = self.getOperandOneWord(inst)
        src2 = self.getOperandTwoWord(inst)
        self.setDestinationWord(inst, (src2 >> src1) | (src2 << (16-src1)))
        #print("ROR Executed")
        
    # ------------------------- ROL ------------------------- #
    def instruction_ROL(self, inst):
        #print("LRL")
        src1 = self.getOperandOneWord(inst)
        src2 = self.getOperandTwoWord(inst)
        self.setDestinationWord(inst, (src2 << src1) | (src2 >> (16-src1)))
        #print("ROL Executed")
    
    # ------------------------- HLT ------------------------- #
    def instruction_HLT(self, inst):
        #print("HLT")
        self.running = "off"
        #print("HLT Executed")
    
    # ------------------------- MOVB ------------------------- #    
    def instruction_MOVB(self, inst):
        #print("MOVB")
        src1 = self.getOperandOneByte(inst)
        self.setDestinationByte(inst, src1)
        #print("MOVB Executed")
        
    # ------------------------- MOV ------------------------- #
    def instruction_MOV(self, inst):
        #print("MOV")
        src1 = self.getOperandOneWord(inst)
        self.setDestinationWord(inst, src1)
        #print("MOV Executed")
        
    # ------------------------- CMP ------------------------- #
    def instruction_CMP(self, inst):
        #print("CMP")
        src2 = self.getOperandOneWord(inst)
        src1 = self.getOperandTwoWord(inst)
        
        #print(src1)
        #print(src2)
        self.updateFlags(src1, src2)
        #print("CMP Executed")
        
    # ------------------------- JMP ------------------------- #
    def instruction_JMP(self, inst):
        #print("JMP")
        if inst[-2:] == "00":
            jmpdest = int(self.regbank[inst[-5:-2]], 16)
        elif inst[-2:] == "01":
            val = int(self.regbank[inst[-5:-2]], 16)
            if val > 32767:
                val -= 65536
            jmpdest = int(self.regbank["pc"], 16) + val
        elif inst[-2:] == "10":
            jmpdest = int(self.nextInstruction(), 16)
        elif inst[-2:] == "11":
            val = int(self.nextInstruction(), 16)
            if val > 32767:
                val -= 65536
            jmpdest = int(self.regbank["pc"], 16) + val
            #print(self.regbank["pc"])
            #print(val)
            #print(inttohex(jmpdest))

        #print(inst)
        if inst[-10] == "1":
            self.pc = int(jmpdest / 2)
        elif int(inst[-9:-5], 2) & int(hextobin(self.regbank["flags"])[-16:-12], 2) > 0:
            self.pc = int(jmpdest / 2)
            #print("Taking JMP")
        
        #print("JMP Executed")
        
    # ------------------------- ADD ------------------------- #
    def instruction_ADD(self, inst):
        #print("ADD")
        src1 = self.getOperandOneWord(inst)
        src2 = self.getOperandTwoWord(inst)
        self.setDestinationWord(inst, src1 + src2)
        #print("ADD Executed")
        
    # ------------------------- SUB ------------------------- #
    def instruction_SUB(self, inst):
        #print("SUB")
        src1 = self.getOperandOneWord(inst)
        src2 = self.getOperandTwoWord(inst)
        self.setDestinationWord(inst, src2 - src1)
        #print("SUB Executed")
        
    # ------------------------- PUSH ------------------------- #
    def instruction_PUSH(self, inst):
        intsp = int(self.regbank["sp"], 16)
        self.setWord(intsp, inttohex(self.getOperandOneWord(inst)))
        self.regbank["sp"] = inttohex(intsp-2)
    
    # ------------------------- POP ------------------------- #
    def instruction_POP(self, inst):
        intsp = int(self.regbank["sp"], 16) + 2
        self.setDestinationWord(inst, int(self.getWord(intsp), 16))
        self.regbank["sp"] = inttohex(intsp)
        pass

    # ------------------------- CALL ------------------------- #
    def instruction_CALL(self, inst):
        if inst[-2:] == "00":
            jmpdest = int(self.regbank[inst[-5:-2]], 16)
        elif inst[-2:] == "01":
            val = int(self.regbank[inst[-5:-2]], 16)
            if val > 32767:
                val -= 65536
            jmpdest = int(self.regbank["pc"], 16) + val
        elif inst[-2:] == "10":
            jmpdest = int(self.nextInstruction(), 16)
        elif inst[-2:] == "11":
            val = int(self.nextInstruction(), 16)
            if val > 32767:
                val -= 65536
            jmpdest = int(self.regbank["pc"], 16) + val

        intsp = int(self.regbank["sp"], 16)
        self.setWord(intsp, inttohex(2*self.pc))
        self.regbank["sp"] = inttohex(intsp-2)

        self.pc = int(jmpdest / 2)

    # ------------------------- RET ------------------------- #
    def instruction_RET(self, inst):
        intsp = int(self.regbank["sp"], 16) + 2
        self.pc = int(int(self.getWord(intsp), 16) / 2)
        self.regbank["sp"] = inttohex(intsp)

    # ------------------------- Misc ------------------------- #
    def getOperandOneWord(self, inst):
        if inst[-2:] == "00":
            src1 = int(self.regbank[inst[-5:-2]], 16)
        elif inst[-2:] == "01":
            src1 = int(self.getWord(int(self.regbank[inst[-5:-2]], 16)), 16)
        elif inst[-2:] == "10":
            src1 = int(self.nextInstruction(), 16)
        return src1
    
    def getOperandOneByte(self, inst):
        if inst[-2:] == "00":
            src1 = int(self.regbank[inst[-5:-2]][-2:], 16)
        elif inst[-2:] == "01":
            src1 = int(self.getByte(int(self.regbank[inst[-5:-2]], 16))[-2:], 16)
        elif inst[-2:] == "10":
            src1 = int((self.nextInstruction())[-2:], 16)
        return src1
    
    def getOperandTwoWord(self, inst):
        if inst[-7:-5] == "00":
            src2 = int(self.regbank[inst[-10:-7]], 16)
        elif inst[-7:-5] == "01":
            src2 = int(self.getWord(int(self.regbank[inst[-10:-7]], 16)), 16)
        return src2
    
    def getOperandTwoByte(self, inst):
        if inst[-7:-5] == "00":
            src2 = int(self.regbank[inst[-10:-7]][-2:], 16)
        elif inst[-7:-5] == "01":
            src2 = int(self.getWord(int(self.regbank[inst[-10:-7]], 16))[-2:], 16)
        return src2
    
    def setDestinationWord(self, inst, dest):
        if inst[-7:-5] == "00":
            self.regbank[inst[-10:-7]] = inttohex(dest)
        elif inst[-7:-5] == "01":
            self.setWord(int(self.regbank[inst[-10:-7]], 16), inttohex(dest))
            
    def setDestinationByte(self, inst, dest):
        if inst[-7:-5] == "00":
            self.regbank[inst[-10:-7]] = self.regbank[inst[-10:-17]][-4:-2] + inttohex(dest)[-2:] 
        elif inst[-7:-5] == "01":
            self.setByte(int(self.regbank[inst[-10:-7]], 16), inttohex(dest)[-2:])
    
    def getByte(self, byteNo):
        if byteNo % 2 == 0:
            return self.ui.memory.item(byteNo, 1)[:2]
        else:
            return self.ui.memory.item(byteNo - 1, 1)[2:]
    
    def setByte(self, byteNo, val):
        word = self.ui.memory.item(byteNo, 1)
        if byteNo % 2 == 0:
            word = val + word[2:] 
        else:
            word = word[:2] + val
        word = self.ui.memory.setItem(byteNo - (byteNo % 2), 1, self.newItem(word))
        
    def getWord(self, wordNo):
        wordNo = int(wordNo / 2)
        return self.ui.memory.item(wordNo, 1).text()
    
    def setWord(self, wordNo, val):
        wordNo = int(wordNo / 2)
        self.ui.memory.setItem(wordNo, 1, self.newItem(val))
        
    def updateFlags(self, src1, src2):
        flags = hextobin(self.regbank["flags"])
        if src1 == src2 != 0:
            flags = "0100" + flags[-12:]
        elif src1 == src2 == 0:
            flags = "1100" + flags[-12:]
        elif src1 < src2:
            flags = "0001" + flags[-12:]
        elif src1 > src2:
            flags = "0010" + flags[-12:]
        self.regbank["flags"] = bintohex(flags)
        
    def aboutProgram(self):
        QtGui.QMessageBox.information(self, 'About', 'Software Machine\nVersion 1.3\n\nDesigned and Developed by\nSathyam M Vellal', QtGui.QMessageBox.Ok)
        
    
if __name__ == '__main__':
    qApp = QtGui.QApplication(sys.argv)
    pyasm = PyASM()
    #pyasm.show()
    sys.exit(qApp.exec_())
