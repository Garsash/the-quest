from mathLib import Vector
from mathLib import Random
from rcolors import colors
import os

def randomTiles(tiles):
    out=[]
    for tile in tiles:
        if len(tile)==1:
            tile.append(1)
        out+=[tile[0] for x in range(tile[1])]
    out+=[1] 
    print(out)   
    return out

colorise=colors.colorise
#tiles to display differently
replaceTiles={
    "/":" ",
    "#":[[colorise("#","yellow"),0.9],[colorise("%","yellow"),0.1]],
    ".":colorise(".","gray"),
    ":":colorise(".","gray"),
    "R":colorise(".","gray"),
    ">":colorise(".","gray"),
    "'":colorise(",","gray"),
    "Y":colorise("%","yellow"),
    "$":colorise("S","green"),
    "%":colorise("s","green"),
    "r":colorise("R","yellow"),
    "g":colorise(".","green"),
    "G":colorise(",","green"),
    "t":colorise("-","white"),
    "?":colorise("?","green"),
    "W":colorise(".","yellow"),
    "H":colorise("\\","yellow"),
    "h":colorise("/","yellow"),
    "k":colorise("[]","yellow"),
    "l":colorise("{}","yellow"),
    "|":colorise("|","yellow"),
    "w":[colorise("~ ","blue"),colorise("~~","blue"),colorise(" ~","blue")],
    "f":[colorise("t","yellow"),colorise("f","yellow")],
    ",":colorise(",","red"),
    "^":colorise("^","red"),
    "\"":colorise("^","red"),
    "*":colorise("*","purple"),
    "-":colorise("-","yellow"),
    "~":colorise("~","red"),
    "E":colorise("E","red"),
    "=":colorise("=","gray"),
    ";":colorise(";","yellow"),
    "b":colorise(".","blue"),
    "o":colorise(".","yellow"),
    "s":colorise("s","yellow"),
    "(":colorise("~","red")
    }

replaceTitles={
    "y":colors.color("yellow"),
    "%":colors.color("red"),
    "w":colors.color("white")
}

#camera obj
class Camera():
    global replaceTiles
    global replaceTitles

    def __init__(self,x,y,width=15,height=15):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        os.system("mode "+ str(self.width*2+5)+", "+str(self.height+9))
    
    def moveTo(self,val1,val2=None):
        if type(val1)==Vector:
            self.x=val1.x-int(self.width/2)
            self.y=val1.y-int(self.height/2)
        else:
            self.x=val1-int(self.width/2)
            self.y=val2-int(self.height/2)

    def drawTitle(self,title):
        os.system("cls")
        titleDisplay=open("titles/"+title+".txt")
        for line in titleDisplay.readlines():
            text=""
            for char in line[:-1]:
                if char in replaceTitles.keys():
                    text+=replaceTitles[char]
                else:
                    text+=char
            print(text)

    def subDraw(self,obj,attribute,layers):
        if hasattr(obj,attribute):
            for subItem in getattr(obj,attribute):
                if subItem.x>=self.x and subItem.x<self.x+self.width and subItem.y>=self.y and subItem.y<self.y+self.height:
                    if not subItem.layer in layers.keys():
                        layers[subItem.layer]=[]
                    layers[subItem.layer].append(subItem)

    def draw(self,level,frame,signText,debug,shader={"tiles":{},"background":" "}):
        #clear screen
        os.system("cls")
        debug.print()
        readPos=Vector(self.x,self.y)

        #create empty array to draw on
        display=[]
        for y in range(self.height):
            line=[]
            for x in range(self.width):
                line.append(shader["background"])
            display.append(line)

        #read map to display
        for y in range(self.height):
            readPos.y=self.y+y
            if readPos.y<0:
                continue
            if readPos.y >= len(level.tiles):
                break
            line=[]
            for x in range(self.width):
                readPos.x=self.x+x
                if readPos.x<0:
                    continue
                if readPos.x >= len(level.tiles[readPos.y]):
                    break
                tile=level.getTile(readPos.x,readPos.y)
                display[y][x]=tile

        frameReplaceTiles=replaceTiles.copy()
        frameReplaceTiles.update(shader["tiles"])

        #draw correct tiles to display
        for y in range(len(display)):
            for x in range(len(display[y])):
                #tile in display to be replaced
                tileToReplace=display[y][x]
                #loop all tiles that it could be replaced with
                for tileCheck in frameReplaceTiles:
                    #if tile in display matches replacement
                    if tileToReplace==tileCheck:
                        replacement=frameReplaceTiles[tileCheck]
                        #determine if tile is static animated or random
                        if type(replacement)==list:
                            replacementCheck=replacement
                            replacement=replacement[0]
                            #if random
                            if type(replacement)==list:
                                #get tile seed
                                rnd=Random.setRandom(((y+self.y+1)*(x+self.x+1))%255)
                                limit=255
                                for tiles in replacementCheck:
                                    chance=tiles[1]*255
                                    if rnd<=chance+limit:
                                        display[y][x]=tiles[0]
                                    limit-=chance
                            else:
                                #animate in world space
                                display[y][x]=replacementCheck[(frame+self.x+self.y+x+y)%(len(replacementCheck))]
                        #else replace
                        else:
                            display[y][x]=replacement

        #sort objects by layer
        layers={}
        for obj in level.objects:
            if obj.x>=self.x and obj.x<self.x+self.width and obj.y>=self.y and obj.y<self.y+self.height:
                if not obj.layer in layers.keys():
                    layers[obj.layer]=[]
                layers[obj.layer].append(obj)

            #upgrade this
            self.subDraw(obj,"flames",layers)
            self.subDraw(obj,"body",layers)
            self.subDraw(obj,"wires",layers)
            self.subDraw(obj,"doors",layers)
        
        #draw objects to display
        layers = dict(sorted(layers.items()))
        for x in layers:
            for obj in layers[x]:
                image=obj.draw(frame=frame)
                if type(image) == str:
                    display[obj.y-self.y][obj.x-self.x]=image
                #better draw method but needs some work to be up to date
                #if type(image) == list:
                #    for tile in image:
                #        display[tile.y-self.y][tile.x-self.x]=tile.tile

        #draw display to screen
        print(colors.color("white")+"  "+("_"*(self.width*2+1)))
        for lines in display:
            line=""
            for char in lines:
                length=len(char)-len(colors.color("red"))*2
                #print(length)
                line+=char
                if length<=1:
                    line+=" "
            content=f'{line: <{self.width*2}}'
            if any(key=="colorise" for key in shader.keys()):
                for color in colors.allColors():
                    content=colorise(content.replace(colors.allColors()[color],colors.color(shader["colorise"])),"red")
            print(" |"+content+" |")
        print(" |"+("_"*(self.width*2+1))+"|" )
        for line in signText.text:
            print(f'{line: ^{self.width*2+5}}')
