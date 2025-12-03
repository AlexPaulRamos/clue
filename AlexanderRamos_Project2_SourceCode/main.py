import pygame
from clue.constants import *
from clue.board import Board
import random
from numpy import array_split
from clue.room import Room
from clue.card import Card
from clue.notes import Notes
from clue.player import Player



#game refresh speed setup
FPS=60
clock= pygame.time.Clock()
#solution setup
suspectSolution="no solution"
weaponSolution="no solution"
roomSolution="no solution"


def wait():
    #for when the game needs to pause
    #no key inputs unless close game or enter
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    return True
                
def findOpenSpace(board,row,col):
    #used for teleporting to rooms
    #given a row and col
    #cycle through nearby room spaces to find an open one
    shiftC=0
    shiftR=0
    while True:
        found=board.getSpace(row+shiftR,col+shiftC)
        if found==None or found[0]==0:
            shiftR=shiftR+1
            shiftC=0
        else:
            if found[1]==0:
                return (row+shiftR,col+shiftC)
            else:
                shiftC=shiftC+1

def suggestion(room,WIN,board):
    #gather suggestion from consol
    #making a suggestion in pool will trigger the win_lose flag for final suggestion
    room=room
    win_lose=False
    if room=="Pool":
        win_lose=True
        room=input("What do you think? "+str(ROOM)+ ": ")
        while room not in ROOM:
            suspect=input("Invalid choice. What do you think? "+str(ROOM)+ ": ")
    else:
        suspect=input("Who do you suspect? "+str(SUS)+ ": ")
        while suspect not in SUS:
            suspect=input("Invalid choice. Who do you suspect? "+str(SUS)+ ": ")
        weapon=input("What weapon do you suspect? "+str(WEP)+ ": ")
        while weapon not in WEP:
            weapon=input("Invalid choice. What weapon do you suspect? "+str(WEP)+ ": ")

    return [room,suspect,weapon,win_lose]


def main():
    #all the setup stuff

    ########select number of players
    numplayers=input("Please select the number of players (3-6): ")
    while(numplayers not in ("3","4","5","6")):
        numplayers=input("Sorry, not a valid selection. Please select the number of players (3-6): ")
    numplayers=int(numplayers)
    ###############set up the deck and draw solution
    deck=[]
    suspects=list(SUS)
    weapons=list(WEP)
    rooms=list(ROOM)
    suspectSolution=suspects.pop(random.randrange(len(suspects)))
    weaponSolution=weapons.pop(random.randrange(len(weapons)))
    roomSolution=rooms.pop(random.randrange(len(rooms)))

    #########create deck
    for suspect in suspects:
        deck.append(Card(suspect,"Suspect"))
    for weapon in weapons:
        deck.append(Card(weapon,"Weapon"))
    for room in rooms:
        deck.append(Card(room,"Room"))
    #################shuffle and split cards into hands
    random.shuffle(deck)
    hands=array_split(deck,numplayers)
    ######generate players
    playerCounter=1
    availableChr=list(SUS)
    players=[]
    for hand in hands:
        #choose if player is AI controled
        #TODO add AI
        choiceAI=input("Select if player "+str(playerCounter)+" will be controlled by AI? (Y/N): ").lower()
        while choiceAI not in ('y','n','yes','no'):
            choiceAI=input("Sorry, please limit respnse to 'y'/'n' or 'yes'/'no'. Select if player "+str(playerCounter)+" will be controlled by AI? (Y/N): ").lower()
        if choiceAI in ('y','yes'):
            #if AI choose random character 
            choiceC=availableChr.pop(random.randrange(len(availableChr)))
            ai=True
        else:
            ai=False
            #choose player character
            choiceC=input("Player "+str(playerCounter)+" choose your character (" +str(availableChr)+"): ")
            while choiceC not in availableChr:
                choiceC=input("Sorry Character not available, Player "+str(playerCounter)+" choose your character ("+str(availableChr)+"): ")
            availableChr.remove(choiceC)

        #initialize starting locations
        if choiceC=="Miss Scarlett":
            players.append(Player(id=choiceC,color=SCARLET,row=21,col=8,hand=hand,numplayers=numplayers,ai=ai))
        elif choiceC=="Colonel Mustard":
            players.append(Player(id=choiceC,color=MUSTARD,row=14,col=0,hand=hand,numplayers=numplayers,ai=ai))
        elif choiceC=="Reverend Green":
            players.append(Player(id=choiceC,color=GREEN,row=5,col=0,hand=hand,numplayers=numplayers,ai=ai))
        elif choiceC=="Mrs. White":
            players.append(Player(id=choiceC,color=WHITE,row=0,col=7,hand=hand,numplayers=numplayers,ai=ai))
        elif choiceC=="Mrs. Peacock":
            players.append(Player(id=choiceC,color=PEACOCK,row=4,col=21,hand=hand,numplayers=numplayers,ai=ai))
        elif choiceC=="Professor Plum":
            players.append(Player(id=choiceC,color=PLUM,row=18,col=21,hand=hand,numplayers=numplayers,ai=ai))

        playerCounter +=1



    #create blank gameboard
    WIN=pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Clue")

    run=True
    board=Board(players)
    turnCount=-1
    turn=-1
    dice=0
    currentPlayer=None
    suggest=False
    

    while run:
        #main game loop
        clock.tick(FPS)
        board.draw(WIN)
        pygame.display.flip()

        if(dice==0):
            #turn order changes when out of moves
            turnCount=turnCount+1
            turn=(len(players)+turnCount)%len(players)
            currentPlayer=players[turn]
            #prompt to let new player roll
            pygame.display.set_caption("PLAYER "+str(turn+1)+": "+str(players[turn].id)+"'s TURN. PRESS ENTER TO ROLL THE DICE AND CONTINUE")
            run=wait()
            dice=random.randint(1,6)
            continue
            
        
        pygame.display.set_caption("PLAYER "+str(turn+1)+": "+str(currentPlayer.id)+" YOU HAVE **" +str(dice)+ "** SPACES LEFT (Arrow Keys to Move) ('H' to View hand)")
        currentSpace=board.getSpace(currentPlayer.row,currentPlayer.col)
        #currentSpace[0] is Room or 0 if non room space
        #currentSpace[1] is Player or 0 if non player space
        if(currentSpace[0]!=0):
            inRoom=True
            inEntance=currentSpace[0].entrance
        else:
            inRoom=False
            inEntance=False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #end game if you click exit
                run=False
            if event.type == pygame.KEYDOWN:
                #movement controled by Arrow keys
                if event.key==pygame.K_h:
                    #h to show hand
                    currentPlayer.showHand(WIN)
                    pygame.display.flip()
                    run=wait()
                    board.draw(WIN)
                    pygame.display.flip()
                if event.key==pygame.K_LEFT:
                    targetR=currentPlayer.row
                    targetC=currentPlayer.col-1
                    target=board.getSpace(targetR,targetC)
                    if(target!=None and not inRoom and target[1]==0 and (target[0]==0 or target[0].entrance)):
                        #check if valid movement while outside of room
                        if(target[0]!=0 and target[0].entrance):
                            #if you enter a room trigger suggest flag
                            suggest=True
                        board.move(currentPlayer,targetR,targetC,WIN)
                        dice=dice-1
                    elif(target!=None and inRoom and target[0]!=0 and target[1]==0):
                         #movement in a room does not require dice movement
                         board.move(currentPlayer,targetR,targetC,WIN)
                    elif (target!=None and inRoom and target[0]==0 and inEntance and target[1]==0):
                        #leaving a room
                        board.move(currentPlayer,targetR,targetC,WIN)
                        dice=dice-1
                elif event.key==pygame.K_RIGHT:
                    targetR=currentPlayer.row
                    targetC=currentPlayer.col+1
                    target=board.getSpace(targetR,targetC)
                    if(target!=None and not inRoom and target[1]==0 and  (target[0]==0 or target[0].entrance)):
                        if(target[0]!=0 and target[0].entrance):
                            suggest=True
                        board.move(currentPlayer,targetR,targetC,WIN)
                        dice=dice-1
                    elif(target!=None and inRoom and target[0]!=0 and target[1]==0):
                         board.move(currentPlayer,targetR,targetC,WIN)
                    elif (target!=None and inRoom and target[0]==0 and inEntance and target[1]==0):
                        board.move(currentPlayer,targetR,targetC,WIN)
                        dice=dice-1
                elif event.key==pygame.K_UP:
                    targetR=currentPlayer.row-1
                    targetC=currentPlayer.col
                    target=board.getSpace(targetR,targetC)
                    if(target!=None and not inRoom and target[1]==0 and  (target[0]==0 or target[0].entrance)):
                        if(target[0]!=0 and target[0].entrance):
                            suggest=True
                        board.move(currentPlayer,targetR,targetC,WIN)
                        dice=dice-1
                    elif(target!=None and inRoom and target[0]!=0 and target[1]==0):
                         board.move(currentPlayer,targetR,targetC,WIN)
                    elif (target!=None and inRoom and target[0]==0 and inEntance and target[1]==0):
                        board.move(currentPlayer,targetR,targetC,WIN)
                        dice=dice-1
                elif event.key==pygame.K_DOWN:
                    targetR=currentPlayer.row+1
                    targetC=currentPlayer.col
                    target=board.getSpace(targetR,targetC)
                    if(target!=None and not inRoom and target[1]==0 and (target[0]==0 or target[0].entrance)):
                        if(target[0]!=0 and target[0].entrance):
                            suggest=True
                        board.move(currentPlayer,targetR,targetC,WIN)
                        dice=dice-1
                    elif(target!=None and inRoom and target[0]!=0 and target[1]==0):
                         board.move(currentPlayer,targetR,targetC,WIN)
                    elif (target!=None and inRoom and target[0]==0 and inEntance and target[1]==0):
                        board.move(currentPlayer,targetR,targetC,WIN)
                        dice=dice-1


                if(suggest): 
                    #the suggest flag has been triggered
                    pygame.display.set_caption("PLAYER "+str(turn+1)+": "+str(players[turn].id)+" MAKE A SUGGESTION IN CONSOL")
                    board.draw(WIN)
                    pygame.display.flip()
                    #prompt suggestion
                    guess=suggestion(target[0].id,WIN,board)
                    guessRoom=guess[0]
                    guessSuspect=guess[1]
                    guessWeapon=guess[2]
                    #move player to room/unblock door
                    moveTo=findOpenSpace(board,LOCATIONS[guessRoom][0],LOCATIONS[guessRoom][1])
                    board.move(currentPlayer,moveTo[0],moveTo[1],WIN)
                    for p in players:
                        #check if suggested character is a player and teleport them if they are
                        if p.id==guessSuspect:
                            moveTo=findOpenSpace(board,LOCATIONS[guessRoom][0],LOCATIONS[guessRoom][1])
                            board.move(p,moveTo[0],moveTo[1],WIN)
                    dice=0#suggesting ends movement
                    suggest=False

        board.draw(WIN)
        pygame.display.flip()
    pygame.quit()

if __name__=='__main__':
    main()