
#model
from PyQt5 import QtCore, QtGui, QtWidgets

import numpy as np

class Connection():
    def __init__(self):
        self.IP = None
        # 1 bajt-ledy, 2 bajt-lewy silnik, 3 bajt-prawy silnik -- dlugosc w hex 6
        self.frameSend = [np.uint8(0), np.int8(0), np.int8(0)]
        self.lastFrameSend = [np.uint8(0), np.int8(0), np.int8(0)]
        # 1 bajt-status, 2,3 bajt-bateria,
        #  4,5 bajt-czujnik1, 6,7 bajt-czujnik2, 8,9 bajt-czujnik3, 10,11 bajt-czujnik4, 12,13 bajt-czujnik5
        # 1 bajt - uint8, 2 bajty - uint16 -- dlugosc w hex 26
        self.frameReceived = [np.uint8(0), np.uint16(0), np.uint16(0), np.uint16(0), np.uint16(0), np.uint16(0), np.uint16(0)]
        self.connected = False
        self.sending = False
        self.manualSending = False
        self.manualSend = False

    def checkManualSend(self):
        return self.manualSend

    def getManualSend(self):
        if self.manualSend:
            self.manualSend = False
            return True
        else:
            return False

    def setManualSend(self):
        self.manualSend = True

    def getStatus(self):
        return self.frameReceived[0]

    def getBattery(self):
        return self.frameReceived[1]

    def getSensors(self):
        return self.frameReceived[2:]



    def setFrameReceived(self, frame):
        self.frameReceived[0] = int(frame[:2], 16)

        # battery 0-4800(mV)?
        battery = frame[4:6] + frame[2:4]
        battery = np.uint16(int(battery, 16))
        self.frameReceived[1] = battery

        # sensors 0-2000
        s1 = frame[8:10] + frame[6:8]
        s2 = frame[12:14] + frame[10:12]
        s3 = frame[16:18] + frame[14:16]
        s4 = frame[20:22] + frame[18:20]
        s5 = frame[24:26] + frame[22:24]
        s1 = int(s1, 16)
        s2 = int(s2, 16)
        s3 = int(s3, 16)
        s4 = int(s4, 16)
        s5 = int(s5, 16)
        self.frameReceived[2] = np.uint16(s1)
        self.frameReceived[3] = np.uint16(s2)
        self.frameReceived[4] = np.uint16(s3)
        self.frameReceived[5] = np.uint16(s4)
        self.frameReceived[6] = np.uint16(s5)


    def getLastFrameSend(self):
        f = self.lastFrameSend
        return "[%02x%02x%02x]" % (f[0] & 0xff, f[1] & 0xff, f[2] & 0xff)

    def setLastFrameSend(self):
        self.lastFrameSend = self.frameSend

    def getFrameSend(self):
        f = self.frameSend
        return "[%02x%02x%02x]" % (f[0] & 0xff, f[1] & 0xff, f[2] & 0xff)

    def getFrameReceived(self):
        f = self.frameReceived
        ret = "[%02x%04x%04x%04x%04x%04x%04x]" % tuple(f)
        for i in [3, 7, 11, 15, 19, 23]:
            ret = ret[:i] + ret[i+2:i+4] + ret[i:i+2] + ret[i+4:]
        return ret


    def setEngine(self, role, value):
        if role == "Left":
            self.frameSend[1] = np.int8(value)
        elif role == "Right":
            self.frameSend[2] = np.int8(value)

    def getEngine(self, role):
        if role == "Left":
            return self.frameSend[1]
        elif role == "Right":
            return self.frameSend[2]


    def setLED(self, number, on):
        if number == 1:
            if on:
                self.frameSend[0] |= 1
            else:
                self.frameSend[0] &= 254
        elif number == 2:
            if on:
                self.frameSend[0] |= 2
            else:
                self.frameSend[0] &= 253

    def getLED(self):
        return self.frameSend[0]


    def isConnected(self):
        if self.connected:
            return True
        else:
            return False

    def isSending(self):
        if self.sending:
            return True
        else:
            return False

    def isManualSending(self):
        return self.manualSending

    def setConnection(self, connect):
        self.connected = bool(connect)

    def setSending(self, send):
        self.sending = bool(send)

    def setManualSending(self, man):
        self.manualSending = bool(man)


    def getIP(self):
        return self.IP

    def setIP(self, IP):
        self.IP = IP














