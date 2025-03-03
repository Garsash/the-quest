import json
from mathLib import Vector
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

class Object():
    pos=None
    From=None
    to=None
    type=None
    time=None
    state=None
    text=None
    
class Level():
    objects=[]
    def createObject(self,object):
        self.objects.append(object)

def getTiles(data):
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

def getObjects(data, level):
    objectData=data["objects"]
    
    for object in objectData:
        obj=Object()
        obj.type=object["type"]
        
        ##get pos
        if "pos" in object.keys(): #hasattr is for object this is other kind of object
            obj.pos=Vector(object["pos"][0],object["pos"][1])
        elif "from" in object.keys() and "to" in object.keys():
            obj.From=Vector(object["from"][0],object["from"][1])
            obj.to=Vector(object["to"][0],object["to"][1])
        
        if "time" in object.keys():
            obj.time=object["time"]
        if "state" in object.keys():
            obj.state=object["state"]

        if "text" in object.keys():
            obj.text=object["text"]

        print(str(obj.From)+", "+str(obj.to))

        ##player
        if obj.type=="player":
            player=Player(obj.pos.x,obj.pos.y)
            level.createObject(player)
        
        ##spikes
        elif obj.type=="spikes":
            time=3
            state=False
            if obj.time!=None:
                time=obj.time
            if obj.state!=None:
                state=obj.state
            if obj.pos!=None:
                spike=Spike(obj.pos.x,obj.pos.y,state,time)
                level.createObject(spike)
            else:
                for y in range(obj.From.y,obj.to.y+1):
                    for x in range(obj.From.x,obj.to.x+1):
                        spike=Spike(x,y,state,time)
                        level.createObject(spike)
        
        elif obj.type=="sign":
            sign=Sign(obj.pos.x,obj.pos.y,obj.text)
            level.createObject(sign)

        elif obj.type=="end":
            end=End(obj.pos.x,obj.pos.y)
            level.createObject(end)

def readFile(fileDirectory):
    file=open(fileDirectory)
    text=file.read()
    data=json.loads(text)

    world=getTiles(data)
    level=Level()
    objects=getObjects(data,level)




fileDirectory=input("Enter file location: ")
if fileDirectory == "":
    fileDirectory="levels/rooms/level1.json"

readFile(fileDirectory)
input()