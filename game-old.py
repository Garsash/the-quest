from textwrap import wrap
import os
import time
#import click
import keyboard
from rcolors import colors
import random

from objects.player import Player
from mathLib import Vector

out=[]

#start_time = time.time()

#camera set up
cam=[0,0,15,15]
os.system("mode "+ str(cam[2]*2+5)+", "+str(cam[3]+9))

#tile groups
wallTiles = ["#","=","T","/","&","D", "w","H","h","|","?","r","k","Y"] #Map.py
deathTiles = ["^","~","-","$","%","E","("] #Map.py

#random number generation
rndTable=open("rnd.txt").read().strip().split(",")
for x in range(len(rndTable)):
    rndTable[x]=int(rndTable[x])

#get title card from files
def getTitle(name):
    #open and read
    title="titles\\"+name+".txt"
    titleFile = open(title, "r")
    titleLines = titleFile.readlines()
    title=""
    #loop and assign colours
    for lines in titleLines:
        line=""
        for character in lines:
            if character == "y":
                line+="\033[1;33;40m"
            elif character == "w":
                line+="\033[1;37;40m"
            elif character == "%":
                line+="\033[1;31;40m"
            elif character == "p":
                line+="\033[1;35;40m"
            else:
                line+=character
        title+=line
    return title
    

def getMap(x,y):
    global map
    return map[y][x]

def setMap(x,y,tile):
    global map
    map[y][x]=str(tile)

#define spike object
class Spike():
    @classmethod
    def create(cls,x,y,map):
        tile=getMap(x,y)  
        global spikes    

        if tile == '^' or tile == ',':
            spikes.append(Spike(x,y,0,3))
        if tile == '^' or tile == '"':
            spikes.append(Spike(x,y,0,7))
        setMap(x,y,".")
    def __init__(self,xPos,yPos,State,Timer):
        self.x = xPos
        self.y = yPos
        self.state = State
        self.maxTime = Timer
        self.time = 0
    
    def tick(self):
        #up
        if self.time == 0:
            map[self.y][self.x]="^"
            self.state = 1
        #down
        elif self.time == 2:
            map[self.y][self.x]=","
            self.state = 0
        self.time+=1
        #reset
        if self.time > self.maxTime:
            self.time = 0

#define flamethrower object
class Flamethrower():
    @classmethod
    def create(cls,x,y,map):
        tile=getMap(x,y)  
        global flames   

        #find and create flamethrowers
        if tile == '=':
            left=getMap(x-1,y)  
            right=getMap(x+1,y)  
            flameDir=0
            if left in wallTiles:
                flameDir=1
            elif right in wallTiles:
                flameDir=-1
            else:
                return
            flames.append(Flamethrower(x,y,0,flameDir,3,7))

    def __init__(self,xPos,yPos,Stage,Facing,Range,Timer):
        self.x = xPos
        self.y = yPos
        self.stage = Stage
        self.facing = Facing
        self.range= Range
        self.maxTime = Timer
        self.time = 0
    
    def tick(self):
        #loop range
        for dist in range(self.range):
            #selfs
            if self.time >= 0 and self.time <= 3:
                if (dist+(self.time%2))%2==0:
                    map[self.y][self.x+((dist+1)*self.facing)]="~"
                else:
                    map[self.y][self.x+((dist+1)*self.facing)]="-"
            #reset
            elif self.time==4:
                map[self.y][self.x+((dist+1)*self.facing)]="."
            #warning
            elif self.time==7:
                map[self.y][self.x+(1*self.facing)]=";"
        self.time+=1
        #reset
        if self.time > self.maxTime:
            self.time = 0

#define snake object
class Snake():
    def __init__(self,xPos,yPos,Segments):
        self.x = xPos
        self.y = yPos
        self.segments = Segments
    
    def getDirections(self,previousSegment):
        #forward=[self.x-previousSegment.x,self.y-previousSegment.y]
        forward=Vector(self.x-previousSegment.x,self.y-previousSegment.y)
        #out.append(str(aforward.x)+str(aforward.y))
        #left=[forward[1]*-1,forward[0]]
        left=forward.transformLeft()
        #out.append(str(vleft.x)+str(vleft.y))
        #right=[forward[1],forward[0]*-1]
        right=forward.transformRight()
        #out.append(str(vright.x)+str(vright.y))
        #out.append("^ "+str(aforward.x)+", "+str(aforward.y)+" < "+str(vleft.x)+", "+str(vleft.y)+" > "+str(vright.x)+", "+str(vright.y))
        return forward,left,right

    def tick(self):
        #direction vecors
        forward,left,right=self.getDirections(self.segments[0])

        #find next space
        if getMap(self.x+forward.x,self.y+forward.y) == ":" or getMap(self.x+forward.x,self.y+forward.y) == "(":
            nextPos=Vector(self.x+forward.x,self.y+forward.y)
        elif getMap(self.x+left.x,self.y+left.y) == ":" or getMap(self.x+left.x,self.y+left.y) == "(":
            nextPos=Vector(self.x+left.x,self.y+left.y)
        elif getMap(self.x+right.x,self.y+right.y) == ":" or getMap(self.x+right.x,self.y+right.y) == "(":
            nextPos=Vector(self.x+right.x,self.y+right.y)

        #delete end segment
        setMap(self.segments[-1].x,self.segments[-1].y,":")
        for neighbor in neighborVectors:
            if getMap(self.segments[-1].x+neighbor.x,self.segments[-1].y+neighbor.y) == "#":
                setMap(self.segments[-1].x,self.segments[-1].y,"(")

        self.segments.pop(-1)

        #add new segment
        setMap(self.x,self.y,"%")
        self.segments.insert(0,Segment(self.x,self.y))

        #move forward
        self.x=nextPos.x
        self.y=nextPos.y
        setMap(self.x,self.y,"$")

#define snake segment object
class Segment():
    def __init__(self,xPos,yPos):
        self.x = xPos
        self.y = yPos

#define enemy object
class Enemy():
    def __init__(self,xPos,yPos):
        self.x = xPos
        self.y = yPos
        self.here = "."

    def tick(self):
        #find distance from player
        distx=player.x-enemy.x
        disty=player.y-enemy.y
        target=[0,0]

        if abs(distx) <= 6 and abs(disty) <= 6:
            #create scent map
            scentMap=[]
            for y in range(13):
                row=[]
                for x in range(13):
                    row.append(26)
                scentMap.append(row)

            #create searching map
            searching=[]
            for y in range(13):
                row=[]
                for x in range(13):
                    row.append(False)
                searching.append(row)

            #set player location
            searching[6][6]=True
            scentMap[6][6]=0
            nodes=[[6,6]]

            #loop through nodes
            for node in nodes:
                #look at neighbors
                for neighbor in neighbors:
                    #variable set up
                    neighborx=node[0]+neighbor[0] #nx
                    neighbory=node[1]+neighbor[1] #ny
                    nodex=node[0] #hx
                    nodey=node[1] #hy
                    worldy=player.y+neighbory-6
                    worldx=player.x+neighborx-6

                    #if inside map
                    if neighbory < 0 or neighbory >= 13:
                        continue
                    if neighborx < 0 or neighborx >= 13:
                        continue

                    here=scentMap[nodey][nodex]
                    #if not searched already
                    if searching[neighbory][neighborx] == False:
                        #is there a wall
                        state=map[worldy][worldx]
                        if state in wallTiles or state in deathTiles and state != "E":
                            continue

                        #get smallest scent
                        if scentMap[neighbory][neighborx] >= here:
                            scentMap[neighbory][neighborx]=here+1
                            nodes.append([neighborx,neighbory])
                        searching[neighbory][neighborx]=True

                        #found enemy
                        if state=="E" and worldx==enemy.x and worldy==enemy.y:
                            #out.append([worldx,worldy])
                            #Loc=[worldx,worldy]
                            #out.append("enemy pos "+str(Loc))
                            #if Loc in foundEnemies:
                            #    continue
                            nodes=[]
                            lowest=26
                            target=[0,0]
                            values=[]

                            #look at neighbors
                            for Neighbor in neighbors:   
                                enemyx=neighborx+Neighbor[0]
                                enemyy=neighbory+Neighbor[1]
                                if enemyy < 0 or enemyy >= 13:
                                    continue
                                if enemyx < 0 or enemyx >= 13:
                                    continue
                                #find values
                                if map[player.y+enemyy-6][player.x+enemyx-6] == "E":
                                    continue
                                values.append([Neighbor[0],Neighbor[1],scentMap[enemyy][enemyx]])

                            #get smallest values
                            minV=24
                            for min in values:
                                if min[2] < minV:
                                    minV=min[2]

                            #pick random closest direction
                            closest=[value for value in values if value[2]==minV]
                            if len(closest)>=1:
                                choice=random.choice(closest)
                                target=[choice[0],choice[1]]
                            break
        #move enemy
        map[enemy.y][enemy.x]=enemy.here
        enemy.x+=target[0]
        enemy.y+=target[1]
        enemy.here=map[enemy.y][enemy.x]
        map[enemy.y][enemy.x]="E"

#define box object
class Box():
    def __init__(self,xPos,yPos):
        self.x = xPos
        self.y = yPos
        self.here = "."
    
    def move(self,moveX,moveY):
        #move box
        tileTest=map[self.y+moveY][self.x+moveX]
        if not tileTest in wallTiles and not tileTest in deathTiles:
            map[self.y][self.x] = self.here
            self.x+=moveX
            self.y+=moveY
            self.here=map[self.y][self.x]
            map[self.y][self.x]="&"
        else:
            move=[0,0]

#define button object
class Button():
    def __init__(self,xPos,yPos,Doors,Wires):
        self.x = xPos
        self.y = yPos
        self.state = False
        self.doors = Doors
        self.wires=Wires
    
    def pressed(self):
        self.state=True
        for door in self.doors:
            map[door.y][door.x]="o"
        for wire in self.wires:
            if any(enemy.x == wire[0] and enemy.y == wire[1] for enemy in enemies):
                for enemy in enemies:
                    enemy.here="o"
            else:
                map[wire[1]][wire[0]]="o"

    def released(self):
        self.state=False
        for door in self.doors:
            map[door.y][door.x]="D"
        for wire in self.wires:
            if any(enemy.x == wire[0] and enemy.y == wire[1] for enemy in enemies):
                for enemy in enemies:
                    enemy.here="b"
            else:
                map[wire[1]][wire[0]]="b"

    def tick(self):
        #if pressed
        if any(box.x == self.x and box.y == self.y for box in boxes) or any(enemy.x == self.x and enemy.y == self.y for enemy in enemies) or self.x == player.x+move[0] and self.y == player.y+move[1]:
            self.pressed()
        else:
            self.released()

#define switch object
class Switch():
    def __init__(self,xPos,yPos,Doors,Wires):
        self.x = xPos
        self.y = yPos
        self.state = False
        self.doors = Doors
        self.wires=Wires

    def tick(self):
        if any(box.x == self.x and box.y == self.y for box in boxes) or any(enemy.x == self.x and enemy.y == self.y for enemy in enemies) or self.x == player.x+move[0] and self.y == player.y+move[1]:
                if self.state==False:
                    self.state=True
                    for door in self.doors:
                        map[door.y][door.x]="o"
                    if any(enemy.x == self.x and enemy.y == self.y for enemy in enemies):
                        for enemy in enemies:
                            enemy.here="s"
                    else:
                        map[self.y][self.x]="s"
                    for wire in self.wires:
                        if any(enemy.x == wire[0] and enemy.y == wire[1] for enemy in enemies):
                            for enemy in enemies:
                                enemy.here="o"
                        else:
                            map[wire[1]][wire[0]]="o"
                else:
                    self.state=False
                    for door in self.doors:
                        map[door.y][door.x]="D"
                    if any(enemy.x == self.x and enemy.y == self.y for enemy in enemies):
                        for enemy in enemies:
                            enemy.here="S"
                    else:
                        map[self.y][self.x]="S"
                    for wire in self.wires:
                        map[wire[1]][wire[0]]="b"

#define door object
class Door():
    def __init__(self,xPos,yPos):
        self.x = xPos
        self.y = yPos

#display opening title card
print(getTitle("title"))

#get level skip input
cheat=input("")
os.system("cls")

#try to skip levels

debug=False
if "d" in cheat:
    debug=True

times=False
if "t" in cheat:
    times=True
tps=[]


numbers=["0","1","2","3","4","5","6","7","8","9"]
for pos in range(len(cheat)):
    if not cheat[pos] in numbers:
        cheat=cheat.replace(cheat[pos]," ")
cheat=cheat.replace(" ","")

try:
    int(cheat)
except:
    cheat=1

level=cheat

first=True

#create global object arrays
spikes=[]
flames=[]
snakes=[]
enemies=[]
boxes=[]
buttons=[]
switches=[]
neighbors=[[-1,0],[0,-1],[1,0],[0,1]]
neighborVectors=[Vector(-1,0),Vector(0,-1),Vector(1,0),Vector(0,1)]

#create player
player=Player(0,0)

map=[]

#define get level function
def getLevel(Level):
        if times==True:
            start_time=time.time()
        #get and reset global variables
        global first, spikes, flames, snakes, enemies, cam, map, player, boxes, buttons, switches
        spikes,flames,snakes,enemies,boxes,buttons,switches=[],[],[],[],[],[],[]
        cam=[0,0,15,15]
        player=Player(0,0)
        map=[]
        
        fill=""
        for x in range(cam[2]):
            fill+="/"
		
        #open level file
        file="levels\level"+str(Level)+".txt"
        file = open(file, "r")
        lines = file.readlines()

        i=0
        #reset map
        map=[]

        #set up file format
        maxmap=0
        for line in lines:
            i+=1
            if i!=len(lines):
                line=line[:-1]
            #print(x)
            line=wrap(line+fill,1)
            map.append(line)
            if maxmap <= len(line):
                maxmap=len(line)

        fill2=[]
        for x in range(maxmap):
            fill2.append("/")
        for x in range(cam[3]):
            map.append(fill2)

        #loop through map
        for y in range(len(map)):
            for x in range(len(map[y])):

                Spike.create(x,y,map)

                Flamethrower.create(x,y,map)

                #find and create snakes
                if map[y][x] == '$':
                    #find body parts
                    body=[Segment(x,y)]
                    for bit in body:
                        for neighbor in neighbors:
                            target=[neighbor[0]+bit.x,neighbor[1]+bit.y]
                            if any(part.x==target[0] and part.y==target[1] for part in body):
                                continue
                            if map[target[1]][target[0]] == "%":
                                body.append(Segment(target[0],target[1]))
                    body.pop(0)
                    snakes.append(Snake(x,y,body))

                #find and create enemies
                elif map[y][x] == 'E':
                    enemies.append(Enemy(x,y))

                #find and create boxes
                elif map[y][x] == '&':
                    boxes.append(Box(x,y))

                #find and create buttons
                elif map[y][x] == 'p':
                    wires=[[x,y]]
                    doors=[]
                    #find wires
                    for wire in wires:
                        for neighbor in neighbors:
                            target=[neighbor[0]+wire[0],neighbor[1]+wire[1]]
                            if any(Wire[0]==target[0] and Wire[1]==target[1] for Wire in wires):
                                continue
                            if map[target[1]][target[0]] == "b":
                                wires.append([target[0],target[1]])
                            if map[target[1]][target[0]] == "D":
                                doors=[Door(target[0],target[1])]
                                #find doors
                                for door in doors:
                                    for meighbor in neighbors:
                                        Target=[meighbor[0]+door.x,meighbor[1]+door.y]
                                        if any(Door.x==Target[0] and Door.y==Target[1] for Door in doors):
                                            continue
                                        if map[Target[1]][Target[0]] == "D":
                                            doors.append(Door(Target[0],Target[1]))
                    wires.pop(0)
                    buttons.append(Button(x,y,doors,wires))

                #find and create switches
                elif map[y][x] == 'S':
                    wires=[[x,y]]
                    doors=[]
                    #find wires
                    for wire in wires:
                        for neighbor in neighbors:
                            target=[neighbor[0]+wire[0],neighbor[1]+wire[1]]
                            if any(Wire[0]==target[0] and Wire[1]==target[1] for Wire in wires):
                                continue
                            if map[target[1]][target[0]] == "b":
                                wires.append([target[0],target[1]])
                            if map[target[1]][target[0]] == "D":
                                doors=[Door(target[0],target[1])]
                                #find doors
                                for door in doors:
                                    for meighbor in neighbors:
                                        Target=[meighbor[0]+door.x,meighbor[1]+door.y]
                                        if any(Door.x==Target[0] and Door.y==Target[1] for Door in doors):
                                            continue
                                        if map[Target[1]][Target[0]] == "D":
                                            doors.append(Door(Target[0],Target[1]))
                    wires.pop(0)
                    switches.append(Switch(x,y,doors,wires))

                #find and move player
                elif map[y][x] == '@':
                    if map[y+1][x] == "#":
                        map[y][x]="_"
                    else:
                        map[y][x]="."
                    player.x=x
                    player.y=y

                #switch out animation shapes
                elif map[y][x] == '-' or map[y][x] == '~' or map[y][x] == ';':
                    if map[y+1][x] == "#":
                        map[y][x]="_"
                    else:
                        map[y][x]="."

                #random tile generation
                if map[y][x] == ".":
                    loc=(x*y)
                    while loc>255:
                        loc-=255
                    if rndTable[loc]>200:
                        map[y][x]="'"
                elif map[y][x] == "g":
                    loc=(x*y)
                    while loc>255:
                        loc-=255
                    if rndTable[loc]>200:
                        map[y][x]="G"
                elif map[y][x] == "#":
                    loc=(x*y)
                    while loc>255:
                        loc-=255
                    if rndTable[loc]>235:
                        map[y][x]="Y"
                        
        #set camera position
        cam[0]=player.x-int(cam[2]/2)
        cam[1]=player.y-int(cam[3]/2) 
        save=[]

        #put player on map
        map[player.y][player.x]="@"
        if times==True:
            end_time=time.time()
            out.append("level load: "+str(end_time-start_time))

#get initial level
getLevel(level)

#set up variables
loops=0
dir=1
      
move=[0,0]
delay=0
looped=0
savePoint=[0,0]

#-t out.append(end_time-start_time)

#game loop
while True:
    delay+=1
    #step frame if button press
    if delay>= 10 and move[0]!=0 or delay>= 10 and move[1]!=0 or first==True:
        if times==True:
            start_time=time.time()
        delay=0
        saved=False
        first=False
        looped+=1
        
        #clear screen
        os.system("cls")

        #loop through spikes and change state
        for spike in spikes:
            spike.tick()

        #loop through flamethrowers and change state
        for flame in flames:
            flame.tick()

        #loop through snakes and move forward
        for snake in snakes:
            snake.tick()

        #loop through enemies and move
        for enemy in enemies:
            enemy.tick()
            
        #if player moving box
        if map[player.y+move[1]][player.x+move[0]] == "&":
            player.moveBox()
                        
        #loop through buttons and check          
        for button in buttons:
            button.tick()

        #loop through switches and check
        for switch in switches:
            switch.tick()

        #reset player pos
        if map[player.y][player.x] == '@':
            if map[player.y+1][player.x] == "#":
                map[player.y][player.x] = "_"
            else:
                map[player.y][player.x] = "."

        #move player and camera
        tileH = map[player.y][player.x+move[0]]
        if not tileH in wallTiles:
            player.x += move[0]
        tileV = map[player.y+move[1]][player.x]
        if not tileV in wallTiles:
            player.y += move[1]
        cam[0]=player.x-int(cam[2]/2)
        cam[1]=player.y-int(cam[3]/2)
        tile = map[player.y][player.x]

        #kill player
        if tile in deathTiles:
            os.system("cls")
            title=getTitle("gameOver")
            print(title)
            input("")
            os.system("cls")
            getLevel(level)

        #next level
        elif tile == "*":
            os.system("cls")
            title=getTitle("nextLevel")
            print(title)
            input("")    
            os.system("cls")
            level=int(level)
            level+=1
            getLevel(level)

        #find signs
        signPos=[0,0]
        for neighbor in neighbors:
            target=[player.x+neighbor[0],player.y+neighbor[1]]
            if map[target[1]][target[0]] == "T":
                signPos=[target[1],target[0]]

        #read sign
        if signPos!=[0,0]:
            textFile="levels\\text\\level"+str(level)+"-text-"+str(signPos[1])+"-"+str(signPos[0])+".txt"
            sign = open(textFile, "r")
            signText = sign.read()
        else:
            signText=""

        #move and reset player sprite
        move=[0,0]
        reset=map[player.y][player.x]
        map[player.y][player.x]="@"

        
        if times==True:
            start_draw_time=time.time()
        #loop through camera and draw map to display buffer
        cameraBuffer=[] #pm
        if len(map)-cam[1]-1 < cam[3]:
            height=len(map)
        else:
            height=cam[3]
        for iy in range(height):
            line=map[iy+cam[1]]
            lineBuffer=""
            if len(line)-cam[0]-1 < cam[2]:
                width=len(line)-cam[0]-1
            else:
                width=cam[2]
            for ix in range(width):
                tile=line[ix+cam[0]]
                #swap and colorise tiles
                if tile=="/":
                    lineBuffer+="  "
                elif tile==":" or tile=="R" or tile=="." or tile==">":
                        lineBuffer+=colors.gray+". "
                elif tile=="'":
                        lineBuffer+=colors.gray+", "
                elif tile=="#":
                    lineBuffer+=colors.yellow+"# "
                elif tile=="Y":
                        lineBuffer+=colors.yellow+"% "
                elif tile=="$":
                    lineBuffer+=colors.green+"S "
                elif tile=="%":
                    lineBuffer+=colors.green+"s "
                elif tile=="r":
                    lineBuffer+=colors.yellow+"R "
                elif tile=="g":
                    lineBuffer+=colors.green+". "
                elif tile=="G":
                    lineBuffer+=colors.green+", "
                elif tile=="t":
                    lineBuffer+=colors.white+"- "
                elif tile=="?":
                    lineBuffer+=colors.green+"? "
                elif tile=="W":
                    lineBuffer+=colors.yellow+". "
                elif tile=="H":
                    lineBuffer+=colors.yellow+"\ "
                elif tile=="h":
                    lineBuffer+=colors.yellow+"/ "
                elif tile=="k":
                    lineBuffer+=colors.yellow+"[]"
                elif tile=="l":
                    lineBuffer+=colors.yellow+"{}"
                elif tile=="|":
                     lineBuffer+=colors.yellow+"| "
                elif tile=="w":
                    if (looped+ix+player.x+iy+player.y)%3==0:
                        lineBuffer+=colors.blue+"~ "
                    elif (looped+ix+player.x+iy+player.y)%3==1:
                        lineBuffer+=colors.blue+"~~"
                    elif (looped+ix+player.x+iy+player.y)%3==2:
                        lineBuffer+=colors.blue+" ~"
                elif tile=="f":
                    if (looped+ix+player.x+iy+player.y)%2==0:
                        lineBuffer+=colors.yellow+"t "
                    elif (looped+ix+player.x+iy+player.y)%2==1:
                        lineBuffer+=colors.yellow+"f "
                elif tile==",":
                    lineBuffer+=colors.red+", "
                elif tile=="^":
                    lineBuffer+=colors.red+"^ "
                elif tile=="\"":
                    lineBuffer+=colors.red+"^ "
                elif tile=="*":
                    lineBuffer+=colors.purple+"* "
                elif tile=="-":
                    lineBuffer+=colors.yellow+"- "
                elif tile=="~":
                    lineBuffer+=colors.red+"~ "
                elif tile=="E":
                    lineBuffer+=colors.red+"E "
                elif tile=="=":
                    lineBuffer+=colors.gray+"= "
                elif tile==";":
                    lineBuffer+=colors.yellow+"; "
                elif tile=="b":
                    lineBuffer+=colors.blue+". "
                elif tile=="o":
                    lineBuffer+=colors.yellow+". "
                elif tile=="s":
                    lineBuffer+=colors.yellow+"s "
                elif tile=="(":
                    lineBuffer+=colors.red+"~ "
                else:
                    lineBuffer+=colors.white+tile+" "
                
            cameraBuffer.append(lineBuffer)

        #display camera, borders and signs
        screen=""
        screen+=colors.white+"  "+("_"*(cam[2]*2+1))+"\n"
        for line in cameraBuffer:
            screen+=f'{colors.white+" | "+line: <{cam[2]*2+13}}'+colors.white+"| \n"
        screen+=" |"+("_"*(cam[2]*2+1))+"|" 
        for output in out:
            print(output)
        out=[]
        print(screen)
        for line in signText.split("\n"):
            width=(cam[2]*2+5)
            print(f'{line: ^{width}}')
        if saved==True:
            print("Game Saved")
        map[player.y][player.x]=reset
        
        if times==True:
            end_draw_time=time.time()
            print("draw: "+str(end_draw_time-start_draw_time))
        if times==True:
            end_time=time.time()
            print("tick: "+str(end_time-start_time))
            print("tps: "+str(1/(end_time-start_time)))
            tps.append(1/(end_time-start_time))
            if len(tps)>5:
                tps.pop(0)
            avg=0
            for x in tps:
                avg+=x
            avg/=len(tps)
            print("avg tps: "+str(avg))
        #-t print(end_time - start_time)

    #read player inputs
    #if delay>= 10 and keyboard.is_pressed("space"):
    #    player.attacking=True
    if player.attacking==False:    
        if delay>= 10 and keyboard.is_pressed("w"):
            move[1]=-1
        if delay>= 10 and keyboard.is_pressed("s"):
            move[1]=1
        if delay>= 10 and keyboard.is_pressed("a"):
            move[0]=-1
        if delay>= 10 and keyboard.is_pressed("d"):
            move[0]=1
    if delay>= 10 and keyboard.is_pressed("esc"):
        exit()
        
    time.sleep(0.01)
    loops+=1
            

