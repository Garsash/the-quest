##from rcolors import colors
##from mathLib import Vector
##from objects.player import *
##from objects.box import *
##from objects.enemy import *
##from objects.door import *
##from objects.wire import *
##from camera import Sprite
##colorise=colors.colorise
##
##class Switch():
##    instantiationTiles=["S"]
##
##    @classmethod
##    def create(cls,x,y,level):
##        wires=[Wire(x,y)]
##        for wire in wires:
##            for neighbor in Vector.neighbors():
##                target=Vector(wire.x+neighbor.x,wire.y+neighbor.y)
##                #skip existing wires
##                if any(previousWire.x==target.x and previousWire.y==target.y for previousWire in wires):
##                    continue
##                if level.getTile(target.x,target.y) in Wire.instantiationTiles:
##                    wires.append(Wire(target.x,target.y))
##                    break
##        wires.pop(0)
##
##        doors=[Door(wires[-1].x,wires[-1].y)]
##        for door in doors:
##            for neighbor in Vector.neighbors():
##                target=Vector(door.x+neighbor.x,door.y+neighbor.y)
##                #skip existing doors
##                if any(previousDoor.x==target.x and previousDoor.y==target.y for previousDoor in doors):
##                    continue
##                if level.getTile(target.x,target.y) in Door.instantiationTiles:
##                    doors.append(Door(target.x,target.y))
##                    break
##        doors.pop(0)
##
##        switch=Switch(x,y,wires,doors)
##        level.createObject(switch)
##
##    def __init__(self,x,y,wires,doors,tile="s",layer=0, executionOrder=11):
##        self.x = x
##        self.y = y
##        self.tile=tile
##        self.layer=layer
##        self.executionOrder=executionOrder
##        self.wires=wires
##        self.doors=doors
##        self.state=False
##        self.activated=False
##    
##    def tick(self,level,debug, **kwargs):
##        if self.activated==False and any(object.x==self.x and object.y==self.y and (type(object)==Box or type(object)==Player or type(object)==Enemy) for object in level.objects):
##            self.state=not self.state
##            for wire in self.wires:
##                wire.state=self.state
##            for door in self.doors:
##                door.state=not self.state
##            self.activated=True
##        else:
##            self.activated=False
##    
##    def draw(self, **kwargs):
##        color={
##            True:"yellow",
##            False:"white"
##        }
##        sprite=colorise(self.tile,color[self.state])
##        return Sprite(self.x,self.y,self.layer,sprite)
##
##    def collision(self,other,move,level):
##        if any(door.collision(other,move,level) for door in self.doors):
##            return True
##        return False

from rcolors import colors
from mathLib import Vector
from objects.player import *
from objects.box import *
from objects.enemy import *
from objects.door import *
from objects.wire import *
from objects.spike import *
from objects.flamethrower import *
from camera import Sprite
colorise=colors.colorise

class Switch():
    instantiationTiles=["S"]

    @classmethod
    def create(cls,x,y,level):
        wires=[Wire(x,y)]
        for wire in wires:
            for neighbor in Vector.neighbors():
                target=Vector(wire.x+neighbor.x,wire.y+neighbor.y)
                #skip existing wires
                if any(previousWire.x==target.x and previousWire.y==target.y for previousWire in wires):
                    continue
                if level.getTile(target.x,target.y) in Wire.instantiationTiles:
                    wires.append(Wire(target.x,target.y))
        wires.pop(0)

        pos=0
        objects=wires.copy()
        while pos<len(objects):
            object=objects[pos]
            for neighbor in Vector.neighbors():
                target=Vector(object.x+neighbor.x,object.y+neighbor.y)
                if any(previousObject.x==target.x and previousObject.y==target.y for previousObject in objects):
                    continue
                if level.getTile(target.x,target.y) in Door.instantiationTiles:
                    objects.append(Door(target.x,target.y))
                elif level.getTile(target.x,target.y) in Flamethrower.instantiationTiles:
                    objects.append(Flamethrower.create(target.x,target.y,level,circuit=True,timer=0))
                elif level.getTile(target.x,target.y) in Spike.instantiationTiles:
                    objects.append(Spike.create(target.x,target.y,level,circuit=True,timer=0))
            if type(object)==Wire:
                objects.pop(pos)
            else:
                pos+=1
                
        ##doors=[Door(wires[-1].x,wires[-1].y)]
        ##for door in doors:
        ##    for neighbor in Vector.neighbors():
        ##        target=Vector(door.x+neighbor.x,door.y+neighbor.y)
        ##        #skip existing doors
        ##        if any(previousDoor.x==target.x and previousDoor.y==target.y for previousDoor in doors):
        ##            continue
        ##        if level.getTile(target.x,target.y) in Door.instantiationTiles:
        ##            doors.append(Door(target.x,target.y))
        ##            break
        ##doors.pop(0)

        switch=Switch(x,y,wires,objects)
        level.createObject(switch)

    def __init__(self,x,y,wires,objects,tile="s",layer=0, executionOrder=11):
        self.x = x
        self.y = y
        self.tile=tile
        self.layer=layer
        self.executionOrder=executionOrder
        self.wires=wires
        self.objects=objects
        self.state=False
        self.activated=False
    
    def tick(self,level,debug, **kwargs):
##        if any(object.x==self.x and object.y==self.y and (type(object)==Box or type(object)==Player or type(object)==Enemy) for object in level.objects):
##            self.state=True
##            for wire in self.wires:
##                wire.state=True
##            for object in self.objects:
##                object.activate(debug=debug)
##                debug.log("active: "+str(object))
##        else:
##            self.state=False
##            for wire in self.wires:
##                wire.state=False
##            for object in self.objects:
##                object.deactivate(debug=debug)
##                debug.log("inactive: "+str(object))
##        debug.log(self.objects)

        if self.activated==False and any(object.x==self.x and object.y==self.y and (type(object)==Box or type(object)==Player or type(object)==Enemy) for object in level.objects):
            self.state=not self.state
            for wire in self.wires:
                wire.state=self.state
            self.activated=True
        else:
            self.activated=False

        if self.state==True:
            for object in self.objects:
                object.activate(debug=debug)
        else:
            for object in self.objects:
                object.deactivate(debug=debug)
        
    
    def draw(self, **kwargs):
        objects=[]
        for object in self.objects:
            objects.append(object.draw())

        wires=[]
        for wire in self.wires:
            wires.append(wire.draw())

        sprite=self.tile
        all=[Sprite(self.x,self.y,self.layer,sprite)]+objects+wires

        sprites=[]
        for sprite in all:
            if type(sprite)==list:
                for sub in sprite:
                    sprites.append(sub.draw())
            elif type(sprite)==Sprite:
                sprites.append(sprite)
            else:
                sprites.append(sprite.draw())
        
        return sprites

    def collision(self,other,move,level):
        if any(hasattr(objects,"collision") and objects.collision(other,move,level) for objects in self.objects):
            return True
        return False