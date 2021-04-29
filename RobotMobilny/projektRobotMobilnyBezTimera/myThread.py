
from PyQt5 import QtCore

class threadConnect(QtCore.QRunnable):

    def __init__(self, model):
        super().__init__()
        self.model = model
        self.IP = self.model.getIP()
        self.PORT = 8000
        self.BUFFSIZE = 28 # dlugosc ramki w hex
        self.signals = threadSignals()
        self.working = self.model.isConnected()
        self.sending = self.model.isSending()
        self.manualSend = self.model.getManualSend()
        self.s = None




    @QtCore.pyqtSlot()
    def run(self):
        from PyQt5.QtTest import QTest
        # watek jest bezpieczny bo GIL umozliwia dzialanie tylko jednega w danej chwili
        import socket
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((self.IP, self.PORT))
            self.signals.connected.emit()
        except ConnectionError as e:
            self.model.setConnection(False)
            self.model.setIP(None)
            self.working = self.model.isConnected()
            self.signals.error.emit(e)

        while self.working:
            QTest.qWait(100)
            if self.sending or self.manualSend:
                self.exchange()
            self.manualSend = self.model.getManualSend()
            self.working = self.model.isConnected()
            self.sending = self.model.isSending()

        self.model.setConnection(False)
        self.model.setIP(None)
        self.s.close()

    def exchange(self):
        try:
            self.model.setLastFrameSend()
            frame = self.model.getLastFrameSend()
            self.s.sendall(frame.encode())
            res = self.s.recv(self.BUFFSIZE).decode()
            self.model.setFrameReceived(res[1:-1])
            self.signals.result.emit()
            #self.signals.result.emit(res) zmiana koncepcji na przekazywanie ramki w watku
            #przez przekazany model(cos ala shared memory), zamiast za pomoca sygnalow
        except ConnectionError as e:
            self.model.setConnection(False)
            self.model.setIP(None)
            self.signals.error.emit(e)
        except Exception as e:
            self.model.setConnection(False)
            self.model.setIP(None)
            self.signals.error.emit(e)



class threadSignals(QtCore.QObject):
    #result = QtCore.pyqtSignal(str) stary result
    result = QtCore.pyqtSignal()
    error = QtCore.pyqtSignal(object)
    connected = QtCore.pyqtSignal()
