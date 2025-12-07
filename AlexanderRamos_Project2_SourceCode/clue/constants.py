import pygame


SUS=("Miss Scarlett","Colonel Mustard","Mrs. White","Reverend Green","Mrs. Peacock","Professor Plum")
WEP=("Candlestick","Dagger","Lead Pipe","Revolver","Rope","Wrench")
ROOM=("Hall","Lounge","Dining Room","Kitchen","Ballroom","Conservatory","Billiard Room","Library","Study")


pygame.init()
w= pygame.display.Info().current_h-100
h= pygame.display.Info().current_h-100

pygame.quit()
ROWS=22
COLS=22
WIDTH=w-(w%COLS)
HEIGHT=h-(h%ROWS)
SQUARE_SIZE=WIDTH//COLS

#coordinates of each room, (row,col)  NOT (x,y)
LOCATIONS={'Kitchen':(2,1),"Ballroom":(2,10),"Conservatory":(1,18),"Dining Room":(10,1),"Pool":(11,12),
           "Billiard Room":(8,18),"Library":(14,18),"Lounge":(19,2),"Hall":(19,11),"Study":(20,18)}

ENTRANCES={'Kitchen':[(4,4)],"Ballroom":[(4,8),(5,9),(5,13),(4,14)],"Conservatory":[(2,17)],"Dining Room":[(10,7),(13,4)],"Pool":[(8,12),(11,10),(11,14),(14,12)],
           "Billiard Room":[(6,20),(7,17)],"Library":[(14,16),(12,19)],"Lounge":[(17,5)],"Hall":[(16,11),(16,12),(19,14)],"Study":[(19,17)]}

#rgb
WHITE=(255,255,255)
MUSTARD=(247, 216, 114)
SCARLET=(194, 10, 56)
PLUM=(95, 10, 161)
PEACOCK=(79, 127, 232)
GREEN=(0, 140, 30)
GREY=(120, 120, 120)
DGREY=(69, 69, 69)
BROWN=(79, 64, 23)
CARD=(159, 140, 173)
BLACK=(0,0,0)
pygame.font.init()
FONT=pygame.font.SysFont('Arial',(3*SQUARE_SIZE)//4)
SUBFONT=pygame.font.SysFont('Arial',(SQUARE_SIZE)//2)