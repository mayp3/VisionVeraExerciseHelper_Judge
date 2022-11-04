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
        #self.logger.info("search || w=%d h=%d",w,h)
    
        res = cv2.matchTemplate(img_rgb, img_target, cv2.TM_CCOEFF_NORMED)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)

        #print("-----------------")
        #print(minVal,maxVal,minLoc,maxLoc)
        #print("#################")
    
        top_left = maxLoc
        #print(top_left)
        bottom_right = (top_left[0] + w, top_left[1] + h)
        #print('bottom_right =', bottom_right)

        cv2.rectangle(img_rgb, top_left, bottom_right, (0,0,255), 2)
        #cv2.imwrite("img_rgb.png", img_rgb)#将画过矩形框的图片保存到当前文件夹
        #cv2.imwrite("img_target.png", img_target)#将画过矩形框的图片保存到当前文件夹
        #print("&&&&&&&&&&&&&&&&")
        return top_left[0] + h/2, top_left[1] + w/2

        #threshold = 0.8
        threshold = 0.58
        #loc = np.where(res >= threshold)
        #for pt in zip(*loc[::-1]):
        #    draw = cv2.rectangle(img_rgb, pt, (pt[0]+h, pt[1]+w), (0,0,255), 2)
        #    cv2.imwrite("test_result.jpg", draw)#将画过矩形框的图片保存到当前文件夹
        #    cv2.imwrite("img_rgb.jpg", img_rgb)#将画过矩形框的图片保存到当前文件夹
        #    cv2.imwrite("img_target.jpg", img_target)#将画过矩形框的图片保存到当前文件夹
        #    self.logger.info("&&&&&&&&&&&&&&&&")
        #    return pt[0]+h/2,pt[1]+w/2

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

