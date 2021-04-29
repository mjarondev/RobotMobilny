
#view?

import gui
from PyQt5 import QtWidgets, QtCore, QtGui


class MyMainWindow(gui.Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)

        self.spinBoxForwardBackward.setKeyboardTracking(False)
        self.spinBoxLeftRight.setKeyboardTracking(False)
        self.spinBoxLeftEngine.setKeyboardTracking(False)
        self.spinBoxRightEngine.setKeyboardTracking(False)


        self.labelStatus.setToolTip("0-Dane odczytano prawidlowo\n"
                                    "1-Brak znaku konczacego ramke przed znakiem rozpoczynajacym\n"
                                    "2-ramka zbyt dluga\n"
                                    "3-Brak znaku rozpoczynajacego ramke przed znakiem  konczacym\n"
                                    "4-Zla wielkosc ramki\n"
                                    "5-Blad dekodowania danych\n"
                                    "6-Blad polaczenia z robotem Pololu3Pi")






