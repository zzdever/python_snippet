import cv2
import numpy as np
import random
import time
import math as Math


filename = '/Users/ying/Italy4.jpg'
img = cv2.imread(filename, 0)   # import as grey value

#img = np.zeros((640, 480, 3), np.int32)

cv2.namedWindow('image')




frameDuration = 1

keyIndices = {0:1, 5000:2}


def indexOfNearestKey(time):
    mindis = 5000
    minindex = keyIndices.keys()[0]
    for i in keyIndices.keys():
        if mindis > abs(time-i):
            mindis = abs(time-i)
            minindex = i
    return keyIndices[minindex]
    
def timeOfkey(n):
    for i in keyIndices.keys():
        if keyIndices[i] == n:
            return 1.0*i/1000
    
def Value(time):
    return 1.0*time/5
    

def velocityAtTime(interval):
    pass
    
def GetValue(time):
    amp = 0.1
    freq = 70.0
    decay = 50.0
    
    numKeys = len(keyIndices)
    
    n = 0
    if numKeys > 0:
    	n = indexOfNearestKey(int(1000*time))
    	if (timeOfkey(n) > time):
            n = n - 1
  
    if n == 0:
    	t = 0
    else:
        t = time - timeOfkey(n)

    if n > 0:
    	v = 1#velocityAtTime( timeOfkey(n)  - frameDuration/10 )
    	return (Value(time) + v * amp * Math.sin(freq*t*2*Math.pi) / (Math.exp(decay*t)))
    else:
    	return Value(time)




while True:
    time = 0
    for i in range(100):
        time = time + frameDuration
        radius = GetValue(1.0*time/1000)*1000 + 100
        if radius<0:
            radius = 0

        imgtmp = img.copy()
        cv2.circle(imgtmp,(int(radius)+100,20), 10,(0,255,255),5,8,0) 
    
    
        cv2.circle(imgtmp,(100,300),int(radius)/2,(0,255,255),5,8,0)
        cv2.circle(imgtmp,(400,200),int(radius)/3,(0,255,255),5,8,0) 
        r2 = (50+120)/3-int(radius)/3
        if r2<0:
            r2 = 0
        cv2.circle(imgtmp,(400+(44+120)/3,200), r2,(0,255,255),5,8,0) 
    
        cv2.circle(imgtmp,(300,200),int(radius),(0,255,255),5,8,0) #point, radius, color, line size, 
        cv2.imshow('image', imgtmp)
        cv2.waitKey(frameDuration)
        
    cv2.waitKey(2)


cv2.waitKey(0)
cv2.destroyAllWindows()
