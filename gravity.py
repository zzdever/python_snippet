import cv2
import numpy as np
import random
import time
import math

import gevent

import sys
import select

def heardEnter():
    i,o,e = select.select([sys.stdin],[],[],0.0001)
    for s in i:
        if s == sys.stdin:
            ink = sys.stdin.readline()
            return ink
    

filename = '/Users/ying/aa.png'
img = cv2.imread(filename)   # import as grey value
cv2.namedWindow('image')



frameDuration = 1

G = 10.0

class Dot(object):
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = 10
        self.vy = 1
        self.m = 100
        self.color = color
        
    def Move(self, m, r, gx, gy):
        dis = math.sqrt(math.pow(gx-self.x, 2) + math.pow(gy-self.y, 2))
        if dis < r:
            dis = r
        sintheta = (gy-self.y)/dis
        costheta = (gx-self.x)/dis
        dax = G*m/(dis*dis) * costheta
        day = G*m/(dis*dis) * sintheta
        self.vx = self.vx + dax
        if self.vx > 20:
            self.vx = 20
        if self.vx < -20:
            self.vx = -20
        if self.x < 0 or self.x > 900:
            self.vx = -self.vx
        self.vy = self.vy + day
        if self.vy > 20:
            self.vy = 20
        if self.vy < -20:
            self.vy = -20
        if self.y < 0 or self.y > 680:
            self.vy = -self.vy
        self.x = self.x + self.vx
        self.y = self.y + self.vy
    


gx = 400
gy = 400
gm = 2000
gr = 20

dots = []
for i in range(50): 
    r = random.randint(0,256)
    d = Dot(i*20,i*10, (r,r,r))
    dots.append(d)
  

cv2.imshow('image', img)  
cv2.waitKey(0)  

while True:
    
    k = heardEnter()
    if k != None:
        if k.strip() == 'w':
            gy = gy - 10
        if k.strip() == 's':
            gy = gy + 10
        if k.strip() == 'a':
            gx = gx - 10
        if k.strip() == 'd':
            gx = gx + 10
    
    for d in dots:
        d.Move(gm, gr, gx, gy)
        
    imgtmp = img.copy()

    cv2.circle(imgtmp,(gx, gy), gr, (255,255,255),5,8,0)
    
    for d in dots:
        cv2.circle(imgtmp,(int(d.x),int(d.y)),3,d.color,5,8,0) #point, radius, color, line size, 
    
    cv2.imshow('image', imgtmp)
    cv2.waitKey(frameDuration)
        

cv2.waitKey(0)
cv2.destroyAllWindows()
