import math

class Vector():
    def __init__(self,x:int=0, y:int=0):
        self.x=x
        self.y=y
    
    def transformLeft(self):
        x,y=self.y*-1,self.x
        return Vector(x,y)

    def transformRight(self):
        x,y=self.y,self.x*-1
        return Vector(x,y)

    def neighbors():
        return [Vector(0,-1),Vector(1,0),Vector(0,1),Vector(-1,0)]

    def __add__(self, other):
        return Vector(self.x+other.x,self.y+other.y)

    def __sub__(self, other):
        return Vector(self.x-other.x,self.y-other.y)

    def __str__(self):
        return "("+str(self.x)+", "+str(self.y)+")"

    def copy(self):
        return Vector(self.x, self.y)

rndTable=open("rnd.txt").read().strip().split(",")
for x in range(len(rndTable)):
    rndTable[x]=int(rndTable[x])

total=0

class Random():
    global rndTable
    
    def setRandom(x):
        return rndTable[x]

    def int(lowerLimit,higherLimit):
        diff=higherLimit-lowerLimit
        if diff < 0:
            raise ValueError("lower limit must be less than higher limit")
        elif diff==0:
            return lowerLimit
        random=math.floor(rndTable[total%255]*((diff+1)/256))
        random+=lowerLimit
        globals()["total"]+=1
        return random

    def choice(array):
        random = Random.int(0,len(array)-1)
        return array[random]