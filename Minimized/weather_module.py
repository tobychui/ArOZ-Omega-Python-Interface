#///////////////////////////////////////////////////////////////////////
#Weather Temperature Module for ArOZ Omega Python Edition
#This weather module shows the weather and temperture of Hong Kong
#Intent to be used with Raspberry pi
#//////////////////////////////////////////////////////////////////////

import pygame, sys
from pygame.locals import *
import requests
import re

def LoadUI(filename,size=[0,0]):
    #Load the image using filename (with resize)
    spritefolder = "ghost/"
    img = pygame.image.load(spritefolder +"ui/" + filename + '.png').convert_alpha()
    defaultsize = img.get_rect().size
    if size==[0,0]:
        return img
    else:
        img = pygame.transform.scale(img,(size[0],size[1]))
        return img

def LoadWeatherIcons(filename,size=[0,0]):
    #Load the image using filename (with resize)
    spritefolder = "ghost/ui/weathericons/"
    img = pygame.image.load(spritefolder  + filename + '.png').convert_alpha()
    defaultsize = img.get_rect().size
    if size==[0,0]:
        return img
    else:
        img = pygame.transform.scale(img,(size[0],size[1]))
        return img

def WriteText(form,string,pos,size):
    textfont = pygame.font.Font("ghost/ui/WHJYT.ttc", size)
    text = textfont.render(string, True, (255,255,255))
    textrect = text.get_rect()
    textrect.top = pos[1]
    textrect.left = pos[0]
    form.blit(text, textrect)
def TRP(pos,rpos):
    #Relative Coordinate to Absolute coordinate
    tmposx = pos[0] + rpos[0]
    tmposy = pos[1] + rpos[1]
    return (tmposx,tmposy)

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
    
def GetWeatherCondition():
    webrequest =  requests.get('http://rss.weather.gov.hk/rss/CurrentWeather_uc.xml')
    content = webrequest.content.decode("utf-8")
    print("[WeatherModule]Requesting HK Observatory for rss feed...")
    position = content.rfind("黃 大 仙 ")
    temp = re.sub("[^0-9]", "",content[position+40 :position + 45])
    print("[WeatherModule]Temp: " + str(temp))
    position = content.rfind("相 對 濕 度")
    humidity = re.sub("[^0-9]", "",content[position :position + 45])
    print("[WeatherModule]Humidity: " + str(humidity) + "%")
    position = content.rfind("http://rss.weather.gov.hk/img/pic")
    weathercode = re.sub("[^0-9]", "",content[position :position +40])
    print("[WeatherModule]Weather Code: " + str(weathercode))
    return (temp,humidity,weathercode)

def WeatherCode2IconId(wc):
    #The return value is the filename of your icon in /ghost/ui/weathericon/
    wc = int(wc)
    if wc in [50,51]:
        return "Sunny"
    elif wc in [52]:
        return "Mostly Cloudy"
    elif wc in [53,54]:
        return "Slight Drizzle"
    elif wc in [60,61]:
        return "Cloudy"
    elif wc in [62,63,64]:
        return "Drizzle"
    elif wc in [65]:
        return "Thunderstorms"
    elif wc in [70,71,72,73,74,75,76,77]:
        return "Moon"
    elif wc in [80]:
        return "Cloudy" #There is no windy icon yet
    elif wc in [84]:
        return "Haze"
    elif wc in [90,91]:
        return "Sunny"
    elif wc in [92,93]:
        return "Snow"
    else:
        return None
class Widget():
    def Launch(self,screen,startarea):
        #Initiating the Weather Widget
        size = [startarea[2],startarea[3]]
        self.pos = (startarea[0],startarea[1])
        print("[WeatherModule]Activating Weather Module with size: " + str(size) + " at location: " + str(self.pos))
        self.area = startarea      
        self.size = size
        self.screen=screen
        self.background = LoadUI("weatherui",size)
        self.screen.blit(self.background,self.pos)
        self.show = True
        self.acc = 0
        Widget.InfoUpdate(self) #Grap Information from observatory
    def update(self):
        #Update the weather widget
        self.screen.blit(self.background,self.pos)
        WriteText(self.screen,u"香港",TRP(self.pos,(165,10)),18)
        weathericon = LoadWeatherIcons(self.weathericon,(86,86))
        self.screen.blit(weathericon,TRP(self.pos,(32,10)))
        WriteText(self.screen,self.t + u"°",TRP(self.pos,(155,33)),40)
        WriteText(self.screen,self.h + u"%",TRP(self.pos,(165,73)),20)
        if self.show == False and self.pos[0] > (0 - self.size[0] + 15):
            Widget.Hide(self)
        elif self.show == False and self.pos[0] < (0 - self.size[0] + 15):
            self.pos = (0 - self.size[0] + 15,self.pos[1])
        if self.show == True and self.pos[0] < self.area[0]:
            Widget.Show(self)
        elif self.show == True and self.pos[0] > self.area[0]:
            self.pos = (self.area[0],self.area[1])
    def click_handler(self,pos):
        #handle all clicks from the main form
        if CheckInRange(pos,(self.pos[0],self.pos[1],self.size[0],self.size[1])) == True:
            #The click is happen inside this Widget
            #print("Clicked on " + str(pos))
            if self.show == True:
                self.acc = 1
                self.show = False
            else:
                self.acc = 24
                self.show = True
    def Hide(self): 
        self.acc += 1
        self.pos = (self.pos[0] - self.acc  ,self.pos[1])
    def Show(self):
        self.acc -= 1
        self.pos = (self.pos[0] +self.acc ,self.pos[1])
    def debug(self):
        GetWeatherCondition()
    def InfoUpdate(self):
        winfo = GetWeatherCondition()
        self.t = winfo[0]
        self.h = winfo[1]
        self.weathericon = WeatherCode2IconId(winfo[2])
    
#//////////////////////////////////////////////
#Debug mode for direct running this module
#//////////////////////////////////////////////
#GetWeatherCondition()
