import random
class Notes:
    def __init__(self):
        #notes are kept as 3 dictionaries (suspects, weapons, rooms)
        #the Key is the item, and the value is a list with information
                #the first slot in the list is whether or not this player has the card
                #the second slot is whether or not it has found another player with the card
                # [0,0] did not start with card and does not know who does
                # [0,1] started with the card
                # [1,0] found someone with the card
                # [-1,0] we asked for the card and no one has it

                #if the [0] is negative then we know the card is the solution
                #if the sum of all pairs in a dictionary is len-1 then can infer [0,0] is [-1,0]

        self.suspectsNotes={"Miss Scarlett":[0,0],"Colonel Mustard":[0,0],"Mrs. White":[0,0],"Reverend Green":[0,0],"Mrs. Peacock":[0,0],"Professor Plum":[0,0]}
        self.weaponsNotes={"Candlestick":[0,0],"Dagger":[0,0],"Lead Pipe":[0,0],"Revolver":[0,0],"Rope":[0,0],"Wrench":[0,0]}
        self.roomsNotes={"Hall":[0,0],"Lounge":[0,0],"Dining Room":[0,0],"Kitchen":[0,0],"Ballroom":[0,0],"Conservatory":[0,0],"Billiard Room":[0,0],"Library":[0,0],"Study":[0,0]}
        self.book=[self.roomsNotes,self.suspectsNotes,self.weaponsNotes]

        #these dictionaries handle possible outcomes
        self.suspectsPossible={"Miss Scarlett":{},"Colonel Mustard":{},"Mrs. White":{},"Reverend Green":{},"Mrs. Peacock":{},"Professor Plum":{}}
        self.weaponsPossible={"Candlestick":{},"Dagger":{},"Lead Pipe":{},"Revolver":{},"Rope":{},"Wrench":{}}
        self.roomsPossible={"Hall":{},"Lounge":{},"Dining Room":{},"Kitchen":{},"Ballroom":{},"Conservatory":{},"Billiard Room":{},"Library":{},"Study":{}}
        self.bookPossible=[self.roomsPossible,self.suspectsPossible,self.weaponsPossible]
        
        self.solution=[None,None,None] #[room,suspect,weapon]

    def fillPossible(self,players): #set up potential players that have the card 
        for page in range(3):
            for key in self.bookPossible[page].keys():
                if(self.book[page][key]!=[0,1]): #if you don't have it, then anyone could have it
                    self.bookPossible[page][key]=players
                else:
                    self.bookPossible[page][key]={"Mine"}


    def __str__(self): 
        return(str(self.roomsNotes)+'\n'+str(self.roomsPossible)+'\n'+str(self.suspectsNotes)+'\n'+str(self.suspectsPossible)+'\n'+str(self.weaponsNotes)+'\n'+str(self.weaponsPossible))
    
    def ruleOut(self,key,player):
        i=-1
        for page in self.bookPossible:
            i=i+1
            if key in page.keys():
                if(player in page[key]):
                    if(self.book[i][key]==[0,0]):
                        page[key].remove(player)
                        page=self.inferProb(page,i)
    
    
    def add(self,key,value,isMine=False):
        i=-1
        for page in self.book:
            i=i+1
            if key in page.keys():
                page[key][isMine]=value
                if(value==-1):
                    self.solution[i]=key
                else:
                    page=self.infer(page,i)

    def infer(self,page,i):  #i is for [room,suspect,weapon]
        if(sum(sum(page.values(),[]))==(len(page)-1)): #if the sum of all pairs in a dictionary is len-1
            #then can infer [0,0] is [-1,0]
            key=list(page.keys())[list(page.values()).index([0,0])]
            page[key]=[-1,0]
            self.solution[i]=key

    def inferProb(self,page,i):
        for key in page:  #if their is only one person
            if len(self.bookPossible[i][key])==0:
                self.add(key,-1,False)
        return page
    
    def getSolution(self):
        return self.solution
    
    def bestSuggest(self):
        bestRoom="place"
        bestSuspect="place"
        bestWeapon="place"

        #maximize the information recieved 
        #minimize information given
        #[0,0] is best because it has potential to gain information
        #[0,1]/[-1,0] if there is not unknowns it is better to randomly choose either your 
        ####choose best room####
        score=-10000
        for key in self.roomsNotes.keys():  
            value=self.roomsNotes[key]
            if(value==[0,0]):
                tempScore=3
            elif(value==[0,1] or value==[-1,0]):
                tempScore=random.randint(1,2)
            else:
                tempScore=0
            if tempScore>score:
                bestRoom=key
                score=tempScore
        ####choose best suspect####
        score=-10000
        for key in self.suspectsNotes.keys():
            value=self.suspectsNotes[key]
            if(value==[0,0]):
                tempScore=3
            elif(value==[0,1]):
                tempScore=2
            elif(value==[-1,0]):
                tempScore=1
            else:
                tempScore=0
            if tempScore>score:
                bestSuspect=key
                score=tempScore
        ####choose best weapon####
        score=-10000
        for key in self.weaponsNotes.keys():
            value=self.weaponsNotes[key]
            if(value==[0,0]):
                tempScore=3
            elif(value==[0,1]):
                tempScore=2
            elif(value==[-1,0]):
                tempScore=1
            else:
                tempScore=0
            if tempScore>score:
                bestWeapon=key
                score=tempScore
        return [bestRoom,bestSuspect,bestWeapon]