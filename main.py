import pygame
import sys

pygame.init()
pygame.joystick.init()

joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for i in range(pygame.joystick.get_count()):
    print (joysticks[i])


clock = pygame.time.Clock()

tile = []
tile.append(pygame.image.load_basic("Sprites\Blank.bmp"))
tile.append(pygame.image.load_basic("Sprites\Wall.bmp"))
tile.append(pygame.image.load_basic("Sprites\DudemanRight.bmp"))
tile.append(pygame.image.load_basic("Sprites\DudemanLeft.bmp"))
tile.append(pygame.image.load_basic("Sprites\Block.bmp"))
tile.append(pygame.image.load_basic("Sprites\Door.bmp"))

def drawTile(s, t, x, y):
    s.blit(tile[t],(int(x)*8, int(y)*8))

screen = pygame.display.set_mode((29*8*10,19*8*10))
gameDisplay = pygame.Surface((29*8, 19*8))
background  = pygame.Surface((29*8, 19*8))

class Controller:
    def __init__(self):
        #self.A = 0      # 0
        #self.B = 0      # 1
        #self.X = 0      # 2
        #self.Y = 0      # 3
        #self.lb = 0     # 4 
        #self.rb = 0     # 5
        #self.select = 0 # 6
        #self.start = 0  # 7
        #self.ls = 0     # 8
        #self.rs = 0     # 9
        self.Home = 0    # 10
        self.Dr = 0      # 11
        self.Du = 0      # 12
        self.Dl = 0      # 13
        self.Dd = 0      # 14
        #self.ljX = 0
        #self.ljY = 0
        #self.rjX = 0
        #self.rjY = 0
        #self.lt = 0
        #self.rt = 0
        self.button = [0 for i in range(11)]
        self.axis   = [0 for i in range( 6)]
        
        self.leftLowTick = 0
        self.leftHighTick = 0 # timers for auto repeat
        
    def checkButt(self, button, value):
        self.button[button] = value
        if (value):
            eventQueue.append(["buttonDown", button])
        else:
            eventQueue.append(["buttonUp", button])
    def checkAxis(self, axis, value):
        if self.axis[axis] < 0.75 and value >= 0.75:
            eventQueue.append(["axisHigh", axis])
        if self.axis[axis] > -0.75 and value <= -0.75:
            eventQueue.append(["axisLow", axis])
        if (self.axis[axis] >= 0.75 and value < 0.75) or (self.axis[axis] <= -0.75 and value > -0.75):
            eventQueue.append(["axisNeutral", axis])
        self.axis[axis] = value
        if abs(value) < .1: # deadzone
            self.axis[axis] = 0
    def checkHat(self, x, y):
        if self.Dl == 1 and x >= 0:
            self.Dl = 0
            eventQueue.append(["buttonUp", 13])
        if self.Dl >= 0 and x < 0:
            self.Dl = 1
            eventQueue.append(["buttonDown", 13])
        if self.Dr == 1 and x <= 0:
            self.Dr = 0
            eventQueue.append(["buttonUp", 11])
        if self.Dr <= 0 and x > 0:
            self.Dr = 1
            eventQueue.append(["buttonDown", 11])
        if self.Dd == 1 and y >= 0:
            self.Dd = 0
            eventQueue.append(["buttonUp", 14])
        if self.Dd >= 0 and y < 0:
            self.Dd = 1
            eventQueue.append(["buttonDown", 14])
        if self.Du == 1 and y <= 0:
            self.Du = 0
            eventQueue.append(["buttonUp", 12])
        if self.Du <= 0 and y > 0:
            self.Du = 1
            eventQueue.append(["buttonDown", 12])
class DudeMan:
    def __init__(self):
        self.x = 20
        self.y = 15
        self.holding = 0
        self.d = 3 # 3 is left, 2 is rght
class LEVEL:
    def __init__(self):
        self.w = 0
        self.h = 0
        self.dms = (0,0)
        self.grid = []
    def load(self, l):
        if l == 0:
            self.w = 20
            self.h = 8
            self.dms = (16,5)
            self.grid = [[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                         [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                         [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                         [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                         [1,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
                         [1,5,0,0,1,0,0,0,1,0,4,0,1,0,4,0,0,0,0,1],
                         [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
        elif l == 1:
            self.w = 22
            self.h = 10
            self.dms = (18,6)
            self.grid = [[0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,1,0,0,0,0],
                         [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
                         [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
                         [1,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
                         [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                         [0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,4,0,0,0,0,1],
                         [0,1,0,0,0,0,0,0,0,0,0,0,0,1,4,0,4,4,0,0,0,1],
                         [0,1,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1],
                         [0,0,0,0,0,1,0,0,4,1,0,0,0,0,0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0]]
        elif l == 2:
            self.w = 19
            self.h = 11
            self.dms = (9,6)
            self.grid = [[0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                         [0,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
                         [1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                         [1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                         [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,1],
                         [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,1],
                         [1,0,1,1,1,0,0,0,0,0,0,0,0,1,4,0,1,1,0],
                         [1,0,1,0,1,0,0,0,0,1,0,0,1,1,1,1,1,0,0],
                         [1,0,1,0,1,4,4,0,1,1,0,0,1,0,0,0,0,0,0],
                         [1,5,1,0,1,1,1,1,1,1,0,1,1,0,0,0,0,0,0],
                         [1,1,1,0,1,1,0,0,0,1,1,1,0,0,0,0,0,0,0]]
        elif l == 3:
            self.w = 24
            self.h = 16
            self.dms = (17,8)
            self.grid = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0],
                         [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0],
                         [0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0],
                         [0,0,0,1,1,1,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0],
                         [0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,1],
                         [0,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1],
                         [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,1],
                         [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,1],
                         [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
                         [1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0],
                         [1,5,0,0,0,0,1,0,4,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0],
                         [1,1,1,1,1,0,1,0,4,0,0,0,4,0,0,1,1,1,0,0,0,0,0,0],
                         [0,0,0,0,1,0,1,0,4,0,1,0,1,4,0,1,0,0,0,0,0,0,0,0],
                         [0,0,0,0,1,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0],
                         [0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
        elif l == 4:
            self.w = 22
            self.h = 14
            self.dms = (12,8)
            self.grid = [[0,0,0,0,0,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,1,0],
                         [0,1,1,1,1,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,1],
                         [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                         [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                         [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                         [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                         [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                         [1,0,0,0,0,0,1,4,4,4,4,0,0,0,0,0,0,0,0,0,0,1],
                         [1,5,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1],
                         [1,1,0,1,1,1,0,0,0,0,0,1,1,0,1,0,0,0,0,0,4,1],
                         [0,1,0,1,0,0,0,0,0,0,0,0,1,0,1,1,0,0,0,4,4,1],
                         [0,1,0,1,0,0,0,0,0,0,0,0,1,0,1,1,0,0,4,4,4,1],
                         [0,1,1,1,0,0,0,0,0,0,0,0,1,0,1,1,1,1,1,1,1,1],
                         [0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0]]
        elif l == 5:
            self.w = 21
            self.h = 13
            self.dms = (13,7)
            self.grid = [[0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
                         [0,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1],
                         [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                         [1,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                         [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                         [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,1],
                         [0,1,4,4,0,0,0,0,0,0,0,0,1,0,0,4,0,0,1,1,1],
                         [0,1,4,4,4,0,0,0,0,0,0,0,1,0,4,4,4,0,1,0,0],
                         [0,1,4,4,4,4,0,0,0,0,0,0,1,1,1,1,1,0,1,0,0],
                         [0,1,1,1,1,1,0,0,0,0,1,1,1,0,0,0,1,1,1,0,0],
                         [0,0,0,0,0,1,0,0,0,4,1,0,0,0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0]]
        elif l == 6:
            self.w = 24
            self.h = 14
            self.dms = (17,9)
            self.grid = [[0,0,1,0,0,0,1,1,1,1,1,0,0,0,1,1,0,0,0,1,1,1,0,0],
                         [0,1,0,1,0,1,0,0,0,0,0,1,0,1,0,0,1,0,1,0,0,0,1,0],
                         [0,1,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,1,1,0,0,0,0,1],
                         [0,1,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],
                         [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,1],
                         [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,1],
                         [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,1],
                         [1,5,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
                         [1,1,0,0,0,1,0,4,0,0,0,0,0,1,0,0,0,0,1,1,0,1,0,0],
                         [0,1,0,0,0,1,0,4,0,0,0,0,1,1,0,4,0,0,1,1,1,1,0,0],
                         [0,1,1,0,0,1,0,4,4,4,0,0,1,1,0,4,4,4,1,0,0,0,0,0],
                         [0,0,1,0,0,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,0,0,0,0],
                         [0,0,1,1,0,1,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0],
                         [0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
        elif l == 7:
            self.w = 27
            self.h = 17
            self.dms = (20,15)
            self.grid = [[0,1,1,1,0,0,0,0,0,0,0,1,1,1,1,0,0,0,1,1,1,1,1,1,1,0,0],
                         [1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0],
                         [1,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1],
                         [1,4,0,0,0,0,1,1,1,0,0,0,0,1,0,1,0,0,0,0,0,1,1,1,0,0,1],
                         [1,4,4,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,1,0,0,1],
                         [1,1,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,5,0,1],
                         [0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1,1,0,1],
                         [0,0,1,0,0,0,0,4,0,1,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,1],
                         [0,0,1,0,0,0,0,4,1,0,1,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,1],
                         [0,1,0,0,0,1,1,1,0,0,0,1,0,0,0,0,1,0,0,1,0,0,0,0,0,4,1],
                         [0,1,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,4,4,1],
                         [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1],
                         [1,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,1],
                         [1,0,0,0,0,4,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,4,1],
                         [1,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,1],
                         [1,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,4,0,0,0,0,0,4,4,4,1],
                         [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
        elif l == 8:
            self.w = 20
            self.h = 16
            self.dms = (14,7)
            self.grid = [[0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,1,1,1,1,1],
                         [0,0,0,0,0,1,0,0,0,0,0,0,0,1,1,0,0,0,0,1],
                         [0,0,0,0,1,0,0,0,0,0,4,0,0,0,0,0,0,0,0,1],
                         [0,0,0,1,0,0,0,0,0,0,4,4,0,0,0,0,0,0,4,1],
                         [0,0,1,0,0,0,0,0,0,0,1,1,1,0,0,0,0,4,4,1],
                         [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
                         [1,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,1],
                         [1,5,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,1],
                         [1,1,0,0,0,0,1,1,0,0,0,1,0,0,0,0,0,0,4,1],
                         [0,1,0,0,0,0,1,1,4,0,0,1,1,0,0,0,1,1,1,1],
                         [0,1,0,0,0,0,1,1,1,1,1,1,1,0,0,1,1,0,0,0],
                         [0,1,1,1,0,0,1,0,0,0,0,0,1,0,1,1,0,0,0,0],
                         [0,0,0,1,0,1,1,0,0,0,0,0,1,1,1,0,0,0,0,0],
                         [0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
        elif l == 9:
            self.w = 27
            self.h = 19
            self.dms = (14,11)
            self.grid = [[0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
                         [0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0],
                         [1,1,1,1,4,0,0,0,0,0,0,0,4,4,1,4,0,0,0,4,4,4,0,4,1,1,0],
                         [1,0,0,1,1,0,0,1,0,0,0,1,1,1,1,1,0,0,4,1,1,1,0,1,1,0,1],
                         [1,0,0,0,1,0,0,1,1,0,0,0,0,0,0,0,0,1,1,1,0,1,1,1,0,0,1],
                         [1,0,0,0,1,1,0,0,1,1,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,1],
                         [1,5,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1],
                         [1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,1,1,0,0,0,0,0,0,0,0,1,1],
                         [0,1,0,0,0,0,0,4,0,0,0,1,0,1,0,0,1,1,0,0,0,0,0,0,0,0,1],
                         [0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,1],
                         [0,1,1,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1],
                         [0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                         [0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
                         [0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1,1,1,1,1,1,1,1],
                         [0,0,0,1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0],
                         [0,0,0,1,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,4,1,0],
                         [0,0,0,1,4,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,4,4,1,0],
                         [0,0,0,1,4,4,0,0,1,1,0,0,0,0,0,0,0,0,0,1,1,0,4,4,4,1,0],
                         [0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0]]
        elif l == 10:
            self.w = 29
            self.h = 19
            self.dms = (13,4)
            self.grid = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                         [1,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                         [1,0,0,0,0,0,4,1,4,4,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,1],
                         [1,4,0,0,0,1,1,1,0,4,1,1,0,0,0,0,0,4,0,0,1,1,0,0,5,0,1,0,1],
                         [1,4,4,0,0,0,0,0,1,1,1,0,0,0,0,0,4,0,0,0,0,0,0,0,1,0,1,0,1],
                         [1,1,1,0,0,4,4,1,0,0,0,0,0,1,0,4,0,0,0,0,0,0,0,0,0,0,1,0,1],
                         [1,0,0,0,1,1,1,1,0,0,0,0,0,0,1,0,0,1,1,1,0,0,0,1,1,1,0,0,1],
                         [1,4,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,0,0,4,0,1],
                         [1,4,4,0,0,0,0,0,0,0,1,1,1,0,1,0,1,4,0,0,0,0,1,0,0,1,1,1,1],
                         [1,1,1,1,0,4,0,0,0,1,1,1,0,0,1,0,1,1,4,0,0,1,0,4,0,1,0,0,1],
                         [1,0,0,0,0,0,0,0,0,0,0,0,4,0,1,1,1,0,0,4,1,0,0,0,1,0,0,0,1],
                         [1,0,0,0,4,0,0,0,0,0,4,4,0,1,0,0,0,1,1,1,1,0,0,0,0,0,0,0,1],
                         [1,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,0,1],
                         [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,4,1,1,0,0,0,0,1,0,1],
                         [1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,1,0,0,0,0,4,4,1,0,1],
                         [1,4,1,1,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,1],
                         [1,1,4,1,1,1,0,1,0,0,0,0,1,0,0,0,4,4,4,0,4,0,0,0,0,0,0,0,1],
                         [1,4,1,4,1,4,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,4,4,4,0,0,0,0,1],
                         [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
        #screen = pygame.display.set_mode((self.w*8*10,self.h*8*10))
        #gameDisplay = pygame.Surface((self.w*8, self.h*8))
        #background  = pygame.Surface((self.w*8, self.h*8))
        background.fill((255,255,255))
        for r in range(self.h):
            for c in range(self.w):
                drawTile(background, level1.grid[r][c], c, r)
        dm.x = self.dms[0]
        dm.y = self.dms[1]
        dm.holding = 0

        
level1 = LEVEL()
XBC = Controller()
dm = DudeMan()


eventQueue = []
l=0
level1.load(l)

bstrings = ['A', 'B', 'X', 'Y', 'Left Button', 'Right Button', 'Select', 'Start', 'Left Stick', 'Right Stick', 'Home', 'Dright', 'Dup', 'Dleft', 'Ddown']
astrings = ['Left Stick X', 'Left Stick Y', 'Right Stick X', 'Right Stick Y', 'Left Trigger', 'Right Trigger']

mode = 1 # 1 - gameplay, 2 - win

while True:
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            XBC.checkButt(event.button, 1)
        elif event.type == pygame.JOYBUTTONUP:
            XBC.checkButt(event.button, 0)
        elif event.type == pygame.JOYAXISMOTION:
            XBC.checkAxis(event.axis, event.value)
        elif event.type == pygame.JOYHATMOTION:
            XBC.checkHat(event.value[0], event.value[1])
        elif event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                eventQueue.append(('axisHigh', 0))
            if event.key == pygame.K_LEFT:
                eventQueue.append(('axisLow', 0))
            if event.key == pygame.K_UP:
                eventQueue.append(('buttonDown',0))
            if event.key == pygame.K_DOWN:
                eventQueue.append(('buttonDown',2))
            if event.key == pygame.K_KP_PLUS:
                eventQueue.append(('buttonDown',5))
            if event.key == pygame.K_KP_MINUS:
                eventQueue.append(('buttonDown',4))
    
    if mode == 1: #gameplay
        while len(eventQueue) > 0:
            if eventQueue[0][0] == 'buttonDown':
                if eventQueue[0][1] == 0: # A button
                    if dm.d == 2:
                        if level1.grid[dm.y][dm.x+1] != 0 and level1.grid[dm.y-1][dm.x+1] == 5: #win
                            mode = 2
                        if level1.grid[dm.y][dm.x+1] != 0 and level1.grid[dm.y-1][dm.x+1] == 0:
                            dm.x+=1
                            dm.y-=1
                    if dm.d == 3:
                        if level1.grid[dm.y][dm.x-1] != 0 and level1.grid[dm.y-1][dm.x-1] == 5: #win
                            mode = 2
                        if level1.grid[dm.y][dm.x-1] != 0 and level1.grid[dm.y-1][dm.x-1] == 0:
                            dm.x-=1
                            dm.y-=1
                if eventQueue[0][1] == 2: # X button
                    if dm.holding:
                        if dm.d == 2:
                            if level1.grid[dm.y-1][dm.x+1] == 0:
                                t = dm.y-1
                                while level1.grid[t+1][dm.x+1] == 0:
                                    t += 1
                                level1.grid[t][dm.x+1] = 4
                                drawTile(background, 4, dm.x+1, t)
                                dm.holding = 0
                        elif dm.d == 3:
                            if level1.grid[dm.y-1][dm.x-1] == 0:
                                t = dm.y-1
                                while level1.grid[t+1][dm.x-1] == 0:
                                    t += 1
                                level1.grid[t][dm.x-1] = 4
                                drawTile(background, 4, dm.x-1, t)
                                dm.holding = 0
                    else:
                        if dm.d == 2 and level1.grid[dm.y][dm.x+1] == 4 and level1.grid[dm.y-1][dm.x] == 0 and level1.grid[dm.y-1][dm.x+1] == 0:
                            dm.holding = 1
                            level1.grid[dm.y][dm.x+1] = 0
                            drawTile(background, 0, dm.x+1, dm.y)
                        if dm.d == 3 and level1.grid[dm.y][dm.x-1] == 4 and level1.grid[dm.y-1][dm.x] == 0 and level1.grid[dm.y-1][dm.x-1] == 0:
                            dm.holding = 1
                            level1.grid[dm.y][dm.x-1] = 0
                            drawTile(background, 0, dm.x-1, dm.y)
                if eventQueue[0][1] == 3: # Y button
                    level1.load(l)
                if eventQueue[0][1] == 4: #left bumper
                    l -= 1
                    level1.load(l)
                if eventQueue[0][1] == 5: #right bumper
                    l += 1
                    level1.load(l)
                if eventQueue[0][1] == 11: #Dpad right
                    eventQueue.append(('axisHigh', 0))
                if eventQueue[0][1] == 13: #Dpad left
                    eventQueue.append(('axisLow', 0))
                if eventQueue[0][1] == 12: #Dpad up
                    eventQueue.append(('buttonDown',0))
                if eventQueue[0][1] == 14: #Dpad down
                    eventQueue.append(('buttonDown',2))
            if eventQueue[0][0] == 'axisLow':
                if eventQueue[0][1] == 0: # left stick left
                    XBC.leftLowTick = 0
                    dm.d = 3
                    if level1.grid[dm.y][dm.x-1] == 5:
                        mode = 2
                    if level1.grid[dm.y][dm.x-1] == 0:
                        if dm.holding and level1.grid[dm.y-1][dm.x-1] != 0:
                            dm.holding = 0
                            level1.grid[dm.y][dm.x] = 4
                            drawTile(background, 4, dm.x, dm.y)
                        dm.x -= 1
            if eventQueue[0][0] == 'axisHigh':
                XBC.leftHighTick = 0
                if eventQueue[0][1] == 0: #left stick right
                    dm.d = 2
                    if level1.grid[dm.y][dm.x+1] == 5:
                        mode = 2
                    if level1.grid[dm.y][dm.x+1] == 0:
                        if dm.holding and level1.grid[dm.y-1][dm.x+1] != 0:
                            dm.holding = 0
                            level1.grid[dm.y][dm.x] = 4
                            drawTile(background, 4, dm.x, dm.y)
                        dm.x += 1
            eventQueue.pop(0)
        
        
        if XBC.axis[0] < -.75:
            XBC.leftLowTick += 1
        if XBC.axis[0] > .75:
            XBC.leftHighTick += 1
        if XBC.leftLowTick >= 10:
            eventQueue.append(('axisLow',0))
        if XBC.leftHighTick >= 10:
            eventQueue.append(('axisHigh',0))
        
        while level1.grid[dm.y+1][dm.x] == 0:
            dm.y += 1
        if level1.grid[dm.y+1][dm.x] == 5:
            mode = 2
        
        gameDisplay.blit(background,(0,0))
        drawTile(gameDisplay, dm.d, dm.x, dm.y) #draw dudeman
        if dm.holding:
            drawTile(gameDisplay, 4, dm.x, dm.y-1)
        
        pygame.transform.scale(gameDisplay,(29*8*10, 19*8*10), screen)
        pygame.display.flip()
        clock.tick(60)
    if mode == 2: #win
        mode = 1
        l+=1
        level1.load(l)
    
