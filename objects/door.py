from rcolors import colors
from mathLib import Vector
from camera import Sprite
colorise=colors.colorise

class Door():
    instantiationTiles=["D"]

    def __init__(self,x,y,tile=["d","D"],color=["gray","yellow"],layer=0):
        self.x=x
        self.y=y
        self.layer=layer
        self.tile=tile
        self.color=color
        self.state=True
    
    def draw(self, **kwargs):
        sprite=colorise(self.tile[self.state],self.color[self.state])
        return Sprite(self.x,self.y,self.layer,sprite)
    
    def collision(self, other, movement, level):
        if self.state==True and self.x==other.x+movement.x and self.y==other.y+movement.y:
            return True
    
    def activate(self, **kwargs):
        self.state=False
    
    def deactivate(self, **kwargs):
        self.state=True