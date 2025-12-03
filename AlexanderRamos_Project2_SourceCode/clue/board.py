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
                    if(row==4 and col==4): # check if that room is also the entrance
                        self.board[row].append([Room(id="Kitchen",row=row,col=col,entrance=True,passage=None),0])
                    else:
                        self.board[row].append([Room(id="Kitchen",row=row,col=col,entrance=False,passage=None),0])
                elif (row<=5 and (8<=col<=14)):
                    if(row==4 and col ==8) or (row==5 and col ==9) or (row==4 and col ==14)or (row==5 and col ==13):
                        self.board[row].append([Room(id="Ballroom",row=row,col=col,entrance=True,passage=None),0])
                    else:
                        self.board[row].append([Room(id="Ballroom",row=row,col=col,entrance=False,passage=None),0])
                elif (row<=3 and 17<=col):
                    if(row==2 and col==17):
                        self.board[row].append([Room(id="Conservatory",row=row,col=col,entrance=True,passage=None),0])
                    else:
                        self.board[row].append([Room(id="Conservatory",row=row,col=col,entrance=False,passage=None),0])
                elif (7<=row<=13 and col<=7):
                    if(row==10 and col==7) or (row==13 and col==4):
                        self.board[row].append([Room(id="Dining Room",row=row,col=col,entrance=True,passage=None),0])
                    else:
                        self.board[row].append([Room(id="Dining Room",row=row,col=col,entrance=False,passage=None),0])
                elif (8<=row<=14 and 10<=col<=14):
                    if(row==8 and col ==12) or (row==11 and col ==10) or (row==11 and col ==14)or (row==14 and col ==12):
                        self.board[row].append([Room(id="Pool",row=row,col=col,entrance=True,passage=None),0])
                    else:
                        self.board[row].append([Room(id="Pool",row=row,col=col,entrance=False,passage=None),0])
                elif (6<=row<=10 and 17<=col):
                    if(row==6 and col==20) or (row==7 and col==17):
                        self.board[row].append([Room(id="Billiard Room",row=row,col=col,entrance=True,passage=None),0])
                    else:
                        self.board[row].append([Room(id="Billiard Room",row=row,col=col,entrance=False,passage=None),0])
                elif (12<=row<=16 and 16<=col):
                    if(row==14 and col==16) or (row==12 and col==19):
                        self.board[row].append([Room(id="Library",row=row,col=col,entrance=True,passage=None),0])
                    else:
                        self.board[row].append([Room(id="Library",row=row,col=col,entrance=False,passage=None),0])
                elif (17<=row and col<=6):
                    if(row==17 and col==5):
                        self.board[row].append([Room(id="Lounge",row=row,col=col,entrance=True,passage=None),0])
                    else:
                        self.board[row].append([Room(id="Lounge",row=row,col=col,entrance=False,passage=None),0])
                elif (16<=row and 9<=col<=14):
                    if(row==16 and 11<col<=12) or (row==19 and col==14):
                        self.board[row].append([Room(id="Hall",row=row,col=col,entrance=True,passage=None),0])
                    else:
                        self.board[row].append([Room(id="Hall",row=row,col=col,entrance=False,passage=None),0])
                elif (19<=row and 16<=col):
                    if(row==19 and col==17):
                        self.board[row].append([Room(id="Study",row=row,col=col,entrance=True,passage=None),0])
                    else:
                        self.board[row].append([Room(id="Study",row=row,col=col,entrance=False,passage=None),0])
                else:
                    #non room space has 0 in room
                    self.board[row].append([0,0])

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