from rcolors import colors
from mathLib import Vector
from objects.player import *
from objects.box import *
from objects.enemy import *
colorise=colors.colorise

class Wire():
    instantiationTiles=["b"]

    def __init__(self,x,y,tile=".",layer=0):
        self.x=x
        self.y=y
        self.layer=layer
        self.tile=tile
        self.state=False
    
    def draw(self, **kwargs):
        color={
            True:"yellow",
            False:"blue"
        }
        return colorise(self.tile,color[self.state])

class Door():
    instantiationTiles=["D"]

    def __init__(self,x,y,tile="D",layer=0):
        self.x=x
        self.y=y
        self.layer=layer
        self.tile=tile
        self.state=True
    
    def draw(self, **kwargs):
        color={
            True:"yellow",
            False:"gray"
        }
        tile={
            True:self.tile,
            False:"."
        }
        return colorise(tile[self.state],color[self.state])
    
    def collision(self, other, movement, level):
        if self.state==True and self.x==other.x+movement.x and self.y==other.y+movement.y:
            return True

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
                    break
        wires.pop(0)

        doors=[Door(wires[-1].x,wires[-1].y)]
        for door in doors:
            for neighbor in Vector.neighbors():
                target=Vector(door.x+neighbor.x,door.y+neighbor.y)
                #skip existing doors
                if any(previousDoor.x==target.x and previousDoor.y==target.y for previousDoor in doors):
                    continue
                if level.getTile(target.x,target.y) in Door.instantiationTiles:
                    doors.append(Door(target.x,target.y))
                    break
        doors.pop(0)

        switch=Switch(x,y,wires,doors)
        level.createObject(switch)

    def __init__(self,x,y,wires,doors,tile="s",layer=0, executionOrder=11):
        self.x = x
        self.y = y
        self.tile=tile
        self.layer=layer
        self.executionOrder=executionOrder
        self.wires=wires
        self.doors=doors
        self.state=False
        self.activated=False
    
    def tick(self,level,debug, **kwargs):
        if self.activated==False and any(object.x==self.x and object.y==self.y and (type(object)==Box or type(object)==Player or type(object)==Enemy) for object in level.objects):
            self.state=not self.state
            for wire in self.wires:
                wire.state=self.state
            for door in self.doors:
                door.state=not self.state
            self.activated=True
        else:
            self.activated=False
    
    def draw(self, **kwargs):
        color={
            True:"yellow",
            False:"white"
        }
        return colorise(self.tile,color[self.state])

    def collision(self,other,move,level):
        if any(door.collision(other,move,level) for door in self.doors):
            return True
        return False