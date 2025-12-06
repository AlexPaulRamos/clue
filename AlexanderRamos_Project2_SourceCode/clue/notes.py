class Notes:
    def __init__(self, numPlayers):
        #notes are kept as 3 dictionaries (suspects, weapons, rooms)
        #the Key is the item, and the value is a list with information
                #each place in the list stands for a player
                #0 means whether or not they have a card is unknown
                #1 means they must have the card
                #-1 means they must not have the card
            #ex 'Colonel_Mustard':[0,-1,0,0]
                    #player 1,3,4 may have the Cononel_Mustard card
                    #player 2 can't have it
        self.suspectsNotes={"Miss Scarlett":[0]*numPlayers,"Colonel Mustard":[0]*numPlayers,"Mrs. White":[0]*numPlayers,"Reverend Green":[0]*numPlayers,"Mrs. Peacock":[0]*numPlayers,"Professor Plum":[0]*numPlayers}
        self.weaponsNotes={"Candlestick":[0]*numPlayers,"Dagger":[0]*numPlayers,"Lead Pipe":[0]*numPlayers,"Revolver":[0]*numPlayers,"Rope":[0]*numPlayers,"Wrench":[0]*numPlayers}
        self.roomsNotes={"Hall":[0]*numPlayers,"Lounge":[0]*numPlayers,"Dining Room":[0]*numPlayers,"Kitchen":[0]*numPlayers,"Ballroom":[0]*numPlayers,"Conservatory":[0]*numPlayers,"Billiard Room":[0]*numPlayers,"Library":[0]*numPlayers,"Study":[0]*numPlayers}

    def __str__(self): 
        return(str(self.suspectsNotes)+'\n'+str(self.weaponsNotes)+'\n'+str(self.roomsNotes))