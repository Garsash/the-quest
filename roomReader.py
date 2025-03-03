import json
from mathLib import Vector
from objects.spike import *
from objects.player import *
from objects.end import *
from objects.sign import *
from objects.flamethrower import *
from objects.snake import *

class Object():
    pos=None
    From=None
    to=None
    type=None

fileDirectory=input("Enter file location: ")
if fileDirectory == "":
    fileDirectory="levels/rooms/level1.json"

file=open(fileDirectory)

text=file.read()

data=json.loads(text)

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

objectData=data["objects"]

class Level():
    objects=[]
    def createObject(self,object):
        self.objects.append(object)

level=Level()

print(objectData)

for object in objectData:
    obj=Object()
    obj.type=object["type"]
    
    ##get pos
    if "pos" in object.keys(): #hasattr is for object this is other kind of object
        obj.pos=Vector(object["pos"][0],object["pos"][1])
    elif "from" in object.keys() and "to" in object.keys():
        obj.From=Vector(object["from"][0],object["from"][1])
        obj.to=Vector(object["to"][0],object["to"][1])

    
    ##player
    if obj.type=="player":
        Player.create(obj.pos.x,obj.pos.y,level)

    elif obj.type=="spikes":
        if obj.pos!=None:
            Spike.create(obj.pos.x,obj.pos.y,level)
        elif obj.From!=None and obj.to!=None:
            for y in range(obj.From.y,obj.to.y):
                for x in range(obj.From.x,obj.to.y):
                    Spike.create(x,y,level)

    print(object)
    


    

for y in world:
    row=""
    for x in y:
        row+=x+" "
    print("> "+row)

print(level.objects)

input()
