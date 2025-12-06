import pygame
from clue.constants import *
from clue.board import Board
import random
from numpy import array_split
from clue.room import Room
from clue.card import Card
from clue.notes import Notes
from clue.player import Player
from queue import Queue


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
            

def checkMoveValid(current,target):
    if(target==None): #can't walk off map
        return False
    elif(target[1]!=0): #can't walk over players
            return False
    elif(current[0]!=0): #you are in a room
        inEntrance=current[0].entrance
        if (target[0]==0 and not inEntrance): #can't walk through walls out
            return False
    else:#you are not in a room
        if(target[0]!=0 and not target[0].entrance): #can't walk through walls in
            return False
    return True

def pathing(start,end,board):
    q = Queue()
    visited={start}
    q.put((start,[]))
    while(not q.empty()):
        n=q.get()
        row=n[0][0]
        col=n[0][1]
        
        if (n[0]==end):
            return(n[1])

        else:
            if checkMoveValid(board.getSpace(row,col),board.getSpace(row+1,col)) and not ((row+1,col) in visited):
                q.put(((row+1,col),n[1]+[pygame.K_DOWN]))
                visited.add((row+1,col))
            if checkMoveValid(board.getSpace(row,col),board.getSpace(row-1,col)) and not ((row-1,col) in visited):
                q.put(((row-1,col),n[1]+[pygame.K_UP]))
                visited.add((row-1,col))
            if checkMoveValid(board.getSpace(row,col),board.getSpace(row,col+1)) and not ((row,col+1) in visited):
                q.put(((row,col+1),n[1]+[pygame.K_RIGHT]))
                visited.add((row+1,col))
            if checkMoveValid(board.getSpace(row,col),board.getSpace(row,col-1)) and not ((row,col-1) in visited):
                q.put(((row,col-1),n[1]+[pygame.K_LEFT]))
                visited.add((row,col-1))
    return([])

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


def suggestion(room):
    #gather suggestion from consol
    #making a suggestion in pool will trigger the win_lose flag for final suggestion
    room=room
    win_lose=False
    if room=="Pool":
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

    return [room,suspect,weapon]

def refute(guess,player):
    ref=input(player.id +" Please refute: "+ str(guess)+" or type 'none' if you can't: ")
    while not((ref in guess) or ref=="none"):
        ref=input("Invalid choice. Please refute: "+ str(guess)+" or type 'none' if you can't: ")
    if(ref=="none"):
        return None
    else:
        return ref

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
            if currentPlayer.dead:
                continue
            #prompt to let new player roll
            pygame.display.set_caption("PLAYER "+str(turn+1)+": "+str(players[turn].id)+"'s TURN. PRESS ENTER TO ROLL THE DICE AND CONTINUE")
            run=wait()
            dice=random.randint(1,6)
            continue
            
        
        pygame.display.set_caption("PLAYER "+str(turn+1)+": "+str(currentPlayer.id)+" YOU HAVE **" +str(dice)+ "** SPACES LEFT (Arrow Keys to Movem, 'SPACE' to use passage) ('TAB' to View hand)")
        currentSpace=board.getSpace(currentPlayer.row,currentPlayer.col)
        #currentSpace[0] is Room or 0 if non room space
        #currentSpace[1] is Player or 0 if non player space
        if(currentSpace[0]!=0):
            inRoom=True
        else:
            inRoom=False

        if currentPlayer.ai:
            if inRoom:
                r=currentSpace[0].id
            else:
                r=0
            t=currentPlayer.pickRoom(r)
            path=pathing((currentPlayer.row,currentPlayer.col),t,board)

        else:
            path=[]
        for event in pygame.event.get()+path:
            if(dice==0):
                break   
            if(currentPlayer.ai):
                typecheck=pygame.KEYDOWN
            else:
                typecheck=event.type
            if typecheck == pygame.QUIT:
                #end game if you click exit
                run=False
            if typecheck == pygame.KEYDOWN:
                #movement controled by Arrow keys
                
                if(currentPlayer.ai):

                    keycheck=path.pop(0)
                else:
                    keycheck=event.key
                if keycheck==pygame.K_SPACE:
                    if(inRoom and currentSpace[0].passage!=None): #using passages
                        moveTo=findOpenSpace(board,LOCATIONS[currentSpace[0].passage][0],LOCATIONS[currentSpace[0].passage][1])
                        board.move(currentPlayer,moveTo[0],moveTo[1],WIN)
                        suggest=True
                if keycheck==pygame.K_TAB:
                    #h to show hand
                    currentPlayer.showHand(WIN)
                    pygame.display.flip()
                    run=wait()
                    board.draw(WIN)
                    pygame.display.flip()
                if keycheck in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                    if keycheck==pygame.K_LEFT:
                        targetR=currentPlayer.row
                        targetC=currentPlayer.col-1
                        target=board.getSpace(targetR,targetC)
                    elif keycheck==pygame.K_RIGHT:
                        targetR=currentPlayer.row
                        targetC=currentPlayer.col+1
                        target=board.getSpace(targetR,targetC)
                    elif keycheck==pygame.K_UP:
                        targetR=currentPlayer.row-1
                        targetC=currentPlayer.col
                        target=board.getSpace(targetR,targetC)
                    elif keycheck==pygame.K_DOWN:
                        targetR=currentPlayer.row+1
                        targetC=currentPlayer.col
                        target=board.getSpace(targetR,targetC)
                    if(checkMoveValid(currentSpace,target)):
                        #check if valid movement
                        if(not inRoom and target[0]!=0 and target[0].entrance):
                            #if you enter a room trigger suggest flag
                            suggest=True
                        if(not inRoom or target[0]==0): #it uses movement to move outside of rooms
                            dice=dice-1
                        board.move(currentPlayer,targetR,targetC,WIN)
                    if(currentPlayer.ai):#Make agent movement look more human
                        pygame.time.delay(800)
                        board.draw(WIN)
                        pygame.display.flip()

                if(suggest): 
                    #the suggest flag has been triggered
                    pygame.display.set_caption("PLAYER "+str(turn+1)+": "+str(players[turn].id)+" MAKE A SUGGESTION IN CONSOL")
                    board.draw(WIN)
                    currentPlayer.showHand(WIN)
                    pygame.display.flip()
                    guess=suggestion(target[0].id)#prompt suggestion
                    board.draw(WIN)
                    pygame.display.flip()
                    
                    guessRoom=guess[0]
                    guessSuspect=guess[1]
                    guessWeapon=guess[2]
                    if target[0].id=="Pool": #Suggestions made in the pool are attempts to win
                        if guessRoom==roomSolution and guessSuspect==suspectSolution and guessWeapon==weaponSolution:
                            winmessage=(currentPlayer.id +"WINS!!! "+suspectSolution +" used the "+ weaponSolution+" in the "+roomSolution)
                            WIN.blit(FONT.render(winmessage,True,WHITE), (LOCATIONS['Pool'][1]*SQUARE_SIZE, LOCATIONS['Pool'][0]*SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))
                            board.draw(WIN)
                            pygame.display.flip()
                            run=False
                            wait()
                        else: #remove failed players
                            currentPlayer.dead=True    
                    else:
                        #move player to room/unblock door
                        moveTo=findOpenSpace(board,LOCATIONS[guessRoom][0],LOCATIONS[guessRoom][1])
                        board.move(currentPlayer,moveTo[0],moveTo[1],WIN)
                        board.draw(WIN)
                        pygame.display.flip()
                        for p in players:
                            #check if suggested character is a player and teleport them if they are
                            if p.id==guessSuspect:
                                moveTo=findOpenSpace(board,LOCATIONS[guessRoom][0],LOCATIONS[guessRoom][1])
                                board.move(p,moveTo[0],moveTo[1],WIN)
                        i=players.index(currentPlayer)
                        if(i==numplayers-1):
                            nextI=0
                        else:
                            nextI=i+1
                        refuteCard=None
                        while nextI!=i:
                            nextplayer=players[nextI]
                            board.draw(WIN)
                            pygame.display.flip()
                            pygame.display.set_caption(nextplayer.id + " must refute: " + str(guess) +" press enter then use consol")
                            board.draw(WIN)
                            pygame.display.flip()
                            run=wait()
                            if(nextplayer.ai):
                                for card in nextplayer.hand:
                                    if card.id in guess:
                                        refuteCard=card.id
                                        break
                            else:
                                board.draw(WIN)
                                nextplayer.showHand(WIN)
                                pygame.display.flip()
                                refuteCard=refute(guess,nextplayer)
                                if not refuteCard==None:
                                    break
                            if(nextI==numplayers-1):
                                nextI=0
                            else:
                                nextI=nextI+1
                        board.draw(WIN)
                        pygame.display.flip()
                        if refuteCard==None:
                            pygame.display.set_caption("no one could prove you wrong....")
                            run=wait()
                        else:
                            pygame.display.set_caption(nextplayer.id + " showed you " +refuteCard)
                            run=wait()

                    dice=0#suggesting ends movement
                    suggest=False

        board.draw(WIN)
        pygame.display.flip()
    pygame.quit()

if __name__=='__main__':
    main()