import os
import pygame

START_BUTTON_POS_X = 14
START_BUTTON_POS_Y = 40
START_BUTTON_LEN = 36
START_BUTTON_HEI = 13

pygame.font.init()


class MainMenu :
    def __init__(self):
        
        self.r_arrow= pygame.image.load("./assets/textures/arrow_right.png")
        self.l_arrow= pygame.image.load("./assets/textures/arrow_left.png")
        
        self.font= pygame.font.Font("assets/font.ttf",7)
        
        self.bg_title_screen = pygame.image.load("./assets/title_screen.png")
        self.bg_level_selection_screen = pygame.image.load("./assets/editor_bg.png")
        
        self.img_level_not_hovered= pygame.image.load("./assets/select_box_off.png")
        self.img_level_hovered= pygame.image.load("./assets/select_box_on.png")
        
        self.level_name_list = []
        self.is_on_title = True
        
        self.level_hovered=0
        self.page=0
        
        content = os.listdir("./levels")
        if len(content)==0:
            print("The level folder is empty!")
            exit(1)
        for i in range(int(len(content)/2)):
            self.level_name_list.append(content[i*2][0:len(content[i*2])-6])
            # print(content[i*2][0:len(content[i*2])-6])





    def display(self,screen,zoom:int,event):
        if self.is_on_title:
            screen.blit(pygame.transform.scale(self.bg_title_screen,(zoom*64,zoom*64)),(0,0))
        
        else:
            screen.blit(pygame.transform.scale(self.bg_level_selection_screen,(zoom*64,zoom*64)),(0,0))
            for i in range(self.page*4,self.page*4+4) :
                if (len(self.level_name_list)>i):
                    if i == self.level_hovered:
                        screen.blit(pygame.transform.scale(self.img_level_hovered,(zoom*60,zoom*10)),(2*zoom,((i%4)*12+2)*zoom,zoom*60,zoom*10))
                    else:
                        screen.blit(pygame.transform.scale(self.img_level_not_hovered,(zoom*60,zoom*10)),(2*zoom,((i%4)*12+2)*zoom,zoom*60,zoom*10))
                    text = self.font.render(self.level_name_list[i],1,(255,255,255))
                    screen.blit(text,(4*zoom,((i%4)*12+4)*zoom))
                else:
                    break
            screen.blit(pygame.transform.scale(self.l_arrow,(8*zoom,zoom*8)),(0,56*zoom,zoom*8,zoom*8))
            screen.blit(pygame.transform.scale(self.r_arrow,(8*zoom,zoom*8)),(56*zoom,56*zoom,zoom*8,zoom*8))
                
            
        return self.detectCollision(event,zoom)
        
            
            
    def detectCollision(self,event,zoom:int):
        if self.is_on_title:
            for ev in event:
                # only do something if the event is of type QUIT
                if ev.type == pygame.QUIT:
                    exit(0)
                if ev.type == pygame.KEYDOWN:
                    k = pygame.key.get_pressed() 
                            
                    if k[pygame.K_SPACE]:
                        self.changeToSelectionScreen()
                        
                    if k[pygame.K_ESCAPE]:
                        exit(0)
                        
                        
                if ev.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if pygame.Rect(START_BUTTON_POS_X*zoom,START_BUTTON_POS_Y*zoom,START_BUTTON_LEN*zoom,START_BUTTON_HEI*zoom).collidepoint(pos):
                        self.changeToSelectionScreen()
        
        else:
            
            pos = pygame.mouse.get_pos()
                        
            
            for i in range(self.page*4,self.page*4+4) :
                if (len(self.level_name_list)>i):
                    if i != self.level_hovered:
                        if pygame.Rect(2*zoom,((i%4)*12+2)*zoom,zoom*60,zoom*10).collidepoint(pos):
                            self.level_hovered=i
                            break
                    # print(pygame.Rect(64*zoom,(i-(self.page*8))*8*zoom,8*zoom,8*zoom))
                else:
                    break
            
            for ev in event:
                # only do something if the event is of type QUIT
                if ev.type == pygame.QUIT:
                    exit(0)
                    
                if ev.type == pygame.KEYDOWN:
                    k = pygame.key.get_pressed() 
                        
                    if k[pygame.K_ESCAPE]:
                        self.changeToTitleScreen()
                        
                    if k[pygame.K_SPACE]:
                        return (True,self.level_name_list[self.level_hovered])

                    if k[pygame.K_DOWN]:
                        self.plusSelection()
                    
                    if k[pygame.K_UP]:
                        self.minusSelection()
                        

                    if k[pygame.K_RIGHT]:
                        self.pagePlus()
                    
                    if k[pygame.K_LEFT]:
                        self.pageMinus()
                    
                if ev.type == pygame.MOUSEBUTTONUP:
                    if pygame.Rect(2*zoom,((self.level_hovered%4)*12+2)*zoom,zoom*60,zoom*10).collidepoint(pos):
                        return (True,self.level_name_list[self.level_hovered])
                        # print(pygame.Rect(64*zoom,(i-(self.page*8))*8*zoom,8*zoom,8*zoom))
                        
                    if pygame.Rect(0,56*zoom,zoom*8,zoom*8).collidepoint(pos):
                        self.pageMinus()
                        
                    if pygame.Rect(56*zoom,56*zoom,zoom*8,zoom*8).collidepoint(pos):
                        self.pagePlus()
        
        return (False,None)

    
    def pagePlus(self):
        if ((self.page+1)*4 < len(self.level_name_list)):
            self.page+=1
            self.level_hovered=self.page*4
            
    def pageMinus(self):
        if self.page>0:
            self.page-=1
            self.level_hovered=self.page*4+3
    
    def minusSelection(self):
        if self.level_hovered%4==0:
            self.pageMinus()
            return
        if self.level_hovered!=0:
            self.level_hovered-=1
            
    def plusSelection(self):
        if self.level_hovered%4==3:
            self.pagePlus()
            return
        if self.level_hovered!=len(self.level_name_list)-1:
            self.level_hovered+=1
        

    def changeToSelectionScreen(self):
        self.is_on_title=False
        
    def changeToTitleScreen(self):
        self.is_on_title=True
        
    def setFontSize(self,zoom):
        self.font= pygame.font.Font("assets/font.ttf",7*zoom)