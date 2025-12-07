from .constants import *
class Card:
    def __init__(self, id, clueType):
        self.id=id
        self.clueType=clueType
    def __str__(self):
        return (self.clueType+': ' +self.id)
    
    def draw(self, win, row, col):
        win.blit(FONT.render(str(self),True,BLACK, CARD), (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE*3,SQUARE_SIZE*3))

    def __eq__(self, value):
        if type(value)==str:
            return value==self.id
        return False