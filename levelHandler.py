import json
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

class Object():
    pos=None
    From=None
    to=None
    type=None
    time=None
    state=None
    text=None

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

    ##def readFile(self,fileDirectory):
    ##    file=open(fileDirectory,"r")
    ##    lines=file.readlines()
    ##    for line in range(len(lines)):
    ##        lines[line]=lines[line].strip().split(" ")
    ##    #lines=fill2DArray(lines,"/")
    ##
    ##    #print(lines)
    ##    return lines

    def readFile(self,fileDirectory):
        file=open(fileDirectory)
        text=file.read()
        data=json.loads(text)

        world=self.getTiles(data)
        objects=self.getObjects(data)
        return world

    def getTiles(self,data):
        worldData=data["world"]
        worldSize=worldData["size"]
        world=[]
        for y in range(worldSize[1]):
            row=[]
            for x in range(worldSize[0]):
                row.append(" ")
            world.append(row)

        wallData=data["walls"]

        for wall in wallData:
            start=Vector(wall["from"][0],wall["from"][1])
            end=Vector(wall["to"][0],wall["to"][1])
            
            if wall["type"]=="room":
                for y in range(start.y-1,end.y+1):
                    for x in range(start.x,end.x+1):
                        if y==start.y or y==end.y or x==start.x or x==end.x:
                            world[y][x]="#"
                        else:
                            world[y][x]="."
                        if y==start.y-1:
                            world[y][x]="_"

            if wall["type"]=="corridor":
                for y in range(start.y-2,end.y+2):
                    for x in range(start.x,end.x+1):
                        if ((y==start.y-1 or y==end.y+1) and wall["dir"]=="horizontal") or ((x==start.x or x==end.x) and wall["dir"]=="vertical"):
                            world[y][x]="#"
                        elif y==start.y-2:
                            world[y][x]="_"
                        else:
                            world[y][x]="."
        return world

    def getObjects(self, data):
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
        ##objectData=data["objects"]
        ##
        ##for object in objectData:
        ##    obj=Object()
        ##    obj.type=object["type"]
        ##    
        ##    ##get pos
        ##    if "pos" in object.keys(): #hasattr is for object this is other kind of object
        ##        obj.pos=Vector(object["pos"][0],object["pos"][1])
        ##    elif "from" in object.keys() and "to" in object.keys():
        ##        obj.From=Vector(object["from"][0],object["from"][1])
        ##        obj.to=Vector(object["to"][0],object["to"][1])
        ##    
        ##    if "time" in object.keys():
        ##        obj.time=object["time"]
        ##    if "state" in object.keys():
        ##        obj.state=object["state"]
##
        ##    if "text" in object.keys():
        ##        obj.text=object["text"]
##
        ##    print(str(obj.From)+", "+str(obj.to))
##
        ##    ##player
        ##    if obj.type=="player":
        ##        Player.create(object,self)
        ##    
        ##    ##spikes
        ##    elif obj.type=="spikes":
        ##        time=3
        ##        state=False
        ##        if obj.time!=None:
        ##            time=obj.time
        ##        if obj.state!=None:
        ##            state=obj.state
        ##        if obj.pos!=None:
        ##            spike=Spike(obj.pos.x,obj.pos.y,state,time)
        ##            self.createObject(spike)
        ##        else:
        ##            for y in range(obj.From.y,obj.to.y+1):
        ##                for x in range(obj.From.x,obj.to.x+1):
        ##                    spike=Spike(x,y,state,time)
        ##                    self.createObject(spike)
        ##    
        ##    elif obj.type=="sign":
        ##        sign=Sign(obj.pos.x,obj.pos.y,obj.text)
        ##        self.createObject(sign)

        ##    elif obj.type=="end":
        ##        end=End(obj.pos.x,obj.pos.y)
        ##        self.createObject(end)

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

    ##def getObjects(self):
    ##    for y in range(len(self.tiles)):
    ##        for x in range(len(self.tiles[y])):
    ##            tile=self.getTile(x,y)
    ##            #print(tile)
    ##            self.objectCheck(Player,tile,x,y)
    ##            self.objectCheck(Spike,tile,x,y)
    ##            self.objectCheck(End,tile,x,y)
    ##            self.objectCheck(Sign,tile,x,y)
    ##            self.objectCheck(Flamethrower,tile,x,y)
    ##            self.objectCheck(Snake,tile,x,y)
    ##            self.objectCheck(Enemy,tile,x,y)
    ##            self.objectCheck(Box,tile,x,y)
    ##            self.objectCheck(Button,tile,x,y)
    ##            self.objectCheck(Switch,tile,x,y)

    def create(self,currentLevel):
        fileDirectory="levels/level"+str(currentLevel)+".json" #test if json version exists, if json read that instead
        self.tiles=[[]]
        self.objects=[]
        self.level=currentLevel
        self.tiles=self.readFile(fileDirectory)
        self.getObjects()

    def __init__(self,currentLevel=0):
        self.create(currentLevel)
