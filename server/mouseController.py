import mouse

class MouseController:
    def __init__(self):
        self.m = mouse


    def clickButton(self,window):
        pass

    def draw(self,func):
        def warpFunc():
            self.hold()
            func()
            self.release()
        return warpFunc

    def moveToLeft(self,distance):
        self.draw(self.move(-distance,0))()

    def moveToRight(self,distance):
        self.draw(self.move(distance, 0))()

    def moveToUp(self,distance):
        self.draw(self.move(0, distance))()

    def moveToDown(self,distance):
        self.draw(self.move(0, -distance))()

    def move(self,x,y):
        self.m.move(x,y)

    def moveRelativeToWindow(self,x,y):
        pass

    def leftClick(self):
        self.m.click('left')

    def hold(self):
        self.m.press('left')

    def getPostion(self):
        return self.m.get_position()

    def release(self):
        self.m.release('left')


