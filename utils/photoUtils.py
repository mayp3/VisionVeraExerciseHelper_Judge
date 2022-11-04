import cv2
import numpy as np
from clients import log

class PhotoSearcher:
    def __init__(self,imgPath,targetPath):
        self.imgPath = imgPath
        self.targetPath = targetPath
        self.logger = log.LoggingFactory.logger(__name__)

    def search(self):
        img_rgb = cv2.imread(self.imgPath)
        img_target = cv2.imread(self.targetPath)
        w, h = img_target.shape[:-1]

        res = cv2.matchTemplate(img_rgb, img_target, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)

        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_rgb,pt,(pt[0]+h,pt[1]+w),(0,0,255),2)
            return pt[0]+h/2,pt[1]+w/2
        self.logger.info("Can't find target:%s",self.targetPath)
        return

    def searchSaveResult(self):
        img_rgb = cv2.imread(self.imgPath)
        img_target = cv2.imread(self.targetPath)
        w, h = img_target.shape[:-1]

        res = cv2.matchTemplate(img_rgb, img_target, cv2.TM_CCOEFF_NORMED)
        threshold = .8
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):  # Switch collumns and rows
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

        cv2.imwrite('result.png', img_rgb)
        return 0,0

def findPosition(imgPath,targetPath):
    mySearcher = PhotoSearcher(imgPath,targetPath)
    try:
        x,y = mySearcher.search()
        return x,y
    except:
        return -1,-1

