from rcolors import colors
from mathLib import Vector
from objects.wire import *
from camera import Sprite
colorise=colors.colorise

class Tile():
    def __init__(self,x,y,tile):
        self.x=x
        self.y=y
        self.tile=tile

class Flame():
    def __init__(self,x,y,state=1,dist=0,layer=0):
        self.x=x
        self.y=y
        self.state=state
        self.damage=state
        self.dist=dist
        self.layer=layer
        self.tile=[colorise(";","yellow"),colorise("~","red"),colorise("-","yellow")]

    def draw(self,frame):
        return Sprite(self.x,self.y,self.layer,self.tile[(((self.dist+frame)%2)+1)*self.state])

class Flamethrower():
    instantiationTiles=["="]

    @classmethod
    def create(cls,x,y,level,circuit=False,timer=7):
        for dir in [Vector(1,0),Vector(-1,0)]:
            if not level.getTile(x+dir.x,y+dir.y) in level.wallTiles:
                direction=dir.x
        for neighbor in Vector.neighbors():
            if circuit==False and level.getTile(x+neighbor.x,y+neighbor.y) in Wire.instantiationTiles:
                return False
        flamethrower=Flamethrower(x,y,direction,timer=timer)
        if circuit==True:
            return flamethrower
        level.createObject(flamethrower)

    def __init__(self,x,y,direction,state=False,timer=7,distance=3,tile="=",layer=0):
        self.x = x
        self.y = y
        self.state = state
        self.tile=tile
        self.layer=layer
        self.maxTime = timer
        self.time = 0
        self.damage=True
        self.solid=True
        self.distance=distance
        self.flames=[]
        self.direction=direction
    
    def tick(self,level,debug, **kwargs):
        if self.maxTime >0:
            #up
            if self.time == 0:
                for x in range(self.distance):
                    self.flames.append(Flame(self.x+((x+1)*self.direction),self.y,1,x))
                self.state = 1
                self.damage=True
            #down
            elif self.time == 4:
                self.flames=[]
                self.damage=False
                self.state = 0
            
            elif self.time==7:
                self.flames=[Flame(self.x+(1*self.direction),self.y,0,0)]
            self.time+=1
            #reset
            if self.time > self.maxTime:
                self.time = 0

    def activate(self,debug=0):
        debug.log(self.time)
        debug.log(self.distance)
        debug.log(self.direction)
        if self.time==0:
            self.flames=[Flame(self.x+(1*self.direction),self.y,0,0)]
        elif self.time>=1:
            for x in range(self.distance):
                self.flames.append(Flame(self.x+((x+1)*self.direction),self.y,1,x))
            self.state = 1
            self.damage=True
        self.time+=1

    def deactivate(self,debug=0):
        self.flames=[]
        self.damage=False
        self.state = 0
        self.time=0

    def attack(self, enemy,level,camera,frame,signText,debug):
        for fire in self.flames:
            if fire.damage==True and enemy.x==fire.x and enemy.y==fire.y:
                if hasattr(enemy, "hurt"): enemy.hurt(level,camera,frame,signText,debug)
                return True
        return False

    def draw(self, frame):
        flames=[]
        for flame in self.flames:
            flames.append(flame.draw(frame))
        sprite=colorise(self.tile,"gray")
        return [Sprite(self.x,self.y,self.layer,sprite)] + flames