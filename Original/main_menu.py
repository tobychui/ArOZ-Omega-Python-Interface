#///////////////////////////////////////////////////////////////////////
#Main Menu for ArOZ Omega Python Edition
#The main menu is mean to be presented with easy touch function
#Intent to be used with Raspberry pi
#//////////////////////////////////////////////////////////////////////

import pygame, sys
from pygame.locals import *
import math

#//////////////////////////////////////////////////////////////////////
#Handful Functions for GUI Rendering
#//////////////////////////////////////////////////////////////////////
def LoadUI(filename,size=[0,0]):
    #Load the image using filename (with resize)
    spritefolder = "ghost/"
    img = pygame.image.load(spritefolder +"ui/main_menuicons/background/" + filename + '.png').convert_alpha()
    defaultsize = img.get_rect().size
    if size==[0,0]:
        return img
    else:
        img = pygame.transform.scale(img,(size[0],size[1]))
        return img

def WriteText(form,string,pos,size):
    textfont = pygame.font.Font("ghost/ui/WHJYT.ttc", size)
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
    
#//////////////////////////////////////////////////////////////////////
#Main Control Class of Menu
#//////////////////////////////////////////////////////////////////////
class Control():
    
    def Initiate(self,screen):
         #Global Layer Storage Data
        self.layer1=[0,0,0,0,0] #Store which layer you pressed
        self.layer1text = [u"選項1",u"選項2",u"選項3",u"選項4",u"選項5"]
        #Initalize Button Interface
        global list_normal,list_press
        list_normal = LoadUI("list_normal")
        list_press = LoadUI("list_press")
        
        #Control Properties
        self.screen = screen
        self.showpos = (screen.get_rect().centerx,screen.get_rect().centery)
        self.show = False
        self.pos = (1106,self.showpos[1])
        self.background = CreateButtonsImage(self.layer1,self.layer1text)
        self.size = self.background.get_size()
    def update(self):
        if self.show == True and self.pos[0] > self.showpos[0]:
            self.pos = (self.pos[0] - self.acc,self.pos[1])
            self.acc -= 5
        elif self.show == True and self.pos[0] < self.showpos[0]:
            self.pos = (self.showpos[0],self.pos[1])
        if self.show == False and self.pos[0] < 1025:
            self.pos = (self.pos[0] + self.acc,self.pos[1])
            self.acc += 5
        elif self.show == False and self.pos[0] > 1025:
            self.pos = (1106,self.pos[1])
        centerpt = (self.pos[0] - self.size[0] /2,self.pos[1] - self.size[1]/2)
        self.screen.blit(self.background,centerpt)
        
    def Show(self):
        self.layer1=[0,0,0,0,0]
        self.background = CreateButtonsImage(self.layer1,self.layer1text)
        self.show = True
        self.acc = 75

    def Hide(self):
        self.acc = 0
        self.show = False   
        
    def click_handler(self,pos):
        if CheckInRange(pos,(self.pos[0] - self.size[0] /2, self.pos[1] - self.size[1]/2 ,self.size[0],self.size[1])) == True:
            if self.show == True:
                #Clicked in range
                if 1 in self.layer1:
                    self.layer1 = [0,0,0,0,0]
                btnid = GetBtnID(C2TL(self.pos,self.size),pos)
                #print("[info]" + str(btnid))
                if self.layer1[btnid] == 0:
                    self.layer1[btnid] = 1
                else:
                    self.layer1[btnid] = 0
                self.background = CreateButtonsImage(self.layer1,self.layer1text)
