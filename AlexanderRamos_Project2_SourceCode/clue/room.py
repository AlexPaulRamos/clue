import pygame
from .constants import *
class Room:
    def __init__(self, row,col,id: str,entrance: bool, passage = None):
        self.row=row
        self.col=col
        self.id=id
        self.entrance=entrance
        self.players={}
        self.passage=passage
    def draw(self,win):
        rec=pygame.Rect(self.col*SQUARE_SIZE, self.row*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE)
        if(self.entrance):
            pygame.draw.rect(win,BROWN,rec)
        else:
            pygame.draw.rect(win,BLACK,rec)
        
