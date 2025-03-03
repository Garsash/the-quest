from rcolors import colors
from mathLib import Vector
from mathLib import Random
from objects.player import Player
from camera import Sprite
colorise=colors.colorise

##        #find distance from player
##        distx=player.x-enemy.x
##        disty=player.y-enemy.y
##        target=[0,0]
##
##        if abs(distx) <= 6 and abs(disty) <= 6:
##            #create scent map
##            scentMap=[]
##            for y in range(13):
##                row=[]
##                for x in range(13):
##                    row.append(26)
##                scentMap.append(row)
##
##            #create searching map
##            searching=[]
##            for y in range(13):
##                row=[]
##                for x in range(13):
##                    row.append(False)
##                searching.append(row)
##
##            #set player location
##            searching[6][6]=True
##            scentMap[6][6]=0
##            nodes=[[6,6]]
##
##            #loop through nodes
##            for node in nodes:
##                #look at neighbors
##                for neighbor in neighbors:
##                    #variable set up
##                    neighborx=node[0]+neighbor[0] #nx
##                    neighbory=node[1]+neighbor[1] #ny
##                    nodex=node[0] #hx
##                    nodey=node[1] #hy
##                    worldy=player.y+neighbory-6
##                    worldx=player.x+neighborx-6
##
##                    #if inside map
##                    if neighbory < 0 or neighbory >= 13:
##                        continue
##                    if neighborx < 0 or neighborx >= 13:
##                        continue
##
##                    here=scentMap[nodey][nodex]
##                    #if not searched already
##                    if searching[neighbory][neighborx] == False:
##                        #is there a wall
##                        state=map[worldy][worldx]
##                        if state in wallTiles or state in deathTiles and state != "E":
##                            continue
##
##                        #get smallest scent
##                        if scentMap[neighbory][neighborx] >= here:
##                            scentMap[neighbory][neighborx]=here+1
##                            nodes.append([neighborx,neighbory])
##                        searching[neighbory][neighborx]=True
##
##                        #found enemy
##                        if state=="E" and worldx==enemy.x and worldy==enemy.y:
##                            #out.append([worldx,worldy])
##                            #Loc=[worldx,worldy]
##                            #out.append("enemy pos "+str(Loc))
##                            #if Loc in foundEnemies:
##                            #    continue
##                            nodes=[]
##                            lowest=26
##                            target=[0,0]
##                            values=[]
##
##                            #look at neighbors
##                            for Neighbor in neighbors:   
##                                enemyx=neighborx+Neighbor[0]
##                                enemyy=neighbory+Neighbor[1]
##                                if enemyy < 0 or enemyy >= 13:
##                                    continue
##                                if enemyx < 0 or enemyx >= 13:
##                                    continue
##                                #find values
##                                if map[player.y+enemyy-6][player.x+enemyx-6] == "E":
##                                    continue
##                                values.append([Neighbor[0],Neighbor[1],scentMap[enemyy][enemyx]])
##
##                            #get smallest values
##                            minV=24
##                            for min in values:
##                                if min[2] < minV:
##                                    minV=min[2]
##
##                            #pick random closest direction
##                            closest=[value for value in values if value[2]==minV]
##                            if len(closest)>=1:
##                                choice=random.choice(closest)
##                                target=[choice[0],choice[1]]
##                            break
##        #move enemy
##        map[enemy.y][enemy.x]=enemy.here
##        enemy.x+=target[0]
##        enemy.y+=target[1]
##        enemy.here=map[enemy.y][enemy.x]
##        map[enemy.y][enemy.x]="E"

class Scent():
    def __init__(self,scent,searched=False):
        self.scent=scent
        self.searched=searched

class Enemy():
    instantiationTiles=["E"]

    #@staticmethod
    #def instantiationTiles():
    #    return ["^"]

    @classmethod
    def create(cls,x,y,level):
        enemy=Enemy(x,y,)
        level.createObject(enemy)
        
    def __init__(self,x,y,distance=13,tile="E",layer=1):
        self.x = x
        self.y = y
        self.tile=tile
        self.layer=layer
        self.distance=distance
        self.damage=True
    
    def tick(self,level,frame,index,player,debug,**kwargs):
        #create map of far scents
        scentMap=[[Scent(self.distance*2,False) for x in range(self.distance)]for x in range(self.distance)]
        #mark center as closest
        center=int(self.distance/2)
        searching=[Vector(center,center)]
        scentMap[center][center].scent=0
        scentMap[center][center].searched=True
        target=Vector(0,0)
        
        ##debug.beginCount("#")
        ##debug.beginCount("@")
        ##debug.log(Vector(player.x,player.y))
        #loop through the map
        for position in searching:
            ##debug.count("#")
            for neighbor in Vector.neighbors():    
                #convert the neighbor vector to a position in the scent map
                mapSpaceNeighborCoords=position+neighbor
            
                #convert a position in the scent map to a position in the level
                levelSpaceNeighborCoords=Vector(player.x,player.y)+mapSpaceNeighborCoords-Vector(center,center)
                ##debug.log(levelSpaceNeighborCoords)

                #skip if outside scentMap
                if mapSpaceNeighborCoords.x < 0 or mapSpaceNeighborCoords.x >= self.distance or mapSpaceNeighborCoords.y < 0 or mapSpaceNeighborCoords.y >= self.distance:
                    continue

                if not level.tileExists(levelSpaceNeighborCoords.x, levelSpaceNeighborCoords.y):
                    continue
                
                #get scent at current search positions
                scentHere=scentMap[position.y][position.x]
                neighborScent=scentMap[mapSpaceNeighborCoords.y][mapSpaceNeighborCoords.x]
                
                #if the position has not been searched
                if neighborScent.searched==False:
                    #get tile in level at current search position
                    tile=level.getTile(levelSpaceNeighborCoords.x,levelSpaceNeighborCoords.y)
                    #if tile is empty
                    if not tile in level.wallTiles: # or any(hasattr(x,"damage") and x.damage==True and x.x==levelSpaceNeighborCoords.x and x.y==levelSpaceNeighborCoords.y and type(x)!=Enemy for x in level.objects)
                        ##debug.log("empty")
                        #set scent at current search location to be one greater than previous
                        if neighborScent.scent >= scentHere.scent:
                            neighborScent.scent=scentHere.scent+1
                            searching.append(mapSpaceNeighborCoords)
                        neighborScent.searched=True
                        
                        #when enemy has been found on the map
                        if self.x==levelSpaceNeighborCoords.x and self.y==levelSpaceNeighborCoords.y:
                            searching=[]
                            lowestScent=self.distance*2
                            possibleMoves=[]
                            
                            #look for scents adjacent to enamy
                            for neighbor in Vector.neighbors():
                                #convert move vector to position on scent map
                                mapSpaceMove=neighbor+mapSpaceNeighborCoords
                                levelSpaceMove=Vector(player.x,player.y)+mapSpaceMove-Vector(center,center)
                                if mapSpaceMove.x < 0 or mapSpaceMove.y >= self.distance or mapSpaceMove.x < 0 or mapSpaceMove.y >= self.distance:
                                    continue
                                if any(type(x)==Enemy and x.damage==True and x.x==levelSpaceMove.x and x.y==levelSpaceMove.y for x in level.objects):
                                    continue
                                possibleMoves.append([Vector(neighbor.x,neighbor.y),scentMap[mapSpaceMove.y][mapSpaceMove.x]])
                            
                            #find the lowest scents
                            closest=[[Vector(0,0),Scent(self.distance*2)]]
                            for move in possibleMoves:
                                if move[1].scent < closest[0][1].scent:
                                    closest=[move]
                                elif move[1].scent == closest[0][1].scent:
                                    closest.append(move)
                            
                            #pick a scent to follow
                            bestMoves=closest
                            if len(closest) > 1:
                                ###swap out for worse random
                                randomMove=Random.choice(bestMoves)
                                #randomMove=bestMoves[Random.setRandom(((frame+index)%255)%len[bestMoves])]
                                target=Vector(randomMove[0].x,randomMove[0].y)
                            elif len(closest) == 1:
                                target=Vector(bestMoves[0][0].x,bestMoves[0][0].y)
                            break

        for y in scentMap:
            row=[]
            for x in y:
                row.append(x.scent)
            ##debug.log(row)

        self.x+=target.x
        self.y+=target.y

    def attack(self,enemy,level,camera,frame,signText,debug):
        if self.damage==True and self.x==enemy.x and self.y==enemy.y:
                    enemy.hurt(level,camera,frame,signText,debug)
                    return True
        return False

    def draw(self, **kwargs):
        sprite=colorise(self.tile,"red")
        return Sprite(self.x,self.y,self.layer,sprite)