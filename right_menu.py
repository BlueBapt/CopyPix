import os
import pygame

class RightMenu :
    def __init__(self):
        
        self.bg_color=pygame.image.load("./assets/right_menu.png")
        
        self.wall_yes=pygame.image.load("./assets/textures/wall_yes.png")
        self.wall_no=pygame.image.load("./assets/textures/wall_no.png")
        
        self.right_arrow=pygame.image.load("./assets/textures/arrow_right.png")
        self.left_arrow=pygame.image.load("./assets/textures/arrow_left.png")
        
        self.is_wall=False
        
        # For backgrounds
        self.bg_list=[]
        self.bg_name_list = os.listdir("./assets/textures/bg")
        if len(self.bg_name_list)==0:
            print("The background folder is empty!")
            exit(1)
        for element in self.bg_name_list:
            self.bg_list.append(pygame.image.load("./assets/textures/bg/"+element))
            
        # For sprites
        self.sprite_list=[]
        self.sprite_name_list = os.listdir("./assets/textures/sprites")
        if len(self.sprite_name_list)==0:
            print("The sprite folder is empty!")
            exit(1)
        for element in self.sprite_name_list:
            self.sprite_list.append(pygame.image.load("./assets/textures/sprites/"+element))

        
        
        self.page=0
        self.selected=0
        
        self.background_selected=True
        
    def display(self,screen,zoom):
        screen.blit(pygame.transform.scale(self.bg_color,(zoom*16,zoom*64)),(64*zoom,0))
        
        if self.background_selected:
            for i in range(self.page*8,self.page*8+8) :
                if (len(self.bg_list)>i):
                    screen.blit(pygame.transform.scale(self.bg_list[i],(zoom*8,zoom*8)),(64*zoom,(i-(self.page*8))*8*zoom,8*zoom,8*zoom))
                    # print(pygame.Rect(64*zoom,(i-(self.page*8))*8*zoom,8*zoom,8*zoom))
                else:
                    break
        else:
            for i in range(self.page*8,self.page*8+8) :
                if (len(self.sprite_list)>i):
                    screen.blit(pygame.transform.scale(self.sprite_list[i],(zoom*8,zoom*8)),(64*zoom,(i-(self.page*8))*8*zoom,8*zoom,8*zoom))
                    # print(pygame.Rect(64*zoom,(i-(self.page*8))*8*zoom,8*zoom,8*zoom))
                else:
                    break
                
            if self.is_wall :
                screen.blit(pygame.transform.scale(self.wall_yes,(zoom*8,zoom*8)),(72*zoom,0,8*zoom,8*zoom))
            else:
                screen.blit(pygame.transform.scale(self.wall_no,(zoom*8,zoom*8)),(72*zoom,0,8*zoom,8*zoom))
        
        screen.blit(pygame.transform.scale(self.right_arrow,(zoom*8,zoom*8)),(72*zoom,8*zoom*6,8*zoom,8*zoom))
        screen.blit(pygame.transform.scale(self.left_arrow,(zoom*8,zoom*8)),(72*zoom,8*zoom*7,8*zoom,8*zoom))
            
            
    def detectCollision(self,pos,zoom:int):
        
        
        if self.background_selected:
            for i in range(self.page*8,self.page*8+8) :
                if (len(self.bg_list)>i):
                    if pygame.Rect(64*zoom,(i-(self.page*8))*8*zoom,8*zoom,8*zoom).collidepoint(pos):
                        print(self.bg_name_list[i])
                        self.selected=i
                        return (True,self.getSelectedImage())
                else:
                    break
        else:
            for i in range(self.page*8,self.page*8+8) :
                if (len(self.sprite_list)>i):
                    if pygame.Rect(64*zoom,(i-(self.page*8))*8*zoom,8*zoom,8*zoom).collidepoint(pos):
                        print(self.sprite_name_list[i])
                        self.selected=i
                        return (True,self.getSelectedImage())
                else:
                    break
            # collision detection for wall
            if pygame.Rect(72*zoom,0,8*zoom,8*zoom).collidepoint(pos):
                self.is_wall= not self.is_wall
            
        if pygame.Rect(72*zoom,8*zoom*6,8*zoom,8*zoom).collidepoint(pos):
            self.pagePlus()
            return (True,self.getSelectedImage())
        if pygame.Rect(72*zoom,8*zoom*7,8*zoom,8*zoom).collidepoint(pos):
            self.pageMinus()
            return (True,self.getSelectedImage())
        
        
            
            
        return (False,None)
            
    def getSelectedImage(self):
        if self.background_selected:
            return self.bg_list[self.selected]
        else:
            return self.sprite_list[self.selected]
    
    def getNameOfSelectedImage(self):
        if self.background_selected:
            return self.bg_name_list[self.selected]
        else:
            return self.sprite_name_list[self.selected]
    
    def pagePlus(self):
        if self.background_selected:
            if ((self.page+1)*8 < len(self.bg_list)):
                self.page+=1
        else:
            if ((self.page+1)*8 < len(self.sprite_list)):
                self.page+=1
            
    def pageMinus(self):
        if (self.page>0):
            self.page-=1
            
    def toggleSelection(self):
        self.background_selected= not self.background_selected
        self.selected=0
        self.page=0
        
    def isBackground(self):
        return self.background_selected
    
    def isWall(self):
        return self.is_wall