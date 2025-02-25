from rcolors import colors
from mathLib import Vector
colorise=colors.colorise

class Box():
    instantiationTiles=["&"]

    @classmethod
    def create(cls,x,y,level):
        box=Box(x,y)
        level.createObject(box)

    def __init__(self,x,y,tile="&",layer=0):
        self.x = x
        self.y = y
        self.tile=tile
        self.layer=layer
    
    def tick(self,level, **kwargs):
        return True
    
    def draw(self, **kwargs):
        return self.tile

    def collision(self,other,move,level):
        if self.x==other.x+move.x and self.y==other.y+move.y:
            if level.getTile(self.x+move.x,self.y+move.y) in level.wallTiles:
                return True
            else:
                self.x+=move.x
                self.y+=move.y
                return False