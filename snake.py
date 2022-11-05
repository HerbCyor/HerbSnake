import pygame
import settings

class Snake(pygame.Rect):

    def __init__(self, main_screen, initial_rect=settings.SNAKE_RECT):

        self.Rect = initial_rect
        self.color = settings.WHITE
        self.x = self.Rect[0]
        self.y = self.Rect[1]
        self.last_x = 0
        self.last_y = 0
        self.screen = main_screen
        self.dx = -10 #initial x speed
        self.dy = 0 #initial y speed

        self._head = False

    def set_snake_head(self):
        self._head = True

    def is_head(self):
        return self._head

    def update(self, snake_body_list):
        #snake's head get's special treatment
        if self.is_head():
            #loops around the screen, no border collision
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
            self.x += self.dx
            self.y += self.dy
            #set_Rect
            self.Rect = pygame.Rect(self.x,self.y, 10,10)
        
        #rest of the snake
        else:
            #registers its current position in the same fashion as snake head. 
            self.last_x = self.x
            self.last_y = self.y
            #updates it's own position based o the last position given by the previous element in mySnake_List
            self.x += (snake_body_list[snake_body_list.index(self)-1].last_x - self.x)
            self.y += (snake_body_list[snake_body_list.index(self)-1].last_y - self.y)
            #set_Rect
            self.Rect = pygame.Rect(self.x,self.y,10,10)
                    
    def movement_handler(self,key):

        if key == 'w' and self.dy <= 0: #can't go up if going down
            self.dx,self.dy = 0,-10
        elif key == 'a' and self.dx <= 0:
            self.dx,self.dy = -10,0
        elif key == 's' and self.dy >= 0:
            self.dx,self.dy = 0,10
        elif key == 'd' and self.dx >= 0:
            self.dx,self.dy = 10,0
        
            
    def draw(self):
        pygame.draw.rect(self.screen,self.color, self.Rect)