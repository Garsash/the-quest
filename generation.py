6##start defining rooms instead so we can add conections ect
from textwrap import wrap

size=[50,50]
map=[["/" for x in range(size[0])] for y in range(size[1])]

#indevidual doors
class Door():
    def __init__(self,xPos,yPos):
        self.x=xPos
        self.y=yPos

#collections of doors and their directions
class Doors():
    def __init__(self,Up,Down,Left,Right):
        self.up=Up
        self.down=Down
        self.left=Left
        self.right=Right
    
    def append(self,Up,Down,Left,Right):
        for x in Up:
            self.up.append(x)
        for x in Down:
            self.down.append(x)
        for x in Left:
            self.left.append(x)
        for x in Right:
            self.right.append(x)

allDoors=Doors([],[],[],[])

#entire rooms data and doors/connections
class Room():
    def __init__(self,Tiles,xPos,yPos,Width,Height,Doors):
        self.roomTiles=Tiles
        self.x=xPos
        self.y=yPos
        self.width=Width
        self.height=Height
        self.doors=Doors

##create a room and find data from file
def createRoom(xPos,yPos,file):
    file="levels\\rooms\\"+file+".txt"
    file = open(file, "r")
    lines = file.readlines()

    ##create and clean up room
    room=[]
    chars=0
    for line in lines:
        chars+=1
        if chars!=len(lines):
            line=line[:-1]
        line=wrap(line,1)
        room.append(line)
    
    up=[]
    down=[]
    left=[]
    right=[]
    for y in range(len(room)):
        for x in range(len(room[y])):
            char=room[y][x]
            if char=="U":
                up.append(Door(x,y))
            elif char=="D":
                down.append(Door(x,y))
            elif char=="L":
                left.append(Door(x,y))
            elif char=="R":
                right.append(Door(x,y))
    doors=Doors(up,down,left,right)
    allDoors.append(up,down,left,right)
    return Room(room,xPos,yPos,len(room[0]),len(room),doors)

##put room on map
def placeRoom():
    a=True

def drawArea(area):
    for y in area:
        line=""
        for x in y:
            line+=x+" "
        print(line)

room=createRoom(10,10,"start")

print(room.doors.left)
drawArea(room.roomTiles)

room=createRoom(10,10,"spikes0")

print(room.doors.left)
drawArea(room.roomTiles)

print(allDoors.left)

while True:
    open=True
