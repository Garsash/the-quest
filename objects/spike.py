from rcolors import colors
colorise=colors.colorise

class Spike():
    instantiationTiles=["^",",","\""]

    #@staticmethod
    #def instantiationTiles():
    #    return ["^"]

    @classmethod
    def create(cls,x,y,level):
        tile=level.getTile(x,y)  
        if tile == '^' or tile == ',':
            spike=Spike(x,y,0,3)
            level.createObject(spike)
        if tile == '"':
            spike=Spike(x,y,0,7)
            level.createObject(spike)

    def __init__(self,x,y,state,timer,tile=",",layer=0):
        self.x = x
        self.y = y
        self.state = state
        self.tile=tile
        self.layer=layer
        self.maxTime = timer
        self.time = 0
        self.damage=True
    
    def tick(self,level, **kwargs):
        #up
        if self.time == 0:
            self.tile="^"
            self.state = 1
            self.damage=True
        #down
        elif self.time == 2:
            self.tile=","
            self.state = 0
            self.damage=False
        self.time+=1
        #reset
        if self.time > self.maxTime:
            self.time = 0
    
    def attack(self, enemy,level,camera,frame,signText,debug):
        if self.damage==True and self.x==enemy.x and self.y==enemy.y:
                    enemy.hurt(level,camera,frame,signText,debug)
                    return True
        return False

    def draw(self, **kwargs):
        return colorise(self.tile,"red")