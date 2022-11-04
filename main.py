from clients import conf,log
import time
from utils import sysUtils
from server import photoSearcher,operator,photoRecognizer


# todo :通过控制器进行控制
class LifeCycleController:
    def __init__(self,conf):
        self.conf = conf
        self.logger = log.LoggingFactory(__name__)
        self.myOperator = operator.Operator(conf)


    def getInfoFromHomePage(self):
        results = self.myOperator.recognizeHomePage()


    def checkCurrentStat(self):
        pass


    def move(self,curState):
        pass



def main():
    Myconfig = conf.initConfig("./conf/conf.toml")
    log.LoggingFactory = log.InitLoggingFacotory(Myconfig["log"])

    myOperator = operator.Operator(Myconfig)
    myOperator.runOperation_panduan(-1)
    #sysUtils.clearScreenShots()


    



def testFunc():
    Myconfig = conf.initConfig("./conf/conf.toml")
    log.LoggingFactory = log.InitLoggingFacotory(Myconfig["log"])
    # myrecognizer = photoRecognizer.PhotoRecognizer(Myconfig["img"]["screenShotsPath"]+"homePage_WatingForWeakup.png")
    # myrecognizer.recognize()
    # myrecognizer
    result = photoSearcher.findPosition("./images/ScreenShots/1_19_0_17_24.png","./images/OperationIcon/friendFriendList.png")

    # window = windowManipulator.WindowManipulator(Myconfig["initWindowConfig"],Myconfig["img"]["screenShotsPath"])
    # window.nomolizeWindowSize()

if __name__ == "__main__":
    main()
    # testFunc()