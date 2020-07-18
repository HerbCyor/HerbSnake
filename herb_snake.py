import pygame
import random

class fruit(pygame.Rect):

    def __init__(self):

        self.Rect = pygame.Rect(random.randrange(290),random.randrange(390),10,10)
        self.color = (255,0,0)
        self.screen = main_screen

    def draw(self):
        pygame.draw.rect(self.screen,self.color,self.Rect)

class snake(pygame.Rect):

    def __init__(self,Rect):

        self.Rect = Rect
        self.color = (255,255,255)
        self.x = self.Rect[0]
        self.y = self.Rect[1]
        self.last_x = 0
        self.last_y = 0
        self.screen = main_screen
        self.horizontal = 0
        self.vertical = 0

    def set_horizontal(self): #to set initial movement
        self.horizontal = -10

    def update(self):
        #snake's head get's special treatment
        if mySnake_list.index(self)==0:
            #loops around the screen, no borders
            if self.x > 290:
                self.x = 0
            elif self.x < 0:
                self.x = 290
            elif self.y > 390:
                self.y =0
            elif self.y < 0:
                self.y = 390
            #the snake registers it's current position (self_x/y) into (last_x/y) before assigning new position
            self.last_x = self.x
            self.last_y = self.y
            #new position assignment according to vertical/horizontal shift.
            self.x += self.horizontal
            self.y += self.vertical
            #set_Rect
            self.Rect = pygame.Rect(self.x,self.y, 10,10)
        
        #rest of the snake
        else:
            #registers its current position in the same fashion as snake head. 
            self.last_x = self.x
            self.last_y = self.y
            #updates it's own position based o the last position given by the previous element in mySnake_List
            self.x += (mySnake_list[mySnake_list.index(self)-1].last_x - self.x)
            self.y += (mySnake_list[mySnake_list.index(self)-1].last_y - self.y)
            #set_Rect
            self.Rect = pygame.Rect(self.x,self.y,10,10)
                    
    def direction(self,key):

        if key == 'w' and self.vertical <= 0: #can't go up if going down
            self.horizontal,self.vertical = 0,-10
        elif key == 'a' and self.horizontal <= 0:
            self.horizontal,self.vertical = -10,0
        elif key == 's' and self.vertical >= 0:
            self.horizontal,self.vertical = 0,10
        elif key == 'd' and self.horizontal >= 0:
            self.horizontal,self.vertical = 10,0
        
            
    def draw(self):
        pygame.draw.rect(self.screen,self.color, self.Rect)
                    
#pygame init
pygame.display.init()
pygame.display.set_caption("Herb's Snake")

main_screen = pygame.display.set_mode([300,400])

def text_render(text, screen,size,pos):
    #custom function to facilitade text rendering. totally unnecessary
    pygame.font.init()
    fnt = pygame.font.SysFont("Comic Sans",size)
    text_render = fnt.render(text,1,(255,255,255))
    screen.blit(text_render,pos)
    
def menu():
    #start menu screen

    menu_screen = pygame.display.set_mode([300,400])
    text = "Herb's Snake"
    text2 = "Press SPACE"
    
    running = True
    
    while running:
        #rendering screen elements
        menu_screen.fill((0,0,0))
        text_render(text,menu_screen,32,(75,100))
        text_render(text2,menu_screen,22,(100,275))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game() #runs game

        pygame.display.update()

def game():
    # main game application.
    global running
    global paused
    global game_over
    global mySnake_list

    game_over = False
    paused = False
    running = True
    #snake's head
    mySnake = snake((150,200,10,10))
    mySnake.set_horizontal()
    mySnake_list = [mySnake]
    
    fruit1 = fruit()
    clock = pygame.time.Clock()
    score = 0

    while running:

        main_screen.fill((0,0,0))
        score_text = "score: " + str(score)
        text_render(score_text,main_screen,16,(1,1))
        fruit1.draw()

        #draws the snake's head first. it helps with the collision detection
        mySnake.update()
        mySnake.draw()
        
        #updates and draws the rest os the snake
        for Snake in mySnake_list[1:]:
            Snake.update()
            Snake.draw()
            
            #this tests with the snake's head Rect contains any other Rect... it runs in the update/draw loop 
            if mySnake.Rect.contains(Snake.Rect):
                print("nhac")
                game_over = True
                gameover()
            
            
        
        #test collision with fruit >> redraws fruit, creates new snake and add it to the snake list on position 1(index)
        if mySnake.Rect.colliderect(fruit1.Rect):
            
            fruit1 = fruit()
            newSnake = snake((mySnake.last_x,mySnake.last_y,10,10))
            mySnake_list.insert(1,newSnake)
            score +=1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    key = 'w'
                elif event.key == pygame.K_a:
                    key = 'a'
                elif event.key == pygame.K_s:
                    key = 's'
                elif event.key == pygame.K_d:
                    key = 'd'    
                elif event.key == pygame.K_SPACE:
                    paused = True
                    pause()
                elif event.key == pygame.K_m: #test tool..makes the snake bigger when pressing m
                    newSnake = snake((mySnake.last_x,mySnake.last_y,10,10))
                    mySnake_list.insert(1,newSnake)
                
                if event.key != pygame.K_SPACE and event.key != pygame.K_m:
                    mySnake.direction(key)
                
        clock.tick(30)
        pygame.display.update()

def pause():
    #pauses the game when SPACE is pressed
    global paused
    global running

    pause_screen = pygame.display.set_mode(([300,400]))

    while paused == True:

        pause_screen.fill((0,0,0))
        #custom render function
        text_render("pause",pause_screen,30,(110,100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False

        pygame.display.update()

def gameover():

    #game over function is called when snake eats itself.
    
    global game_over

    while game_over == True:
        
        text_render("Game Over",main_screen,30,(90,80))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_over = False
                    menu()
        
        pygame.display.update()

menu()
pygame.quit()