
#controller
import sys
import view
import model
from myThread import threadConnect
from PyQt5 import QtWidgets, QtCore


class StartGUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = view.MyMainWindow()
        self.ui.setupUi(self)

        self.model = model.Connection()
        self.models = [self.model]
        self.threadpool = QtCore.QThreadPool()

        # 0 - auto, 1 - manual, 2 - frame
        self.currentTab = self.ui.tabWidget.currentIndex()

        self.ui.buttonConnect.clicked.connect(self.connectClicked)
        self.ui.buttonDisconnect.clicked.connect(self.disconnectClicked)
        self.ui.checkBoxLED1.stateChanged.connect(self.LED1)
        self.ui.checkBoxLED2.stateChanged.connect(self.LED2)
        self.ui.radioStart.toggled.connect(self.startSending)
        self.ui.radioStop.toggled.connect(self.stopSending)
        self.ui.radioManual.toggled.connect(self.manualSending)
        self.ui.sliderLeftEngine.valueChanged.connect(self.leftSliderChanged)
        self.ui.sliderRightEngine.valueChanged.connect(self.rightSliderChanged)
        self.ui.spinBoxLeftEngine.valueChanged.connect(self.leftSpinBoxChanged)
        self.ui.spinBoxRightEngine.valueChanged.connect(self.rightSpinBoxChanged)
        self.ui.sliderForwardBackward.valueChanged.connect(self.autoSliderChanged)
        self.ui.sliderLeftRight.valueChanged.connect(self.autoSliderChanged)
        self.ui.spinBoxForwardBackward.valueChanged.connect(self.autoSpinBoxChanged)
        self.ui.spinBoxLeftRight.valueChanged.connect(self.autoSpinBoxChanged)
        self.ui.tabWidget.currentChanged.connect(self.updateTab)
        self.ui.buttonResetLeft.clicked.connect(self.resetLeftClicked)
        self.ui.buttonResetRight.clicked.connect(self.resetRightClicked)
        self.ui.buttonResetForwardBackward.clicked.connect(self.resetForwardClicked)
        self.ui.buttonResetLeftRight.clicked.connect(self.resetSidesClicked)
        self.ui.buttonSaveFrame.clicked.connect(self.saveManualFrame)
        self.ui.textManualFrame.returnPressed.connect(self.saveManualFrame)
        self.ui.comboRoboty.activated.connect(self.chooseRobot)
        self.ui.buttonManualSend.clicked.connect(self.manualSend)
        self.ui.buttonDeleteRobot.clicked.connect(self.removeRobot)
        self.ui.txtIPaddress.returnPressed.connect(self.connectClicked)



        self.updateData()
        self.updateOnExchange()



    def removeRobot(self):
        if len(self.ui.comboRoboty) > 2 and self.ui.comboRoboty.currentText() != "<nowy>":
            index = self.ui.comboRoboty.currentIndex()
            self.model.setConnection(False)
            self.ui.comboRoboty.removeItem(index)
            self.models.remove(self.model)
            if self.ui.comboRoboty.itemText(index) != "<nowy>":
                self.model = self.models[index]
            else:
                self.ui.comboRoboty.setCurrentIndex(0)
                self.model = self.models[0]


            for i in range(len(self.ui.comboRoboty)-1):
                self.ui.comboRoboty.setItemText(i, "robot" + str(i+1))

        self.updateOnExchange()
        self.updateSidesSlider()
        self.updateData()



    def chooseRobot(self, index):


        if self.ui.comboRoboty.itemText(index) == "<nowy>":
            self.ui.comboRoboty.setItemText(index, "robot"+str(index+1))
            self.ui.comboRoboty.addItem("<nowy>")
            self.models.append(model.Connection())
            self.model = self.models[index]
            self.ui.radioStop.toggle()

        else:
            self.model = self.models[index]
            if self.model.isSending():
                self.ui.radioStart.toggle()
            elif self.model.isManualSending():
                self.ui.radioManual.toggle()
            else:
                self.ui.radioStop.toggle()

        if (self.model.getLED() & 1) == 1:
            self.ui.checkBoxLED1.setChecked(True)
        else:
            self.ui.checkBoxLED1.setChecked(False)
        if (self.model.getLED() & 2) == 2:
            self.ui.checkBoxLED2.setChecked(True)
        else:
            self.ui.checkBoxLED2.setChecked(False)

        self.updateData()
        self.updateSidesSlider()
        self.updateOnExchange()


    def saveManualFrame(self):

        self.ui.labelManualFrame.setText("")
        frame = self.ui.textManualFrame.text()
        self.ui.checkBoxLED1.setChecked(False)
        self.ui.checkBoxLED2.setChecked(False)
        if len(frame) != 6:
            self.ui.labelManualFrame.setText("Błąd!\nZa krótka ramka.")
        else:
            led = frame[:2]
            le = frame[2:4]
            re = frame[4:]
            try:
                ledint = int(led, 16)
                leint = int(le, 16)
                reint = int(re, 16)
                if ledint > 3:
                    raise ValueError
                self.model.setEngine("Left", leint)
                self.model.setEngine("Right", reint)
                if ledint == 0:
                    self.model.setLED(1, False)
                    self.model.setLED(2, False)
                elif ledint == 1:
                    self.model.setLED(1, True)
                    self.model.setLED(2, False)
                elif ledint == 2:
                    self.model.setLED(1, False)
                    self.model.setLED(2, True)
                elif ledint == 3:
                    self.model.setLED(1, True)
                    self.model.setLED(2, True)

            except ValueError:
                self.ui.labelManualFrame.setText("Błąd!\nNieprawidłowe dane w ramce.")
            finally:
                self.updateData()

    def manualSending(self):
        self.model.setManualSending(True)
        self.model.setSending(False)

    def manualSend(self):
        self.connectionUpdate()
        if self.model.isManualSending():
            self.model.setManualSend()

    def resetForwardClicked(self):
        le = self.model.getEngine("Left")
        re = self.model.getEngine("Right")
        if (le>0 and re<0) or (le<0 and re>0):
            self.updateData()
            self.updateSidesSlider()
        else:
            self.model.setEngine("Left", 0)
            self.model.setEngine("Right", 0)
            self.updateData()

    def resetSidesClicked(self):
        le = self.model.getEngine("Left")
        re = self.model.getEngine("Right")
        if (le>0 and re<0) or (le<0 and re>0):
            self.model.setEngine("Left", 0)
            self.model.setEngine("Right", 0)
        else:
            if abs(re) > abs(le):
                self.model.setEngine("Left", re)
            else:
                self.model.setEngine("Right", le)
        self.updateData()
        self.updateSidesSlider()
    def resetLeftClicked(self):
        self.model.setEngine("Left", 0)
        self.updateData()
    def resetRightClicked(self):
        self.model.setEngine("Right", 0)
        self.updateData()

    def updateSidesSlider(self):
        le = int(self.model.getEngine("Left"))
        re = int(self.model.getEngine("Right"))

        if (le>0 and re<0) or (le<0 and re>0):
            sides = round((le-re)/2/1.27)
        else:
            if le != re:
                sides = round((le - re) / (le + re) * 100)
            else:
                sides = 0

        if sides > 100:
            sides = 100
        if sides < -100:
            sides = -100

        self.ui.sliderLeftRight.blockSignals(True)
        self.ui.spinBoxLeftRight.blockSignals(True)
        self.ui.sliderLeftRight.setValue(sides)
        self.ui.spinBoxLeftRight.setValue(sides)
        self.ui.sliderLeftRight.blockSignals(False)
        self.ui.spinBoxLeftRight.blockSignals(False)

    def updateTab(self, num):
        self.currentTab = num
        if num == 0:

            self.ui.checkBoxLED1.setVisible(True)
            self.ui.checkBoxLED2.setVisible(True)
            self.updateSidesSlider()
            self.updateData()

        elif num == 1:

            self.ui.checkBoxLED1.setVisible(True)
            self.ui.checkBoxLED2.setVisible(True)
            self.updateData()
        elif num == 2:

            self.ui.checkBoxLED1.setVisible(False)
            self.ui.checkBoxLED2.setVisible(False)


    def updateData(self):
        self.connectionUpdate()


        le = int(self.model.getEngine("Left"))
        re = int(self.model.getEngine("Right"))

        if self.currentTab == 0:

            if (le>0 and re<0) or (le<0 and re>0):
                forward = 0
            else:
                if abs(le) >= abs(re):
                    forward = round(le / 1.27)
                else:
                    forward = round(re / 1.27)

            if forward > 100:
                forward = 100
            if forward < -100:
                forward = -100

            self.ui.sliderForwardBackward.blockSignals(True)
            self.ui.spinBoxForwardBackward.blockSignals(True)

            self.ui.sliderForwardBackward.setValue(forward)
            self.ui.spinBoxForwardBackward.setValue(forward)

            self.ui.sliderForwardBackward.blockSignals(False)
            self.ui.spinBoxForwardBackward.blockSignals(False)

        elif self.currentTab == 1:

            self.ui.spinBoxLeftEngine.blockSignals(True)
            self.ui.spinBoxRightEngine.blockSignals(True)
            self.ui.sliderLeftEngine.blockSignals(True)
            self.ui.sliderRightEngine.blockSignals(True)

            self.ui.spinBoxLeftEngine.setValue(le)
            self.ui.sliderLeftEngine.setValue(le)
            self.ui.spinBoxRightEngine.setValue(re)
            self.ui.sliderRightEngine.setValue(re)

            self.ui.spinBoxLeftEngine.blockSignals(False)
            self.ui.spinBoxRightEngine.blockSignals(False)
            self.ui.sliderLeftEngine.blockSignals(False)
            self.ui.sliderRightEngine.blockSignals(False)

        elif self.currentTab == 2:
            pass

        self.ui.labelFrameSend.setText(self.model.getFrameSend())
        self.ui.labelFrameReceived.setText(self.model.getFrameReceived())
        self.ui.labelIP.setText(self.model.getIP())


    def autoSpinBoxChanged(self):
        sides = self.ui.spinBoxLeftRight.value()
        forward = self.ui.spinBoxForwardBackward.value()

        right = forward * 1.27
        left = forward * 1.27

        if forward >= 0 and sides >= 0:
            right = right - right * sides * 0.01
        elif forward >= 0 and sides < 0:
            left = left + left * sides * 0.01
        elif forward < 0 and sides >= 0:
            left = left - left * sides * 0.01
        elif forward < 0 and sides < 0:
            right = right + right * sides * 0.01

        self.model.setEngine("Left", left)
        self.model.setEngine("Right", right)
        self.ui.sliderLeftRight.blockSignals(True)
        self.ui.sliderLeftRight.setValue(sides)
        self.ui.sliderLeftRight.blockSignals(False)

        self.updateData()


    def autoSliderChanged(self):
        sides = self.ui.sliderLeftRight.value()
        forward = self.ui.sliderForwardBackward.value()

        if forward != 0:
            right = forward*1.27
            left = forward*1.27

            if forward >= 0 and sides >= 0:
                right = right - right*sides*0.01
            elif forward >= 0 and sides < 0:
                left = left + left*sides*0.01
            elif forward < 0 and sides >= 0:
                left = left - left*sides*0.01
            elif forward < 0 and sides < 0:
                right = right + right*sides*0.01
        else:
            left = sides*1.27
            right = -sides*1.27

        self.model.setEngine("Left", left)
        self.model.setEngine("Right", right)
        self.ui.spinBoxLeftRight.blockSignals(True)
        self.ui.spinBoxLeftRight.setValue(sides)
        self.ui.spinBoxLeftRight.blockSignals(False)

        self.updateData()


    def leftSpinBoxChanged(self):
        self.model.setEngine("Left", self.ui.spinBoxLeftEngine.value())
        self.updateData()

    def rightSpinBoxChanged(self):
        self.model.setEngine("Right", self.ui.spinBoxRightEngine.value())
        self.updateData()

    def leftSliderChanged(self):
        self.model.setEngine("Left", self.ui.sliderLeftEngine.value())
        self.updateData()

    def rightSliderChanged(self):
        self.model.setEngine("Right", self.ui.sliderRightEngine.value())
        self.updateData()


    def startSending(self):
        self.model.setSending(True)
        self.model.setManualSending(False)

    def stopSending(self):
        self.model.setSending(False)
        self.model.setManualSending(False)



    def LED1(self):
        self.model.setLED(1, self.ui.checkBoxLED1.isChecked())
        self.updateData()

    def LED2(self):
        self.model.setLED(2, self.ui.checkBoxLED2.isChecked())
        self.updateData()

    def disconnectClicked(self):
        if self.model.isConnected():
            self.ui.labelConnect.setText("Disconnecting")
            self.model.setConnection(False)
            self.ui.labelConnect.setText("Disconnected")
        self.updateData()

    def showMsgWindowError(self, s):
        self.ui.labelConnect.setText("Not connected")
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText(self.ui.comboRoboty.currentText() + "\n" + str(s))
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.exec_()
        self.updateData()
        self.updateOnExchange()

    def connectClicked(self):

        if not self.model.isConnected():

            self.ui.labelConnect.setText("Connecting")

            self.model.setIP(self.ui.txtIPaddress.text())
            self.model.setConnection(True)

            self.thread = threadConnect(self.model)
            self.thread.signals.result.connect(self.updateOnExchange)
            self.thread.signals.error.connect(self.showMsgWindowError)
            self.thread.signals.connected.connect(self.connectionUpdate)
            self.threadpool.start(self.thread)
        self.updateData()


    def connectionUpdate(self):
        if self.model.isConnected():
            self.ui.labelConnect.setText("Connected")
        else:
            self.ui.labelConnect.setText("Not connected")

    def updateOnExchange(self):

        self.connectionUpdate()

        b = self.model.getBattery()
        self.ui.progressBarBateria.setValue(int(b/48))
        self.ui.labelBateria.setText(str(b) + "mV")
        self.ui.labelStatus.setText(str(self.model.getStatus()))

        sensors = self.model.getSensors()
        self.ui.progressBarCzujnik1.setValue(sensors[0])
        self.ui.labelCzujnik1.setText(str(sensors[0]))
        self.ui.labelCzujnik1Procent.setText(str(int(sensors[0]/20)) + "%")
        self.ui.progressBarCzujnik2.setValue(sensors[1])
        self.ui.labelCzujnik2.setText(str(sensors[1]))
        self.ui.labelCzujnik2Procent.setText(str(int(sensors[1]/20)) + "%")
        self.ui.progressBarCzujnik3.setValue(sensors[2])
        self.ui.labelCzujnik3.setText(str(sensors[2]))
        self.ui.labelCzujnik3Procent.setText(str(int(sensors[2]/20)) + "%")
        self.ui.progressBarCzujnik4.setValue(sensors[3])
        self.ui.labelCzujnik4.setText(str(sensors[3]))
        self.ui.labelCzujnik4Procent.setText(str(int(sensors[3]/20)) + "%")
        self.ui.progressBarCzujnik5.setValue(sensors[4])
        self.ui.labelCzujnik5.setText(str(sensors[4]))
        self.ui.labelCzujnik5Procent.setText(str(int(sensors[4]/20)) + "%")

        self.ui.labelLastFrameSend.setText(self.model.getLastFrameSend())

        self.updateData()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = StartGUI()
    myapp.show()
    sys.exit(app.exec_())
