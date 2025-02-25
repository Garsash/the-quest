from objects.spike import *
from objects.player import *
from objects.end import *
from objects.sign import *
from objects.flamethrower import *
from objects.snake import *
from objects.enemy import *
from objects.box import *
from objects.button import *
from objects.switch import *

wallTiles = ["#","=","T","/","&", "w","H","h","|","?","r","k","Y"]
deathTiles = ["^","~","-","$","%","E","("]

def fill2DArray(array,char):
    maxLen=0
    for row in array:
        if len(row)>maxLen:
            maxLen=len(row)
    for row in range(len(array)):
        while len(array[row])!=maxLen:
            array[row].append(char)
    return array

class Level():
    tiles=[[]]
    objects=[]
    wallTiles = ["#","=","T","/","&", "w","H","h","|","?","r","k","Y"]
    deathTiles = ["^","~","-","$","%","E","("]
    level=0

    def tileExists(self,x,y):
        if y>=0 and y<len(self.tiles):
            if x>=0 and x<(len(self.tiles[y])):
                return True
        return False

    def readFile(self,fileDirectory):
        file=open(fileDirectory,"r")
        lines=file.readlines()
        for line in range(len(lines)):
            lines[line]=lines[line].strip().split(" ")
        #lines=fill2DArray(lines,"/")

        #print(lines)
        return lines

    def getTile(self,x,y):
        return self.tiles[y][x]

    def setTile(self,x,y,tile):
        self.tiles[y][x]=str(tile)

    def setTileDynamic(self,x,y,type=0):
        #0-floor
        if type==0:
            if self.getTile(x,y+1) in self.wallTiles:
                self.setTile(x,y,"_")
            else:
                self.setTile(x,y,".")

    def objectCheck(self,object,tile,x,y):
        if tile in object.instantiationTiles:
            object.create(x,y,self)

    def createObject(self,object):
        if type(object)==Player:
            self.player=object
        if type(object)==Snake:
            for body in object.body:
                self.setTile(body.x,body.y,":")
            self.setTile(object.x,object.y,":")
        else:
            self.setTileDynamic(object.x,object.y,0)
        self.objects.append(object)

    def getObjects(self):
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                tile=self.getTile(x,y)
                #print(tile)
                self.objectCheck(Player,tile,x,y)
                self.objectCheck(Spike,tile,x,y)
                self.objectCheck(End,tile,x,y)
                self.objectCheck(Sign,tile,x,y)
                self.objectCheck(Flamethrower,tile,x,y)
                self.objectCheck(Snake,tile,x,y)
                self.objectCheck(Enemy,tile,x,y)
                self.objectCheck(Box,tile,x,y)
                self.objectCheck(Button,tile,x,y)
                self.objectCheck(Switch,tile,x,y)

    def create(self,currentLevel):
        fileDirectory="levels/level"+str(currentLevel)+".txt" #test if json version exists, if json read that instead
        self.tiles=[[]]
        self.objects=[]
        self.level=currentLevel
        self.tiles=self.readFile(fileDirectory)
        self.getObjects()

    def __init__(self,currentLevel=0):
        self.create(currentLevel)
