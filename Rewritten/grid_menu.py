#////////////////////////////////////////
#Grid Size Menu to replace the traditional menu
#////////////////////////////////////////
import pygame, sys
from pygame.locals import *
import math
print("[info]Grid Menu System Loaded")
pygame.init()
#/////////////////////////////////////////////////////////////////
#Color Define
#/////////////////////////////////////////////////////////////////
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LBLUE = (66, 134, 244)
GREY = (71, 71, 71)

#////////////////////////////////////////
#Functions for quick control
#////////////////////////////////////////
def LoadUI(filename,size=[0,0]):
    #Load the image using filename (with resize)
    img = pygame.image.load("ui/main_menuicons/background/" + filename + '.png').convert_alpha()
    defaultsize = img.get_rect().size
    if size==[0,0]:
        return img
    else:
        img = pygame.transform.scale(img,(size[0],size[1]))
        return img

def WriteText(form,string,pos,size):
    textfont = pygame.font.Font("ui/WHJYT.ttc", size)
    text = textfont.render(string, True, (0,0,0))
    textrect = text.get_rect()
    textrect.top = pos[1]
    textrect.centerx = pos[0]
    form.blit(text, textrect)

def CheckInRange(pos,myarea):
    pos1 = [myarea[0],myarea[1]]
    pos2 = [myarea[0] + myarea[2], myarea[1] + myarea[3]]
    if pos[0] > pos1[0] and pos[0] < pos2[0]:
        #x is within the range
        if pos[1] > pos1[1] and pos[1] < pos2[1]:
            #y is within range
            return True
        else:
            return False
    else:
        return False

def CreateTextList(textarr):
    #Create a surface will all text on it
    number = len(textarr)
    height = 46 * (number)
    width = 163
    bound = pygame.Surface((width,height), pygame.SRCALPHA, 32)
    textfont = pygame.font.Font("ghost/ui/WHJYT.ttc", 18)
    for i in range(0,number):
        pos = (0,46 * i)
        text = textfont.render(textarr[i], True, (0,0,0))
        textrect = text.get_rect()
        textrect.centerx = pos[0] + width/2
        textrect.centery= pos[1] + 23
        bound.blit(text,textrect)
    return bound

def CreateButtonsImage(interfacearr,textarr):
    global list_normal,list_press
    number = len(interfacearr)
    #Create a list of buttons depends on requred numbers
    height = 46 * (number)
    width = 163
    bound = pygame.Surface((width,height), pygame.SRCALPHA, 32)
    for i in range(0,number):
        #For each item
        pos = (0,46 * i)
        if interfacearr[i] == 0:
            bound.blit(list_normal,pos)
        elif interfacearr[i] == 1:
            bound.blit(list_press,pos)
    bound.blit(CreateTextList(textarr),(0,0))
    return bound

def CreateSubMenu(menuid,interfacearr):
    global catb_hover,catb_normal
    print("Required Menu Id: " + str(menuid))
    ch = pygame.transform.rotate(catb_hover,180)
    cn = pygame.transform.rotate(catb_normal,180)
    number = 3
    height = 46 * (number)
    width = 182
    bound = pygame.Surface((width,height), pygame.SRCALPHA, 32)
    for i in range(0,number):
        pos = (0,46 * i)
        if interfacearr[i] == 0:
            bound.blit(cn,pos)
        elif interfacearr[i] == 1:
            bound.blit(ch,pos)
    #bound.blit(CreateTextList(textarr),(0,0))
    return bound 

    
#//////////////////////////////////////////////////////////////////////
#Coordinate and position calculation
#//////////////////////////////////////////////////////////////////////
def R2A (rpos,pos):
    #Relative Position to Absolute Position
    realpos = (pos[0] + rpos[0],pos[1] + rpos[1])
    return realpos

def A2R(formpos,pos):
    #Absolute Position to Relative Position
    relativepos = (pos[0] - formpos[0],pos[1] - formpos[1])
    return relativepos

def C2TL(formpos,size):
    #Convert centered coordinate to top left coordinate
    fx = formpos[0] - size[0]/2
    fy = formpos[1] - size[1]/2
    return (fx,fy)

def GetBtnID(formpos,pos):
    #Assume every button was 46 pixel height
    btnid = math.floor((pos[1] - formpos[1]) / 46)
    return btnid 




class Control():
    def Launch(self,screen,size):
        #Interface Surfaces
        global list_normal,list_press,catb_hover,catb_normal
        list_normal = LoadUI("list_normal")
        list_press = LoadUI("list_press")
        catb_hover = LoadUI("catb_hover")
        catb_normal = LoadUI("catb_normal")
        self.screen = screen
        self.pos = (screen.get_rect().centerx,screen.get_rect().centery)
        self.background = CreateButtonsImage([0,0,0,0,0],["btn1","btn2","btn3","btn4","btn5"])
        self.submenu = CreateSubMenu(0,[0,1,0])
        self.size = self.background.get_size()
        self.hide = False
        self.focus = 0
        self.intarr = [0,0,0]
        self.focusl1 = 0
        self.currentlayer = 1
    def update(self):
        if self.intarr[1] == 0 and self.intarr[2] == 0:
            self.screen.blit(self.background,(C2TL(self.pos,self.size)))
        elif self.intarr[2] == 0:
            self.screen.blit(self.background,(C2TL(self.pos,self.size)))
            self.screen.blit(self.submenu,(C2TL((self.pos[0] - 182,self.pos[1] + (self.focus-1) * 46),self.size)))
    def Hide(self):
        self.pos = (2000,self.screen.get_rect().centery)
        self.hide = True
    def Show(self):
        self.pos = (self.screen.get_rect().centerx,self.screen.get_rect().centery)
        self.hide = False
    def KeyHandler(self,key):
        print(key)
        btnia = [0,0,0,0,0]
        if key == 274:
            if self.intarr[1] == 0:
                self.focus += 1
                self.submenu = CreateSubMenu(self.focus,[0,1,0])
            elif self.intarr[2] == 0:
                self.focusl1 += 1
                self.submenu = CreateSubMenu(self.focus,self.focusl1)
            
        elif key == 273:
            if self.intarr[1] == 0:
                self.focus -= 1
                self.submenu = CreateSubMenu(self.focus,)
            elif self.intarr[2] == 0:
                self.focusl1 -= 1
            
        elif key == 276:
            self.intarr[self.currentlayer] = (self.focus)
            self.currentlayer += 1
            print(self.intarr)
            print(self.currentlayer)
        elif key == 275:
            print(self.currentlayer)
            self.intarr[self.currentlayer] = 0
            self.currentlayer -= 1
            print(self.intarr)
            print(self.currentlayer)
            

        if self.focus < 1 :
            self.focus = 1
        elif self.focus > len(btnia):
            self.focus = len(btnia)
        if self.currentlayer > 2:
            self.currentlayer = 2
        elif self.currentlayer < 1:
            self.currentlayer = 1
                
        if self.focus != 0 and self.focus <= len(btnia):
            btnia[self.focus -1] = 1
        self.background = CreateButtonsImage(btnia,["btn1","btn2","btn3","btn4","btn5"])

