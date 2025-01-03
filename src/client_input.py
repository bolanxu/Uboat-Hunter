import time, math, os, random
import _thread
import copy
from collections import namedtuple
from colorama import Fore
from socket import *
import pickle
import sys



textTime = 0

flag1 = True
framerate = 50

speed = 0
course = 0
depth = -10

serverHost = 'localhost'
serverPort = 50045
socketOutData = []
socketInData = []

message = ""

oldHealthf = 100
oldHealthm = 100
oldHealthr = 100

ab = 0
ba = 0

mode = 0

scan = [['  ','0','1','2','3','4','5','6','7','8','9'],
        [' 0','-','-','-','-','-','-','-','-','-','-'],
        [' 1','-','-','-','-','-','-','-','-','-','-'],
        [' 2','-','-','-','-','-','-','-','-','-','-'],
        [' 3','-','-','-','-','-','-','-','-','-','-'],
        [' 4','-','-','-','-','-','-','-','-','-','-'],
        [' 5','-','-','-','-','-','-','-','-','-','-'],
        [' 6','-','-','-','-','-','-','-','-','-','-'],
        [' 7','-','-','-','-','-','-','-','-','-','-'],
        [' 8','-','-','-','-','-','-','-','-','-','-'],
        [' 9','-','-','-','-','-','-','-','-','-','-']]

scan_short = []

scan_short1 = [['  ','9','8','7','6','5','4','3','2','1','0','1','2','3','4','5','6','7','8','9'],
               [' 9','.','.','.','.','.','.','.','.','.',' ','.','.','.','.','.','.','.','.','.'],
               [' 8','.','.','.','.','.','.','.','.','.','|','.','.','.','.','.','.','.','.','.'],
               [' 7','.','.','.','.','.','.','.','.','.',' ','.','.','.','.','.','.','.','.','.'],
               [' 6','.','.','.','.','.','.','.','.','.','|','.','.','.','.','.','.','.','.','.'],
               [' 5','.','.','.','.','.','.','.','.','.',' ','.','.','.','.','.','.','.','.','.'],
               [' 4','.','.','.','.','.','.','.','.','.','|','.','.','.','.','.','.','.','.','.'],
               [' 3','.','.','.','.','.','.','.','.','.',' ','.','.','.','.','.','.','.','.','.'],
               [' 2','.','.','.','.','.','.','.','.','.','|','.','.','.','.','.','.','.','.','.'],
               [' 1','.','.','.','.','.','.','.','.','.',' ','.','.','.','.','.','.','.','.','.'],
               [' 0','-','-','-','-','-','-','-','-','.','+','-','-','-','-','-','-','-','-','-'],
               [' 1','.','.','.','.','.','.','.','.','.',' ','.','.','.','.','.','.','.','.','.'],
               [' 2','.','.','.','.','.','.','.','.','.','|','.','.','.','.','.','.','.','.','.'],
               [' 3','.','.','.','.','.','.','.','.','.',' ','.','.','.','.','.','.','.','.','.'],
               [' 4','.','.','.','.','.','.','.','.','.','|','.','.','.','.','.','.','.','.','.'],
               [' 5','.','.','.','.','.','.','.','.','.',' ','.','.','.','.','.','.','.','.','.'],
               [' 6','.','.','.','.','.','.','.','.','.','|','.','.','.','.','.','.','.','.','.'],
               [' 7','.','.','.','.','.','.','.','.','.',' ','.','.','.','.','.','.','.','.','.'],
               [' 8','.','.','.','.','.','.','.','.','.','|','.','.','.','.','.','.','.','.','.'],
               [' 9','.','.','.','.','.','.','.','.','.',' ','.','.','.','.','.','.','.','.','.']]


#scan_long = [['  ','0','1','2','3','4','5','6','7','8','9'],
#            [' 0','-','-','-','-','-','-','-','-','-','-'],
#            [' 1','-','-','-','-','-','-','-','-','-','-'],
 #           [' 2','-','-','-','-','-','-','-','-','-','-'],
 #           [' 3','-','-','-','-','-','-','-','-','-','-'],
 #           [' 4','-','-','-','-','-','-','-','-','-','-'],
 #           [' 5','-','-','-','-','-','-','-','-','-','-'],
 #           [' 6','-','-','-','-','-','-','-','-','-','-'],
#            [' 7','-','-','-','-','-','-','-','-','-','-'],
 #           [' 8','-','-','-','-','-','-','-','-','-','-'],
#            [' 9','-','-','-','-','-','-','-','-','-','-']]

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

numbers = ['0','1','2','3','4','5','6','7','8','9']
#Crew = namedtuple('Crew',['FTOR','CREW','COMMAND','ENGINE','ATOR'])
if len(sys.argv) > 1:
    serverPort = int(sys.argv[1])
    if len(sys.argv) > 2:
        mode = int(sys.argv[2])

nowTime = time.asctime()

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

def printText(string,end='\n',color=Fore.GREEN):
    print(color,end='')
    for i in string:
        print(i, end = '' , flush = True)
        delay(textTime)
    print(Fore.GREEN,end='')
    if end == '\n':
        print()

def detect(pos1,pos2):
    distance = math.dist(pos1,pos2)
    angle = math.atan((pos1[1]-pos2[1])/(pos1[0]-pos2[0]))
    angle = math.degrees(angle)
    if (pos1[0] - pos2[0]) > 0:
        angle = (180-angle)*-1
    if angle > 180:
        angle = (360-angle)*-1
    if angle < -180:
        angle = (360+angle)*-1
    return distance, angle

def rotation(pos,angle):
    ax = pos[0]
    ay = pos[1]
    deg = math.radians(angle)
    bx = ax*math.cos(deg) - ay*math.sin(deg)
    by = ay*math.cos(deg) + ax*math.sin(deg)
    return [bx,by]

def calculateScan(pos1,pos2,angle):
    x1 = 0
    y1 = 0
    flag = False
    x = pos2[0] - pos1[0]
    y = pos2[1] - pos1[1]
    [x,y] = rotation([x,y],angle)
    if x < 950 and x > -950:
        if y < 950 and y > -950:
            x1 = x + 950
            y1 = y + 950
            flag = True
    return x1,y1,flag


def getInput(a = '',typ = int):
    while True:
        try:
            out = typ(input(a))
            break
        except ValueError:
            printText("Please Enter a Valid Command.")
            delay(200)
    return out

def scanSonarShort():
    global level1,ab,ba

    scan_short = copy.deepcopy(scan_short1)

    #for i in range(1,11)
        #scan[0][i] = str(numbers[socketInData[0][0]])
        #scan[myBoat.position[1]/10][myBoat.position[0]/0] = 'Y'
    #print(enemy1.position)

    print()

    if name == "Player 1":
        ab = range(9,15)
        for i in range(15,39):
            try:
                if (socketInData[i] != [0,0]):
                    dx,dy,flag = calculateScan(socketInData[0],socketInData[i],-1*(socketInData[46]+90))
                    if flag == True:
                        scan_short[int(dy/100)+1][int(dx/100)+1] = Fore.RED+'T'+Fore.GREEN
            except IndexError:
                pass
        for i in range(9,15):
            try:
                if (socketInData[i] != [0,0]):
                    dx,dy,flag = calculateScan(socketInData[0],socketInData[i],-1*(socketInData[46]+90))
                    if flag == True:
                        scan_short[int(dy/100)+1][int(dx/100)+1] = Fore.WHITE+'T'+Fore.GREEN
            except IndexError:
                pass
    if name == "Player 2":
        ab = range(15,21)
        for i in range(9,15):
            try:
                if (socketInData[i] != [0,0]):
                    dx,dy,flag = calculateScan(socketInData[0],socketInData[i],-1*(socketInData[46]+90))
                    if flag == True:
                        scan_short[int(dy/100)+1][int(dx/100)+1] = Fore.RED+'T'+Fore.GREEN
            except IndexError:
                pass
        for i in range(21,39):
            try:
                if (socketInData[i] != [0,0]):
                    dx,dy,flag = calculateScan(socketInData[0],socketInData[i],-1*(socketInData[46]+90))
                    if flag == True:
                        scan_short[int(dy/100)+1][int(dx/100)+1] = Fore.RED+'T'+Fore.GREEN
            except IndexError:
                pass
        for i in range(15,21):
            try:
                if (socketInData[i] != [0,0]):
                    dx,dy,flag = calculateScan(socketInData[0],socketInData[i],-1*(socketInData[46]+90))
                    if flag == True:
                        scan_short[int(dy/100)+1][int(dx/100)+1] = Fore.WHITE+'T'+Fore.GREEN
            except IndexError:
                pass
    if name == "Player 3":
        ab = range(21,27)
        for i in range(9,21):
            try:
                if (socketInData[i] != [0,0]):
                    dx,dy,flag = calculateScan(socketInData[0],socketInData[i],-1*(socketInData[46]+90))
                    if flag == True:
                        scan_short[int(dy/100)+1][int(dx/100)+1] = Fore.RED+'T'+Fore.GREEN
            except IndexError:
                pass
        for i in range(27,39):
            try:
                if (socketInData[i] != [0,0]):
                    dx,dy,flag = calculateScan(socketInData[0],socketInData[i],-1*(socketInData[46]+90))
                    if flag == True:
                        scan_short[int(dy/100)+1][int(dx/100)+1] = Fore.RED+'T'+Fore.GREEN
            except IndexError:
                pass
        for i in range(21,27):
            try:
                if (socketInData[i] != [0,0]):
                    dx,dy,flag = calculateScan(socketInData[0],socketInData[i],-1*(socketInData[46]+90))
                    if flag == True:
                        scan_short[int(dy/100)+1][int(dx/100)+1] = Fore.WHITE+'T'+Fore.GREEN
            except IndexError:
                pass
    if name == "Player 4":
        ab = range(27,33)
        for i in range(9,27):
            try:
                if (socketInData[i] != [0,0]):
                    dx,dy,flag = calculateScan(socketInData[0],socketInData[i],-1*(socketInData[46]+90))
                    if flag == True:
                        scan_short[int(dy/100)+1][int(dx/100)+1] = Fore.RED+'T'+Fore.GREEN
            except IndexError:
                pass
        for i in range(33,39):
            try:
                if (socketInData[i] != [0,0]):
                    dx,dy,flag = calculateScan(socketInData[0],socketInData[i],-1*(socketInData[46]+90))
                    if flag == True:
                        scan_short[int(dy/100)+1][int(dx/100)+1] = Fore.RED+'T'+Fore.GREEN
            except IndexError:
                pass
        for i in range(27,33):
            try:
                if (socketInData[i] != [0,0]):
                    dx,dy,flag = calculateScan(socketInData[0],socketInData[i],-1*(socketInData[46]+90))
                    if flag == True:
                        scan_short[int(dy/100)+1][int(dx/100)+1] = Fore.WHITE+'T'+Fore.GREEN
            except IndexError:
                pass
    if name == "Player 5":
        ab = range(33,39)
        for i in range(9,33):
            try:
                if (socketInData[i] != [0,0]):
                    dx,dy,flag = calculateScan(socketInData[0],socketInData[i],-1*(socketInData[46]+90))
                    if flag == True:
                        scan_short[int(dy/100)+1][int(dx/100)+1] = Fore.RED+'T'+Fore.GREEN
            except IndexError:
                pass
        for i in range(33,39):
            try:
                if (socketInData[i] != [0,0]):
                    dx,dy,flag = calculateScan(socketInData[0],socketInData[i],-1*(socketInData[46]+90))
                    if flag == True:
                        scan_short[int(dy/100)+1][int(dx/100)+1] = Fore.WHITE+'T'+Fore.GREEN
            except IndexError:
                pass

################################################################################################################

    if name == "Player 1":
        ba = range(48,50)
        for i in range(50,58):
            try:
                if (socketInData[i] != [0,0]):
                    dx,dy,flag = calculateScan(socketInData[0],socketInData[i],-1*(socketInData[46]+90))
                    if flag == True:
                        scan_short[int(dy/100)+1][int(dx/100)+1] = Fore.RED+'S'+Fore.GREEN
            except IndexError:
                pass
        for i in range(48,50):
            try:
                if (socketInData[i] != [0,0]):
                    dx,dy,flag = calculateScan(socketInData[0],socketInData[i],-1*(socketInData[46]+90))
                    if flag == True:
                        scan_short[int(dy/100)+1][int(dx/100)+1] = Fore.WHITE+'S'+Fore.GREEN
            except IndexError:
                pass
    if name == "Player 2":
        ba = range(50,52)
        for i in range(48,50):
            try:
                if (socketInData[i] != [0,0]):
                    dx,dy,flag = calculateScan(socketInData[0],socketInData[i],-1*(socketInData[46]+90))
                    if flag == True:
                        scan_short[int(dy/100)+1][int(dx/100)+1] = Fore.RED+'S'+Fore.GREEN
            except IndexError:
                pass
        for i in range(52,58):
            try:
                if (socketInData[i] != [0,0]):
                    dx,dy,flag = calculateScan(socketInData[0],socketInData[i],-1*(socketInData[46]+90))
                    if flag == True:
                        scan_short[int(dy/100)+1][int(dx/100)+1] = Fore.RED+'S'+Fore.GREEN
            except IndexError:
                pass
        for i in range(50,52):
            try:
                if (socketInData[i] != [0,0]):
                    dx,dy,flag = calculateScan(socketInData[0],socketInData[i],-1*(socketInData[46]+90))
                    if flag == True:
                        scan_short[int(dy/100)+1][int(dx/100)+1] = Fore.WHITE+'S'+Fore.GREEN
            except IndexError:
                pass
    if name == "Player 3":
        ba = range(52,54)
        for i in range(48,52):
            try:
                if (socketInData[i] != [0,0]):
                    dx,dy,flag = calculateScan(socketInData[0],socketInData[i],-1*(socketInData[46]+90))
                    if flag == True:
                        scan_short[int(dy/100)+1][int(dx/100)+1] = Fore.RED+'S'+Fore.GREEN
            except IndexError:
                pass
        for i in range(54,58):
            try:
                if (socketInData[i] != [0,0]):
                    dx,dy,flag = calculateScan(socketInData[0],socketInData[i],-1*(socketInData[46]+90))
                    if flag == True:
                        scan_short[int(dy/100)+1][int(dx/100)+1] = Fore.RED+'S'+Fore.GREEN
            except IndexError:
                pass
        for i in range(52,54):
            try:
                if (socketInData[i] != [0,0]):
                    dx,dy,flag = calculateScan(socketInData[0],socketInData[i],-1*(socketInData[46]+90))
                    if flag == True:
                        scan_short[int(dy/100)+1][int(dx/100)+1] = Fore.WHITE+'S'+Fore.GREEN
            except IndexError:
                pass
    if name == "Player 4":
        ba = range(54,56)
        for i in range(48,54):
            try:
                if (socketInData[i] != [0,0]):
                    dx,dy,flag = calculateScan(socketInData[0],socketInData[i],-1*(socketInData[46]+90))
                    if flag == True:
                        scan_short[int(dy/100)+1][int(dx/100)+1] = Fore.RED+'S'+Fore.GREEN
            except IndexError:
                pass
        for i in range(55,58):
            try:
                if (socketInData[i] != [0,0]):
                    dx,dy,flag = calculateScan(socketInData[0],socketInData[i],-1*(socketInData[46]+90))
                    if flag == True:
                        scan_short[int(dy/100)+1][int(dx/100)+1] = Fore.RED+'S'+Fore.GREEN
            except IndexError:
                pass
        for i in range(54,56):
            try:
                if (socketInData[i] != [0,0]):
                    dx,dy,flag = calculateScan(socketInData[0],socketInData[i],-1*(socketInData[46]+90))
                    if flag == True:
                        scan_short[int(dy/100)+1][int(dx/100)+1] = Fore.WHITE+'S'+Fore.GREEN
            except IndexError:
                pass
    if name == "Player 5":
        ba = range(56,58)
        for i in range(48,56):
            try:
                if (socketInData[i] != [0,0]):
                    dx,dy,flag = calculateScan(socketInData[0],socketInData[i],-1*(socketInData[46]+90))
                    if flag == True:
                        scan_short[int(dy/100)+1][int(dx/100)+1] = Fore.RED+'S'+Fore.GREEN
            except IndexError:
                pass
        for i in range(56,58):
            try:
                if (socketInData[i] != [0,0]):
                    dx,dy,flag = calculateScan(socketInData[0],socketInData[i],-1*(socketInData[46]+90))
                    if flag == True:
                        scan_short[int(dy/100)+1][int(dx/100)+1] = Fore.WHITE+'S'+Fore.GREEN
            except IndexError:
                pass

    for i in range(5,9):
        try:
            if (socketInData[i] != [0,0]):
                dx,dy,flag = calculateScan(socketInData[0],socketInData[i],-1*(socketInData[46]+90))
                if flag == True:
                    scan_short[int(dy/100)+1][int(dx/100)+1] = Fore.RED+'E'+Fore.GREEN
        except IndexError:
            pass


    scan_short[10][10] = '+'

    #for y in range(0,len(level1)):
    #    for x in range(0,len(level1[y])):
    #        if level1[y][x] == 1:


    for y in range(0,20):
        for x in range(0,20):
            print(scan_short[y][x],end = '  ', flush = True)
            #delay(50)
        print()
    print()
    print()



def scanSonarLong():
    global ab,ba
    for y in range(1,11):
        for x in range(1,11):
            if level1[y-1][x-1] == 0:
                scan[y][x] = Fore.LIGHTBLUE_EX+'-'+Fore.GREEN
            elif level1[y-1][x-1] == 1:
                scan[y][x] = Fore.LIGHTGREEN_EX+'X'+Fore.GREEN
        #scan[myBoat.position[1]/10][myBoat.position[0]/0] = 'Y'
    #print(enemy1.position)

    print()

    if name == "Player 1":
        ab = range(9,15)
        for i in range(15,39):
            try:
                if (inLimit(int(socketInData[i][0]/1000)+1,0,11)) and (inLimit(int(socketInData[i][1]/1000)+1,0,11)) and (socketInData[i] != [0,0]):
                    scan[int(socketInData[i][1]/1000)+1][int(socketInData[i][0]/1000)+1] = Fore.RED+'T'+Fore.GREEN
            except IndexError:
                pass
        for i in range(9,15):
            try:
                if (inLimit(int(socketInData[i][0]/1000)+1,0,11)) and (inLimit(int(socketInData[i][1]/1000)+1,0,11)) and (socketInData[i] != [0,0]):
                    scan[int(socketInData[i][1]/1000)+1][int(socketInData[i][0]/1000)+1] = Fore.WHITE+'T'+Fore.GREEN
            except IndexError:
                pass
    if name == "Player 2":
        ab = range(15,21)
        for i in range(9,15):
            try:
                if (inLimit(int(socketInData[i][0]/1000)+1,0,11)) and (inLimit(int(socketInData[i][1]/1000)+1,0,11)) and (socketInData[i] != [0,0]):
                    scan[int(socketInData[i][1]/1000)+1][int(socketInData[i][0]/1000)+1] = Fore.RED+'T'+Fore.GREEN
            except IndexError:
                pass
        for i in range(21,39):
            try:
                if (inLimit(int(socketInData[i][0]/1000)+1,0,11)) and (inLimit(int(socketInData[i][1]/1000)+1,0,11)) and (socketInData[i] != [0,0]):
                    scan[int(socketInData[i][1]/1000)+1][int(socketInData[i][0]/1000)+1] = Fore.RED+'T'+Fore.GREEN
            except IndexError:
                pass
        for i in range(15,21):
            try:
                if (inLimit(int(socketInData[i][0]/1000)+1,0,11)) and (inLimit(int(socketInData[i][1]/1000)+1,0,11)) and (socketInData[i] != [0,0]):
                    scan[int(socketInData[i][1]/1000)+1][int(socketInData[i][0]/1000)+1] = Fore.WHITE+'T'+Fore.GREEN
            except IndexError:
                pass
    if name == "Player 3":
        ab = range(21,27)
        for i in range(9,21):
            try:
                if (inLimit(int(socketInData[i][0]/1000)+1,0,11)) and (inLimit(int(socketInData[i][1]/1000)+1,0,11)) and (socketInData[i] != [0,0]):
                    scan[int(socketInData[i][1]/1000)+1][int(socketInData[i][0]/1000)+1] = Fore.RED+'T'+Fore.GREEN
            except IndexError:
                pass
        for i in range(27,39):
            try:
                if (inLimit(int(socketInData[i][0]/1000)+1,0,11)) and (inLimit(int(socketInData[i][1]/1000)+1,0,11)) and (socketInData[i] != [0,0]):
                    scan[int(socketInData[i][1]/1000)+1][int(socketInData[i][0]/1000)+1] = Fore.RED+'T'+Fore.GREEN
            except IndexError:
                pass
        for i in range(21,27):
            try:
                if (inLimit(int(socketInData[i][0]/1000)+1,0,11)) and (inLimit(int(socketInData[i][1]/1000)+1,0,11)) and (socketInData[i] != [0,0]):
                    scan[int(socketInData[i][1]/1000)+1][int(socketInData[i][0]/1000)+1] = Fore.WHITE+'T'+Fore.GREEN
            except IndexError:
                pass
    if name == "Player 4":
        range(27,33)
        for i in range(9,27):
            try:
                if (inLimit(int(socketInData[i][0]/1000)+1,0,11)) and (inLimit(int(socketInData[i][1]/1000)+1,0,11)) and (socketInData[i] != [0,0]):
                    scan[int(socketInData[i][1]/1000)+1][int(socketInData[i][0]/1000)+1] = Fore.RED+'T'+Fore.GREEN
            except IndexError:
                pass
        for i in range(33,39):
            try:
                if (inLimit(int(socketInData[i][0]/1000)+1,0,11)) and (inLimit(int(socketInData[i][1]/1000)+1,0,11)) and (socketInData[i] != [0,0]):
                    scan[int(socketInData[i][1]/1000)+1][int(socketInData[i][0]/1000)+1] = Fore.RED+'T'+Fore.GREEN
            except IndexError:
                pass
        for i in range(27,33):
            try:
                if (inLimit(int(socketInData[i][0]/1000)+1,0,11)) and (inLimit(int(socketInData[i][1]/1000)+1,0,11)) and (socketInData[i] != [0,0]):
                    scan[int(socketInData[i][1]/1000)+1][int(socketInData[i][0]/1000)+1] = Fore.WHITE+'T'+Fore.GREEN
            except IndexError:
                pass
    if name == "Player 5":
        ab = range(33,39)
        for i in range(9,33):
            try:
                if (inLimit(int(socketInData[i][0]/1000)+1,0,11)) and (inLimit(int(socketInData[i][1]/1000)+1,0,11)) and (socketInData[i] != [0,0]):
                    scan[int(socketInData[i][1]/1000)+1][int(socketInData[i][0]/1000)+1] = Fore.RED+'T'+Fore.GREEN
            except IndexError:
                pass
        for i in range(33,39):
            try:
                if (inLimit(int(socketInData[i][0]/1000)+1,0,11)) and (inLimit(int(socketInData[i][1]/1000)+1,0,11)) and (socketInData[i] != [0,0]):
                    scan[int(socketInData[i][1]/1000)+1][int(socketInData[i][0]/1000)+1] = Fore.WHITE+'T'+Fore.GREEN
            except IndexError:
                pass


################################################################################################################

    if name == "Player 1":
        ba = range(48,50)
        for i in range(50,58):
            try:
                if (inLimit(int(socketInData[i][0]/1000)+1,0,11)) and (inLimit(int(socketInData[i][1]/1000)+1,0,11)) and (socketInData[i] != [0,0]):
                    scan[int(socketInData[i][1]/1000)+1][int(socketInData[i][0]/1000)+1] = Fore.RED+'S'+Fore.GREEN
            except IndexError:
                pass
        for i in range(48,50):
            try:
                if (inLimit(int(socketInData[i][0]/1000)+1,0,11)) and (inLimit(int(socketInData[i][1]/1000)+1,0,11)) and (socketInData[i] != [0,0]):
                    scan[int(socketInData[i][1]/1000)+1][int(socketInData[i][0]/1000)+1] = Fore.WHITE+'S'+Fore.GREEN
            except IndexError:
                pass
    if name == "Player 2":
        ba = range(50,52)
        for i in range(48,50):
            try:
                if (inLimit(int(socketInData[i][0]/1000)+1,0,11)) and (inLimit(int(socketInData[i][1]/1000)+1,0,11)) and (socketInData[i] != [0,0]):
                    scan[int(socketInData[i][1]/1000)+1][int(socketInData[i][0]/1000)+1] = Fore.RED+'S'+Fore.GREEN
            except IndexError:
                pass
        for i in range(52,58):
            try:
                if (inLimit(int(socketInData[i][0]/1000)+1,0,11)) and (inLimit(int(socketInData[i][1]/1000)+1,0,11)) and (socketInData[i] != [0,0]):
                    scan[int(socketInData[i][1]/1000)+1][int(socketInData[i][0]/1000)+1] = Fore.RED+'S'+Fore.GREEN
            except IndexError:
                pass
        for i in range(50,52):
            try:
                if (inLimit(int(socketInData[i][0]/1000)+1,0,11)) and (inLimit(int(socketInData[i][1]/1000)+1,0,11)) and (socketInData[i] != [0,0]):
                    scan[int(socketInData[i][1]/1000)+1][int(socketInData[i][0]/1000)+1] = Fore.WHITE+'S'+Fore.GREEN
            except IndexError:
                pass
    if name == "Player 3":
        ba = range(52,54)
        for i in range(48,52):
            try:
                if (inLimit(int(socketInData[i][0]/1000)+1,0,11)) and (inLimit(int(socketInData[i][1]/1000)+1,0,11)) and (socketInData[i] != [0,0]):
                    scan[int(socketInData[i][1]/1000)+1][int(socketInData[i][0]/1000)+1] = Fore.RED+'S'+Fore.GREEN
            except IndexError:
                pass
        for i in range(54,58):
            try:
                if (inLimit(int(socketInData[i][0]/1000)+1,0,11)) and (inLimit(int(socketInData[i][1]/1000)+1,0,11)) and (socketInData[i] != [0,0]):
                    scan[int(socketInData[i][1]/1000)+1][int(socketInData[i][0]/1000)+1] = Fore.RED+'S'+Fore.GREEN
            except IndexError:
                pass
        for i in range(52,54):
            try:
                if (inLimit(int(socketInData[i][0]/1000)+1,0,11)) and (inLimit(int(socketInData[i][1]/1000)+1,0,11)) and (socketInData[i] != [0,0]):
                    scan[int(socketInData[i][1]/1000)+1][int(socketInData[i][0]/1000)+1] = Fore.WHITE+'S'+Fore.GREEN
            except IndexError:
                pass
    if name == "Player 4":
        ba = range(54,56)
        for i in range(48,54):
            try:
                if (inLimit(int(socketInData[i][0]/1000)+1,0,11)) and (inLimit(int(socketInData[i][1]/1000)+1,0,11)) and (socketInData[i] != [0,0]):
                    scan[int(socketInData[i][1]/1000)+1][int(socketInData[i][0]/1000)+1] = Fore.RED+'S'+Fore.GREEN
            except IndexError:
                pass
        for i in range(55,58):
            try:
                if (inLimit(int(socketInData[i][0]/1000)+1,0,11)) and (inLimit(int(socketInData[i][1]/1000)+1,0,11)) and (socketInData[i] != [0,0]):
                    scan[int(socketInData[i][1]/1000)+1][int(socketInData[i][0]/1000)+1] = Fore.RED+'S'+Fore.GREEN
            except IndexError:
                pass
        for i in range(54,56):
            try:
                if (inLimit(int(socketInData[i][0]/1000)+1,0,11)) and (inLimit(int(socketInData[i][1]/1000)+1,0,11)) and (socketInData[i] != [0,0]):
                    scan[int(socketInData[i][1]/1000)+1][int(socketInData[i][0]/1000)+1] = Fore.WHITE+'S'+Fore.GREEN
            except IndexError:
                pass
    if name == "Player 5":
        ba = range(56,58)
        for i in range(48,56):
            try:
                if (inLimit(int(socketInData[i][0]/1000)+1,0,11)) and (inLimit(int(socketInData[i][1]/1000)+1,0,11)) and (socketInData[i] != [0,0]):
                    scan[int(socketInData[i][1]/1000)+1][int(socketInData[i][0]/1000)+1] = Fore.RED+'S'+Fore.GREEN
            except IndexError:
                pass
        for i in range(56,58):
            try:
                if (inLimit(int(socketInData[i][0]/1000)+1,0,11)) and (inLimit(int(socketInData[i][1]/1000)+1,0,11)) and (socketInData[i] != [0,0]):
                    scan[int(socketInData[i][1]/1000)+1][int(socketInData[i][0]/1000)+1] = Fore.WHITE+'S'+Fore.GREEN
            except IndexError:
                pass



    for i in range(5,9):
        try:
            if socketInData[i] != [0,0]:
                scan[int(socketInData[i][1]/1000)+1][int(socketInData[i][0]/1000)+1] = Fore.RED+'E'+Fore.GREEN
        except IndexError:
            pass

    if socketInData[0] != [0,0]:
        try:
            scan[int(socketInData[0][1]/1000)+1][int(socketInData[0][0]/1000)+1] = Fore.WHITE+'Y'+Fore.GREEN
        except IndexError:
            pass

    for y in range(0,11):
        for x in range(0,11):
            print(scan[y][x],end = '   ', flush = True)
            #delay(50)
        print()
    print()
    print()

def calcHits():
    global level1
    while True:
        for y in range(0,len(level1)):
            for x in range(0,len(level1[y])):
                if level1[y][x] == 1:
                    if inLimit(socketInData[0][0],x*1000-1,x*1000+1001) == True and inLimit(socketInData[0][1],y*1000-1,y*1000+1001) == True:
                        socketSendData("set speed -10")
                        delay(100)
                        socketSendData("set speed 0")
                        #speed = 0.0
        delay(1000/framerate)

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
def showLive():
    global message, ab, mode, nowTime
    while(flag1):
        clear()
        printText("Speed:            "+str(round(socketInData[45],2)))
        printText("Course:           "+str(round(socketInData[46],2)))
        printText("Depth:            "+str(round(socketInData[47],2)))
        printText("Health:           "+str(socketInData[4]))
        printText("Crew Number:      "+str(socketInData[3]))
        printText("Position:         X: "+str(round(socketInData[0][0],2))+" Y: "+str(round(socketInData[0][1],2)))
        printText("Torpedoes Loaded: "+ str(socketInData[1] + socketInData[2]))
        printText("Shells Loaded:    "+ str(socketInData[60]))
        print()
        printText("Targets:")
        print()

        for i in range(5,9):
            if socketInData[i] != [0,0]:
                distance,angle = detect(socketInData[0],socketInData[i])
                printText("Enemy Ship"+":   Position: X: "+str(round(socketInData[i][0],2))+" Y: "+str(round(socketInData[i][1],2))+"  Distance: "+str(round(distance,2))+" Bearing: "+str(round(angle,2)))
        print()
        printText("Intercom: ")
        if message != '':
            #Tue Jun  6 14:35:58 2023
            #nowTime = time.asctime()
            printText(nowTime[11:16]+"  "+message,color = Fore.RED)

        print()
        printText("Long Range Sonar  x10")
        scanSonarLong()
        if mode == 0:
            printText("Short Range Sonar x1")
            scanSonarShort()
        print("Torpedoes Fired:")
        for i in ab:
            if socketInData[i] != [0,0]:
                print("Torpedo:   Position X: "+str(round(socketInData[i][0],2))+" Y: "+str(round(socketInData[i][1],2)))
        print("Shells Fired:")
        for i in ba:
            if socketInData[i] != [0,0]:
                print("Shell:   Position X: "+str(round(socketInData[i][0],2))+" Y: "+str(round(socketInData[i][1],2)))
        print()

        printText("Press Enter to Stop")
        oldHealthf = socketInData[4][0]
        oldHealthm = socketInData[4][1]
        oldHealthr = socketInData[4][2]
        delay(500)
        if socketInData[4][0] <= 0 or socketInData[4][1] <= 0 or socketInData[4][2] <= 0:
            break
        if socketInData[4][0] < oldHealthf:
            #oldHealthf = socketInData[4][0]
            message = "Sir! We have been hit at the bow."
            nowTime = time.asctime()
        if socketInData[4][1] < oldHealthm:
            #oldHealthm = socketInData[4][1]
            message = "Sir! We have been hit at the center."
            nowTime = time.asctime()
        if socketInData[4][2] < oldHealthr:
            #oldHealthr = socketInData[4][2]
            message = "Sir! We have been hit at the stern."
            nowTime = time.asctime()
        if socketInData[39] == 1 or socketInData[40] == 1 or socketInData[41] == 1 or socketInData[42] == 1 or socketInData[43] == 1 or socketInData[44] == 1:
            message = "Sir! Torpedo Hit!"
            nowTime = time.asctime()
        if socketInData[58] == 1 or socketInData[59] == 1:
            message = "Sir! Shell Hit!"
            nowTime = time.asctime()
        if socketInData[0] == [0,0]:
            message = "Sir! Our ship is sinking."
            nowTime = time.asctime()
            break
    #return 0

def socketThread():
    global socketInData
    #socketInData = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
    while True:

        #delay(1000/framerate)

        data = sockobj.recv(1024)
        while not data:
            data = sockobj.recv(1024)
        #data = sockobj.recv(1024)
        #print(data)
        try:
            socketInData = pickle.loads(data)
        except:
            pass
        if socketInData[4][0] <= 0 or socketInData[4][1] <= 0 or socketInData[4][2] <= 0:
            break
        #print(data)
        #print(socketInData)

def socketSendData(dat):
    sockobj.send(pickle.dumps(dat))




#clear()
#flag = True

#printText("Mission Breifing:")
#printText("You have been chosen for a mission to attack 3 enemy cargo ships 150 km off the coast of England.")
#printText("You are in command of the newest model, Uboat 1944.")
#printText("Specifications:")
#printText("Max Speed: 10 knots\nCrew: 15 men, 5 officers\nForward torpedoes: 4\nAft torpedoes: 2")
#printText("Will you accept this request [Y, N]")
#input(">>")
#printText("Good luck this mission depends on you.")
#delay(1000)
#clear()

#myBoat = Uboat(0, 4, 2, [[1,3],[1,3],[1,4],[1,1],[1,4],0,0]], [100,100,100], [random.randint(0,999),random.randint(0,999)],0,-10)



#random.seed(time.time())


#torpedoE0 = TorpedoE(0)
#torpedoE1 = TorpedoE(0)
#torpedoE2 = TorpedoE(0)
#torpedoE3 = TorpedoE(0)
#torpedoE4 = TorpedoE(0)
#torpedoE5 = TorpedoE(0)

#enemy1 = EnemyShip(100)


#d,r = myBoat.detect([0,0],[3,4])
#print(d)
#print(r)
#print(time.time())


sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.connect((serverHost, serverPort))
da = sockobj.recv(1024)
while not da:
    da = sockobj.recv(1024)
daa = pickle.loads(da)
if daa == 0:
    name = "Player 1"
elif daa == 1:
    name = "Player 2"
elif daa == 2:
    name = "Player 3"
elif daa == 3:
    name = "Player 4"
elif daa == 4:
    name = "Player 5"

#_thread.start_new_thread(calculateBoat,(myBoat,))

_thread.start_new_thread(socketThread,())

delay(1000)
_thread.start_new_thread(calcHits,())
#input()
#print(socketInData)


#_thread.start_new_thread(enemy1.checkEnemyShip,())


#_thread.start_new_thread(torpedoE0.checkTorpedo,(1,))
#_thread.start_new_thread(torpedoE1.checkTorpedo,(2,))
#_thread.start_new_thread(torpedoE2.checkTorpedo,(3,))
#_thread.start_new_thread(torpedoE3.checkTorpedo,(4,))
#_thread.start_new_thread(torpedoE4.checkTorpedo,(5,))
#_thread.start_new_thread(torpedoE5.checkTorpedo,(6,))




#_thread.start_new_thread(calculateBoat,(enemy1,))
#_thread.start_new_thread(calculateBoat,(enemy2,))
#_thread.start_new_thread(calculateBoat,(enemy3,))

#_thread.start_new_thread(myBoat.reloadTube,(0,))
#_thread.start_new_thread(myBoat.reloadTube,(1,))

#_thread.start_new_thread(damageThread,(myBoat,))


while True:

    #while True:

            #print(enemy1.health)
            #print(hit1,hit2,hit3,hit4,hit5,hit6)
            #if hit1 == 1:
                #del torpedo0
            #if hit2 == 1:
                #del torpedo1
            #if hit3 == 1:
                #del torpedo2
            #if hit4 == 1:
                #del torpedo3
            #if hit5 == 1:
                #del torpedo4
            #if hit6 == 1:
                #del torpedo5

    flag1 = True
    _thread.start_new_thread(showLive,())
    input()
    flag1 = False
    delay(50)
    if socketInData[4][0] <= 0 or socketInData[4][1] <= 0 or socketInData[4][2] <= 0:
        break
    printText("C:  Set Course")
    printText("S:  Set Speed")
    printText("D:  Set Depth")
    printText("T:  Fire Torpedo")
    printText("G:  Fire Deck Gun")
    printText("M:  Crew Management")
    printText("L:  Show Live View")
    printText("A:  Abandon Ship")
        #print(socketInData)
        #print(calculateScan(socketInData[0],socketInData[5],-1*course+90))
        #print(getCrewPoints((socketInData[3][3])))
            #print(socketOutData)
    choice = getInput(">> ",typ = str)
    choice = choice.lower()
            #clear()

    if socketInData[4][0] <= 0 or socketInData[4][1] <= 0 or socketInData[4][2] <= 0:
        break

    if choice == 'c':
        if (getCrewPoints(socketInData[3][2]) > 0) and (socketInData[4][1] > 60):
            printText("      -90")
            printText("       |")
            printText("       |")
            printText("180----o-----0")
            printText("       |")
            printText("       |")
            printText("       90")
            num = getInput("Set Course: ",typ = float)
            course = num
            message = "New course: "+str(num)
            nowTime = time.asctime()
            socketSendData("set course "+str(num))
        else:
            printText("Sir, the course cannot be set.")
    elif choice == 's':
        if socketInData[4][2] > 60 and getCrewPoints((socketInData[3][3])) > 0:
            while True:
                num = getInput("Set Speed: ",typ = float)
                if num > 20.0 or num < -20.0:
                    printText("Sir, the max speed is 20.")
                else:
                    break
            message = "New speed: "+str(num)
            nowTime = time.asctime()
            socketSendData("set speed "+str(num))
            speed = num
        else:
            printText("Sir, the speed cannot be set.")
    elif choice == 'd':
        if (getCrewPoints(socketInData[3][2]) > 0) and (socketInData[4][1] > 60):
            num = getInput("Set Depth [-100 to 0]: ",typ = float)
            message = "New depth: "+str(num)
            nowTime = time.asctime()
            socketSendData("set depth "+str(num))
            depth = num
        else:
            printText("Sir, the depth cannot be set.")
    elif choice == 't':
        #clear()
        printText("Forward Tube: "+ str(socketInData[1])+" Left")
        printText("Aft Tube    : "+ str(socketInData[2])+" Left")
        while True:
            tube = getInput("Select Tube:\n1: Forward Tube\n2: Aft Tube\n3: Cancel\n>> ")
            if tube == 1:
                if socketInData[1] > 0:
                    #socketInData[1] -= 1
                    break
                else:
                    printText("Sir, that tube is empty.")
            if tube == 2:
                if socketInData[2] > 0:
                    #socketInData[2] -= 1
                    break
                else:
                    printText("Sir, that tube is empty.")
            if tube == 3:
                break
        if tube != 3:
            printText("      -90")
            printText("       |")
            printText("       |")
            printText("180----o-----0")
            printText("       |")
            printText("       |")
            printText("       90")
            c = getInput("Set Torpedo Course [-180 to 180] (Relative to Boat Bearing): ",typ = float)
            message = "Torpedo in the water."
            nowTime = time.asctime()
            socketSendData("fire torpedo "+str(tube)+' '+str(c))

        #if myBoat.fireTorpedo(c,enemy1.position) == True:
    elif choice == 'm':
        while True:
            o1 = makeDigits(socketInData[3][0][0], 2)
            m1 = makeDigits(socketInData[3][0][1], 2)
            o2 = makeDigits(socketInData[3][1][0], 2)
            m2 = makeDigits(socketInData[3][1][1], 2)
            o3 = makeDigits(socketInData[3][2][0], 2)
            m3 = makeDigits(socketInData[3][2][1], 2)
            o4 = makeDigits(socketInData[3][3][0], 2)
            m4 = makeDigits(socketInData[3][3][1], 2)
            o5 = makeDigits(socketInData[3][4][0], 2)
            m5 = makeDigits(socketInData[3][4][1], 2)
            o6 = makeDigits(socketInData[3][5][0], 2)
            m6 = makeDigits(socketInData[3][5][1], 2)
            o7 = makeDigits(socketInData[3][6][0], 2)
            m7 = makeDigits(socketInData[3][6][1], 2)

            h0 = makeDigits(socketInData[4][0], 3)
            h1 = makeDigits(socketInData[4][1], 3)
            h2 = makeDigits(socketInData[4][2], 3)

            printText("      -------------------                   ---------           ______________                  ")
            printText("     |   Damage Control  |                 |         |         |   Deck Gun   |           ")
            printText(f"     |   O:{o6}     M:{m6}   |                 |         |         |     O:{o7}     |                 ")
            printText(f"      -------------------                  |         |         |     M:{m7}     |            ")
            printText(" --------------------------------------------------------------------------------------------- ")
            printText("|  Forward   |  Crew Quarters |      Command Room       |      Engine Room      |     Aft     |")
            printText("|            |                |                         |                       |             |")
            printText(f" \ O:{o1} M:{m1} |   O:{o2} M:{m2}    |        O:{o3} M:{m3}        |        O:{o4} M:{m4}      | O:{o5} M:{m5}  /")
            printText("  \          |                |                         |                       |           / ")
            printText("   \_______________________________________________________________________________________/  ")
            printText(f"  Bow    Status: {h0}%                   Status: {h1}%                     Status: {h2}%   Stern          ")

            printText("1: Change Forward Torpedo")
            printText("2: Change Crew Quarters")
            printText("3: Change Command Room")
            printText("4: Change Engine Room")
            printText("5: Change Aft Torpedo")
            printText("6: Change Damage Control")
            printText("7: Change Deck Gun")
            printText("8: Exit Crew Management")
            change = getInput(">> ")
            if change == 8:
                break
            printText("1: Officer\n2: Men")
            tp = getInput(">> ")
            while True:
                printText("How many should be reassigned: ",end = '')
                reassign = getInput()
                if reassign > socketInData[3][change-1][tp-1]:
                    printText("Sorry that is not possible.")
                else:
                    break
            while True:
                printText("1: Forward Torpedo")
                printText("2: Crew Quarters")
                printText("3: Command Room")
                printText("4: Engine Room")
                printText("5: Aft Torpedo")
                printText("6: Damage Control")
                printText("7: Deck Gun")
                printText("To which location: ",end = '')
                change1 = getInput()
                if change1 != 7:
                    break
                else:
                    if socketInData[47] > -5:
                        break
                    else:
                        printText("Sorry that is not possible. You are underwater.")

            printText("Reassigning...", end = '')
            #print("set crew "+str(change-1)+' '+str(tp-1)+' '+str(reassign*-1))
            socketSendData("set crew "+str(change-1)+' '+str(tp-1)+' '+str(reassign*-1))
            #myBoat.crewNum[][] -= reassign
            #print("set crew "+str(change1-1)+' '+str(tp-1)+' '+str(reassign))
            socketSendData("set crew "+str(change1-1)+' '+str(tp-1)+' '+str(reassign))
            #myBoat.crewNum[change1-1][tp-1] += reassign
            delay(2000)
            print('\n')
    elif choice == 'g':
        if socketInData[60] > 0 and getCrewPoints(socketInData[3][6]) > 0 and socketInData[47] > -5:
            c = getInput("Set Shell Course [-180 to 180] (Relative to Boat Bearing): ",typ = float)
            angle = getInput("Set Gun Angle [0 to 90]: ",typ = float)
            c = makeDigits(c,3)
            angle = makeDigits(angle,2)
            socketSendData("fire shell "+c+' '+angle)
            message = "Shell Fired."
            nowTime = time.asctime()
        else:
            printText("Sorry, you cannot fire the Deck Gun.")
            delay(2000)



printText("Game Over. Your ship has sunk.")

sockobj.close()
