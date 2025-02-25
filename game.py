from levelHandler import Level
from camera import Camera
from debug import Debug
from objects.player import Player
from objects.sign import SignText
import time
import os

camera=Camera(0,0)

camera.drawTitle("title")

cheat=input("")
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

level=Level(level)
debug=Debug()

firstTick=True
frame=0

while True:
    #keyboard yes?
    recievedInput=False
    inputs=Player.getInputs()
    for x in inputs:
        if inputs[x]==True:
            recievedInput=True
            break

    #if yes then do
    if recievedInput==True or firstTick==True:
        time.sleep(0.05)
        #get new possible inputs
        allInputs=Player.getInputs()
        for x in inputs:
            if allInputs[x]==True and inputs[x]==False:
                inputs[x]=True
        firstTick=False
        frame+=1

        #sort objects by update order
        update={}
        for obj in level.objects:
            if hasattr(obj,"executionOrder"):
                if not obj.executionOrder in update.keys():
                    update[obj.executionOrder]=[]
                update[obj.executionOrder].append(obj)
            else:
                if not obj.layer in update.keys():
                    update[obj.layer]=[]
                update[obj.layer].append(obj)
        
        signText=SignText("")
        #update objects
        updates = dict(sorted(update.items()))
        index=0
        for x in updates:
            for obj in updates[x]:
                index+=1
                obj.tick(level,inputs=inputs,camera=camera,player=level.player,frame=frame,index=index,signText=signText,debug=debug)

        ###loop through all objects
        ##for obj in level.objects:
        ##    #tick each object
        ##    obj.tick(level,inputs=inputs,camera=camera)

        if inputs["skip"]==True:
            level.create(level.level+1)
            camera.moveTo(level.player.x,level.player.y)
        if inputs["exit"]==True:
            quit()
            
        camera.draw(level,frame,signText,debug)
        time.sleep(0.2)

input()
