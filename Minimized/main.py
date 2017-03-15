import pygame, sys
import weather_module as wm
#import news_module as nm
import main_menu as mm
from pygame.locals import *
from time import gmtime, strftime
print("///////////////////ArOZ Omega Raspberry pi Edition/////////////////////////")
print("Developed by Toby Chui @ 2017")
print("[info]Loading System Variables and Starting Initiation...")
#/////////////////////////////////////////////////////////////////
#Color Define
#/////////////////////////////////////////////////////////////////
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#/////////////////////////////////////////////////////////////////
#define system variables
#/////////////////////////////////////////////////////////////////
ScreenWidth = 800 #The Screen Width in pixels
ScreenHeight = 600 #The Screen Height in pixels
spritefolder = "ghost/" #The directory to store all the surface
goffsets = [50,30] #Offsets of ghost to the boundary of form
ghostlocation = (0,0)#define ghost location
global eyelayer, cl1, cl2, expressiontick,hourticking,mousedown
eyelayer = None #Top layer
cl1 = None #Layer 1
cl2 = None #Layer 2
expressiontick = 0 #Time counter for expression changes
fontcolor = [BLACK,BLACK,BLACK,BLACK,WHITE] #Color of text of "earily morning" /  "morning" / "noon" / "afternoon"/ "night"
hourticking = False
mousedown = False


#/////////////////////////////////////////////////////////////////
#System Initiation
#/////////////////////////////////////////////////////////////////
pygame.init()
print("[info]PyGame Initiated")
form = pygame.display.set_mode((ScreenWidth, ScreenHeight))
#form = pygame.display.set_mode((ScreenWidth, ScreenHeight),pygame.NOFRAME)
pygame.display.set_caption('ArOZ Omega Raspberry pi Edition')
EYECONTROL, t = pygame.USEREVENT+1, 100
pygame.time.set_timer(EYECONTROL, t)

#/////////////////////////////////////////////////////////////////
#Load Global ArOZ Interface
#/////////////////////////////////////////////////////////////////
global ghostimg,s100,s101
ghostimg = pygame.image.load(spritefolder + 'surface0.png').convert_alpha()
s100  = pygame.image.load(spritefolder + 'surface100.png').convert_alpha() #Eyes semi closed
s101 = pygame.image.load(spritefolder + 'surface101.png').convert_alpha() #Eye closed
#/////////////////////////////////////////////////////////////////
#Convenience Functions for file and image handling
#/////////////////////////////////////////////////////////////////
def LoadImage(filename,size=[0,0]):
    #Load the image using filename (with resize)
    img = pygame.image.load(spritefolder + filename + '.png').convert_alpha()
    defaultsize = img.get_rect().size
    if size==[0,0]:
        return img
    else:
        img = pygame.transform.scale(img,(size[0],size[1]))
        return img
    
def LoadUI(filename,size=[0,0]):
    #Load the image using filename (with resize)
    img = pygame.image.load(spritefolder +"ui/" + filename + '.png').convert_alpha()
    defaultsize = img.get_rect().size
    if size==[0,0]:
        return img
    else:
        img = pygame.transform.scale(img,(size[0],size[1]))
        return img
    
def DrawImage(image,location):
    #Draw the image to screen with certain location.
    form.blit(image,location)

def GetImageSize(image):
    #Get the image size in array[x,y]
    return image.get_rect().size

def Merge(image1,image2):
    image1.blit(image2,(0,0))
    return image1
#/////////////////////////////////////////////////////////////////
#Motion Controlling Functions
#/////////////////////////////////////////////////////////////////
global eyestate,expressionmode
eyestate = 0#eyestate use as a timer for eye status calculation
expressionmode = False
def Eye_blink():
    global eyestate,s100,s101
    if expressionmode == False:
        eyestate += 1
        if eyestate == 1:
            #print("Looped Eyestate")
            return None
        elif eyestate == 53:
            #print("Eye Semiclosed")
            eyeimg = s100.copy()
            return eyeimg
        elif eyestate == 54:
            #print("Eye closed")
            eyeimg = s101.copy()
            return eyeimg
        elif eyestate == 55:
            #print("Eye Semiclosed")
            eyeimg = s100.copy()
            eyestate = 0
            return eyeimg
    else:
        return None
    
def ClickHandler(coordinates,ghostlocation,ghostsize):
    global expressionmode
    clickx = coordinates[0]
    clicky = coordinates[1]
    glx = ghostlocation[0]
    gly = ghostlocation[1]
    gsx = ghostsize[0]
    gsy = ghostsize[1]
    mlx =ScreenWidth * 0.9
    mly =ScreenHeight * 0.03
    msx = 64
    msy = 64
    if clickx > glx and clickx < (glx + gsx):
        if clicky > gly and clicky < (gly + gsy):
            #It is clicked within ArOZ Ghost Image
            expressionmode = True
            return True
    if clickx > mlx and clickx < (mlx + msx):
        if clicky > mly and clicky < (mly + msy):
            #It is clicked within the menu button
            return "menu"
    return None
def InterfaceReset(expressiontick):
    global expressionmode
    if expressiontick > 30:
        expressionmode = False
    return False

def GetDisplayTime():
    sec = strftime("%S", gmtime())
    if int(sec)%2 != 0:
        return strftime("%H:%M")
    else:
        return strftime("%H %M")
    
def GetTimeOfDay():
    hour = int(strftime("%H"))
    if hour < 6:
        return "earily morning"
    elif hour >= 6 and hour <12:
        return "morning"
    elif hour >= 12 and hour<13:
        return "noon"
    elif hour >=13 and hour < 19:
        return "afternoon"
    elif hour >= 19 and hour <24:
        return "night"

def CheckHourUpdate():
    #This update only take place once 60 minutes.
    global hourticking
    ctime = strftime("%M%S")
    if (ctime) == "0500" and hourticking == False:
        print("[info]HourTicks")
        hourticking = True
        return True
    elif (ctime) == "0501" and hourticking == True:
        hourticking = False
    return False
#/////////////////////////////////////////////////////////////////
#Main Loop
#/////////////////////////////////////////////////////////////////
def main():
    print("[info]Lauching Main Logic System...")
    #////////Advanced Initiations////
    global eyelayer,cl1,cl2,expressiontick,expressionmode,ghostimg,mousedown
    #Set Icon
    icon = LoadImage("icon")
    pygame.display.set_icon(icon)
    #Set background
    
    #Set stationary object
    toolbar =  LoadUI("base",(ScreenWidth,ScreenHeight))
    #Set Buttons object
    more = LoadUI("more")
    
    # set up the text
    timefont = pygame.font.SysFont("Arial", 24)
    text = timefont.render('Loading', True, fontcolor[0])
    timerect = text.get_rect()
    timerect.top = ScreenHeight * 0.05
    timerect.centerx= ScreenWidth / 2

    #Set up Module Objects
    Menu = mm.Control()
    Menu.Initiate(form)
    WeatherWidget = wm.Widget()
    WeatherWidget.Launch(form,(50,90,220,100))
        
    # draw the white background onto the surface
    form.fill(BLACK)
    # draw the text onto the surface
    form.blit(text, timerect)
    ghostimg = LoadImage("surface0")
    ims = GetImageSize(ghostimg)
    ghostlocation = (ScreenWidth - ims[0] + goffsets[0],ScreenHeight - ims[1]+goffsets[1])

    #Load all stationary layers
    cl1 = LoadImage("surface1100")
    cl2 = LoadImage("surface1400")
    #///////////////////////////////////////
    #MAIN LOGIC LOOP
    while True:
        #Initializing all layers
        #There are four layers
        # TOP: Eye Layer
        # 2nd: Clothes Layer 1
        # 3rd: Clothes Layer 2
        # 4th: Body Layer (Standard)
        #Background Handling
        form.fill(BLACK)
        form.blit(toolbar,(0,0))
        form.blit(more ,(ScreenWidth * 0.9,ScreenHeight * 0.03))
        WeatherWidget.update()
        Menu.update()

        
        #Process UI Text Update
        currenttime = GetDisplayTime()
        text = timefont.render(currenttime, True, WHITE)
        form.blit(text, timerect)

        bl = ghostimg.copy()
        if CheckHourUpdate() == True:
            #Tick every whole hours
            WeatherWidget.InfoUpdate()
            #NewsWidget.InfoUpdate()
                    
        #EVENTS HANDLER
        for event in pygame.event.get():

            if event.type == QUIT: #Closing Handler
                print("[Info]System Exiting...")
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:#Mouse Up Handler
                mousedown = False
                pos = pygame.mouse.get_pos()
                print("[Debug]",pos[0],pos[1])
                returnvalue = ClickHandler(pos,ghostlocation,GetImageSize(bl))
                #Process the returned value of click location
                if returnvalue == True:
                    eyelayer = LoadImage("surface2")
                elif returnvalue == "menu":
                    if Menu.show == True:
                        Menu.Hide()
                        WeatherWidget.acc = 24
                        WeatherWidget.show = True
                    else:
                        Menu.Show()
                        WeatherWidget.acc = 1
                        WeatherWidget.show = False

                Menu.click_handler(pos)
                WeatherWidget.click_handler(pos)
            if event.type == pygame.MOUSEBUTTONDOWN:#Mouse Down Handler
                mousedown = True

            if event.type == pygame.MOUSEMOTION: #Mouse Move
                if mousedown == True:
                    #Draging over the interface
                    pos = pygame.mouse.get_pos()
                    NewsWidget.Draging(pos)
            if event.type == pygame.KEYDOWN:#Keypress Handler
                if event.key == pygame.K_ESCAPE:
                    print("[Info]System Exiting...")
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_0:#Debug button holds to key 0
                    if NewsWidget.show == True:
                        NewsWidget.Hide()
                        WeatherWidget.acc = 1
                        WeatherWidget.show = False
                        Menu.Show()
                    else:
                        NewsWidget.Show()
                        WeatherWidget.acc = 24
                        WeatherWidget.show = True
                        Menu.Hide()
                    
            if event.type == EYECONTROL: #Eye Blink Controller, also act as timer
                if expressionmode == False:
                    eyelayer = Eye_blink()
                    expressiontick = 0
                else:
                    expressiontick += 1
                    InterfaceReset(expressiontick)
        #END OF EVENTS HANDLER
                    
        #Compare layers and draw them to the form
        if cl2 != None:
            bl.blit(cl2,(0,0))
        if cl1 != None:
            bl.blit(cl1,(0,0))
        if eyelayer != None:
            bl.blit(eyelayer,(0,0))
        form.blit(bl,ghostlocation)
        pygame.display.flip()
        #pygame.time.delay(10)
#/////////////////////////////////////////////////////////////////
#Initiation of Main
#/////////////////////////////////////////////////////////////////
main()
