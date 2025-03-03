from rcolors import colors
from mathLib import Vector
from objects.wire import *
from camera import Sprite
colorise=colors.colorise

class Spike():
    instantiationTiles=["^",",","\""]

    #@staticmethod
    #def instantiationTiles():
    #    return ["^"]

    @classmethod
    def create(cls,x,y,level,circuit=False,timer=0):
        for neighbor in Vector.neighbors():
            if circuit==False and level.getTile(x+neighbor.x,y+neighbor.y) in Wire.instantiationTiles:
                return False
        tile=level.getTile(x,y)  
        if circuit==True:
            return Spike(x,y,0,0)
        if tile == '"':
            spike=Spike(x,y,0,7)
            level.createObject(spike)
        else:
            spike=Spike(x,y,0,3)
            level.createObject(spike)

    def __init__(self,x,y,state,timer,tile=[",","^"],layer=0):
        self.x = x
        self.y = y
        self.state = state
        self.tile=tile
        self.layer=layer
        self.maxTime = timer
        self.time = 0
        self.damage=True
    
    def tick(self,level,debug, **kwargs):
        if self.maxTime>0:
            #up
            if self.time == 0:
                self.activate()
            #down
            elif self.time == 2:
                self.deactivate()
            self.time+=1
            #reset
            if self.time > self.maxTime:
                self.time = 0
    
    def activate(self, **kwargs):
        self.state = 1
        self.damage=True
    
    def deactivate(self, **kwargs):
        self.state = 0
        self.damage=False
    
    def attack(self, enemy,level,camera,frame,signText,debug):
        if self.damage==True and self.x==enemy.x and self.y==enemy.y:
                    enemy.hurt(level,camera,frame,signText,debug)
                    return True
        return False

    def draw(self, **kwargs):
        sprite=colorise(self.tile[self.state],"red")
        return Sprite(self.x,self.y,self.layer,sprite)