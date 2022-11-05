import pygame
import random
from snake import Snake
from fruit import Fruit
import settings    

class Game:
    def __init__(self):
        #pygame init
        pygame.init()
        pygame.display.init()
        pygame.display.set_caption("Herb's Snake")
        
        self.main_screen = pygame.display.set_mode(settings.SCREEN_RESOLUTION)
        self.game_over = False
        self.paused = False        
        self.running = False
        self.clock = pygame.time.Clock()

    def new_game(self):
        
        self.snake_head = Snake(self.main_screen)
        self.snake_head.set_snake_head()
        self.snake_body_list = [self.snake_head]
    
        self.fruit = Fruit(self.main_screen)
        
        
        self.score = 0

    def text_render(self, text, size,pos):
        #custom function to facilitate text rendering.
        pygame.font.init()
        fnt = pygame.font.SysFont("Arial",size)
        render = fnt.render(text,1,settings.WHITE)
        self.main_screen.blit(render,pos)

    def run(self):
        self.new_game()
        
        while self.running:

            self.main_screen.fill((0,0,0))
            score_text = "score: " + str(self.score)
            self.text_render(score_text,16,(1,1))
            self.fruit.draw()

            #draws the snake's head first. it helps with the collision detection
            self.snake_head.update(self.snake_body_list)
            self.snake_head.draw()
            
            #updates and draws the rest os the snake
            for snake_piece in self.snake_body_list[1:]:
                snake_piece.update(self.snake_body_list)
                snake_piece.draw()
                
                #this tests with the snake's head Rect contains any other Rect... it runs in the update/draw loop 
                if self.snake_head.Rect.contains(snake_piece.Rect):
                    self.game_over = True
                    self.gameover()
                
                
            
            #test collision with fruit >> redraws fruit, creates new snake and add it to the snake list on position 1(index)
            if self.snake_head.Rect.colliderect(self.fruit.Rect):
                
                self.fruit = Fruit(self.main_screen)
                new_snake_piece = Snake(self.main_screen,(self.snake_head.last_x,self.snake_head.last_y,10,10))
                self.snake_body_list.insert(1,new_snake_piece)
                self.score +=1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    exit()
                
                elif event.type == pygame.KEYDOWN:
                    key = None
                    if event.key == pygame.K_w:
                        key = 'w'
                    elif event.key == pygame.K_a:
                        key = 'a'
                    elif event.key == pygame.K_s:
                        key = 's'
                    elif event.key == pygame.K_d:
                        key = 'd'    
                    elif event.key == pygame.K_SPACE:
                        self.paused = True
                        self.pause()
                    elif event.key == pygame.K_m: #test tool..makes the snake bigger when pressing m
                        new_snake_piece = Snake(self.main_screen,(self.snake_head.last_x,self.snake_head.last_y,10,10)) #
                        self.snake_body_list.insert(1,new_snake_piece)
                    
                    if event.key != pygame.K_SPACE and event.key != pygame.K_m:
                        self.snake_head.movement_handler(key)
                    
            self.clock.tick(30)
            pygame.display.update()
        
    def start(self):
        #start menu screen
        pygame.display.init()
        
        while not self.running:
            #rendering screen elements
            self.main_screen.fill(settings.BLACK)
            self.text_render("Herb's Snake",settings.FONT_SIZE1,(settings.SCREEN_RESOLUTION[0]/4,settings.SCREEN_RESOLUTION[1]/4))
            self.text_render("Press SPACE to start",settings.FONT_SIZE2,(settings.SCREEN_RESOLUTION[0]/3,settings.SCREEN_RESOLUTION[1]/2))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    exit()
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.running = True
                        self.run()

            pygame.display.update()

    def pause(self):
        #pauses the game when SPACE is pressed
        
        while self.paused:

            self.main_screen.fill((0,0,0))
            #custom render function
            self.text_render("pause",settings.FONT_SIZE1,(settings.SCREEN_RESOLUTION[0]/4,settings.SCREEN_RESOLUTION[1]/4))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    exit()
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.paused = False

            pygame.display.update()

    def gameover(self):

        #game over function is called when snake eats itself.
        
        while self.game_over:
            
            self.text_render("Game Over",settings.FONT_SIZE1,(settings.SCREEN_RESOLUTION[0]/4,settings.SCREEN_RESOLUTION[1]/4))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.game_over = False
                        self.new_game()
                        self.run()
            
            pygame.display.update()
