# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import math
import pygame
import random
import time
pygame.init()
WIDTH, HEIGHT=800,600
WIN=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("AIM TRAINER")
tarinc=400
tarevent=pygame.USEREVENT
tarpadding=30
Lives=10
top_bar_height=50
Label_font=pygame.font.SysFont("comicsans", 24)
class Target:
    msize=30
    grate=0.2
    color="red"
    scolor="yellow"
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.grow=True
        self.size=0
    def update(self):
        if self.size+self.grate>=self.msize:
            self.grow=False
        if self.grow:
            self.size+=self.grate
        else:
            self.size-=self.grate
    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.x,self.y),self.size)
        pygame.draw.circle(win,self.scolor,(self.x,self.y),self.size*0.8)
        pygame.draw.circle(win,self.color,(self.x,self.y),self.size*0.6)
        pygame.draw.circle(win,self.scolor,(self.x,self.y),self.size*0.4)
    def collide(self,x,y):
        dis=math.sqrt((self.x-x)**2+(self.y-y)**2)
        return dis<=self.size
        
def draw(win,targets):
    win.fill("green")
    for target in targets:
        target.draw(win)
    
    

def format_time(secs):
    milli=math.floor(int(secs*1000%1000)/100)
    seconds=int(round(secs%60,1))
    minutes=int(secs//60)
    return f"{minutes:02d}:{seconds:02d}.{milli}"

def draw_top_bar(win,elapsed_time,tarpress,miss):
    pygame.draw.rect(win,"skyblue",(0,0,WIDTH,top_bar_height))
    timelabel=Label_font.render(f"Time: {format_time(elapsed_time)}",1,"black")
    speed=round(tarpress/elapsed_time,1)
    speedlabel=Label_font.render(f"speed: {speed} t/s",1,"black")
    hitlabel=Label_font.render(f"Hits: {tarpress}",1,"black")
    liveslabel=Label_font.render(f"lives: {Lives-miss}",1,"black")   
    
    win.blit(timelabel,(5,5))
    win.blit(speedlabel,(200,5))
    win.blit(hitlabel, (450,5))
    win.blit(liveslabel,(650,5))

def endscreen(win,elapsed_time,tarpress,clicks):
    win.fill("green")
    timelabel=Label_font.render(f"Time: {format_time(elapsed_time)}",1,"black")
    speed=round(tarpress/elapsed_time,1)
    speedlabel=Label_font.render(f"speed: {speed} t/s",1,"black")
    hitlabel=Label_font.render(f"Hits: {tarpress}",1,"black")
    accuracy=round((tarpress/clicks)*100,1)     
    accuracylabel=Label_font.render(f"Accuracy: {accuracy}%",1,"black")
    win.blit(timelabel,(getmiddle(timelabel),100))
    win.blit(speedlabel,(getmiddle(speedlabel),200))
    win.blit(hitlabel,(getmiddle(hitlabel),300))
    win.blit(accuracylabel,(getmiddle(accuracylabel),400))    
    
    pygame.display.update()
    run=True
    while run:
        for event in pygame.event.get():
            if event.type==pygame.QUIT or event.type==pygame.KEYDOWN:
                pygame.quit()
    
def getmiddle(surface):
    return WIDTH/2 - surface.get_width()/2

def main():
    run=True
    targets=[]
    clk=pygame.time.Clock()
    tarpress=0
    miss=0
    clicks=0
    start=time.time()
    pygame.time.set_timer(tarevent, tarinc)
    while run:
        clk.tick(60)
        click=False
        mouseposition=pygame.mouse.get_pos()
        elapsed_time=time.time()-start
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
                break
            if event.type==tarevent:
                x=random.randint(tarpadding, WIDTH-tarpadding)
                y=random.randint(tarpadding + top_bar_height, HEIGHT-tarpadding)
                target=Target(x, y)
                targets.append(target)
            
            if event.type==pygame.MOUSEBUTTONDOWN:
                click=True
                clicks+=1
        for target in targets:
            target.update()
            if target.size<=0:
                targets.remove(target)
                miss+=1
            if click and target.collide(*mouseposition):
                targets.remove(target)
                tarpress+=1
        if miss>=Lives:
            endscreen(WIN, elapsed_time, tarpress, clicks)
        draw(WIN, targets)
        draw_top_bar(WIN,elapsed_time,tarpress,miss)
        pygame.display.update()
    pygame.quit()

if __name__=="__main__":
    main()