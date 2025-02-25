import os
os.system("color")

red="\033[1;31;40m"
yellow="\033[1;33;40m"
green="\033[1;32;40m"
cyan="\033[1;36;40m"
blue="\033[1;34;40m"
purple="\033[1;35;40m"
white="\033[1;37;40m"
gray="\033[1;30;40m"

colorValues={
        "red":red,
        "yellow":yellow,
        "green":green,
        "cyan":cyan,
        "blue":blue,
        "purple":purple,
        "white":white,
        "gray":gray
    }

colorArray=[red,yellow,green,cyan,blue,purple,white,gray]

colorNames=["red","yellow","green","cyan","blue","purple","white","gray"]

def isIn(string, array):
    for x in array:
        if string==x:
            return True
    return False

class colors:
    global colorValues,red,yellow,green,cyan,blue,purple,white,gray,colorArray,colorNames

    #def color(color):
    #    if isinstance(color, int)==False:
    #        raise Exeption("Not an integer")
    #    return "\033[9"+str(color)+"m"

    def color(color):
        if isinstance(color,str):
            color=color.lower()
            if isIn(color,colorNames):
                    return colorValues[color]
            else:
                raise ValueError(color, "color does not exist")
        else:
            if color>0 and color<len(colorArray):
                    return colorArray[color]
            else:
                raise ValueError(color, "color outside length of colors array")

    def colorise(string:str,color,reset:bool=True):
        out=colors.color(color)+string
        if reset==True: out+=white
        return out

    def allColors():
        return colorValues


