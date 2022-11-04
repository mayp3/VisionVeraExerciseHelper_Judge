from clients import conf,log
from server import mouseController,windowManipulator,photoRecognizer,photoSearcher
import time
from functools import wraps
import datetime
import os



class Operator:
    def __init__(self,myConfig):
        self.conf = myConfig
        self.logger = log.LoggingFactory.logger(__name__)
        self.buttons = myConfig["buttons"]
        self.publicpath = self.conf["initWindowConfig"]["publicpath"]
        self.iconpath = self.publicpath + self.conf["initWindowConfig"]["dpi"] + "/"
        self.mouse = mouseController.MouseController()
        self.window = windowManipulator.WindowManipulator(self.conf["initWindowConfig"],self.conf["img"])
        self.recognizer = photoRecognizer.PhotoRecognizer()
        self.workingQueue = []
        self.newestPhotoPath = ""
        self.weekTaskElimination = 1<<10
        self.takeDrug = int(myConfig["initWindowConfig"]["takeDrag"])

        if not self.window.gameIsStart():
            self.startGame()
        self.logger.info("Operator __init__ finally")

    #wating:time to sleep before press button
    #delay:time to sleep after press button
    def __clickButton(self,buttonIcon,xOffset=0,yOffset=0,waiting=0,delay=0):
        buttonIconPath = self.iconpath + self.buttons[buttonIcon]
        self.logger.info("current Operate:%s",buttonIcon)
        self.newestPhotoPath = self.window.screenShotForWindow()
        moveX, moveY = photoSearcher.findPosition(self.newestPhotoPath, buttonIconPath)

        x1, y1 = self.window.getWindowLeftUpCornerPos()
        #self.logger.info("__clickButton || moveX=%d moveY=%d", moveX, moveY)
        #self.logger.info("__clickButton || x1=%d y1=%d", x1, y1)

        if moveX == -1 and moveY == -1:
            self.logger.info("Can't find button:%s",buttonIcon)
            return False

        time.sleep(waiting)

        localPos = self.mouse.getPostion()
        self.mouse.move(x1 + moveX + xOffset, y1 + moveY + yOffset)
        self.mouse.leftClick()
        self.mouse.move(localPos[0],localPos[1])
        self.mouse.leftClick()
        os.remove(self.newestPhotoPath) #delete screenshot
        time.sleep(delay)
        return True

    # delay:time to sleep after press button
    def __clickMiddleOfWindow(self,delay=0):
        x1,y1,x2,y2 = self.window.getWindowPos()
        self.mouse.move((x1+x2)/2,(y1+y2)/2)
        self.mouse.leftClick()
        time.sleep(delay)
        return True

    def __clickMiddleDownOfWindow(self,delay=0):
        x1, y1, x2, y2 = self.window.getWindowPos()
        self.mouse.move((x1 + x2) / 2, (y1 + y2) * 2 / 3)
        self.mouse.leftClick()
        time.sleep(delay)
        return True

    def startGame(self):
        #self.tryToClickButton("arkNightsApp",delay=self.conf["time"]["gameStartTime"])
        self.window.getGameWindow()
        self.window.nomolizeWindowSize()
        time.sleep(self.conf["time"]["gameWatingTime"])
        self.__clickMiddleOfWindow()
        #self.tryToClickButton("homePage_WatingForWeakup",delay=10)
        #self.tryToClickButton("closePost",skip=True)


    def checkState(self,buttonIcon):
        pass

    # skip:失败一次过后直接跳过
    def tryToClickButton(self,buttonIcon,xOffset=0,yOffset=0,waiting=0,delay=1,timeOut=300,skip=False,retryGap=0):
        result = False
        startTime = time.time()
        while result != True:
            result = self.__clickButton(buttonIcon,xOffset,yOffset,waiting,delay)
            if time.time() - startTime > timeOut:
                self.logger.error("click button timeout!!! %s",buttonIcon)
                return False
            if skip == True:
                self.logger.info("click button skip!!! %s",buttonIcon)
                return result
            time.sleep(retryGap)
        return True


    def runOperation(self,round=10):
        if round == -1:
            round = 100000
            self.logger.info("runOperation round = %d",round)

        for i in range(round):
            self.tryToClickButton("startOperation")
            if self.takeDrug and self.tryToClickButton("takeFuckingDrug",delay=5,skip=True):
                self.tryToClickButton("startOperation")


            self.tryToClickButton("startOperationInOperatorView")
            self.tryToClickButton("operationEnd",waiting=5,delay=5,retryGap=10)

    #刷判断题
    def runOperation_panduan(self,round=10):
        if round == -1:
            round = 2000
            #round = 100000

        self.logger.info("runOperation_panduan || initWindowConfig.flag = %s", self.conf["initWindowConfig"]["flag"])

        #刷收藏夹中的判断题（选择"正确"选项）
        if self.conf["initWindowConfig"]["flag"] == "True":
            for i in range(round):
                #if self.takeDrug and self.tryToClickButton("takeFuckingDrug",delay=5,skip=True):
                #    self.tryToClickButton("startOperation"
                #self.logger.info("process deal before: %d", datetime.datetime.now().microsecond)
                self.tryToClickButton("correctOption", 
                                      waiting=self.conf["time"]["ocrDelayTime"], 
                                      delay=self.conf["time"]["clickDelayTime"], 
                                      retryGap=self.conf["time"]["retryGapTime"])
                self.tryToClickButton("commitAnswer", 
                                      waiting=self.conf["time"]["ocrDelayTime"], 
                                      delay=self.conf["time"]["clickDelayTime"], 
                                      retryGap=self.conf["time"]["retryGapTime"])
                self.tryToClickButton("nextQuestion", 
                                      waiting=self.conf["time"]["ocrDelayTime"], 
                                      delay=self.conf["time"]["clickDelayTime"], 
                                      retryGap=self.conf["time"]["retryGapTime"])
                #self.logger.info("process deal after: %d", datetime.datetime.now().microsecond)

                #self.tryToClickButton("nextQuestion",waiting=5,delay=5,retryGap=10)

        #刷错题集中的判断题（选择"错误"选项）
        elif self.conf["initWindowConfig"]["flag"] == "False":
            for i in range(round):
                #if self.takeDrug and self.tryToClickButton("takeFuckingDrug",delay=5,skip=True):
                #    self.tryToClickButton("startOperation"
                self.tryToClickButton("errorOption", 
                                      waiting=self.conf["time"]["ocrDelayTime"], 
                                      delay=self.conf["time"]["clickDelayTime"], 
                                      retryGap=self.conf["time"]["retryGapTime"])
                self.tryToClickButton("commitAnswer", 
                                      waiting=self.conf["time"]["ocrDelayTime"], 
                                      delay=self.conf["time"]["clickDelayTime"], 
                                      retryGap=self.conf["time"]["retryGapTime"])
                self.tryToClickButton("nextQuestion", 
                                      waiting=self.conf["time"]["ocrDelayTime"], 
                                      delay=self.conf["time"]["clickDelayTime"], 
                                      retryGap=self.conf["time"]["retryGapTime"])

                #self.tryToClickButton("nextQuestion",waiting=5,delay=5,retryGap=10)
                
        else:
            self.logger.info("Can't set conf.toml's flag... || flag = %s", self.conf["flag"])

    #collection items from base
    #基建收菜
    def collectBase(self):
        self.tryToClickButton("base",skip=True)
        self.tryToClickButton("baseRing",waiting=5)
        for i in range(3):
            self.tryToClickButton("baseTodoList",xOffset=100,skip=True)
        self.navigateToHome()

    #daily task collection
    #任务收菜
    def collectTaskItem(self):
        self.tryToClickButton("task",skip=True)
        self.tryToClickButton("taskCollectAll",skip=True)
        self.__clickMiddleDownOfWindow()
        self.navigateToHome()

    #信用点数全流程
    def creditOperation(self):
        self.collectFrientPoints()
        self.navigateToHome()
        self.buyByCridit()
        self.navigateToHome()

    # 收集信用点数
    def collectFrientPoints(self):
        self.tryToClickButton("friendPage")
        self.tryToClickButton("friendList")
        self.tryToClickButton("visitFriend")
        for i in range(15):
            self.tryToClickButton("visitFriendNext",skip=True)


    #返回主界面
    def navigateToHome(self):
        self.tryToClickButton("navigate",delay=5)
        self.tryToClickButton("navigateHome")

    #消费信用点数
    def buyByCridit(self):
        self.tryToClickButton("store")
        self.tryToClickButton("storeCredit")
        self.tryToClickButton("collectStoreCredit",skip=True)
        self.__clickMiddleDownOfWindow()
        for i in range(10):
            self.tryToClickButton("storeCreditItem",delay=3,skip=True)
            self.tryToClickButton("storeCreditItemBuy",delay=3,skip=True)
            self.__clickMiddleDownOfWindow()

    # 识别桌面
    def recognizeHomePage(self):
        self.logger.info("recognizeHomePage")
        newestPhotoPath = self.window.screenShotForWindow()
        results = self.recognizer.recognize(newestPhotoPath)
        for r in results:
            print(r)
        return results

    def routeToLastTask(self):
        self.tryToClickButton("terminal", waiting=3)
        newestPhotoPath = self.window.screenShotForWindow()
        results = self.recognizer.recognize(newestPhotoPath)
        for i in results:
            print(i)

    #执行每周剿灭任务全流程
    def runWeekTasks_elimination(self):
        self.gotoEliminatePage()
        self.eliminateOperation()
        self.navigateToHome()

    #执行任务
    def eliminateOperation(self):
        self.recognizeWeekTasks_eliminate()
        self.logger.info("eliminateOperation||gap = %d",self.weekTaskElimination)
        while self.weekTaskElimination != 0:
            self.tryToClickButton("startOperation")
            self.tryToClickButton("startOperationInOperatorView")
            self.tryToClickButton("eliminateFinish",timeOut=800, waiting=10, delay=10,retryGap=10)
            self.tryToClickButton("operationEnd",waiting=10, delay=10)
            self.recognizeWeekTasks_eliminate()

    #进入剿灭界面
    def gotoEliminatePage(self):
        self.logger.info("gotoEliminatePage")
        self.tryToClickButton("terminal",waiting=3)
        self.tryToClickButton("eliminateOperation")

    #识别当前是否已经完成本周任务
    def recognizeWeekTasks_eliminate(self):
        newestPhotoPath = self.window.screenShotForWindow()
        results = self.recognizer.recognize(newestPhotoPath)

        result = [i[-2] for i in results if "1800" in i[1]][0]
        total = int(result[len(result)-4:])
        current = int(result[:len(result)-5])
        # print(result,total,current)

        # result = [int(i) for i in [results[i+1][-2] for i in range(len(results)) if results[i][-2] == "每周报酬合成玉"][0].split("/")]
        self.weekTaskElimination = total - current
        self.logger.info("recognizeOperationPage||result = %d",self.weekTaskElimination)

