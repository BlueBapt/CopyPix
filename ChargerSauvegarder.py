import pygame
from pygame.locals import *

class ChargerSauvegarder:
    def charger(niveau:str):
        file = open("levels/"+niveau+".level")
        bg = file.readlines()
        
        backgrounds = []
        
        for element in bg:
            info = element.split(",")
            image = pygame.image.load("./assets/textures/bg/"+info[0])
            backgrounds.append((int(info[1]),int(info[2]),info[0],image))
            
        sprites = []
        
        file = open("levels/"+niveau+".sprites")
        sp = file.readlines()
        
        for element in sp:
            info = element.split(",")
            image = pygame.image.load("./assets/textures/sprites/"+info[0])
            info[3] = info[3].replace("\n","")=="True"
            sprites.append((int(info[1]),int(info[2]),info[0],image,bool(info[3])))
        
        return (backgrounds,sprites)


    def sauvegarder(niveau,listeArrierePlan,listeSprites):
        fichier = open("levels/"+niveau+".level","w")
        for element in listeArrierePlan:
            (x,y,name,_)=element
            fichier.write(name+","+str(x)+","+str(y)+"\n")
        fichier.close()
        
        fichier = open("levels/"+niveau+".sprites","w")
        for element in listeSprites:
            (x,y,name,_,is_wall)=element
            fichier.write(name+","+str(x)+","+str(y)+","+str(is_wall)+"\n")
        fichier.close()
