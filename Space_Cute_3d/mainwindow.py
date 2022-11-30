# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!
from _ast import Str

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtMultimedia import QSound

class Ui_MainWindow(object):
    def setupUi(self, MainWindow, glwindow):
        # Window's settings
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1366, 768)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setFixedSize(1366, 768)
        self.centralWidget.setObjectName("centralWidget")
        self.openGLWidget = glwindow(self.centralWidget)
        self.openGLWidget.setGeometry(QtCore.QRect(3, 0, 1200, 730))
        self.openGLWidget.setObjectName("openGLWidget")
        self.openGLWidget.setFocus()
        # Separator V 1
        self.line = QtWidgets.QFrame(self.centralWidget)
        self.line.setGeometry(QtCore.QRect(1213, 3, 20, 730))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        # Separator H 2
        self.line2 = QtWidgets.QFrame(self.centralWidget)
        self.line2.setGeometry(QtCore.QRect(1242, 10, 100, 730))
        self.line2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line2.setObjectName("line2")
        # Separator H 3
        self.line3 = QtWidgets.QFrame(self.centralWidget)
        self.line3.setGeometry(QtCore.QRect(1242, -94, 100, 730))
        self.line3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line3.setObjectName("line3")
        # Separator H 4
        self.line4 = QtWidgets.QFrame(self.centralWidget)
        self.line4.setGeometry(QtCore.QRect(1242, -190, 100, 730))
        self.line4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line4.setObjectName("line4")
        # Score counter
        self.score_line = QtWidgets.QLineEdit(self.centralWidget)
        self.score_line.setEnabled(True)
        self.score_line.setGeometry(QtCore.QRect(1240, 200, 110, 50))
        self.score_line.setReadOnly(True)
        self.score_line.setObjectName("score_line")
        # Record counter
        self.Record_line = QtWidgets.QLineEdit(self.centralWidget)
        self.Record_line.setEnabled(True)
        self.Record_line.setGeometry(QtCore.QRect(1240, 300, 110, 50))
        self.Record_line.setReadOnly(True)
        self.Record_line.setObjectName("Record_line")
        # Life counter
        self.Life_line = QtWidgets.QLineEdit(self.centralWidget)
        self.Life_line.setEnabled(True)
        self.Life_line.setGeometry(QtCore.QRect(1240, 400, 110, 50))
        self.Life_line.setReadOnly(True)
        self.Life_line.setObjectName("Life_line")
        # Button to start or reestart the game
        self.btn_Start = QtWidgets.QPushButton(self.centralWidget)
        self.btn_Start.setGeometry(QtCore.QRect(1240, 10, 110, 50))
        self.btn_Start.setObjectName("btn_Start")
        # Button to stop the game
        self.btn_Stop = QtWidgets.QPushButton(self.centralWidget)
        self.btn_Stop.setGeometry(QtCore.QRect(1240, 70, 110, 50))
        self.btn_Stop.setObjectName("btn_Stop")

        MainWindow.setCentralWidget(self.centralWidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        # Button functions
        self.btn_Start.clicked.connect(self.start_game)
        self.btn_Stop.clicked.connect(self.stop_game)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.score = 0
        self.record = 0
        self.vida = 3



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_Start.setText(_translate("MainWindow", "Start"))
        self.btn_Stop.setText(_translate("MainWindow", "Stop"))
        self.score_line.setWhatsThis(_translate("MainWindow",
                                                "<html><head/><body><p><span style=\" font-size:50pt; font-weight:900; font-style:italic;\">Score</span></p></body></html>"))
        self.score_line.setText(_translate("MainWindow", "Score: 0"))

        self.Record_line.setWhatsThis(_translate("MainWindow",
                                                 "<html><head/><body><p><span style=\" font-size:50pt; font-weight:900; font-style:italic;\">Score</span></p></body></html>"))
        self.Record_line.setText(_translate("MainWindow", "Record: 0"))

        self.Life_line.setWhatsThis(_translate("MainWindow",
                                                 "<html><head/><body><p><span style=\" font-size:50pt; font-weight:900; font-style:italic;\">Score</span></p></body></html>"))
        self.Life_line.setText(_translate("MainWindow", "Life: 3"))


    # Inicia o jogo
    def start_game(self):
        self.openGLWidget.reestart()
        self.score = 0
        self.vida = 3
        self.Shaplou = 3
        self.atualize()
        self.openGLWidget.started = True
        self.openGLWidget.setFocus()
        self.btn_Start.setText("Reestart")

    # Para o jogo
    def stop_game(self):
        self.openGLWidget.stop()
        self.btn_Start.setText("Start")
        self.check_record()
        self.score = 0
        self.atualize()

    # Ganha pontos
    def up_point(self, points):
        self.score += points
        self.check_record()
        self.atualize()

    # Perde pontos
    def down_point(self, points):
        self.score -= points
        self.atualize()

    # Perde vida
    def down_life(self):
        if self.vida <= 1:
            self.openGLWidget.dead()
        self.vida -= 1
        self.atualize()

    # Ganha vida
    def up_life(self):
        if self.vida < 3:
            self.vida += 1
            self.atualize()

    # Atualiza os campos
    def atualize(self):
        self.score_line.setText(f"Score: {str(self.score)}")
        self.Record_line.setText(f"Record: {str(self.record)}")
        self.Life_line.setText(f"Vida: {str(self.vida)}")

    #  Verifica se o record foi ultrapassado
    def check_record(self):
        if self.score > self.record:
            self.record = self.score
            self.atualize()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

