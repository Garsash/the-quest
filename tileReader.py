import json
from mathLib import Vector

fileDirectory=input("Enter file location: ")
if fileDirectory == "":
    fileDirectory="displayTiles.json"

file=open(fileDirectory)
text=file.read()
data=json.loads(text)

tilesData=data["Tiles"]

tiles={}
for tileData in tilesData:
	if type(tileData["from"])==string:
		fromTile=tileData["from"]
		if type(tileData["to"])==list:
			if tileData["to"][0].has_key("chance"):
			
			else:
			
		else:
			if tileData["to"].has_key("tile"):
				toTile=tileData["to"]["tile"]
			else:
				toTile=fromTile
			
	else:
		for tile in tileData["from"]:
			

#world=[]
#for y in range(worldSize[1]):
#    row=[]
#    for x in range(worldSize[0]):
#        row.append(" ")
#    world.append(row)
#
#wallData=data["walls"]
#
#for wall in wallData:
#    start=Vector(wall["from"][0],wall["from"][1])
#    end=Vector(wall["to"][0],wall["to"][1])
#    
#    if wall["type"]=="room":
#        for y in range(start.y-1,end.y+1):
#            for x in range(start.x,end.x+1):
#                if y==start.y or y==end.y or x==start.x or x==end.x:
#                    world[y][x]="#"
#				elif y==start.y-1:
#					world[y][x]="_"
#                else:
#					world[y][x]="."
#
#    if wall["type"]=="corridor":
#        for y in range(start.y-2,end.y+2):
#            for x in range(start.x,end.x+1):
#                if ((y==start.y-1 or y==end.y+1) and wall["dir"]=="horizontal") or ((x==start.x or x==end.x) and wall["dir"]=="vertical"):
#                    world[y][x]="#"
#				elif y==start.y-2:
#					world[y][x]="_"
#				else:
#					world[y][x]="."
#
#objectData=data["objects"]
#
#class Level():
#    objects=[]
#    def createObject(self,object):
#        self.objects.append(object)
#
#level=Level()
#
#print(objectData)
#
#for object in objectData:
#    type=object["type"]
#    if object.has_key("pos"): #hasattr is for object this is other kind of object
#        pos=Vector(object["pos"][0],object["pos"][1])
#    if type=="player":
#        print(object)
#        Player.create(pos.x,pos.y,level)
#    
#
#for y in world:
#    row=""
#    for x in y:
#        row+=x+" "
#    print("> "+row)
#
#print(level.objects)
#
#input()