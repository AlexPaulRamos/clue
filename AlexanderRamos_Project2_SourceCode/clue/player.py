from .notes import Notes
from .constants import *

class Player:
    def __init__(self,  id:str,  color, row, col, hand:tuple, numplayers:int, ai: bool=False):
        self.id=id
        self.hand=hand
        self.notes=Notes(numplayers)
        self.row=row
        self.col=col
        self.color=color
        self.ai=ai
    def __str__(self):
        if self.ai:
            return (self.id + " AI")
        else:
            return (self.id + " Human")
        
    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.col*SQUARE_SIZE, self.row*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))

    def __repr__(self):
        return str(self.color)
    
    def move(self,row,col):
        self.row=row
        self.col=col
        

    def showHand(self,win):
        c=1
        for card in self.hand:
            card.draw(win, 10, c)
            c=c+2
        win.blit(FONT.render("'ENTER' to hide hand",True,BLACK, CARD), (10*SQUARE_SIZE, (c+2)*SQUARE_SIZE, SQUARE_SIZE*3,SQUARE_SIZE*3))
