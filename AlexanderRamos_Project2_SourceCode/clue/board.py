from .constants import *
from .room import *
from .player import *
class Board:
    def __init__(self,players):
        self.board=[]
        self.characters=None
        self.createBoard(players)

    def draw_grid(self,win): #creates blank gride
        win.fill(GREY) 
        for row in range(ROWS):
            for col in range(row % 2,ROWS,2):
                pygame.draw.rect(win,DGREY,(row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))

    def createBoard(self,players):
        #board is technically a 3D list but is easier to think of as 2D list of spaces
        #space=board[row][col] NOT board[x][y]
            #space[0] is the Room data or 0 if not a room
            #space[1] is the Player data or 0 if no player on that space
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if (row<=4 and col <=5): #first check if region is part of a room
                    self.board[row].append([Room(id="Kitchen",row=row,col=col,entrance=False,passage="Study"),0])
                elif (row<=5 and (8<=col<=14)):
                    self.board[row].append([Room(id="Ballroom",row=row,col=col,entrance=False,passage=None),0])
                elif (row<=3 and 17<=col):
                    self.board[row].append([Room(id="Conservatory",row=row,col=col,entrance=False,passage="Lounge"),0])
                elif (7<=row<=13 and col<=7):
                    self.board[row].append([Room(id="Dining Room",row=row,col=col,entrance=False,passage=None),0])
                elif (8<=row<=14 and 10<=col<=14):
                    self.board[row].append([Room(id="Pool",row=row,col=col,entrance=False,passage=None),0])
                elif (6<=row<=10 and 17<=col):
                    self.board[row].append([Room(id="Billiard Room",row=row,col=col,entrance=False,passage=None),0])
                elif (12<=row<=16 and 16<=col):
                    self.board[row].append([Room(id="Library",row=row,col=col,entrance=False,passage=None),0])
                elif (17<=row and col<=6):
                    self.board[row].append([Room(id="Lounge",row=row,col=col,entrance=False,passage="Conservatory"),0])
                elif (16<=row and 9<=col<=14):
                    self.board[row].append([Room(id="Hall",row=row,col=col,entrance=False,passage=None),0])
                elif (19<=row and 16<=col):
                    self.board[row].append([Room(id="Study",row=row,col=col,entrance=False,passage="Kitchen"),0])
                else:
                    #non room space has 0 in room
                    self.board[row].append([0,0])

        for v in ENTRANCES.values():#add entrances
            for coord in v:
                self.board[coord[0]][coord[1]][0].entrance=True

        for player in players: #add players onto board
            self.board[player.row][player.col][1]=player

    def draw(self,win):
        self.draw_grid(win)  
        for row in range(ROWS):
            for col in range(COLS):
                room=self.board[row][col][0]
                if room!=0:
                    room.draw(win) #draw rooms over grid
                player=self.board[row][col][1]
                if player!=0:
                    player.draw(win) #draw players over grid

        for locationKey in LOCATIONS: #dray room labels
            if locationKey == "Kitchen":
                win.blit(SUBFONT.render("Passage to Study",True,WHITE), (LOCATIONS[locationKey][1]*SQUARE_SIZE, (LOCATIONS[locationKey][0]+1)*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))
            if locationKey =="Study":
                win.blit(SUBFONT.render("Passage to Kitchen",True,WHITE), (LOCATIONS[locationKey][1]*SQUARE_SIZE, (LOCATIONS[locationKey][0]+1)*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))
            if locationKey =="Lounge":
                win.blit(SUBFONT.render("Passage to Conservatory",True,WHITE), (LOCATIONS[locationKey][1]*SQUARE_SIZE, (LOCATIONS[locationKey][0]+1)*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))
            if locationKey =="Conservatory":
                win.blit(SUBFONT.render("Passage to Lounge",True,WHITE), (LOCATIONS[locationKey][1]*SQUARE_SIZE, (LOCATIONS[locationKey][0]+1)*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))
            win.blit(FONT.render(locationKey,True,WHITE), (LOCATIONS[locationKey][1]*SQUARE_SIZE, LOCATIONS[locationKey][0]*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))
     

    def move(self, player, row,col,win):
        self.board[player.row][player.col][1], self.board[row][col][1] = self.board[row][col][1], self.board[player.row][player.col][1]
        player.move(row,col)
        self.draw(win)

    def getSpace(self, row, col):
        if(row in range(ROWS) and col in range(COLS)):
            return self.board[row][col]
        else:
            return None
        


