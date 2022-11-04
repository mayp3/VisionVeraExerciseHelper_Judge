import os
import glob
from clients import log

# todo: 定时任务启动
def clearScreenShots():
    logger = log.LoggingFactory.logger(__name__)
    fileNames =  glob.glob("./images/ScreenShots/*")
    i = 0
    for fileName in fileNames:
        print(fileName)
        i += 1
        try:
            os.remove(fileName)
        except:
            logger.error("clear file fail")
    logger.info("clear screenShots success||number = %s",str(i))