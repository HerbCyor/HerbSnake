import pygame
import random

class Fruit(pygame.Rect):

    def __init__(self, main_screen):

        self.Rect = pygame.Rect(random.randrange(290),random.randrange(390),10,10)
        self.color = (255,0,0)
        self.screen = main_screen

    def draw(self):
        pygame.draw.rect(self.screen,self.color,self.Rect)