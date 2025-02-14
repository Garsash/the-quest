import keyboard
from mathLib import Vector

#define player object
class Player():
    instantiationTiles=["@"]

    @classmethod
    def create(cls,x,y,level): 
        player=Player(x,y)
        level.createObject(player)

    def __init__(self,x,y,tile="@",layer=10):
        self.x = x
        self.y = y
        self.tile=tile
        self.layer=layer
        self.solid=False

    @classmethod
    def getInputs(cls):
        inputs={"up":0,"down":0,"left":0,"right":0}
        inputs["up"]=keyboard.is_pressed("w")
        inputs["left"]=keyboard.is_pressed("a")
        inputs["down"]=keyboard.is_pressed("s")
        inputs["right"]=keyboard.is_pressed("d")
        return inputs

    def hurt(self,level,camera):
        camera.drawTitle("gameOver")
        input("")
        level.create(level.level)
        camera.moveTo(level.player.x,level.player.y)
    
    def tick(self,level,inputs,camera, **kwargs):
        move=Vector(0,0)
        move.y=inputs["down"]-inputs["up"]
        move.x=inputs["right"]-inputs["left"]
        #if inputs["up"]:
        #    move.y-=1
        #if inputs["down"]:
        #    move.y+=1
        #if inputs["left"]:
        #    move.x-=1
        #if inputs["right"]:
        #    move.x+=1

        if level.getTile(self.x+move.x,self.y+move.y) in level.wallTiles or (any(hasattr(x, "solid") and x.solid==True and x.x==self.x+move.x and x.y==self.y+move.y  for x in level.objects)):
            move.x=0
            move.y=0
        else:
            if level.getTile(self.x+move.x,self.y) in level.wallTiles or (any(hasattr(x, "solid") and x.solid==True and x.x==self.x+move.x and x.y==self.y for x in level.objects)):
                move.x=0
            elif level.getTile(self.x,self.y+move.y) in level.wallTiles or (any(hasattr(x, "solid") and x.solid==True and x.x==self.x and x.y==self.y+move.y for x in level.objects)):
                move.y=0

        self.x+=move.x
        self.y+=move.y

        self.tile="@"
        for obj in level.objects:
            if hasattr(obj,"attack"):
                obj.attack(self,level,camera)
                
        
        camera.x=self.x-int(camera.width/2)
        camera.y=self.y-int(camera.height/2)

    def draw(self, **kwargs):
        return self.tile

#    def moveBox(self):
#        #loop through boxes
#        for box in boxes:
#            #find correct box
#            if box.x == player.x+move[0] and box.y == player.y+move[1]:
#                box.move(move[0],move[1])