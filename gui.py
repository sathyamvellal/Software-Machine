# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PyASM.ui'
#
# Created: Mon Dec 24 13:08:16 2012
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(551, 507)
        self.regBank = QtGui.QFrame(Form)
        self.regBank.setGeometry(QtCore.QRect(10, 40, 151, 461))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        self.regBank.setFont(font)
        self.regBank.setFrameShape(QtGui.QFrame.StyledPanel)
        self.regBank.setFrameShadow(QtGui.QFrame.Raised)
        self.regBank.setObjectName(_fromUtf8("regBank"))
        self.r0 = QtGui.QPushButton(self.regBank)
        self.r0.setGeometry(QtCore.QRect(10, 0, 131, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        font.setPointSize(12)
        self.r0.setFont(font)
        self.r0.setText(_fromUtf8(""))
        self.r0.setCheckable(False)
        self.r0.setChecked(False)
        self.r0.setObjectName(_fromUtf8("r0"))
        self.r1 = QtGui.QPushButton(self.regBank)
        self.r1.setGeometry(QtCore.QRect(10, 40, 131, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        font.setPointSize(12)
        self.r1.setFont(font)
        self.r1.setText(_fromUtf8(""))
        self.r1.setCheckable(False)
        self.r1.setChecked(False)
        self.r1.setObjectName(_fromUtf8("r1"))
        self.r3 = QtGui.QPushButton(self.regBank)
        self.r3.setGeometry(QtCore.QRect(10, 120, 131, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        font.setPointSize(12)
        self.r3.setFont(font)
        self.r3.setText(_fromUtf8(""))
        self.r3.setCheckable(False)
        self.r3.setChecked(False)
        self.r3.setObjectName(_fromUtf8("r3"))
        self.r2 = QtGui.QPushButton(self.regBank)
        self.r2.setGeometry(QtCore.QRect(10, 80, 131, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        font.setPointSize(12)
        self.r2.setFont(font)
        self.r2.setText(_fromUtf8(""))
        self.r2.setCheckable(False)
        self.r2.setChecked(False)
        self.r2.setObjectName(_fromUtf8("r2"))
        self.r5 = QtGui.QPushButton(self.regBank)
        self.r5.setGeometry(QtCore.QRect(10, 200, 131, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        font.setPointSize(12)
        self.r5.setFont(font)
        self.r5.setText(_fromUtf8(""))
        self.r5.setCheckable(False)
        self.r5.setChecked(False)
        self.r5.setObjectName(_fromUtf8("r5"))
        self.r6 = QtGui.QPushButton(self.regBank)
        self.r6.setGeometry(QtCore.QRect(10, 240, 131, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        font.setPointSize(12)
        self.r6.setFont(font)
        self.r6.setText(_fromUtf8(""))
        self.r6.setCheckable(False)
        self.r6.setChecked(False)
        self.r6.setObjectName(_fromUtf8("r6"))
        self.r7 = QtGui.QPushButton(self.regBank)
        self.r7.setGeometry(QtCore.QRect(10, 280, 131, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        font.setPointSize(12)
        self.r7.setFont(font)
        self.r7.setText(_fromUtf8(""))
        self.r7.setCheckable(False)
        self.r7.setChecked(False)
        self.r7.setObjectName(_fromUtf8("r7"))
        self.r4 = QtGui.QPushButton(self.regBank)
        self.r4.setGeometry(QtCore.QRect(10, 160, 131, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        font.setPointSize(12)
        self.r4.setFont(font)
        self.r4.setText(_fromUtf8(""))
        self.r4.setCheckable(False)
        self.r4.setChecked(False)
        self.r4.setObjectName(_fromUtf8("r4"))
        self.flags = QtGui.QPushButton(self.regBank)
        self.flags.setGeometry(QtCore.QRect(10, 360, 131, 101))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        font.setPointSize(12)
        self.flags.setFont(font)
        self.flags.setText(_fromUtf8(""))
        self.flags.setCheckable(False)
        self.flags.setChecked(False)
        self.flags.setObjectName(_fromUtf8("flags"))
        self.pc = QtGui.QPushButton(self.regBank)
        self.pc.setGeometry(QtCore.QRect(10, 320, 131, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        font.setPointSize(12)
        self.pc.setFont(font)
        self.pc.setText(_fromUtf8(""))
        self.pc.setCheckable(False)
        self.pc.setChecked(False)
        self.pc.setObjectName(_fromUtf8("pc"))
        self.flagZ = QtGui.QCheckBox(self.regBank)
        self.flagZ.setEnabled(True)
        self.flagZ.setGeometry(QtCore.QRect(20, 420, 16, 19))
        self.flagZ.setText(_fromUtf8(""))
        self.flagZ.setCheckable(False)
        self.flagZ.setObjectName(_fromUtf8("flagZ"))
        self.flagE = QtGui.QCheckBox(self.regBank)
        self.flagE.setEnabled(True)
        self.flagE.setGeometry(QtCore.QRect(50, 420, 16, 19))
        self.flagE.setText(_fromUtf8(""))
        self.flagE.setCheckable(False)
        self.flagE.setObjectName(_fromUtf8("flagE"))
        self.flagG = QtGui.QCheckBox(self.regBank)
        self.flagG.setEnabled(True)
        self.flagG.setGeometry(QtCore.QRect(80, 420, 16, 19))
        self.flagG.setText(_fromUtf8(""))
        self.flagG.setCheckable(False)
        self.flagG.setObjectName(_fromUtf8("flagG"))
        self.flagL = QtGui.QCheckBox(self.regBank)
        self.flagL.setEnabled(True)
        self.flagL.setGeometry(QtCore.QRect(110, 420, 16, 19))
        self.flagL.setText(_fromUtf8(""))
        self.flagL.setCheckable(False)
        self.flagL.setObjectName(_fromUtf8("flagL"))
        self.step = QtGui.QPushButton(Form)
        self.step.setGeometry(QtCore.QRect(170, 470, 131, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        font.setPointSize(12)
        self.step.setFont(font)
        self.step.setObjectName(_fromUtf8("step"))
        self.instructioHolder = QtGui.QScrollArea(Form)
        self.instructioHolder.setGeometry(QtCore.QRect(170, 40, 131, 391))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        self.instructioHolder.setFont(font)
        self.instructioHolder.setWidgetResizable(True)
        self.instructioHolder.setObjectName(_fromUtf8("instructioHolder"))
        self.scrollAreaWidgetContents_2 = QtGui.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 127, 387))
        self.scrollAreaWidgetContents_2.setObjectName(_fromUtf8("scrollAreaWidgetContents_2"))
        self.instructions = QtGui.QTextEdit(self.scrollAreaWidgetContents_2)
        self.instructions.setGeometry(QtCore.QRect(0, 0, 131, 391))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        font.setPointSize(12)
        self.instructions.setFont(font)
        self.instructions.setReadOnly(False)
        self.instructions.setObjectName(_fromUtf8("instructions"))
        self.instructioHolder.setWidget(self.scrollAreaWidgetContents_2)
        self.memory = QtGui.QTableWidget(Form)
        self.memory.setGeometry(QtCore.QRect(310, 40, 221, 461))
        self.memory.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.memory.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.memory.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.memory.setObjectName(_fromUtf8("memory"))
        self.memory.setColumnCount(2)
        self.memory.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.memory.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.memory.setHorizontalHeaderItem(1, item)
        self.memory.horizontalHeader().setVisible(True)
        self.memory.verticalHeader().setVisible(True)
        self.run = QtGui.QPushButton(Form)
        self.run.setGeometry(QtCore.QRect(170, 440, 131, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        font.setPointSize(12)
        self.run.setFont(font)
        self.run.setObjectName(_fromUtf8("run"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.step.setText(QtGui.QApplication.translate("Form", "Step (F11)", None, QtGui.QApplication.UnicodeUTF8))
        item = self.memory.horizontalHeaderItem(0)
        item.setText(QtGui.QApplication.translate("Form", "Address", None, QtGui.QApplication.UnicodeUTF8))
        item = self.memory.horizontalHeaderItem(1)
        item.setText(QtGui.QApplication.translate("Form", "Data", None, QtGui.QApplication.UnicodeUTF8))
        self.run.setText(QtGui.QApplication.translate("Form", "Run (F5)", None, QtGui.QApplication.UnicodeUTF8))

