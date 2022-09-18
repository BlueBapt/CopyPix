# import the pygame module, so you can use it
import pygame
from ChargerSauvegarder import ChargerSauvegarder

from right_menu import RightMenu

ZOOM = 10

editor_bg=pygame.image.load("assets/editor_bg.png")
wall_sprite=pygame.image.load("./assets/textures/wall.png")

clock = pygame.time.Clock()

rightmenu = RightMenu()
backgrounds = []
sprites = []

cursor_image=rightmenu.getSelectedImage()

cursor_x=0
cursor_y=0

camera_x=0
camera_y=0

 
     
# initialize the pygame module
pygame.init()
# load and set the logo
logo = pygame.image.load("icon.ico")
pygame.display.set_icon(logo)
pygame.display.set_caption("CopyPix - Builder")

#pygame.key.set_repeat(5,1)
    
# create a surface on screen that has the size of 240 x 180
screen = pygame.display.set_mode((80*ZOOM,64*ZOOM))
    
# define a variable to control the main loop
running = True
    
def repaint():
    # screen.fill([255,255,255])
    screen.blit(pygame.transform.scale(editor_bg,(ZOOM*64,ZOOM*64)),(0,0))
    for element in backgrounds:
        (x,y,_,img)=element
        screen.blit(pygame.transform.scale(img,(ZOOM*8,ZOOM*8)),((x-camera_x)*8*ZOOM,(y-camera_y)*8*ZOOM))
    for element in sprites:
        (x,y,_,img,is_wall)=element
        screen.blit(pygame.transform.scale(img,(ZOOM*8,ZOOM*8)),((x-camera_x)*8*ZOOM,(y-camera_y)*8*ZOOM))
        if is_wall:
            screen.blit(pygame.transform.scale(wall_sprite,(ZOOM*8,ZOOM*8)),((x-camera_x)*8*ZOOM,(y-camera_y)*8*ZOOM))
    
    rightmenu.display(screen,ZOOM)
    screen.blit(pygame.transform.scale(cursor_image,(ZOOM*8,ZOOM*8)),((cursor_x-camera_x)*8*ZOOM,(cursor_y-camera_y)*8*ZOOM))
    pygame.display.flip()
    clock.tick(60)
    
# main loop
while running:
    # event handling, gets all event from the event queue
    for event in pygame.event.get():
        # only do something if the event is of type QUIT
        if event.type == pygame.QUIT:
            name_of_level = input("In what name to save this level? ")
            ChargerSauvegarder.sauvegarder(name_of_level,backgrounds,sprites)
            # change the value to False, to exit the main loop
            running = False
        if event.type == pygame.KEYDOWN:
            k = pygame.key.get_pressed()
            if k[pygame.K_UP]:
                cursor_y-=1
                if cursor_y<camera_y:
                    camera_y=cursor_y
            elif k[pygame.K_DOWN]:
                cursor_y+=1
                if cursor_y>=camera_y+8:
                    camera_y+=1
            elif k[pygame.K_RIGHT]:
                cursor_x+=1
                if cursor_x>=camera_x+8:
                    camera_x+=1
            elif k[pygame.K_LEFT]:
                cursor_x-=1
                if cursor_x<camera_x:
                    camera_x=cursor_x
                    
                    
                    
                    
            elif k[pygame.K_SPACE]:
                if rightmenu.isBackground():
                    for element in backgrounds:
                        (x,y,_,_)=element
                        if (x==cursor_x and y==cursor_y):
                            backgrounds.remove(element)
                    backgrounds.append((cursor_x,cursor_y,rightmenu.getNameOfSelectedImage(),cursor_image))
                else:
                    for element in sprites:
                        (x,y,_,_,_)=element
                        if (x==cursor_x and y==cursor_y):
                            sprites.remove(element)                       

                    sprites.append((cursor_x,cursor_y,rightmenu.getNameOfSelectedImage(),cursor_image,rightmenu.isWall()))  
                
                
                
            elif k[pygame.K_TAB]:
                rightmenu.toggleSelection()
                cursor_image=rightmenu.getSelectedImage()
                
                
        if event.type == pygame.MOUSEBUTTONUP:
            position = pygame.mouse.get_pos()
            (change,img) = rightmenu.detectCollision(position,ZOOM)
            if change:
                cursor_image=img
                
    repaint()
                
                
    
    
