from rcolors import colors
from mathLib import Vector
from camera import Sprite
colorise=colors.colorise

class Default():
    instantiationTiles=[]

    @classmethod
    def create(cls,x,y,level):
        default=Default(x,y)
        level.createObject(default)

    def __init__(self,x,y,tile="",layer=0):
        self.x = x
        self.y = y
        self.tile=tile
        self.layer=layer
    
    def tick(self,level, **kwargs):
        return True
    
    def draw(self, **kwargs):
        sprite=self.tile
        return Sprite(self.x,self.y,self.layer,sprite)