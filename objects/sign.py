from mathLib import Vector
from rcolors import colors
from camera import Sprite
colorise=colors.colorise

##change signs to only be text and dynamicly format themselves

#define end object
class Sign():
    instantiationTiles=["T"]
    directions=[Vector(0,-1),Vector(0,1),Vector(-1,0),Vector(1,0)]

    @classmethod
    def create(cls,x,y,level): 
        fileDirectory="levels\\text\\level"+str(level.level)+"-text-"+str(x)+"-"+str(y)+".txt"
        file=open(fileDirectory,"r")
        text=file.read().splitlines()
        sign=Sign(x,y,text)
        level.createObject(sign)

    def __init__(self,x,y,text,tile="T",layer=11):
        self.x = x
        self.y = y
        self.tile=tile
        self.layer=layer
        self.text=text
        self.solid=True

    def tick(self,level,player,signText, **kwargs):
        for x in self.directions:
            if player.x==self.x+x.x and player.y==self.y+x.y:
                signText.text=self.text

    def draw(self, **kwargs):
        sprite=self.tile
        return Sprite(self.x,self.y,self.layer,sprite)

    def collision(self, other, movement,level):
        if self.x==other.x+movement.x and self.y==other.y+movement.y:
            return True
    
class SignText():
    def __init__(self,text=""):
        self.text=text