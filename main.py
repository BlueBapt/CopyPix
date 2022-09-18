    # import the pygame module, so you can use it
import pygame
from ChargerSauvegarder import ChargerSauvegarder
from main_menu import MainMenu

ZOOM = 10
FORCE = 2

clock = pygame.time.Clock()

hero = pygame.image.load("assets/textures/hero/hero.png")

(BACKGROUNDS,SPRITES) = ([],[])

hero_x=0
hero_y=0

camera_x=-4
camera_y=-4


def detectCollision(x,y,coming_from,force):
    i=0
    for (x_sprite,y_sprite,name,img,is_wall) in SPRITES:
        if x_sprite == x and y_sprite == y :
            print(is_wall)
            if is_wall:
                return False
            else:
                if coming_from=="EAST":
                    for (x_spr2,y_spr2,_,_,is_wall2) in SPRITES :
                        if x-1 == x_spr2 and y == y_spr2 :
                            if not is_wall2 and force >0:
                                res= detectCollision(x-1,y,"EAST",force-1)
                                if res:
                                    SPRITES[i]=(x_sprite-1,y_sprite,name,img,is_wall)
                                return res
                            return False
                    SPRITES[i]=(x_sprite-1,y_sprite,name,img,is_wall)
                        
                    x_sprite-=1
                elif coming_from=="WEST":
                    for (x_spr2,y_spr2,_,_,is_wall2) in SPRITES :
                        if x+1 == x_spr2 and y == y_spr2 :
                            if not is_wall2 and force >0:
                                res = detectCollision(x+1,y,"WEST",force-1)   
                                if res:
                                    SPRITES[i]=(x_sprite+1,y_sprite,name,img,is_wall)
                                return res                       
                            return False
                    SPRITES[i]=(x_sprite+1,y_sprite,name,img,is_wall)
                        
                    x_sprite+=1
                elif coming_from=="NORTH":
                    for (x_spr2,y_spr2,_,_,is_wall2) in SPRITES :
                        if x == x_spr2 and y+1 == y_spr2 :
                            if not is_wall2 and force >0:
                                res = detectCollision(x,y+1,"NORTH",force-1)
                                if res:
                                    SPRITES[i]=(x_sprite,y_sprite+1,name,img,is_wall)
                                return res                              
                            return False
                    SPRITES[i]=(x_sprite,y_sprite+1,name,img,is_wall)
                    
                        
                    y_sprite+=1
                elif coming_from=="SOUTH":
                    for (x_spr2,y_spr2,_,_,is_wall2) in SPRITES :
                        if x == x_spr2 and y-1 == y_spr2 :
                            if not is_wall2 and force >0:
                                res = detectCollision(x,y-1,"SOUTH",force-1)
                                if res:
                                    SPRITES[i]=(x_sprite,y_sprite-1,name,img,is_wall)
                                return res              
                            return False
                    SPRITES[i]=(x_sprite,y_sprite-1,name,img,is_wall)
                        
                    y_sprite-=1
                return True
        i+=1
    return True

 
     
# initialize the pygame module
pygame.init()
# load and set the logo
logo = pygame.image.load("icon.ico")
pygame.display.set_icon(logo)
pygame.display.set_caption("CopyPix")

#pygame.key.set_repeat(5,1)
    
# create a surface on screen that has the size of 240 x 180
screen = pygame.display.set_mode((64*ZOOM,64*ZOOM))
    
# define a variable to control the main loop
running = True

main_menu = MainMenu()
main_menu.setFontSize(ZOOM)

def display_main_menu():
    is_on_main_menu=True
    
    while is_on_main_menu:
        (chosen,level_chosen)=main_menu.display(screen,ZOOM,pygame.event.get())
        if chosen:
            is_on_main_menu=False
            return ChargerSauvegarder.charger(level_chosen)
        pygame.display.flip()
        clock.tick(60)
        
        
        
def repaint():
    screen.fill([255,255,255])
    for element in BACKGROUNDS:
        (x,y,_,img)=element
        screen.blit(pygame.transform.scale(img,(ZOOM*8,ZOOM*8)),((x-camera_x)*8*ZOOM,(y-camera_y)*8*ZOOM))
    for element in SPRITES:
        (x,y,_,img,_)=element
        screen.blit(pygame.transform.scale(img,(ZOOM*8,ZOOM*8)),((x-camera_x)*8*ZOOM,(y-camera_y)*8*ZOOM))
    
    screen.blit(pygame.transform.scale(hero,(ZOOM*8,ZOOM*8)),((hero_x-camera_x)*8*ZOOM,(hero_y-camera_y)*8*ZOOM))
    pygame.display.flip()
    clock.tick(60)
    
    
(BACKGROUNDS,SPRITES)=display_main_menu()

# main loop
while running:
    
    
    # event handling, gets all event from the event queue
    for event in pygame.event.get():
        # only do something if the event is of type QUIT
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            k = pygame.key.get_pressed()
            if k[pygame.K_UP]:
                print("UP")
                if detectCollision(hero_x,hero_y-1,"SOUTH",FORCE):
                    hero_y-=1
                    if hero_y<camera_y+3:
                        camera_y-=1
            elif k[pygame.K_DOWN]:
                print("DOWN")
                if detectCollision(hero_x,hero_y+1,"NORTH",FORCE):
                    hero_y+=1
                    if hero_y>=camera_y+5:
                        camera_y+=1
            elif k[pygame.K_RIGHT]:
                print("RIGHT")
                if detectCollision(hero_x+1,hero_y,"WEST",FORCE):
                    hero_x+=1
                    if hero_x>=camera_x+5:
                        camera_x+=1
            elif k[pygame.K_LEFT]:
                print("LEFT")
                if detectCollision(hero_x-1,hero_y,"EAST",FORCE):
                    hero_x-=1
                    if hero_x<camera_x+3:
                        camera_x-=1
            elif k[pygame.K_ESCAPE]:
                (BACKGROUNDS,SPRITES)=display_main_menu()
                hero_x=0
                hero_y=0

                camera_x=-4
                camera_y=-4
                    
                
    repaint()
                
                
    
    
