from .notes import Notes
from .constants import *


class Player:
    def __init__(self,  id:str,  color, row, col, hand:tuple, ai: bool=False):
        self.id=id
        self.hand=hand
        self.notes=Notes()
        self.row=row
        self.col=col
        self.color=color
        self.ai=ai
        self.dead=False
        self.noteHand()
    def __str__(self):
            return self.id
        
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
        if(not (None in self.getSolution())):#we Know the solution. Go to Pool
            for coord in ENTRANCES["Pool"]:
                    d=(abs(self.row-coord[0])+abs(self.col-coord[1]))
                    if d<dist:
                        dist=d
                        target=coord
            return target

        for k,v in ENTRANCES.items(): #bot chooses the nearest room where it has no information
            if(k!="Pool" and k!=currentRoom):
                for coord in v:
                    d=(abs(self.row-coord[0])+abs(self.col-coord[1]))
                    if(self.notes.roomsNotes[k]==[0,0]):
                        if d<dist:
                            dist=d
                            target=coord
                    if d<backupDist:  #if there is only 1 room that could be the solution and the bot is already in it
                        #we just go to the nearest room
                        backupDist=d
                        backup=coord
        if(target==(0,0)):
            target = backup
        fname=self.id+".txt"
        with open(fname, 'a') as file:    
            file.write("Targeting: "+str((self.row,self.col))+" to "+str(target))
            file.write("\n********\n")
        return target

    def add(self,key,value):
        if not(key in self.hand): #no need to track things already known
            self.notes.add(key,value,False)
        if self.ai:
            fname=self.id+".txt"
            with open(fname, 'a') as file:
                file.write("Learned "+key + " is "+str(value)+"\n")
                file.write(str(self.notes)+"\n")
                file.write(str(self.getSolution())+"\n")
                file.write("********************\n")

    def ruleOut(self,key,player):
        self.notes.ruleOut(key,player)
        if self.ai:
            fname=self.id+".txt"
            with open(fname, 'a') as file:
                file.write("Learned "+player + " does not have "+str(key)+"\n")
                file.write(str(self.notes)+"\n")
                file.write(str(self.getSolution())+"\n")
                file.write("********************\n")

    def getSolution(self):
        return self.notes.getSolution()
    
    def noteHand(self):
        for card in self.hand:
            self.notes.add(card.id,1,True)

    def makeSuggestion(self):
        sug=self.notes.bestSuggest()
        fname=self.id+".txt"
        
        with open(fname, 'a') as file:    
            file.write("I want to Know: "+str(sug))
            file.write("\n********\n")
        return sug

    def fillPossible(self,players):
        self.notes.fillPossible(set(map(str,players)))
        fname=self.id+".txt"
        with open(fname, 'w') as file:
            file.write("starting hand \n")
            for c in self.hand:
                file.write(str(c) +"\n")
            file.write(str(self.notes)+"\n")
            file.write(str(self.getSolution())+"\n")
            file.write("********************\n")
