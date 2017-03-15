print("///////////////////ArOZ Omega Raspberry pi Edition/////////////////////////")
print("Developed by Toby Chui @ 2017")
print("[info]Loading System Variables and Starting Initiation...")

import pygame, sys
import grid_menu
from pygame.locals import *
from time import gmtime, strftime

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
#/////////////////////////////////////////////////////////////////
#define system variables
#/////////////////////////////////////////////////////////////////
ScreenWidth = 800 #The Screen Width in pixels
ScreenHeight = 480 #The Screen Height in pixels
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
gm = grid_menu.Control()

#/////////////////////////////////////////////////////////////////
#Load Global ArOZ Interface
#/////////////////////////////////////////////////////////////////

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
    img = pygame.image.load("ui/" + filename + '.png').convert_alpha()
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
    background = LoadUI("background",(ScreenWidth,ScreenHeight))
    
    #Set stationary object
    toolbar =  LoadUI("base",(ScreenWidth,ScreenHeight))
    
    #Set Buttons object
    more = LoadUI("more")
    
    # set up the text
    timefont = pygame.font.SysFont("Arial", 24)
    text = timefont.render('Loading', True, LBLUE)
    timerect = text.get_rect()
    timerect.top = ScreenHeight * 0.05
    timerect.centerx= ScreenWidth / 2

    #Set up Module Objects
    gm.Launch(form,(300,300))
    # draw the white background onto the surface
    form.fill(BLACK)
    # draw the text onto the surface
    form.blit(text, timerect)


    #Load all stationary layers

    #///////////////////////////////////////
    #MAIN LOGIC LOOP
    while True:
        #Initializing all layers
        form.fill(BLACK)
        form.blit(background,(0,0))
        form.blit(toolbar,(0,0))
        form.blit(more ,(ScreenWidth * 0.9,ScreenHeight * 0.03))

        
        #Process UI Text Update
        currenttime = GetDisplayTime()
        text = timefont.render(currenttime, True, GREY)
        form.blit(text, timerect)

        #Process Modules Update
        gm.update()

        if CheckHourUpdate() == True:
            #Tick every whole hours
            print("Hourly Tick") 
                    
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


            if event.type == pygame.MOUSEBUTTONDOWN:#Mouse Down Handler
                mousedown = True

            if event.type == pygame.MOUSEMOTION: #Mouse Move
                if mousedown == True:
                    #Draging over the interface
                    pos = pygame.mouse.get_pos()

            if event.type == pygame.KEYDOWN:#Keypress Handler
                if event.key == pygame.K_ESCAPE:
                    print("[Info]System Exiting...")
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_0:#Debug button holds to key 0
                    print("Debug Mode Finished")
                    if gm.hide == True:
                        gm.Show()
                    else:
                        gm.Hide()
                gm.KeyHandler(event.key)
            if event.type == EYECONTROL: #Eye Blink Controller, also act as timer
               pass
        #END OF EVENTS HANDLER
                    
        #Compare layers and draw them to the form

        pygame.display.flip()
        #pygame.time.delay(10)
#/////////////////////////////////////////////////////////////////
#Initiation of Main
#/////////////////////////////////////////////////////////////////
main()
