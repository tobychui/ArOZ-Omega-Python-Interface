#///////////////////////////////////////////////////////////////////////
#News Module for ArOZ Omega Python Edition
#This News Modules shows the current news request from YAHOO rss feed.
#Intent to be used with Raspberry pi
#//////////////////////////////////////////////////////////////////////

import pygame, sys
from pygame.locals import *
import requests, re

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

def GetLatestNews(newsno):
    webrequest =  requests.get('https://hk.news.yahoo.com/rss/hong-kong')
    content = webrequest.content.decode("utf-8")
    print("[NewsModule]Requesting YAHOO! News for rss feed...")
    titles = content.split("</title>")
    titlearr = []
    i = 0
    for title in titles:
        if "<title>" in title:
            if not "Yahoo" in title and not "搜尋" in title:
                if i < newsno:
                    position = title.rfind("<title>")
                    realtitle = title[position + 7:]
                    print("[NewsModule]" + realtitle)
                    titlearr.append(realtitle)
                    i += 1
    return titlearr

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
def ArrayToSring(newsarr):
    newstring = " "
    for item in newsarr:
        #newstring += (item + "。▎◆")
        newstring += (item + "。 ")
    return newstring[:-1]

def WriteText(form,string,pos,size):
    textfont = pygame.font.Font("ghost/ui/WHJYT.ttc", size)
    text = textfont.render(string, True, (0,0,0))
    textrect = text.get_rect()
    textrect.top = pos[1]
    textrect.centerx = pos[0]
    form.blit(text, textrect)

def TRP(pos,rpos):
    #Relative Coordinate to Absolute coordinate
    tmposx = pos[0] + rpos[0]
    tmposy = pos[1] + rpos[1]
    return (tmposx,tmposy)

    
class Widget():
    def Launch(self,screen,startarea):
        #Initialize the news module
        print("[NewsModule]Activating News Feed Module...")
        self.size=[startarea[2],startarea[3]]
        self.pos = [startarea[0],startarea[1]]
        self.area = startarea
        self.screen = screen
        self.background = LoadUI("newsbar",self.size)
        self.show = True
        Widget.InfoUpdate(self)
    def update(self):
        #Update the news wedget (Text Shifting)
        textlen = 10
        sp = int(self.scroll)
        displaytext = self.news[sp:sp + textlen]
        self.screen.blit(self.background,self.pos)
        WriteText(self.screen,displaytext,TRP(self.pos,(130,10)),18)
        if self.scroll > len(self.news):
            self.scroll = 0
        else:
            self.scroll += 0.2
    def InfoUpdate(self):
        #Update the news info again
        winfo = GetLatestNews(8)
        self.news = ArrayToSring(winfo)
        self.scroll = 0
    def Draging(self,pos):
        myarea = (self.pos[0],self.pos[1],self.size[0],self.size[1])
        if CheckInRange(pos,myarea) == True: 
            self.pos = (pos[0] - self.size[0]/2,pos[1] - self.size[1]/2)
    def Hide(self):
        self.show = False
        self.pos = (0 - self.size[0] ,self.pos[1])
    def Show(self):
        self.show = True
        self.pos = (self.area[0] ,self.area[1])
        
#//////////////////////////////////////////////
#Debug mode for direct running this module
#//////////////////////////////////////////////
#arr = GetLatestNews(8)
#news = ArrayToSring(arr)
#print(news)
