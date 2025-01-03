import time, math, os, random
import _thread
import copy
from collections import namedtuple
from colorama import Fore
from socket import *
import pickle
import sys

textTime = 0
torpedoSpeed = 50.0
framerate = 50

die1Bit = 0
die2Bit = 0
die3Bit = 0

hit1 = 0
hit2 = 0
hit3 = 0
hit4 = 0
hit5 = 0
hit6 = 0

flag1 = True

flagSock = True

torpedoID1 = 0
torpedoID2 = 0
torpedoID3 = 0
torpedoID4 = 0
torpedoID5 = 0

shellID1 = 0
shellID2 = 0


myHost = ''
myPort = 50045
socketOutData = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]


level1 = [[0,0,0,0,0,0,0,0,0,0],
          [0,1,1,1,0,0,0,1,1,0],
          [0,0,0,0,0,0,0,0,1,0],
          [0,0,0,0,1,1,0,0,0,0],
          [0,0,0,1,1,1,0,0,0,0],
          [1,0,0,0,0,1,1,0,0,0],
          [1,0,0,0,0,1,0,0,0,0],
          [0,0,1,1,0,0,0,0,0,1],
          [0,0,1,1,0,0,0,1,1,0],
          [0,0,0,0,0,0,0,0,0,0]]


socketInData =  [[],[],[],[],[]]
#Crew = namedtuple('Crew',['FTOR','CREW','COMMAND','ENGINE','ATOR'])

if len(sys.argv) > 1:
    myPort = int(sys.argv[1])

startTime = time.time()


def delay(t):
    time.sleep(float(t)/1000.0)
def clear():
    os.system('clear')
def get2digit(num):
    num = num % 10
    return num

def getCrewPoints(data):
    return (data[0]*3) + data[1]

def getDigitNum(num):
    digit = 0
    if num == 0:
        return 1
    while num >= 1:
        digit += 1
        num = num / 10
    return digit
def makeDigits(num,digits):
    d = getDigitNum(num)
    return (' '*(digits-d))+str(num)

def inLimit(num,min1,max1):
    if (num < max1) and (num > min1):
        return True
    else:
        return False
def getHitPos(torpedoPos,pos,angle):
    x = math.cos(math.radians(angle))*15
    y = math.sin(math.radians(angle))*15

    frontPos = [pos[0]+x,pos[1]+y]
    rearPos = [pos[0]-x,pos[1]-y]

    frontDis = math.dist(torpedoPos,frontPos)
    rearDis = math.dist(torpedoPos,rearPos)
    centerDis = math.dist(torpedoPos,pos)

    a = min(frontDis,rearDis,centerDis)
    if a == frontDis:
        return 0,frontDis
    elif a == rearDis:
        return 2,rearDis
    elif a == centerDis:
        return 1,centerDis

class Uboat:
    def __init__(self, speed, fTorpedoNum, aTorpedoNum, crewNum, health, position,orientation,depth):
        self.speed = speed
        self.fTorpedoNum = fTorpedoNum
        self.aTorpedoNum = aTorpedoNum
        self.crewNum = crewNum
        self.health = health
        self.position = position
        self.orientation = orientation
        self.depth = depth
        self.shellNum = 2
    def detect(self,pos1,pos2):
        distance = math.dist(pos1,pos2)
        angle = math.atan((pos1[1]-pos2[1])/(pos1[0]-pos2[0]))
        angle = math.degrees(angle)
        if (pos1[0] - pos2[0]) > 0:
            angle = (180-angle)*-1
        if angle > 180:
            angle = (360-angle)*-1
        if angle < -180:
            angle = (360+angle)*-1
        return round(distance,2), angle+(self.orientation*-1)
    def setCourse(self,course):
        if course > self.orientation:
            while True:
                self.orientation += 1
                delay(100)
                if self.orientation >= course:
                    break
        elif course < self.orientation:
            while True:
                self.orientation -= 1
                delay(100)
                if self.orientation <= course:
                    break
        elif course == self.orientation:
            self.orientation = course
    def setSpeed(self,newSpeed):
        self.speed = newSpeed
    def setDepth(self,newDepth):
        if newDepth > self.depth:
            while True:
                self.depth += 1
                delay(500)
                if self.depth >= newDepth:
                    break
        elif newDepth < self.depth:
            while True:
                self.depth -= 1
                delay(500)
                if self.depth <= newDepth:
                    break
        elif newDepth == self.depth:
            self.depth = newDepth
    def calcNewPos(self,passedTime):
        hypo = passedTime * self.speed
        x = math.cos(math.radians(self.orientation)) * hypo
        y = math.sin(math.radians(self.orientation)) * hypo
        self.position[0] = self.position[0] + x
        self.position[1] = self.position[1] + y
    def reloadTube(self,tube):
        while True:
            if tube == 0:
                while getCrewPoints(self.crewNum[0]) != 0:
                    if self.fTorpedoNum < 4:
                        delay((31-getCrewPoints(self.crewNum[0]))*4000)
                        self.fTorpedoNum += 1
                    delay(1000/framerate)
            elif tube == 1:
                while getCrewPoints(self.crewNum[4]) != 0:
                    if self.aTorpedoNum < 2:
                        delay((31-getCrewPoints(self.crewNum[4]))*4000)
                        self.aTorpedoNum += 1
                    delay(1000/framerate)

            delay(1000/framerate)
    def reloadShell(self):
        while True:
            #if tube == 0:
            while getCrewPoints(self.crewNum[6]) != 0:
                if self.shellNum < 2:
                    delay((31-getCrewPoints(self.crewNum[6]))*4000)
                    self.shellNum += 1
                delay(1000/framerate)
            delay(1000/framerate)
class Torpedo:
    def __init__(self, name, speed, firepower, orientation, position, hit):
        self.name = name
        self.speed = speed
        self.firepower = 20
        self.orientation = orientation
        self.position = position
        self.hit = hit

    def fireTorpedo(self,n):
        #targetPosition = copy.deepcopy(self.position)
        #torpedoID += 1
        #torpedoID = 0
        global torpedoID1,torpedoID2,torpedoID3,torpedoID4,torpedoID5
        global level1
        hypo = (1/framerate) * self.speed
        x = math.cos(math.radians(self.orientation)) * hypo
        y = math.sin(math.radians(self.orientation)) * hypo

        if n == '0':
            sHypo = (1/framerate) * myBoat1.speed
            sX = math.cos(math.radians(myBoat1.orientation)) * hypo
            sY = math.sin(math.radians(myBoat1.orientation)) * hypo
        if n == '1':
            sHypo = (1/framerate) * myBoat2.speed
            sX = math.cos(math.radians(myBoat2.orientation)) * hypo
            sY = math.sin(math.radians(myBoat2.orientation)) * hypo
        if n == '2':
            sHypo = (1/framerate) * myBoat3.speed
            sX = math.cos(math.radians(myBoat3.orientation)) * hypo
            sY = math.sin(math.radians(myBoat3.orientation)) * hypo
        if n == '3':
            sHypo = (1/framerate) * myBoat4.speed
            sX = math.cos(math.radians(myBoat4.orientation)) * hypo
            sY = math.sin(math.radians(myBoat4.orientation)) * hypo
        if n == '4':
            sHypo = (1/framerate) * myBoat5.speed
            sX = math.cos(math.radians(myBoat5.orientation)) * hypo
            sY = math.sin(math.radians(myBoat5.orientation)) * hypo

        flag = True
        while flag:
            self.position[0] = self.position[0] + x + sX
            self.position[1] = self.position[1] + y + sY
           # try:
                #print(torpedo0a.position,self.name)
            #except:
            #    pass
            #print(targetPosition)
            if n == '0':
                if math.dist(self.position,myBoat1.position) > 1000.0:
                    break

                if math.dist(self.position,myBoat2.position) <= 30.0:
                    index,dis = getHitPos(self.position,myBoat2.position,myBoat2.orientation)
                    myBoat2.health[index] -= self.firepower/(dis/30)

                    self.hit = 1
                    break
                if math.dist(self.position,myBoat3.position) <= 30.0:
                    index,dis = getHitPos(self.position,myBoat3.position,myBoat3.orientation)
                    myBoat3.health[index] -= self.firepower/(dis/30)
                    self.hit = 1
                    break
                if math.dist(self.position,myBoat4.position) <= 30.0:
                    index,dis = getHitPos(self.position,myBoat4.position,myBoat4.orientation)
                    myBoat4.health[index] -= self.firepower/(dis/30)
                    self.hit = 1
                    break
                if math.dist(self.position,myBoat5.position) <= 30.0:
                    index,dis = getHitPos(self.position,myBoat5.position,myBoat5.orientation)
                    myBoat5.health[index] -= self.firepower/(dis/30)
                    self.hit = 1
                    break
            elif n == '1':
                if math.dist(self.position,myBoat2.position) > 1000.0:
                    break

                if math.dist(self.position,myBoat1.position) <= 30.0:
                    index,dis = getHitPos(self.position,myBoat1.position,myBoat1.orientation)
                    myBoat1.health[index] -= self.firepower/(dis/30)
                    self.hit = 1
                    break
                if math.dist(self.position,myBoat3.position) <= 30.0:
                    index,dis = getHitPos(self.position,myBoat3.position,myBoat3.orientation)
                    myBoat3.health[index] -= self.firepower/(dis/30)
                    self.hit = 1
                    break
                if math.dist(self.position,myBoat4.position) <= 30.0:
                    index,dis = getHitPos(self.position,myBoat4.position,myBoat4.orientation)
                    myBoat4.health[index] -= self.firepower/(dis/30)
                    self.hit = 1
                    break
                if math.dist(self.position,myBoat5.position) <= 30.0:
                    index,dis = getHitPos(self.position,myBoat5.position,myBoat5.orientation)
                    myBoat5.health[index] -= self.firepower/(dis/30)
                    self.hit = 1
                    break
            elif n == '2':
                if math.dist(self.position,myBoat3.position) > 1000.0:
                    break

                if math.dist(self.position,myBoat1.position) <= 30.0:
                    index,dis = getHitPos(self.position,myBoat1.position,myBoat1.orientation)
                    myBoat1.health[index] -= self.firepower/(dis/30)
                    self.hit = 1
                    break
                if math.dist(self.position,myBoat2.position) <= 30.0:
                    index,dis = getHitPos(self.position,myBoat2.position,myBoat2.orientation)
                    myBoat2.health[index] -= self.firepower/(dis/30)
                    self.hit = 1
                    break
                if math.dist(self.position,myBoat4.position) <= 30.0:
                    index,dis = getHitPos(self.position,myBoat4.position,myBoat4.orientation)
                    myBoat4.health[index] -= self.firepower/(dis/30)
                    self.hit = 1
                    break
                if math.dist(self.position,myBoat5.position) <= 30.0:
                    index,dis = getHitPos(self.position,myBoat5.position,myBoat5.orientation)
                    myBoat5.health[index] -= self.firepower/(dis/30)
                    self.hit = 1
                    break
            elif n == '3':
                if math.dist(self.position,myBoat4.position) > 1000.0:
                    break

                if math.dist(self.position,myBoat1.position) <= 30.0:
                    index,dis = getHitPos(self.position,myBoat1.position,myBoat1.orientation)
                    myBoat1.health[index] -= self.firepower/(dis/30)
                    self.hit = 1
                    break
                if math.dist(self.position,myBoat2.position) <= 30.0:
                    index,dis = getHitPos(self.position,myBoat2.position,myBoat2.orientation)
                    myBoat2.health[index] -= self.firepower/(dis/30)
                    self.hit = 1
                    break
                if math.dist(self.position,myBoat3.position) <= 30.0:
                    index,dis = getHitPos(self.position,myBoat3.position,myBoat3.orientation)
                    myBoat3.health[index] -= self.firepower/(dis/30)
                    self.hit = 1
                    break
                if math.dist(self.position,myBoat5.position) <= 30.0:
                    index,dis = getHitPos(self.position,myBoat5.position,myBoat5.orientation)
                    myBoat5.health[index] -= self.firepower/(dis/30)
                    self.hit = 1
                    break
            elif n == '4':
                if math.dist(self.position,myBoat5.position) > 1000.0:
                    break

                if math.dist(self.position,myBoat1.position) <= 30.0:
                    index,dis = getHitPos(self.position,myBoat1.position,myBoat1.orientation)
                    myBoat1.health[index] -= self.firepower/(dis/30)
                    self.hit = 1
                    break
                if math.dist(self.position,myBoat2.position) <= 30.0:
                    index,dis = getHitPos(self.position,myBoat2.position,myBoat2.orientation)
                    myBoat2.health[index] -= self.firepower/(dis/30)
                    self.hit = 1
                    break
                if math.dist(self.position,myBoat3.position) <= 30.0:
                    index,dis = getHitPos(self.position,myBoat3.position,myBoat3.orientation)
                    myBoat3.health[index] -= self.firepower/(dis/30)
                    self.hit = 1
                    break
                if math.dist(self.position,myBoat4.position) <= 30.0:
                    index,dis = getHitPos(self.position,myBoat4.position,myBoat4.orientation)
                    myBoat4.health[index] -= self.firepower/(dis/30)
                    self.hit = 1
                    break
            #else:
                #return False
            for y1 in range(0,len(level1)):
                for x1 in range(0,len(level1[y1])):
                    if level1[y1][x1] == 1:
                        if inLimit(self.position[0],x1*1000-1,x1*1000+1001) == True and inLimit(self.position[1],y1*1000-1,y1*1000+1001) == True:
                            flag = False
            delay(1000/framerate)

        self.position = [0,0]

        if n == '0':
            torpedoID1 -= 1
        if n == '1':
            torpedoID2 -= 1
        if n == '2':
            torpedoID3 -= 1
        if n == '3':
            torpedoID4 -= 1
        if n == '4':
            torpedoID5 -= 1

class Shell:
    def __init__(self,velocity,position,orientation,angle,firepower,hit):
        self.velocity = velocity
        self.position = position
        self.orientation = orientation
        self.angle = angle
        self.firepower = firepower
        self.hit = hit
        self.height = 0
        self.vx = math.cos(math.radians(self.angle))*self.velocity
        self.vy = math.sin(math.radians(self.angle))*self.velocity
    def fireShell(self,n):
        global framerate
        global shellID1,shellID2
        t = 1/framerate
        hypo = t * self.vx

        x = math.cos(math.radians(self.orientation)) * hypo
        y = math.sin(math.radians(self.orientation)) * hypo

        if n == '0':
            sHypo = (1/framerate) * myBoat1.speed
            sX = math.cos(math.radians(myBoat1.orientation)) * hypo
            sY = math.sin(math.radians(myBoat1.orientation)) * hypo
        if n == '1':
            sHypo = (1/framerate) * myBoat2.speed
            sX = math.cos(math.radians(myBoat2.orientation)) * hypo
            sY = math.sin(math.radians(myBoat2.orientation)) * hypo
        if n == '2':
            sHypo = (1/framerate) * myBoat3.speed
            sX = math.cos(math.radians(myBoat3.orientation)) * hypo
            sY = math.sin(math.radians(myBoat3.orientation)) * hypo
        if n == '3':
            sHypo = (1/framerate) * myBoat4.speed
            sX = math.cos(math.radians(myBoat4.orientation)) * hypo
            sY = math.sin(math.radians(myBoat4.orientation)) * hypo
        if n == '4':
            sHypo = (1/framerate) * myBoat5.speed
            sX = math.cos(math.radians(myBoat5.orientation)) * hypo
            sY = math.sin(math.radians(myBoat5.orientation)) * hypo

        while True:
            time.sleep(t)
            #hypo = t * self.vx


            self.position[0] = self.position[0] + x + sX
            self.position[1] = self.position[1] + y + sY

            self.vy = self.vy + (-9.8*t)
            self.height = self.height + self.vy*t
            #print("Pos: ",x,y)
            #print("Vel: ",vy)
            if self.height <= 0:
                break

        if n == '0':
            if math.dist(self.position,myBoat2.position) <= 30.0:
                index,dis = getHitPos(self.position,myBoat2.position,myBoat2.orientation)
                myBoat2.health[index] -= self.firepower/(dis/30)

                self.hit = 1

            if math.dist(self.position,myBoat3.position) <= 30.0:
                index,dis = getHitPos(self.position,myBoat3.position,myBoat3.orientation)
                myBoat3.health[index] -= self.firepower/(dis/30)
                self.hit = 1

            if math.dist(self.position,myBoat4.position) <= 30.0:
                index,dis = getHitPos(self.position,myBoat4.position,myBoat4.orientation)
                myBoat4.health[index] -= self.firepower/(dis/30)
                self.hit = 1

            if math.dist(self.position,myBoat5.position) <= 30.0:
                index,dis = getHitPos(self.position,myBoat5.position,myBoat5.orientation)
                myBoat5.health[index] -= self.firepower/(dis/30)
                self.hit = 1

        elif n == '1':
            if math.dist(self.position,myBoat1.position) <= 30.0:
                index,dis = getHitPos(self.position,myBoat1.position,myBoat1.orientation)
                myBoat1.health[index] -= self.firepower/(dis/30)
                self.hit = 1

            if math.dist(self.position,myBoat3.position) <= 30.0:
                index,dis = getHitPos(self.position,myBoat3.position,myBoat3.orientation)
                myBoat3.health[index] -= self.firepower/(dis/30)
                self.hit = 1

            if math.dist(self.position,myBoat4.position) <= 30.0:
                index,dis = getHitPos(self.position,myBoat4.position,myBoat4.orientation)
                myBoat4.health[index] -= self.firepower/(dis/30)
                self.hit = 1

            if math.dist(self.position,myBoat5.position) <= 30.0:
                index,dis = getHitPos(self.position,myBoat5.position,myBoat5.orientation)
                myBoat5.health[index] -= self.firepower/(dis/30)
                self.hit = 1

        elif n == '2':
            if math.dist(self.position,myBoat1.position) <= 30.0:
                index,dis = getHitPos(self.position,myBoat1.position,myBoat1.orientation)
                myBoat1.health[index] -= self.firepower/(dis/30)
                self.hit = 1

            if math.dist(self.position,myBoat2.position) <= 30.0:
                index,dis = getHitPos(self.position,myBoat2.position,myBoat2.orientation)
                myBoat2.health[index] -= self.firepower/(dis/30)
                self.hit = 1

            if math.dist(self.position,myBoat4.position) <= 30.0:
                index,dis = getHitPos(self.position,myBoat4.position,myBoat4.orientation)
                myBoat4.health[index] -= self.firepower/(dis/30)
                self.hit = 1

            if math.dist(self.position,myBoat5.position) <= 30.0:
                index,dis = getHitPos(self.position,myBoat5.position,myBoat5.orientation)
                myBoat5.health[index] -= self.firepower/(dis/30)
                self.hit = 1

        elif n == '3':
            if math.dist(self.position,myBoat1.position) <= 30.0:
                index,dis = getHitPos(self.position,myBoat1.position,myBoat1.orientation)
                myBoat1.health[index] -= self.firepower/(dis/30)
                self.hit = 1

            if math.dist(self.position,myBoat2.position) <= 30.0:
                index,dis = getHitPos(self.position,myBoat2.position,myBoat2.orientation)
                myBoat2.health[index] -= self.firepower/(dis/30)
                self.hit = 1

            if math.dist(self.position,myBoat3.position) <= 30.0:
                index,dis = getHitPos(self.position,myBoat3.position,myBoat3.orientation)
                myBoat3.health[index] -= self.firepower/(dis/30)
                self.hit = 1

            if math.dist(self.position,myBoat5.position) <= 30.0:
                index,dis = getHitPos(self.position,myBoat5.position,myBoat5.orientation)
                myBoat5.health[index] -= self.firepower/(dis/30)
                self.hit = 1

        elif n == '4':
            if math.dist(self.position,myBoat1.position) <= 30.0:
                index,dis = getHitPos(self.position,myBoat1.position,myBoat1.orientation)
                myBoat1.health[index] -= self.firepower/(dis/30)
                self.hit = 1

            if math.dist(self.position,myBoat2.position) <= 30.0:
                index,dis = getHitPos(self.position,myBoat2.position,myBoat2.orientation)
                myBoat2.health[index] -= self.firepower/(dis/30)
                self.hit = 1

            if math.dist(self.position,myBoat3.position) <= 30.0:
                index,dis = getHitPos(self.position,myBoat3.position,myBoat3.orientation)
                myBoat3.health[index] -= self.firepower/(dis/30)
                self.hit = 1

            if math.dist(self.position,myBoat4.position) <= 30.0:
                index,dis = getHitPos(self.position,myBoat4.position,myBoat4.orientation)
                myBoat4.health[index] -= self.firepower/(dis/30)
                self.hit = 1

        self.position = [0,0]
        if n == '0':
            shellID1 -= 1
        if n == '1':
            shellID2 -= 1

#class Rock:
#    def __init__(self, name, position):
#        self.name = name
#        self.position = position

def printText(string,end='\n',color=Fore.GREEN):
    print(color,end='')
    for i in string:
        print(i, end = '' , flush = True)
        delay(textTime)
    print(Fore.GREEN,end='')
    if end == '\n':
        print()

def displayStart():
    for i in range(0,50):
        clear()
        print('-'*150)
        print(' '*i,"                  ")
        print(' '*i,"         ****     ")
        print(' '*i,"         *  *     ")
        print(' '*i," **************** ")
        print(' '*i,"*                *")
        print(' '*i," **************** ")
        print(' '*i,"                  ")
        delay(100)
    #printText("  ******   ***  ***      ******  **     **  *****         ***                           ")
    #printText("  **       ***  ***      **      ****   **  *****         ***                     ")
    #printText("  ******   ***  ***      ******  ** **  **   **           ***                          ")
    #printText("      **   ***  *******  **      **  ** **   **                                 ")
    #printText("  ******   ***  *******  ******  **   ****   **                                     ")
    #printText("                                                          ")
    #printText("                                                           ")
def calculateBoat(objectID):
    while True:
        objectID.calcNewPos(1/framerate)
        delay(1000/framerate)
        if objectID.health[0] <= 0 or objectID.health[1] <= 0 or objectID.health[2] <= 0:
            objectID.position == [0,0]
            break
        #if int(socketInData[i][1]/1000)+1

def torpedoThread(name):
    name.fireTorpedo()

def torCalc(connectionID,torpedoID,tube,c):
    global torpedo0a,torpedo1a,torpedo2a,torpedo3a,torpedo4a,torpedo5a,torpedo0b,torpedo1b,torpedo2b,torpedo3b,torpedo4b,torpedo5b,torpedo0c,torpedo1c,torpedo2c,torpedo3c,torpedo4c,torpedo5c,torpedo0d,torpedo1d,torpedo2d,torpedo3d,torpedo4d,torpedo5d,torpedo0e,torpedo1e,torpedo2e,torpedo3e,torpedo4e,torpedo5e

    if connectionID == 0:
        if torpedoID == 0:
            #print("fire torpedo0a")
            torpedo0a = Torpedo("torpedo0a",torpedoSpeed, 50, myBoat1.orientation+c, copy.deepcopy(myBoat1.position),0)
            _thread.start_new_thread(torpedo0a.fireTorpedo,("0",))
        if torpedoID == 1:
            #print("fire torpedo1a")
            torpedo1a = Torpedo("torpedo1a",torpedoSpeed, 50, myBoat1.orientation+c, copy.deepcopy(myBoat1.position),0)
            _thread.start_new_thread(torpedo1a.fireTorpedo,("0",))
        if torpedoID == 2:
            #print("fire torpedo2a")
            torpedo2a = Torpedo("torpedo2a",torpedoSpeed, 50, myBoat1.orientation+c, copy.deepcopy(myBoat1.position),0)
            _thread.start_new_thread(torpedo2a.fireTorpedo,("0",))
        if torpedoID == 3:
            torpedo3a = Torpedo("torpedo3a",torpedoSpeed, 50, myBoat1.orientation+c, copy.deepcopy(myBoat1.position),0)
            _thread.start_new_thread(torpedo3a.fireTorpedo,("0",))
        if torpedoID == 4:
            torpedo4a = Torpedo("torpedo4a",torpedoSpeed, 50, myBoat1.orientation+c, copy.deepcopy(myBoat1.position),0)
            _thread.start_new_thread(torpedo4a.fireTorpedo,("0",))
        if torpedoID == 5:
            torpedo5a = Torpedo("torpedo5a",torpedoSpeed, 50, myBoat1.orientation+c, copy.deepcopy(myBoat1.position),0)
            _thread.start_new_thread(torpedo5a.fireTorpedo,("0",))
        if tube == 1:
            myBoat1.fTorpedoNum -= 1
        elif tube == 2:
            myBoat1.aTorpedoNum -= 1
    if connectionID == 1:
        if torpedoID == 0:
            torpedo0b = Torpedo("torpedo0b",torpedoSpeed, 50, myBoat2.orientation+c, copy.deepcopy(myBoat2.position),0)
            _thread.start_new_thread(torpedo0b.fireTorpedo,("1",))
        if torpedoID == 1:
            torpedo1b = Torpedo("torpedo1b",torpedoSpeed, 50, myBoat2.orientation+c, copy.deepcopy(myBoat2.position),0)
            _thread.start_new_thread(torpedo1b.fireTorpedo,("1",))
        if torpedoID == 2:
            torpedo2b = Torpedo("torpedo2b",torpedoSpeed, 50, myBoat2.orientation+c, copy.deepcopy(myBoat2.position),0)
            _thread.start_new_thread(torpedo2b.fireTorpedo,("1",))
        if torpedoID == 3:
            torpedo3b = Torpedo("torpedo3b",torpedoSpeed, 50, myBoat2.orientation+c, copy.deepcopy(myBoat2.position),0)
            _thread.start_new_thread(torpedo3b.fireTorpedo,("1",))
        if torpedoID == 4:
            torpedo4b = Torpedo("torpedo4b",torpedoSpeed, 50, myBoat2.orientation+c, copy.deepcopy(myBoat2.position),0)
            _thread.start_new_thread(torpedo4b.fireTorpedo,("1",))
        if torpedoID == 5:
            torpedo5b = Torpedo("torpedo5b",torpedoSpeed, 50, myBoat2.orientation+c, copy.deepcopy(myBoat2.position),0)
            _thread.start_new_thread(torpedo5b.fireTorpedo,("1",))
        if tube == 1:
            myBoat2.fTorpedoNum -= 1
        elif tube == 2:
            myBoat2.aTorpedoNum -= 1
    if connectionID == 2:
        if torpedoID == 0:
            torpedo0c = Torpedo("torpedo0c",torpedoSpeed, 50, myBoat3.orientation+c, copy.deepcopy(myBoat3.position),0)
            _thread.start_new_thread(torpedo0c.fireTorpedo,("2",))
        if torpedoID == 1:
            torpedo1c = Torpedo("torpedo1c",torpedoSpeed, 50, myBoat3.orientation+c, copy.deepcopy(myBoat3.position),0)
            _thread.start_new_thread(torpedo1c.fireTorpedo,("2",))
        if torpedoID == 2:
            torpedo2c = Torpedo("torpedo2c",torpedoSpeed, 50, myBoat3.orientation+c, copy.deepcopy(myBoat3.position),0)
            _thread.start_new_thread(torpedo2c.fireTorpedo,("2",))
        if torpedoID == 3:
            torpedo3c = Torpedo("torpedo3c",torpedoSpeed, 50, myBoat3.orientation+c, copy.deepcopy(myBoat3.position),0)
            _thread.start_new_thread(torpedo3c.fireTorpedo,("2",))
        if torpedoID == 4:
            torpedo4c = Torpedo("torpedo4c",torpedoSpeed, 50, myBoat3.orientation+c, copy.deepcopy(myBoat3.position),0)
            _thread.start_new_thread(torpedo4c.fireTorpedo,("2",))
        if torpedoID == 5:
            torpedo5c = Torpedo("torpedo5c",torpedoSpeed, 50, myBoat3.orientation+c, copy.deepcopy(myBoat3.position),0)
            _thread.start_new_thread(torpedo5c.fireTorpedo,("2",))
        if tube == 1:
            myBoat3.fTorpedoNum -= 1
        elif tube == 2:
            myBoat3.aTorpedoNum -= 1
    if connectionID == 3:
        if torpedoID == 0:
            torpedo0d = Torpedo("torpedo0d",torpedoSpeed, 50, myBoat4.orientation+c, copy.deepcopy(myBoat4.position),0)
            _thread.start_new_thread(torpedo0d.fireTorpedo,("3",))
        if torpedoID == 1:
            torpedo1d = Torpedo("torpedo1d",torpedoSpeed, 50, myBoat4.orientation+c, copy.deepcopy(myBoat4.position),0)
            _thread.start_new_thread(torpedo1d.fireTorpedo,("3",))
        if torpedoID == 2:
            torpedo2d = Torpedo("torpedo2d",torpedoSpeed, 50, myBoat4.orientation+c, copy.deepcopy(myBoat4.position),0)
            _thread.start_new_thread(torpedo2d.fireTorpedo,("3",))
        if torpedoID == 3:
            torpedo3d = Torpedo("torpedo3d",torpedoSpeed, 50, myBoat4.orientation+c, copy.deepcopy(myBoat4.position),0)
            _thread.start_new_thread(torpedo3d.fireTorpedo,("3",))
        if torpedoID == 4:
            torpedo4d = Torpedo("torpedo4d",torpedoSpeed, 50, myBoat4.orientation+c, copy.deepcopy(myBoat4.position),0)
            _thread.start_new_thread(torpedo4d.fireTorpedo,("3",))
        if torpedoID == 5:
            torpedo5d = Torpedo("torpedo5d",torpedoSpeed, 50, myBoat4.orientation+c, copy.deepcopy(myBoat4.position),0)
            _thread.start_new_thread(torpedo5d.fireTorpedo,("3",))
        if tube == 1:
            myBoat4.fTorpedoNum -= 1
        elif tube == 2:
            myBoat4.aTorpedoNum -= 1
    if connectionID == 4:
        if torpedoID == 0:
            torpedo0e = Torpedo("torpedo0e",torpedoSpeed, 50, myBoat5.orientation+c, copy.deepcopy(myBoat5.position),0)
            _thread.start_new_thread(torpedo0e.fireTorpedo,("4",))
        if torpedoID == 1:
            torpedo1e = Torpedo("torpedo1e",torpedoSpeed, 50, myBoat5.orientation+c, copy.deepcopy(myBoat5.position),0)
            _thread.start_new_thread(torpedo1e.fireTorpedo,("4",))
        if torpedoID == 2:
            torpedo2e = Torpedo("torpedo2e",torpedoSpeed, 50, myBoat5.orientation+c, copy.deepcopy(myBoat5.position),0)
            _thread.start_new_thread(torpedo2e.fireTorpedo,("4",))
        if torpedoID == 3:
            torpedo3e = Torpedo("torpedo3e",torpedoSpeed, 50, myBoat5.orientation+c, copy.deepcopy(myBoat5.position),0)
            _thread.start_new_thread(torpedo3e.fireTorpedo,("4",))
        if torpedoID == 4:
            torpedo4e = Torpedo("torpedo4e",torpedoSpeed, 50, myBoat5.orientation+c, copy.deepcopy(myBoat5.position),0)
            _thread.start_new_thread(torpedo4e.fireTorpedo,("4",))
        if torpedoID == 5:
            torpedo5e = Torpedo("torpedo5e",torpedoSpeed, 50, myBoat5.orientation+c, copy.deepcopy(myBoat5.position),0)
            _thread.start_new_thread(torpedo5e.fireTorpedo,("4",))
        if tube == 1:
            myBoat5.fTorpedoNum -= 1
        elif tube == 2:
            myBoat5.aTorpedoNum -= 1

def shellCalc(connectionID,shellID,course,angle):
    global shell0a,shell1a,shell0b,shell1b,shell0c,shell1c,shell0d,shell1d,shell0e,shell1e
    if connectionID == 0:
        if shellID == 0:
            shell0a = Shell(300,copy.deepcopy(myBoat1.position),myBoat1.orientation+course,angle,30,0)
            _thread.start_new_thread(shell0a.fireShell,("0",))
        if shellID == 1:
            shell1a = Shell(300,copy.deepcopy(myBoat1.position),myBoat1.orientation+course,angle,30,0)
            _thread.start_new_thread(shell1a.fireShell,("0",))
        myBoat1.shellNum -= 1
    if connectionID == 1:
        if shellID == 0:
            shell0b = Shell(300,copy.deepcopy(myBoat2.position),myBoat2.orientation+course,angle,30,0)
            _thread.start_new_thread(shell0b.fireShell,("1",))
        if shellID == 1:
            shell1b = Shell(300,copy.deepcopy(myBoat2.position),myBoat2.orientation+course,angle,30,0)
            _thread.start_new_thread(shell1b.fireShell,("1",))
        myBoat2.shellNum -= 1
    if connectionID == 2:
        if shellID == 0:
            shell0c = Shell(300,copy.deepcopy(myBoat3.position),myBoat3.orientation+course,angle,30,0)
            _thread.start_new_thread(shell0c.fireShell,("2",))
        if shellID == 1:
            shell1c = Shell(300,copy.deepcopy(myBoat3.position),myBoat3.orientation+course,angle,30,0)
            _thread.start_new_thread(shell1c.fireShell,("2",))
        myBoat3.shellNum -= 1
    if connectionID == 3:
        if shellID == 0:
            shell0d = Shell(300,copy.deepcopy(myBoat4.position),myBoat4.orientation+course,angle,30,0)
            _thread.start_new_thread(shell0d.fireShell,("3",))
        if shellID == 1:
            shell1d = Shell(300,copy.deepcopy(myBoat4.position),myBoat4.orientation+course,angle,30,0)
            _thread.start_new_thread(shell1d.fireShell,("3",))
        myBoat4.shellNum -= 1
    if connectionID == 4:
        if shellID == 0:
            shell0e = Shell(300,copy.deepcopy(myBoat5.position),myBoat5.orientation+course,angle,30,0)
            _thread.start_new_thread(shell0e.fireShell,("4",))
        if shellID == 1:
            shell1e = Shell(300,copy.deepcopy(myBoat5.position),myBoat5.orientation+course,angle,30,0)
            _thread.start_new_thread(shell1e.fireShell,("4",))
        myBoat5.shellNum -= 1


def receive(connection,connectionID):
    global socketInData
    global torpedoID1,torpedoID2,torpedoID3,torpedoID4,torpedoID5, shellID1,shellID2,shellID3,shellID4,shellID5
    torpedoID1 = 0
    torpedoID2 = 0
    torpedoID3 = 0
    torpedoID4 = 0
    torpedoID5 = 0
    while True:
        delay(1000/framerate)
        data = connection.recv(1024)
        while not data:
            data = connection.recv(1024)

        socketInData[connectionID] = pickle.loads(data)
        if "fire torpedo" in socketInData[connectionID]:
            print("Recieved fire torpedo command",int(socketInData[connectionID][13]),float(socketInData[connectionID][15:]))
            if connectionID == 0:
                torCalc(connectionID,torpedoID1,int(socketInData[connectionID][13]),float(socketInData[connectionID][15:]))
                torpedoID1 += 1
            if connectionID == 1:
                torCalc(connectionID,torpedoID2,int(socketInData[connectionID][13]),float(socketInData[connectionID][15:]))
                torpedoID2 += 1
            if connectionID == 2:
                torCalc(connectionID,torpedoID3,int(socketInData[connectionID][13]),float(socketInData[connectionID][15:]))
                torpedoID3 += 1
            if connectionID == 3:
                torCalc(connectionID,torpedoID4,int(socketInData[connectionID][13]),float(socketInData[connectionID][15:]))
                torpedoID4 += 1
            if connectionID == 4:
                torCalc(connectionID,torpedoID5,int(socketInData[connectionID][13]),float(socketInData[connectionID][15:]))
                torpedoID5 += 1
        if "set speed" in socketInData[connectionID]:
            print("Recieved set speed command",float(socketInData[connectionID][10:]))
            if connectionID == 0:
                myBoat1.setSpeed(float(socketInData[connectionID][10:]))
            if connectionID == 1:
                myBoat2.setSpeed(float(socketInData[connectionID][10:]))
            if connectionID == 2:
                myBoat3.setSpeed(float(socketInData[connectionID][10:]))
            if connectionID == 3:
                myBoat4.setSpeed(float(socketInData[connectionID][10:]))
            if connectionID == 4:
                myBoat5.setSpeed(float(socketInData[connectionID][10:]))
        if "set depth" in socketInData[connectionID]:
            print("Recieved set depth command")
            if connectionID == 0:
                _thread.start_new_thread(myBoat1.setDepth,(float(socketInData[connectionID][10:]),))
            if connectionID == 1:
                _thread.start_new_thread(myBoat2.setDepth,(float(socketInData[connectionID][10:]),))
            if connectionID == 2:
                _thread.start_new_thread(myBoat3.setDepth,(float(socketInData[connectionID][10:]),))
            if connectionID == 3:
                _thread.start_new_thread(myBoat4.setDepth,(float(socketInData[connectionID][10:]),))
            if connectionID == 4:
                _thread.start_new_thread(myBoat5.setDepth,(float(socketInData[connectionID][10:]),))
        if "set course" in socketInData[connectionID]:
            print("Recieved set course command")
            if connectionID == 0:
                _thread.start_new_thread(myBoat1.setCourse,(float(socketInData[connectionID][11:]),))
            if connectionID == 1:
                _thread.start_new_thread(myBoat2.setCourse,(float(socketInData[connectionID][11:]),))
            if connectionID == 2:
                _thread.start_new_thread(myBoat3.setCourse,(float(socketInData[connectionID][11:]),))
            if connectionID == 3:
                _thread.start_new_thread(myBoat4.setCourse,(float(socketInData[connectionID][11:]),))
            if connectionID == 4:
                _thread.start_new_thread(myBoat5.setCourse,(float(socketInData[connectionID][11:]),))
        if "set crew" in socketInData[connectionID]:
            print("Recieved set crew command")
            if connectionID == 0:
                myBoat1.crewNum[int(socketInData[connectionID][9])][int(socketInData[connectionID][11])] += int(socketInData[connectionID][12:])
            if connectionID == 1:
                myBoat2.crewNum[int(socketInData[connectionID][9])][int(socketInData[connectionID][11])] += int(socketInData[connectionID][12:])
            if connectionID == 2:
                myBoat3.crewNum[int(socketInData[connectionID][9])][int(socketInData[connectionID][11])] += int(socketInData[connectionID][12:])
            if connectionID == 3:
                myBoat4.crewNum[int(socketInData[connectionID][9])][int(socketInData[connectionID][11])] += int(socketInData[connectionID][12:])
            if connectionID == 4:
                myBoat5.crewNum[int(socketInData[connectionID][9])][int(socketInData[connectionID][11])] += int(socketInData[connectionID][12:])
            print(int(socketInData[connectionID][9]),int(socketInData[connectionID][11]),int(socketInData[connectionID][12:]))
            print(myBoat1.crewNum)
        if "fire shell" in socketInData[connectionID]:
            data = socketInData[connectionID]
            data = data.split()
            print("Recieved fire shell command",float(data[2]),float(data[3]))
            if connectionID == 0:
                shellCalc(connectionID,shellID1,float(data[2]),float(data[3]))
                shellID1 += 1
            if connectionID == 1:
                shellCalc(connectionID,shellID2,float(data[2]),float(data[3]))
                shellID2 += 1
            if connectionID == 2:
                shellCalc(connectionID,shellID3,float(data[2]),float(data[3]))
                shellID3 += 1
            if connectionID == 3:
                shellCalc(connectionID,shellID4,float(data[2]),float(data[3]))
                shellID4 += 1
            if connectionID == 4:
                shellCalc(connectionID,shellID5,float(data[2]),float(data[3]))
                shellID5 += 1


def socketThread(connection,connectionID):
    global socketOutData
    while True:
        delay(1000/framerate)

        try:
        ##if (torpedo0.hit == 0):
            socketOutData[connectionID][9] = torpedo0a.position
        except NameError:
            socketOutData[connectionID][9] = [0,0]
        try:
        ##if (torpedo1.hit == 0):
            socketOutData[connectionID][10] = torpedo1a.position
        except NameError:
            socketOutData[connectionID][10] = [0,0]
        try:
        #if (torpedo2.hit == 0):
            socketOutData[connectionID][11] = torpedo2a.position
        except NameError:
            socketOutData[connectionID][11] = [0,0]
        try:
        ##if (torpedo3.hit == 0):
            socketOutData[connectionID][12] = torpedo3a.position
        except NameError:
            socketOutData[connectionID][12] = [0,0]
        try:
            ##if (torpedo4.hit == 0):
            socketOutData[connectionID][13] = torpedo4a.position
        except NameError:
            socketOutData[connectionID][13] = [0,0]
        try:
            socketOutData[connectionID][14] = torpedo5a.position
        except NameError:
            socketOutData[connectionID][14] = [0,0]

        ################################################################################
        try:
        ##if (torpedo0.hit == 0):
            socketOutData[connectionID][15] = torpedo0b.position
        except NameError:
            socketOutData[connectionID][15] = [0,0]
        try:
        ##if (torpedo1.hit == 0):
            socketOutData[connectionID][16] = torpedo1b.position
        except NameError:
            socketOutData[connectionID][16] = [0,0]
        try:
        #if (torpedo2.hit == 0):
            socketOutData[connectionID][17] = torpedo2b.position
        except NameError:
            socketOutData[connectionID][17] = [0,0]
        try:
        ##if (torpedo3.hit == 0):
            socketOutData[connectionID][18] = torpedo3b.position
        except NameError:
            socketOutData[connectionID][18] = [0,0]
        try:
        ##if (torpedo4.hit == 0):
            socketOutData[connectionID][19] = torpedo4b.position
        except NameError:
            socketOutData[connectionID][19] = [0,0]
        try:
            socketOutData[connectionID][20] = torpedo5b.position
        except NameError:
            socketOutData[connectionID][20] = [0,0]
        ################################################################################
        try:
        ##if (torpedo0.hit == 0):
            socketOutData[connectionID][21] = torpedo0c.position
        except NameError:
            socketOutData[connectionID][21] = [0,0]
        try:
        ##if (torpedo1.hit == 0):
            socketOutData[connectionID][22] = torpedo1c.position
        except NameError:
            socketOutData[connectionID][22] = [0,0]
        try:
        #if (torpedo2.hit == 0):
            socketOutData[connectionID][23] = torpedo2c.position
        except NameError:
            socketOutData[connectionID][23] = [0,0]
        try:
        ##if (torpedo3.hit == 0):
            socketOutData[connectionID][24] = torpedo3c.position
        except NameError:
            socketOutData[connectionID][24] = [0,0]
        try:
        ##if (torpedo4.hit == 0):
            socketOutData[connectionID][25] = torpedo4c.position
        except NameError:
            socketOutData[connectionID][25] = [0,0]
        try:
            socketOutData[connectionID][26] = torpedo5c.position
        except NameError:
            socketOutData[connectionID][26] = [0,0]################################################################################
        try:
        ##if (torpedo0.hit == 0):
            socketOutData[connectionID][27] = torpedo0d.position
        except NameError:
            socketOutData[connectionID][27] = [0,0]
        try:
        ##if (torpedo1.hit == 0):
            socketOutData[connectionID][28] = torpedo1d.position
        except NameError:
            socketOutData[connectionID][28] = [0,0]
        try:
        #if (torpedo2.hit == 0):
            socketOutData[connectionID][29] = torpedo2d.position
        except NameError:
            socketOutData[connectionID][29] = [0,0]
        try:
        ##if (torpedo3.hit == 0):
            socketOutData[connectionID][30] = torpedo3d.position
        except NameError:
            socketOutData[connectionID][30] = [0,0]
        try:
        ##if (torpedo4.hit == 0):
            socketOutData[connectionID][31] = torpedo4d.position
        except NameError:
            socketOutData[connectionID][31] = [0,0]
        try:
            socketOutData[connectionID][32] = torpedo5d.position
        except NameError:
            socketOutData[connectionID][32] = [0,0]################################################################################
        try:
        ##if (torpedo0.hit == 0):
            socketOutData[connectionID][33] = torpedo0e.position
        except NameError:
            socketOutData[connectionID][33] = [0,0]
        try:
        ##if (torpedo1.hit == 0):
            socketOutData[connectionID][34] = torpedo1e.position
        except NameError:
            socketOutData[connectionID][34] = [0,0]
        try:
        #if (torpedo2.hit == 0):
            socketOutData[connectionID][35] = torpedo2e.position
        except NameError:
            socketOutData[connectionID][35] = [0,0]
        try:
        ##if (torpedo3.hit == 0):
            socketOutData[connectionID][36] = torpedo3e.position
        except NameError:
            socketOutData[connectionID][36] = [0,0]
        try:
        ##if (torpedo4.hit == 0):
            socketOutData[connectionID][37] = torpedo4e.position
        except NameError:
            socketOutData[connectionID][37] = [0,0]
        try:
            socketOutData[connectionID][38] = torpedo5e.position
        except NameError:
            socketOutData[connectionID][38] = [0,0]
#####################################################################
        try:
            socketOutData[connectionID][48] = shell0a.position
        except NameError:
            socketOutData[connectionID][48] = [0,0]
        try:
            socketOutData[connectionID][49] = shell1a.position
        except NameError:
            socketOutData[connectionID][49] = [0,0]
        try:
            socketOutData[connectionID][50] = shell0b.position
        except NameError:
            socketOutData[connectionID][50] = [0,0]
        try:
            socketOutData[connectionID][51] = shell1b.position
        except NameError:
            socketOutData[connectionID][51] = [0,0]
        try:
            socketOutData[connectionID][52] = shell0c.position
        except NameError:
            socketOutData[connectionID][52] = [0,0]
        try:
            socketOutData[connectionID][53] = shell1c.position
        except NameError:
            socketOutData[connectionID][53] = [0,0]
        try:
            socketOutData[connectionID][54] = shell0d.position
        except NameError:
            socketOutData[connectionID][54] = [0,0]
        try:
            socketOutData[connectionID][55] = shell1d.position
        except NameError:
            socketOutData[connectionID][55] = [0,0]
        try:
            socketOutData[connectionID][56] = shell0e.position
        except NameError:
            socketOutData[connectionID][56] = [0,0]
        try:
            socketOutData[connectionID][57] = shell1e.position
        except NameError:
            socketOutData[connectionID][57] = [0,0]




        if connectionID == 0:
            socketOutData[connectionID][0] = myBoat1.position
            socketOutData[connectionID][1] = myBoat1.fTorpedoNum
            socketOutData[connectionID][2] = myBoat1.aTorpedoNum
            socketOutData[connectionID][3] = myBoat1.crewNum
            socketOutData[connectionID][4] = myBoat1.health
            socketOutData[connectionID][45] = myBoat1.speed
            socketOutData[connectionID][46] = myBoat1.orientation
            socketOutData[connectionID][47] = myBoat1.depth
            socketOutData[connectionID][60] = myBoat1.shellNum

            socketOutData[connectionID][5] = myBoat2.position
            socketOutData[connectionID][6] = myBoat3.position
            socketOutData[connectionID][7] = myBoat4.position
            socketOutData[connectionID][8] = myBoat5.position

            try:
                socketOutData[connectionID][39] = torpedo0a.hit
            except NameError:
                socketOutData[connectionID][39] = 0
            try:
                socketOutData[connectionID][40] = torpedo1a.hit
            except NameError:
                socketOutData[connectionID][40] = 0
            try:
                socketOutData[connectionID][41] = torpedo2a.hit
            except NameError:
                socketOutData[connectionID][41] = 0
            try:
                socketOutData[connectionID][42] = torpedo3a.hit
            except NameError:
                socketOutData[connectionID][42] = 0
            try:
                socketOutData[connectionID][43] = torpedo4a.hit
            except NameError:
                socketOutData[connectionID][43] = 0
            try:
                socketOutData[connectionID][44] = torpedo5a.hit
            except NameError:
                socketOutData[connectionID][44] = 0

            try:
                socketOutData[connectionID][58] = shell0a.hit
            except NameError:
                socketOutData[connectionID][58] = 0
            try:
                socketOutData[connectionID][59] = shell1a.hit
            except NameError:
                socketOutData[connectionID][59] = 0




        if connectionID == 1:
            socketOutData[connectionID][0] = myBoat2.position
            socketOutData[connectionID][1] = myBoat2.fTorpedoNum
            socketOutData[connectionID][2] = myBoat2.aTorpedoNum
            socketOutData[connectionID][3] = myBoat2.crewNum
            socketOutData[connectionID][4] = myBoat2.health
            socketOutData[connectionID][45] = myBoat2.speed
            socketOutData[connectionID][46] = myBoat2.orientation
            socketOutData[connectionID][47] = myBoat2.depth
            socketOutData[connectionID][60] = myBoat2.shellNum

            socketOutData[connectionID][5] = myBoat1.position
            socketOutData[connectionID][6] = myBoat3.position
            socketOutData[connectionID][7] = myBoat4.position
            socketOutData[connectionID][8] = myBoat5.position


            try:
                socketOutData[connectionID][39] = torpedo0b.hit
            except NameError:
                socketOutData[connectionID][39] = 0
            try:
                socketOutData[connectionID][40] = torpedo1b.hit
            except NameError:
                socketOutData[connectionID][40] = 0
            try:
                socketOutData[connectionID][41] = torpedo2b.hit
            except NameError:
                socketOutData[connectionID][41] = 0
            try:
                socketOutData[connectionID][42] = torpedo3b.hit
            except NameError:
                socketOutData[connectionID][42] = 0
            try:
                socketOutData[connectionID][43] = torpedo4b.hit
            except NameError:
                socketOutData[connectionID][43] = 0
            try:
                socketOutData[connectionID][44] = torpedo5b.hit
            except NameError:
                socketOutData[connectionID][44] = 0


            try:
                socketOutData[connectionID][58] = shell0b.hit
            except NameError:
                socketOutData[connectionID][58] = 0
            try:
                socketOutData[connectionID][59] = shell1b.hit
            except NameError:
                socketOutData[connectionID][59] = 0

        if connectionID == 2:
            socketOutData[connectionID][0] = myBoat3.position
            socketOutData[connectionID][1] = myBoat3.fTorpedoNum
            socketOutData[connectionID][2] = myBoat3.aTorpedoNum
            socketOutData[connectionID][3] = myBoat3.crewNum
            socketOutData[connectionID][4] = myBoat3.health
            socketOutData[connectionID][45] = myBoat3.speed
            socketOutData[connectionID][46] = myBoat3.orientation
            socketOutData[connectionID][47] = myBoat3.depth
            socketOutData[connectionID][60] = myBoat3.shellNum

            socketOutData[connectionID][5] = myBoat1.position
            socketOutData[connectionID][6] = myBoat2.position
            socketOutData[connectionID][7] = myBoat4.position
            socketOutData[connectionID][8] = myBoat5.position


            try:
                socketOutData[connectionID][39] = torpedo0c.hit
            except NameError:
                socketOutData[connectionID][39] = 0
            try:
                socketOutData[connectionID][40] = torpedo1c.hit
            except NameError:
                socketOutData[connectionID][40] = 0
            try:
                socketOutData[connectionID][41] = torpedo2c.hit
            except NameError:
                socketOutData[connectionID][41] = 0
            try:
                socketOutData[connectionID][42] = torpedo3c.hit
            except NameError:
                socketOutData[connectionID][42] = 0
            try:
                socketOutData[connectionID][43] = torpedo4c.hit
            except NameError:
                socketOutData[connectionID][43] = 0
            try:
                socketOutData[connectionID][44] = torpedo5c.hit
            except NameError:
                socketOutData[connectionID][44] = 0


            try:
                socketOutData[connectionID][58] = shell0c.hit
            except NameError:
                socketOutData[connectionID][58] = 0
            try:
                socketOutData[connectionID][59] = shell1c.hit
            except NameError:
                socketOutData[connectionID][59] = 0

        if connectionID == 3:
            socketOutData[connectionID][0] = myBoat4.position
            socketOutData[connectionID][1] = myBoat4.fTorpedoNum
            socketOutData[connectionID][2] = myBoat4.aTorpedoNum
            socketOutData[connectionID][3] = myBoat4.crewNum
            socketOutData[connectionID][4] = myBoat4.health
            socketOutData[connectionID][45] = myBoat4.speed
            socketOutData[connectionID][46] = myBoat4.orientation
            socketOutData[connectionID][47] = myBoat4.depth
            socketOutData[connectionID][60] = myBoat4.shellNum

            socketOutData[connectionID][5] = myBoat1.position
            socketOutData[connectionID][6] = myBoat2.position
            socketOutData[connectionID][7] = myBoat3.position
            socketOutData[connectionID][8] = myBoat5.position


            try:
                socketOutData[connectionID][39] = torpedo0d.hit
            except NameError:
                socketOutData[connectionID][39] = 0
            try:
                socketOutData[connectionID][40] = torpedo1d.hit
            except NameError:
                socketOutData[connectionID][40] = 0
            try:
                socketOutData[connectionID][41] = torpedo2d.hit
            except NameError:
                socketOutData[connectionID][41] = 0
            try:
                socketOutData[connectionID][42] = torpedo3d.hit
            except NameError:
                socketOutData[connectionID][42] = 0
            try:
                socketOutData[connectionID][43] = torpedo4d.hit
            except NameError:
                socketOutData[connectionID][43] = 0
            try:
                socketOutData[connectionID][44] = torpedo5d.hit
            except NameError:
                socketOutData[connectionID][44] = 0



            try:
                socketOutData[connectionID][58] = shell0d.hit
            except NameError:
                socketOutData[connectionID][58] = 0
            try:
                socketOutData[connectionID][59] = shell1d.hit
            except NameError:
                socketOutData[connectionID][59] = 0

        if connectionID == 4:
            socketOutData[connectionID][0] = myBoat5.position
            socketOutData[connectionID][1] = myBoat5.fTorpedoNum
            socketOutData[connectionID][2] = myBoat5.aTorpedoNum
            socketOutData[connectionID][3] = myBoat5.crewNum
            socketOutData[connectionID][4] = myBoat5.health
            socketOutData[connectionID][45] = myBoat5.speed
            socketOutData[connectionID][46] = myBoat5.orientation
            socketOutData[connectionID][47] = myBoat5.depth
            socketOutData[connectionID][60] = myBoat5.shellNum

            socketOutData[connectionID][5] = myBoat1.position
            socketOutData[connectionID][6] = myBoat2.position
            socketOutData[connectionID][7] = myBoat3.position
            socketOutData[connectionID][8] = myBoat4.position


            try:
                socketOutData[connectionID][39] = torpedo0e.hit
            except NameError:
                socketOutData[connectionID][39] = 0
            try:
                socketOutData[connectionID][40] = torpedo1e.hit
            except NameError:
                socketOutData[connectionID][40] = 0
            try:
                socketOutData[connectionID][41] = torpedo2e.hit
            except NameError:
                socketOutData[connectionID][41] = 0
            try:
                socketOutData[connectionID][42] = torpedo3e.hit
            except NameError:
                socketOutData[connectionID][42] = 0
            try:
                socketOutData[connectionID][43] = torpedo4e.hit
            except NameError:
                socketOutData[connectionID][43] = 0
            try:
                socketOutData[connectionID][44] = torpedo5e.hit
            except NameError:
                socketOutData[connectionID][44] = 0


            try:
                socketOutData[connectionID][58] = shell0e.hit
            except NameError:
                socketOutData[connectionID][58] = 0
            try:
                socketOutData[connectionID][59] = shell1e.hit
            except NameError:
                socketOutData[connectionID][59] = 0


        connection.send(pickle.dumps(socketOutData[connectionID]))


def damageThread(name):
    while True:
        while getCrewPoints(name.crewNum[5]) != 0:
            delay((31-getCrewPoints(name.crewNum[5]))*200)
            if name.health[1] < 100 and name.health[1] > 0:
                name.health[1] += 1

            elif name.health[0] < 100 and name.health[0] > 0:
                name.health[0] += 1

            elif name.health[2] < 100 and name.health[2] > 0:
                name.health[2] += 1

        delay(1000/framerate)

def dispatcher():
    global connectionID, myBoat1, myBoat2, myBoat3, myBoat4, myBoat5
    global level1
    connectionID = 0
    flag = True
    while connectionID < 5:
        connection, address = sockobj.accept()
        print('\nServer connected by', address)
        connection.send(pickle.dumps(connectionID))
        _thread.start_new_thread(socketThread, (connection,connectionID))
        _thread.start_new_thread(receive, (connection,connectionID))
        if connectionID == 0:
            while flag:
                flag = False
                myBoat1 = Uboat(0, 4, 2, [[1,3],[1,3],[1,4],[1,1],[1,4],[0,0],[0,0]], [100,100,100], [float(random.randint(0,9999)),float(random.randint(0,9999))],0,-10)
                for y in range(0,len(level1)):
                    for x in range(0,len(level1[y])):
                        if level1[y][x] == 1:
                            if inLimit(myBoat1.position[0],x*1000-1,x*1000+1001) == True and inLimit(myBoat1.position[1],y*1000-1,y*1000+1001) == True:
                                myBoat1 = Uboat(0, 4, 2, [[1,3],[1,3],[1,4],[1,1],[1,4],[0,0],[0,0]], [100,100,100], [float(random.randint(0,9999)),float(random.randint(0,9999))],0,-10)
                                flag = True
            flag = True
        if connectionID == 1:
            while flag:
                flag = False
                myBoat2 = Uboat(0, 4, 2, [[1,3],[1,3],[1,4],[1,1],[1,4],[0,0],[0,0]], [100,100,100], [float(random.randint(0,9999)),float(random.randint(0,9999))],0,-10)
                for y in range(0,len(level1)):
                    for x in range(0,len(level1[y])):
                        if level1[y][x] == 1:
                            if inLimit(myBoat2.position[0],x*1000-1,x*1000+1001) == True and inLimit(myBoat2.position[1],y*1000-1,y*1000+1001) == True:
                                myBoat2 = Uboat(0, 4, 2, [[1,3],[1,3],[1,4],[1,1],[1,4],[0,0],[0,0]], [100,100,100], [float(random.randint(0,9999)),float(random.randint(0,9999))],0,-10)
                                flag = True
            flag = True
        if connectionID == 2:
            while flag:
                flag = False
                myBoat3 = Uboat(0, 4, 2, [[1,3],[1,3],[1,4],[1,1],[1,4],[0,0],[0,0]], [100,100,100], [float(random.randint(0,9999)),float(random.randint(0,9999))],0,-10)
                for y in range(0,len(level1)):
                    for x in range(0,len(level1[y])):
                        if level1[y][x] == 1:
                            if inLimit(myBoat3.position[0],x*1000-1,x*1000+1001) == True and inLimit(myBoat3.position[1],y*1000-1,y*1000+1001) == True:
                                myBoat3 = Uboat(0, 4, 2, [[1,3],[1,3],[1,4],[1,1],[1,4],[0,0],[0,0]], [100,100,100], [float(random.randint(0,9999)),float(random.randint(0,9999))],0,-10)
                                flag = True
            flag = True
        if connectionID == 3:
            while flag:
                flag = False
                myBoat4 = Uboat(0, 4, 2, [[1,3],[1,3],[1,4],[1,1],[1,4],[0,0],[0,0]], [100,100,100], [float(random.randint(0,9999)),float(random.randint(0,9999))],0,-10)
                for y in range(0,len(level1)):
                    for x in range(0,len(level1[y])):
                        if level1[y][x] == 1:
                            if inLimit(myBoat4.position[0],x*1000-1,x*1000+1001) == True and inLimit(myBoat4.position[1],y*1000-1,y*1000+1001) == True:
                                myBoat4 = Uboat(0, 4, 2, [[1,3],[1,3],[1,4],[1,1],[1,4],[0,0],[0,0]], [100,100,100], [float(random.randint(0,9999)),float(random.randint(0,9999))],0,-10)
                                flag = True
            flag = True
        if connectionID == 4:
            while flag:
                flag = False
                myBoat5 = Uboat(0, 4, 2, [[1,3],[1,3],[1,4],[1,1],[1,4],[0,0],[0,0]], [100,100,100], [float(random.randint(0,9999)),float(random.randint(0,9999))],0,-10)
                for y in range(0,len(level1)):
                    for x in range(0,len(level1[y])):
                        if level1[y][x] == 1:
                            if inLimit(myBoat5.position[0],x*1000-1,x*1000+1001) == True and inLimit(myBoat5.position[1],y*1000-1,y*1000+1001) == True:
                                myBoat5 = Uboat(0, 4, 2, [[1,3],[1,3],[1,4],[1,1],[1,4],[0,0],[0,0]], [100,100,100], [float(random.randint(0,9999)),float(random.randint(0,9999))],0,-10)
                                flag = True
            flag = True


        connectionID += 1

clear()


myBoat1 = Uboat(0, 4, 2, [[1,3],[1,3],[1,4],[1,1],[1,4],[0,0],[0,0]], [100,100,100], [0,0],0,-10)
myBoat2 = Uboat(0, 4, 2, [[1,3],[1,3],[1,4],[1,1],[1,4],[0,0],[0,0]], [100,100,100], [0,0],0,-10)
myBoat3 = Uboat(0, 4, 2, [[1,3],[1,3],[1,4],[1,1],[1,4],[0,0],[0,0]], [100,100,100], [0,0],0,-10)
myBoat4 = Uboat(0, 4, 2, [[1,3],[1,3],[1,4],[1,1],[1,4],[0,0],[0,0]], [100,100,100], [0,0],0,-10)
myBoat5 = Uboat(0, 4, 2, [[1,3],[1,3],[1,4],[1,1],[1,4],[0,0],[0,0]], [100,100,100], [0,0],0,-10)

#random.seed(time.time())

#enemy1 = EnemyShip(100)


#d,r = myBoat.detect([0,0],[3,4])
#print(d)
#print(r)
#print(time.time())


sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.bind((myHost, myPort))
sockobj.listen(5)

_thread.start_new_thread(dispatcher,())
input("Press Enter when all players are ready. ")
delay(1000)
print(socketInData)



_thread.start_new_thread(calculateBoat,(myBoat1,))
_thread.start_new_thread(calculateBoat,(myBoat2,))
_thread.start_new_thread(calculateBoat,(myBoat3,))
_thread.start_new_thread(calculateBoat,(myBoat4,))
_thread.start_new_thread(calculateBoat,(myBoat5,))

#_thread.start_new_thread(socketThread,())

#input()

#_thread.start_new_thread(enemy1.checkEnemyShip,())






#_thread.start_new_thread(calculateBoat,(enemy1,))
#_thread.start_new_thread(calculateBoat,(enemy2,))
#_thread.start_new_thread(calculateBoat,(enemy3,))

_thread.start_new_thread(myBoat1.reloadTube,(0,))
_thread.start_new_thread(myBoat1.reloadTube,(1,))

_thread.start_new_thread(myBoat2.reloadTube,(0,))
_thread.start_new_thread(myBoat2.reloadTube,(1,))

_thread.start_new_thread(myBoat3.reloadTube,(0,))
_thread.start_new_thread(myBoat3.reloadTube,(1,))

_thread.start_new_thread(myBoat4.reloadTube,(0,))
_thread.start_new_thread(myBoat4.reloadTube,(1,))

_thread.start_new_thread(myBoat5.reloadTube,(0,))
_thread.start_new_thread(myBoat5.reloadTube,(1,))

_thread.start_new_thread(myBoat1.reloadShell,())
_thread.start_new_thread(myBoat2.reloadShell,())
_thread.start_new_thread(myBoat3.reloadShell,())
_thread.start_new_thread(myBoat4.reloadShell,())
_thread.start_new_thread(myBoat5.reloadShell,())

_thread.start_new_thread(damageThread,(myBoat1,))
_thread.start_new_thread(damageThread,(myBoat2,))
_thread.start_new_thread(damageThread,(myBoat3,))
_thread.start_new_thread(damageThread,(myBoat4,))
_thread.start_new_thread(damageThread,(myBoat5,))


print("Enter q to stop server")

while True:
    #print(socketOutData)
    try:
        #print(socketOutData)
        delay(500)
        #clear()
    except KeyboardInterrupt:
        break

sockobj.close()
