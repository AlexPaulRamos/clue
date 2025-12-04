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

    def pickRoom(self,currentRoom):
        dist=10000000
        backupDist=10000000
        target=(0,0)
        backup=(0,0)
        for k,v in ENTRANCES.items(): #bot chooses the nearest room where it has no information
            if(k!="Pool" and k!=currentRoom):
                for coord in v:
                    d=(abs(self.row-coord[0])+abs(self.col-coord[1]))
                    if(0 in self.notes.roomsNotes[k]):
                        if d<dist:
                            dist=d
                            target=coord
                    if d<backupDist:  #if there is only 1 room that could be the solution and the bot is already in it
                        #we just go to the nearest room
                        backupDist=d
                        backup=coord
        if(target==(0,0)):
            return backup
        return target

    

