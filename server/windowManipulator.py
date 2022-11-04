import time
from PIL import ImageGrab
from clients import log
import win32gui,win32console,win32con
import os


class WindowManipulator:
    def __init__(self,initWindowConfig,screenShotPath):
        self.logger = log.LoggingFactory.logger(__name__)
        self.conf = initWindowConfig
        self.screenShotPath = screenShotPath["screenShotsPath"]
        if self.gameIsStart():
            self.getGameWindow()
        #else:
        #    if self.emulatorIsStart():
        #        self.getEmulatorWindow()
        #    else:
        #        self.startEmulator()
        #        time.sleep(self.conf["emulatorStartTime"])
        #        self.getEmulatorWindow()
        self.nomolizeWindowSize()

    def gameIsStart(self):
        return win32gui.FindWindow(0, self.conf["emulatorGameName"]) != 0

    def emulatorIsStart(self):
        return win32gui.FindWindow(0, self.conf["emulatorName"]) != 0

    def getEmulatorWindow(self):
        self.handle = win32gui.FindWindow(0, self.conf["emulatorName"])
        if self.handle == 0:
            self.logger.info("Can't find screen... || try to start emulator")
            return False
        self.logger.info("getEmulatorWindow success...")
        return True

    def getGameWindow(self):
        self.handle = win32gui.FindWindow(0,self.conf["emulatorGameName"])
        if self.handle == 0:
            self.logger.info("Can't find Game Window... || try to start game")
            return False
        self.logger.info("getGameWindow success...")
        return True

    def startEmulator(self):
        #os.system(self.conf["emulatorPath"])
        #time.sleep(self.conf["emulatorStartTime"])
        self.logger.info("Start Emulator...")

    def setWindowForeground(self):
        win32gui.SetForegroundWindow(self.handle)

    def getWindowPos(self):
        x1, y1, x2, y2 = win32gui.GetWindowRect(self.handle)
        #self.logger.info("getWindowPos || Window's x1=%d, y1=%d, x2=%d, y2=%d", x1, y1, x2, y2)
        #若电脑分辨率缩放比例为150%，则x2、y2均*1.5；缩放比为100%则为x2、y2
        return x1, y1, x2, y2
        #return x1, y1, x2*1.5, y2*1.5

    def getWindowLeftUpCornerPos(self):
        x1, y1, x2, y2 = win32gui.GetWindowRect(self.handle)
        return x1, y1

    def screenShotForWindow(self):
        startTime = time.time()
        myTime = time.localtime(startTime)
        timeName = str(myTime.tm_mon) + "_" + str(myTime.tm_mday) + "_" + str(myTime.tm_hour) + "_" + str(
            myTime.tm_min) + "_" + str(myTime.tm_sec) + ".png"
        imgName = self.screenShotPath + timeName
        myImg = ImageGrab.grab(bbox=(self.getWindowPos()),all_screens=True)
        myImg.save(imgName)
        self.logger.info("image save succeed||path=%s||spendTime=%sSecond",imgName,time.time()-startTime)
        return imgName

    def nomolizeWindowSize(self):
        x,y = self.conf["startPos"][0], self.conf["startPos"][1]
        length,high = self.conf["size"][0], self.conf["size"][1]
        win32gui.SetWindowPos(self.handle,win32con.HWND_TOPMOST,x,y,length,high, win32con.SWP_SHOWWINDOW)
        time.sleep(2)
        return True

