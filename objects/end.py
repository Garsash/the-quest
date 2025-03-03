from mathLib import Vector
from rcolors import colors
from camera import Sprite
colorise=colors.colorise

#define end object
class End():
    instantiationTiles=["*"]

    @classmethod
    def create(cls,x,y,level): 
        end=End(x,y)
        level.createObject(end)

    def __init__(self,x,y,tile="*",layer=11):
        self.x = x
        self.y = y
        self.tile=tile
        self.layer=layer

    def tick(self,level,player,inputs,camera, **kwargs):
        if player.x==self.x and player.y==self.y:
            camera.drawTitle("nextLevel")
            input()
            level.create(level.level+1)
            camera.moveTo(level.player.x,level.player.y)
        return True

    def draw(self, **kwargs):
        sprite=colorise(self.tile,"purple")
        return Sprite(self.x,self.y,self.layer,sprite)