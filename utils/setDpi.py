from win32 import win32api, win32gui, win32print
from win32.lib import win32con
from win32.win32api import GetSystemMetrics
import os
import time

def getRealResolution():
    """获取真实的分辨率"""
    hDC = win32gui.GetDC(0)
    # 横向分辨率
    w = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
    # 纵向分辨率
    h = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
    return w, h

def getScreenSize():
    """获取缩放后的分辨率"""
    w = GetSystemMetrics (0)
    h = GetSystemMetrics (1)
    return w, h

def getDpi():
    real_resolution = getRealResolution()
    screen_size = getScreenSize()

    screen_scale_rate = round(real_resolution[0] / screen_size[0], 2)
    screen_scale_rate = screen_scale_rate * 100
    return screen_scale_rate


def setDefaultDpi():
    print('xx程序运行前检测')
    userdpi = getDpi()
    print('当前系统缩放比例为:',userdpi,'%',end='')
    if userdpi == 100 :
        print(' 程序直接运行')
    else:
        print('正在调整为100%缩放率')
        location = os.getcwd() + '\SetDpi.exe'
        win32api.ShellExecute(0, 'open', location,' 100', '', 1)
        print('运行中 请等待')
        time.sleep(2)

def resetDpi(userDpi):
        print('xx程序运行完成 缩放自动调回初始')
        location = os.getcwd() + '\SetDpi.exe'
        resetDpi = " " + str(userDpi)
        win32api.ShellExecute(0, 'open', location, resetDpi, '', 1)