from rcolors import colors
from mathLib import Vector
from camera import Sprite
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
        sprite=colorise(self.tile,color[self.state])
        return Sprite(self.x,self.y,self.layer,sprite)
