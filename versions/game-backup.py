from textwrap import wrap
import os
import time
#import click
import keyboard
from rcolors import colors
#file=input("Enter Name of Map File: ")
#if file == "":
#	file = "map.txt"
#if file[4:] != ".txt":
#	file+=".txt"
#os.system("cls")

cam=[0,0,15,15]
os.system("mode "+ str(cam[2]*2+5)+", "+str(cam[3]+9))

def getTitle(name):
    title="titles\\"+name+".txt"
    t = open(title, "r")
    tl = t.readlines()
    title=""
    for l in tl:
        line=""
        for c in l:
            if c == "y":
                line+="\033[1;33;40m"
            elif c == "w":
                line+="\033[1;37;40m"
            elif c == "%":
                line+="\033[1;31;40m"
            elif c == "p":
                line+="\033[1;35;40m"
            else:
                line+=c
        title+=line
    return title



title="titles\\title.txt"
t = open(title, "r")
tl = t.readlines()
title=getTitle("title")
print(title)

cheat=input("")
os.system("cls")

level=1

first=True

spikes=[]
flames=[]
snakes=[]
enemies=[]

pos=[0,0]

map=[]

def getLevel(Level):
        #if Level=="save":
        #    file="save.txt"
        #else:
        file="levels\level"+str(Level)+".txt"
        global first, spikes, flames, snakes, enemies, pos, cam, map
        spikes=[]
        flames=[]
        snakes=[]
        enemies=[]
        pos=[0,0]
        cam=[0,0,15,15]
        map=[]
        fill=""
        for x in range(cam[2]):
            fill+="/"
        maxmap=0
		
        f = open(file, "r")
        l = f.readlines()
        i=0
        map=[]
        for x in l:
            i+=1
            if i!=len(l):
                x=x[:-1]
            #print(x)
            x=wrap(x+fill,1)
            map.append(x)
            if maxmap <= len(x):
                maxmap=len(x)
        fill2=[]
        for x in range(maxmap):
            fill2.append("/")
        for x in range(cam[3]):
            map.append(fill2)
        #print(map)
        for y in range(len(map)):
            for x in range(len(map[y])):
                if map[y][x] == '^' or map[y][x] == ',':
                    spikes.append([x,y])
                elif map[y][x] == '=':
                    flames.append([x,y])
                elif map[y][x] == '$':
                    snakes.append([x,y])
                elif map[y][x] == 'E':
                    enemies.append([x,y])
                #if map[y][x] == '/':
                    #map[y][x]=" "
                elif map[y][x] == '@':
                    if map[y+1][x] == "#":
                        map[y][x]="_"
                    else:
                        map[y][x]="."
                    pos=[x,y]
                elif map[y][x] == '-' or map[y][x] == '~' or map[y][x] == ';':
                    if map[y+1][x] == "#":
                        map[y][x]="_"
                    else:
                        map[y][x]="."
        cam[0]=pos[0]-int(cam[2]/2)
        cam[1]=pos[1]-int(cam[3]/2) 
        save=[]
        map[pos[1]][pos[0]]="@"
        for ys in range(len(map)-cam[3]):
            line=""
            for xs in range(len(map[ys])-cam[2]):
                line+=map[ys][xs]+" "
                save.append(line)
            s=open("save.txt", "w")
            for x in save:
                #print(x)
                s.write(x+"\n")
        s.close()
getLevel(level)

			
#print(map)
#print(len(map))
loops=0
dir=1
      
move=[0,0]
delay=0
looped=0
savePoint=[0,0]
out=[]

while True:
    delay+=1
    if delay>= 10 and move[0]!=0 or delay>= 10 and move[1]!=0 or first==True:
        out=[]
        saved=False
        first=False
        looped+=1
        os.system("cls")
        for s in spikes:
            if looped%4 == 0:
                map[s[1]][s[0]]="^"
            elif looped%4 == 2:
                map[s[1]][s[0]]=","

        for f in flames:
            for d in range(3):
                if looped%8 >= 0 and looped%8 <= 3:
                    if (d+(looped%2))%2==0:
                        if map[f[1]][f[0]+1]=="#":
                            map[f[1]][f[0]-d-1]="~"
                        if map[f[1]][f[0]-1]=="#":
                            map[f[1]][f[0]+d+1]="~"
                            
                    else:
                        if map[f[1]][f[0]+1]=="#":
                            map[f[1]][f[0]-d-1]="-"
                        if map[f[1]][f[0]-1]=="#":
                            map[f[1]][f[0]+d+1]="-"
                elif looped%8==4:
                    if map[f[1]][f[0]+1]=="#":
                        map[f[1]][f[0]-d-1]="."
                    if map[f[1]][f[0]-1]=="#":
                        map[f[1]][f[0]+d+1]="."
                elif looped%8==7:
                    if map[f[1]][f[0]+1]=="#":
                        map[f[1]][f[0]-1]=";"
                    if map[f[1]][f[0]-1]=="#":
                        map[f[1]][f[0]+1]=";"
        
        for n in range(len(snakes)):
            sPastPos=[]
            if map[snakes[n][1]+1][snakes[n][0]]==":":
                map[snakes[n][1]+1][snakes[n][0]]="$"
                map[snakes[n][1]][snakes[n][0]]="%"
                snakes[n]=[snakes[n][0],snakes[n][1]+1]
            elif map[snakes[n][1]][snakes[n][0]+1]==":":
                map[snakes[n][1]][snakes[n][0]+1]="$"
                map[snakes[n][1]][snakes[n][0]]="%"
                snakes[n]=[snakes[n][0]+1,snakes[n][1]]
            elif map[snakes[n][1]-1][snakes[n][0]]==":":
                map[snakes[n][1]-1][snakes[n][0]]="$"
                map[snakes[n][1]][snakes[n][0]]="%"
                snakes[n]=[snakes[n][0],snakes[n][1]-1]
            elif map[snakes[n][1]][snakes[n][0]-1]==":":
                map[snakes[n][1]][snakes[n][0]-1]="$"
                map[snakes[n][1]][snakes[n][0]]="%"
                snakes[n]=[snakes[n][0]-1,snakes[n][1]]
            sEndPos=[snakes[n][0],snakes[n][1]]  
            found=False
            while found==False:
                sPastPos.append(sEndPos)
                #print(sPastPos)
                if not [sEndPos[0],sEndPos[1]+1] in sPastPos and map[sEndPos[1]+1][sEndPos[0]]=="%":
                    sEndPos=[sEndPos[0],sEndPos[1]+1]
                    #print("1")
                elif not [sEndPos[0]+1,sEndPos[1]] in sPastPos and map[sEndPos[1]][sEndPos[0]+1]=="%":
                    sEndPos=[sEndPos[0]+1,sEndPos[1]]
                    #print("2")
                elif not [sEndPos[0],sEndPos[1]-1] in sPastPos and map[sEndPos[1]-1][sEndPos[0]]=="%":
                    sEndPos=[sEndPos[0],sEndPos[1]-1]
                    #print("3")
                elif not [sEndPos[0]-1,sEndPos[1]] in sPastPos and map[sEndPos[1]][sEndPos[0]-1]=="%":
                    sEndPos=[sEndPos[0]-1,sEndPos[1]]
                    #print("4")
                else:
                    #print(sEndPos)
                    #print(map[sEndPos[1]][sEndPos[0]])
                    map[sEndPos[1]][sEndPos[0]]=":"
                    found=True
                    
            first=False
            
        for e in range(len(enemies)):
            enemy=enemies[e]
            distx=pos[0]-enemy[0]
            disty=pos[1]-enemy[1]
            target=[0,0]

            if abs(distx) <= 6 and abs(disty) <= 6:
                scentMap=[]
                neighbors=[[-1,0],[0,-1],[1,0],[0,1]]
                for y in range(13):
                    row=[]
                    for x in range(13):
                        row.append(26)
                    scentMap.append(row)
                    
                searching=[]
                for y in range(13):
                    row=[]
                    for x in range(13):
                        row.append(False)
                    searching.append(row)

                searching[6][6]=True

                scentMap[6][6]=0
                nodes=[[6,6]]

                for n in nodes:
                    for x in neighbors:
                        nx=n[0]+x[0]
                        ny=n[1]+x[1]
                        hx=n[0]
                        hy=n[1]
                        worldy=pos[1]+ny-6
                        worldx=pos[0]+nx-6
                        if ny < 0 or ny >= 13:
                            continue
                        if nx < 0 or nx >= 13:
                            continue
                        here=scentMap[hy][hx]
                        if searching[ny][nx] == False:
                            state=map[worldy][worldx]
                            if state=="#":
                                continue
                            if scentMap[ny][nx] >= here:
                                scentMap[ny][nx]=here+1
                                nodes.append([nx,ny])
                            searching[ny][nx]=True
                            if state=="E":
                                nodes=[]
                                lowest=26
                                target=[0,0]
                                for y in neighbors:
                                    ex=nx+y[0]
                                    ey=ny+y[1]
                                    #out.append(str(ex)+" "+str(ey))
                                    if ey < 0 or ey >= 13:
                                        continue
                                    if ex < 0 or ex >= 13:
                                        continue
                                    if scentMap[ey][ex] <= lowest:
                                        lowest=scentMap[ey][ex]
                                        target=[y[0],y[1]]
                                break
                #for p in scentMap:
                    #out.append(p)
                #for p in searching:
                    #out.append(p)
                #out.append(target)
            if map[enemy[1]+1][enemy[0]] == "#":
                map[enemy[1]][enemy[0]]="_"
            else:
                map[enemy[1]][enemy[0]]="."
            enemy[0]+=target[0]
            enemy[1]+=target[1]
            map[enemy[1]][enemy[0]]="E"
            enemies[e]=enemy
            
                
        delay=0
        if map[pos[1]][pos[0]] == '@':
            if map[pos[1] + 1][pos[0]] == "#":
                map[pos[1]][pos[0]] = "_"
            else:
                map[pos[1]][pos[0]] = "."
        #if dir==1 and pos[1]>=len(map)-1:
        #  dir=-1
        #elif dir==-1 and pos[1]==0:
        #  dir=1
        #pos[1]+=dir
        tileH = map[pos[1]][pos[0]+move[0]]
        if not tileH == "#" and not tileH == "=" and not tileH == "T" and not tileH == "/":
            pos[0] += move[0]
        tileV = map[pos[1]+move[1]][pos[0]]
        if not tileV == "#" and not tileV == "=" and not tileV == "T" and not tileV == "/":
            pos[1] += move[1]
        cam[0]=pos[0]-int(cam[2]/2)
        cam[1]=pos[1]-int(cam[3]/2)
        tile = map[pos[1]][pos[0]]
        if tile == "^" or tile == "~" or tile == "-" or tile == "$" or tile == "%":
            os.system("cls")
            title=getTitle("gameOver")
            print(title)
            input("")
            os.system("cls")
            getLevel(level)
        elif tile == "*":
            os.system("cls")
            title=getTitle("nextLevel")
            print(title)
            input("")    
            os.system("cls")
            level+=1
            getLevel(level)
            #if tile == "R":
            #    if pos[0] == savePos[0] and abs(pos[1]-savePos[1]) < 5:
            #        false=False
            #    elif pos[1] == savePos[1] and abs(pos[0]-savePos[0]) < 5:
            #        false=False
            #    else:
            #        savePos=pos
            #        save=[]
            #        saved=True
            #        map[pos[1]][pos[0]]="@"
            #        for ys in range(len(map)-cam[3]):
            #            line=""
            #            for xs in range(len(map[ys])-cam[2]):
            #                line+=map[ys][xs]+" "
            #            save.append(line)
            #        s=open("save.txt", "w")
            #        for x in save:
            #            #print(x)
            #            s.write(x+"\n")
            #            s.close()
            #            #os.system("start "+"map2.txt")
        signPos=[0,0]
        if map[pos[1]+1][pos[0]] == "T":
            signPos=[pos[1]+1,pos[0]]
        elif map[pos[1]][pos[0]+1] == "T":
            signPos=[pos[1],pos[0]+1]
        elif map[pos[1]-1][pos[0]] == "T":
            signPos=[pos[1]-1,pos[0]]
        elif map[pos[1]][pos[0]-1] == "T":
            signPos=[pos[1],pos[0]-1]
        elif map[pos[1]][pos[0]] == "T":
            signPos=[pos[1],pos[0]]
        if signPos!=[0,0]:
            textFile="levels\\text\\level"+str(level)+"-text-"+str(signPos[1])+"-"+str(signPos[0])+".txt"
            sign = open(textFile, "r")
            signText = sign.read()
        else:
            signText=""
        move=[0,0]
        reset=map[pos[1]][pos[0]]
        map[pos[1]][pos[0]]="@"
        pm=[]
        if len(map)-cam[1]-1 < cam[3]:
            height=len(map)
        else:
            height=cam[3]
        for iy in range(height):
            y=map[iy+cam[1]]
            py=""
            if len(y)-cam[0]-1 < cam[2]:
                width=len(y)-cam[0]-1
            else:
                width=cam[2]
            for ix in range(width):
                x=y[ix+cam[0]]
                if x=="/":
                    py+="  "
                elif x==":" or x=="R" or x==".":
                    py+=colors.cyan+". "
                elif x=="$":
                    py+=colors.green+"S "
                elif x=="%":
                    py+=colors.green+"s "
                elif x=="#":
                    py+=colors.yellow+"# "
                elif x==",":
                    py+=colors.gray+", "
                elif x=="^":
                    py+=colors.red+"^ "
                elif x=="*":
                    py+=colors.purple+"* "
                elif x=="-":
                    py+=colors.yellow+"- "
                elif x=="~":
                    py+=colors.red+"~ "
                elif x=="E":
                    py+=colors.red+"E "
                elif x=="=":
                    py+=colors.gray+"= "
                elif x==";":
                    py+=colors.yellow+"; "
                else:
                    py+=colors.white+x+" "
                
            pm.append(py)
            #click.clear()
        screen=""
        #print("  _______________________________")
        screen+=colors.white+"  "+("_"*(cam[2]*2+1))+"\n"
        for p in pm:
            #print(" | "+p+"| ") 
            screen+=f'{colors.white+" | "+p: <{cam[2]*2+13}}'+colors.white+"| \n"
        #print(" |_______________________________|")
        screen+=" |"+("_"*(cam[2]*2+1))+"|" 
        for x in out:
            print(x)
        print(screen)
        for x in signText.split("\n"):
            width=(cam[2]*2+5)
            print(f'{x: ^{width}}')
        if saved==True:
            print("Game Saved")
        map[pos[1]][pos[0]]=reset

    if delay>= 10 and keyboard.is_pressed("w"):
        move[1]=-1
    if delay>= 10 and keyboard.is_pressed("s"):
        move[1]=1
    if delay>= 10 and keyboard.is_pressed("a"):
        move[0]=-1
    if delay>= 10 and keyboard.is_pressed("d"):
        move[0]=1
    if delay>= 10 and keyboard.is_pressed("space"):
        attacking=True
    if delay>= 10 and keyboard.is_pressed("esc"):
##        save=[]
##        map[pos[1]][pos[0]]="@"
##        for ys in range(len(map)-cam[3]):
##            line=""
##            for xs in range(len(map[ys])-cam[2]):
##                line+=map[ys][xs]+" "
##            save.append(line)
##        s=open("map2.txt", "w")
##        for x in save:
##            #print(x)
##            s.write(x+"\n")
##        s.close()
##        #os.system("start "+"map2.txt")
        exit()
        
    time.sleep(0.01)
    loops+=1
            

