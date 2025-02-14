from rcolors import colors
from mathLib import Vector
colorise=colors.colorise

class Tile():
    def __init__(self,x,y,tile):
        self.x=x
        self.y=y
        self.tile=tile

class Body():
    instantiationTiles=["%"]

    def __init__(self,x,y,tile="s",layer=0):
        self.x=x
        self.y=y
        self.damage=True
        self.layer=layer
        self.tile=tile
    
    def draw(self, **kwargs):
        return colorise(self.tile,"green")

class Snake():
    instantiationTiles=["$"]

    def getDirections(self,previousPart):
        forward=Vector(self.x-previousPart.x,self.y-previousPart.y)
        left=forward.transformLeft()
        right=forward.transformRight()
        return [forward,left,right]

    @classmethod
    def create(cls,x,y,level):
        body=[Body(x,y)]
        for part in body:
            for neighbor in Vector.neighbors():
                target=Vector(part.x+neighbor.x,part.y+neighbor.y)
                #skip existing parts
                if any(previousPart.x==target.x and previousPart.y==target.y for previousPart in body):
                    continue
                if level.getTile(target.x,target.y) in Body.instantiationTiles:
                    body.append(Body(target.x,target.y))
                    break
        body.pop(0)
        snake=Snake(x,y,body)
        level.createObject(snake)

    def __init__(self,x,y,body,tile="S",layer=0):
        self.x = x
        self.y = y
        self.tile=tile
        self.layer=layer
        self.damage=True
        self.body=body
    
    def tick(self,level, **kwargs):
        directions=self.getDirections(self.body[0])
        for dir in directions:
            target=Vector(self.x+dir.x,self.y+dir.y)
            if level.getTile(target.x,target.y) == ":":
                move=dir
                break

        self.body.pop(-1)
        self.body.insert(0,Body(self.x,self.y))
        self.x+=move.x
        self.y+=move.y

    def attack(self,enemy,level,camera):
        for part in self.body:
            if enemy.x==part.x and enemy.y==part.y and part.damage==True:
                enemy.hurt(level,camera)
                return True
        return False

    def draw(self, **kwargs):
        return colorise(self.tile,"green")