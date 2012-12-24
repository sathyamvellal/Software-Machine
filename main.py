#!/usr/bin/python3.2

import sys
from PyQt4 import QtGui, QtCore
from gui import Ui_Form

def inttohex(int_):
	"""
	Convert an integer to 4 digit hex string
	@param int_ integer to be converted
	@return 4 digit hex string
	"""
	if int_ >= 0:
		return ("{0:0>4s}".format(hex(int_ % (1 << 16))[2:])).upper()
	else:
		return (hex((int_ + (1 << 16)) % (1 << 16)).upper()[2:]).upper()

def inttobin(int_):
	"""
	convert an integer to 16 bit binary sting
	@param int_ integer to be converted
	@return 16 bit binary string
	"""
	if int_ >= 0:
		return "{0:0>16s}".format(bin(int_)[2:])
	else:
		return bin((int_ + (1 << 16)) % (1 << 16)).upper()[2:]
	
def hextobin(hex_):
	"""
	convert 4 digit hex string to 16 bit binary string
	@param hex_ 4 digit hex string
	@return 16 bit binary string
	"""
	return inttobin(int(hex_, 16))

def bintohex(bin_):
	"""
	convert a 16 bit binary string to 4 digit hex string
	@param bin_ 16 bit binary string
	@return 4 digit hex string
	"""
	return inttohex(int(bin_, 2))

class PyASM(QtGui.QMainWindow):
	"""
	Application class responsible for the instantiation of the GUI and simulation of the Software Machine.
	@extends QtGui.QMainWindow framework for building the application's GUI
	"""
	
	def __init__(self):
		"""
		Constructor. 
		Inititalizes GUI, event handling, hotkeys, etc
		"""
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
			self.ui.memory.setItem(row, 0, self.newItem(inttohex(i)))
			self.ui.memory.setItem(row, 1, self.newItem("0000"))
			self.ui.memory.item(row, 0).setFlags(QtCore.Qt.ItemIsSelectable)
			i += 2
		self.updateUI()
		self.show()
	
	def updateUI(self):
		"""
		Updates the the GUI with the backend data used by the simulator
		"""
		self.ui.r0.setText("r0:	 " + self.regbank["000"])
		self.ui.r1.setText("r1:	 " + self.regbank["001"])
		self.ui.r2.setText("r2:	 " + self.regbank["010"])
		self.ui.r3.setText("r3:	 " + self.regbank["011"])
		self.ui.r4.setText("r4:	 " + self.regbank["100"])
		self.ui.r5.setText("r5:	 " + self.regbank["101"])
		self.ui.r6.setText("r6:	 " + self.regbank["110"])
		self.ui.r7.setText("r7:	 " + self.regbank["111"])
		self.regbank["pc"] = inttohex(2 * self.pc)
		self.ui.pc.setText("pc:	 " + self.regbank["pc"])
		self.ui.sp.setText("sp:	 " + self.regbank["sp"])
		tmp = hextobin(self.regbank["flags"])
		self.ui.flags.setText("Flags:\n" + "Z" + tmp[-16] + 
							  ", E" + tmp[-15] + 
							  ", G" + tmp[-14] +
							  ", L" + tmp[-13])
		
	def initSIM(self):
		"""
		Initialize the backend of the Simulator. 
		"""
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
		"""
		Load a program from a file. Opens a QFileDialog instance to read the input program file to the text editor in the Simulator.
		"""
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
		"""
		Instructions to be given to the simulator are read from the text editor and are loaded to memory.
		"""
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
				i += 2
		self.updateUI()
		self.defaultColor = self.ui.memory.item(0, 0).background()
		self.running = "on"
		self.previnst = ""
	
	def run(self):
		"""
		Runs the next instruction (if any). Equivalent to 'step'
		"""
		if self.running == "on" and self.pc < 32768:
			if self.previnst != "":
				self.ui.memory.item(self.prevpc-1, 1).setBackground(self.defaultColor)
				if self.previnst[-2:] == "10" or self.previnst[-2:] == "11" or self.previnst[-7:-5] == "10" or self.previnst[-7:-5] == "11":
					self.ui.memory.item(self.prevpc-2, 1).setBackground(self.defaultColor)
			inst = hextobin(self.nextInstruction())
			self.simulateInstruction(inst)
			self.updateUI()
			self.previnst = inst
			
	def runFull(self):
		"""
		Runs the whole program (or the remaining) till the end of the program. Equivalent to 'run'
		"""
		while self.running == "on" and self.pc < 32768:
			self.run()
		
	def nextInstruction(self):
		"""
		Obtains the next word from memory which can be used either as instruction/data and highlights it.
		@return 4 digit hex string
		"""
		inst = self.ui.memory.item(self.pc, 1).text()
		self.ui.memory.item(self.pc, 1).setBackground(QtGui.QBrush(QtGui.QColor(0, 255, 255)))
		self.pc += 1
		self.prevpc = self.pc
		return inst
		# boundary conditions to be added
		
	def simulateInstruction(self, inst):
		"""
		Starts simulation of the instruction provided. 
		@param inst instruction to be simulated. 
		"""
		self.instructionTable[inst[-16:-10]](inst)
	
	def instruction_NEG(self, inst):
		"""
		Simulation of NEG (negation)
		Details in specs document
		@param inst NEG instruction 
		"""
		src1 = self.getOperandOneWord(inst)
		self.setDestinationWord(inst, ~src1)
	
	def instruction_AND(self, inst):
		"""
		Simulation of AND (bitwise and)
		Details in specs document
		@param inst AND instruction 
		"""
		src1 = self.getOperandOneWord(inst)
		src2 = self.getOperandTwoWord(inst)
		self.setDestinationWord(inst, src1 & src2)
	
	def instruction_XOR(self, inst):
		"""
		Simulation of XOR (bitwise xor)
		Details in specs document
		@param inst NEG instruction 
		"""
		src1 = self.getOperandOneWord(inst)
		src2 = self.getOperandTwoWord(inst)
		self.setDestinationWord(inst, src1 ^ src2)
	
	def instruction_OR(self, inst):
		"""
		Simulation of OR (or)
		Details in specs document
		@param inst OR instruction 
		"""
		src1 = self.getOperandOneWord(inst)
		src2 = self.getOperandTwoWord(inst)
		self.setDestinationWord(inst, src1 | src2)
	
	def instruction_LSR(self, inst):
		"""
		Simulation of LSR (Logical Right-Shift)
		Details in specs document
		@param inst LSR instruction 
		"""
		src1 = self.getOperandOneWord(inst)
		src2 = self.getOperandTwoWord(inst)
		self.setDestinationWord(inst, src2 >> src1)
	
	def instruction_LSL(self, inst):
		"""
		Simulation of LSL (Logical Left-Shift) - Also applies for ASL (Arithmetic Left-Shift)
		Details in specs document
		@param inst LSL instruction 
		"""
		src1 = self.getOperandOneWord(inst)
		src2 = self.getOperandTwoWord(inst)
		self.setDestinationWord(inst, src2 << src1)
	
	def instruction_ASR(self, inst):
		"""
		Simulation of ASR (Arithmetic Right-Shft)
		Details in specs document
		@param inst ASL instruction 
		"""
		src1 = self.getOperandOneWord(inst)
		src2 = self.getOperandTwoWord(inst)
		if src2 > 32767:
			src2 -= 65536
		self.setDestinationWord(inst, src2 >> src1)
	
	def instruction_TST(self, inst):
		"""
		Simulation of TST (Test bit)
		Details in specs document
		@param inst TST instruction 
		"""
		if inst[-7:-5] == "00":
			src = int(self.regbank[inst[-10:-7]], 16)
		elif inst[-7:-5] == "01":
			src = int(self.getWord(int(self.regbank[inst[-10:-5]], 16)), 16)
			
		bit = 2**(int(inst[-4:], 2))
		if bit & src == 0:
			tmp = "1000000000000000"
		else:
			tmp = "0000000000000000"
			
		self.regbank["flags"] = bintohex(tmp)
	
	def instruction_ROR(self, inst):
		"""
		Simulation of ROR (Rotate Right)
		Details in specs document
		@param inst ROR instruction 
		"""
		src1 = self.getOperandOneWord(inst)
		src2 = self.getOperandTwoWord(inst)
		self.setDestinationWord(inst, (src2 >> src1) | (src2 << (16-src1)))
		
	def instruction_ROL(self, inst):
		"""
		Simulation of ROL (Rotate Left)
		Details in specs document
		@param inst ROL instruction 
		"""
		src1 = self.getOperandOneWord(inst)
		src2 = self.getOperandTwoWord(inst)
		self.setDestinationWord(inst, (src2 << src1) | (src2 >> (16-src1)))
	
	def instruction_HLT(self, inst):
		"""
		Simulation of HLT (Halt)
		Details in specs document
		@param inst HLT instruction 
		"""
		self.running = "off"
	
	def instruction_MOVB(self, inst):
		"""
		Simulation of MOVB (Move byte)
		Details in specs document
		@param inst  instruction 
		"""
		src1 = self.getOperandOneByte(inst)
		self.setDestinationByte(inst, src1)
		
	def instruction_MOV(self, inst):
		"""
		Simulation of MOV (Move)
		Details in specs document
		@param inst MOV instruction 
		"""
		src1 = self.getOperandOneWord(inst)
		self.setDestinationWord(inst, src1)
		
	def instruction_CMP(self, inst):
		"""
		Simulation of CMP (Compare)
		Details in specs document
		@param inst CMP instruction 
		"""
		src2 = self.getOperandOneWord(inst)
		src1 = self.getOperandTwoWord(inst)
		self.updateFlags(src1, src2)
		
	def instruction_JMP(self, inst):
		"""
		Simulation of JMP (Jump/Branch). Different types of jumping use JMP with different flags set.
		Details in specs document
		@param inst  instruction 
		"""
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
		if inst[-10] == "1":
			self.pc = int(jmpdest / 2)
		elif int(inst[-9:-5], 2) & int(hextobin(self.regbank["flags"])[-16:-12], 2) > 0:
			self.pc = int(jmpdest / 2)
		
	def instruction_ADD(self, inst):
		"""
		Simulation of ADD (addition)
		Details in specs document
		@param inst ADD instruction 
		"""
		src1 = self.getOperandOneWord(inst)
		src2 = self.getOperandTwoWord(inst)
		self.setDestinationWord(inst, src1 + src2)
		
	def instruction_SUB(self, inst):
		"""
		Simulation of SUB (subtraction)
		Details in specs document
		@param inst SUB instruction 
		"""
		src1 = self.getOperandOneWord(inst)
		src2 = self.getOperandTwoWord(inst)
		self.setDestinationWord(inst, src2 - src1)
		
	def instruction_PUSH(self, inst):
		"""
		Simulation of PUSH (push to stack)
		Details in specs document
		@param inst PUSH instruction 
		"""
		intsp = int(self.regbank["sp"], 16)
		self.setWord(intsp, inttohex(self.getOperandOneWord(inst)))
		self.regbank["sp"] = inttohex(intsp-2)
	
	def instruction_POP(self, inst):
		"""
		Simulation of POP (pop from stack)
		Details in specs document
		@param inst POP instruction 
		"""
		intsp = int(self.regbank["sp"], 16) + 2
		self.setDestinationWord(inst, int(self.getWord(intsp), 16))
		self.regbank["sp"] = inttohex(intsp)
		pass

	def instruction_CALL(self, inst):
		"""
		Simulation of CALL (sub-routine call)
		Details in specs document
		@param inst CALL instruction 
		"""
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

	def instruction_RET(self, inst):
		"""
		Simulation of RET (sub-routine return)
		Details in specs document
		@param inst RET instruction 
		"""
		intsp = int(self.regbank["sp"], 16) + 2
		self.pc = int(int(self.getWord(intsp), 16) / 2)
		self.regbank["sp"] = inttohex(intsp)

	def getOperandOneWord(self, inst):
		"""
		Gets a word denoted by bits 2 to 5 of the instruction
		@param inst instruction which contains flags set for the method of data access
		@return 4 digit hex string
		"""
		if inst[-2:] == "00":
			src1 = int(self.regbank[inst[-5:-2]], 16)
		elif inst[-2:] == "01":
			src1 = int(self.getWord(int(self.regbank[inst[-5:-2]], 16)), 16)
		elif inst[-2:] == "10":
			src1 = int(self.nextInstruction(), 16)
		return src1
	
	def getOperandOneByte(self, inst):
		"""
		Gets a byte denoted by bits 2 to 5 of the instruction
		@param inst instruction which contains flags set for the method of data access
		@return 2 digit hex string
		"""
		if inst[-2:] == "00":
			src1 = int(self.regbank[inst[-5:-2]][-2:], 16)
		elif inst[-2:] == "01":
			src1 = int(self.getByte(int(self.regbank[inst[-5:-2]], 16))[-2:], 16)
		elif inst[-2:] == "10":
			src1 = int((self.nextInstruction())[-2:], 16)
		return src1
	
	def getOperandTwoWord(self, inst):
		"""
		Gets a word denoted by bits 7 to 10 of the instruction
		@param inst instruction which contains flags set for the method of data access
		@return 4 digit hex string
		"""
		if inst[-7:-5] == "00":
			src2 = int(self.regbank[inst[-10:-7]], 16)
		elif inst[-7:-5] == "01":
			src2 = int(self.getWord(int(self.regbank[inst[-10:-7]], 16)), 16)
		return src2
	
	def getOperandTwoByte(self, inst):
		"""
		Gets a byte denoted by bits 7 to 10 of the instruction
		@param inst instruction which contains flags set for the method of data access
		@return 2 digit hex string
		"""
		if inst[-7:-5] == "00":
			src2 = int(self.regbank[inst[-10:-7]][-2:], 16)
		elif inst[-7:-5] == "01":
			src2 = int(self.getWord(int(self.regbank[inst[-10:-7]], 16))[-2:], 16)
		return src2
	
	def setDestinationWord(self, inst, dest):
		"""
		Sets a word denoted by bits 7 to 10 of the instruction
		@param inst instruction which contains flags set for the method of data access
		"""
		if inst[-7:-5] == "00":
			self.regbank[inst[-10:-7]] = inttohex(dest)
		elif inst[-7:-5] == "01":
			self.setWord(int(self.regbank[inst[-10:-7]], 16), inttohex(dest))
			
	def setDestinationByte(self, inst, dest):
		"""
		Sets a byte denoted by bits 7 to 10 of the instruction
		@param inst instruction which contains flags set for the method of data access
		"""
		if inst[-7:-5] == "00":
			self.regbank[inst[-10:-7]] = self.regbank[inst[-10:-17]][-4:-2] + inttohex(dest)[-2:] 
		elif inst[-7:-5] == "01":
			self.setByte(int(self.regbank[inst[-10:-7]], 16), inttohex(dest)[-2:])
	
	def getByte(self, byteNo):
		"""
		Gets a byte of data from memory
		@param byteNo the byte to be obtained
		@return 2 digit hex string
		"""
		if byteNo % 2 == 0:
			return self.ui.memory.item(byteNo, 1)[:2]
		else:
			return self.ui.memory.item(byteNo - 1, 1)[2:]
	
	def setByte(self, byteNo, val):
		"""
		Sets a byte of data in memory
		@param byteNo the byte to be set
		@param val value to be set in memory
		"""
		word = self.ui.memory.item(byteNo, 1)
		if byteNo % 2 == 0:
			word = val + word[2:] 
		else:
			word = word[:2] + val
		word = self.ui.memory.setItem(byteNo - (byteNo % 2), 1, self.newItem(word))
		
	def getWord(self, wordNo):
		"""
		Gets a word of data from memory
		@param wordNo the word to be obtained
		@return 4 digit hex string
		"""
		wordNo = int(wordNo / 2)
		return self.ui.memory.item(wordNo, 1).text()
	
	def setWord(self, wordNo, val):
		"""
		Sets a word of data in memory
		@param wordNo the word to be set
		@param val value to be set in memory
		"""
		wordNo = int(wordNo / 2)
		self.ui.memory.setItem(wordNo, 1, self.newItem(val))
		
	def updateFlags(self, src1, src2):
		"""
		Update flag register with respect to the values provided
		@param src1 1st value, operand one
		@param src2 2nd value, operand two
		"""
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
		"""
		Displays a message box about the Simulator
		"""
		QtGui.QMessageBox.information(self, 'About', 'Software Machine\nVersion 1.3\n\nDesigned and Developed by\nSathyam M Vellal', QtGui.QMessageBox.Ok)
		
	
if __name__ == '__main__':
	qApp = QtGui.QApplication(sys.argv)
	pyasm = PyASM()
	sys.exit(qApp.exec_())
