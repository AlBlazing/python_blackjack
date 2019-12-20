from random import randint
import time
import os

suits  = ["Hearts","Diamonds","Clubs","Spades"]
values = ["A","2","3","4","5","6","7","8","9","X","J","Q","K"]

# --- function that returns a random card --- #
def giveCard():
    value = values[randint(0, 12)] #randomly pics a value
    suit = suits[randint(0, 3)]    #randomly pics a suit
    card = suit+value
    # checking that the card is not already drawn
    while card in hand:
        value = values[randint(0, 12)]
        suit = suits[randint(0, 3)]
        card = suit+value
    return card

# --- initializing the game --- #
def startGame(first):
    if first:
        # giving first 2 cards to player
        for i in range(2):
            card = giveCard()
            hand.append(card)
        # giving first 2 cards to the house
        for i in range(2):
            card = giveCard()
            house.append(card)
        displayTable()
        
# --- reset the game --- #
def reset():
    while len(hand)>0:
        del hand[0]
    while len(house)>0:
        del house[0]
    global first
    first = 1
    global bust, bustH, unveil
    bust, bustH, unveil = 0, 0, 0
    
# --- checking if you busted --- #
def checkHand(hand):
    aces = 0
    value = 0
    for card in hand:
        if ('2' <= card[-1]) and (card[-1] <= '9'):
            value += int(card[-1]) #add the value of the number
        elif card[-1] == 'A':
            value += 1
            aces += 1
        else:
            value += 10
    for i in range(aces):
        if value+10<=21:
            value += 10   #if it can, count Ace as 11
    return value

# --- The player chooses what to do --- #
def playerMove():
    global play
    c = input("Another card (Y/N)? ")
    if c == 'Y' or c == 'y':
        card = giveCard()
        hand.append(card)
        displayTable()
    else:
        play = 0

# --- house playing --- #
"""
-The house is forced to get another card if the value is
lower than 17 (Blackjack rules)
"""
def houseMove():
    global playH
    if (checkHand(house)<=17 and checkHand(house)<checkHand(hand)) and checkHand(house)<21:
        card = giveCard()
        house.append(card)
        displayTable()
    else:
        playH = 0
        
# --- busted --- #
def busted():
    global play, bust
    play = 0
    bust = 1
    
def houseBusted():
    global playH, bustH
    playH = 0
    bustH = 1
            
# --- print values and hands --- #
def displayTable():
    global play
    h = []
    h.append(house[0])
    clear = lambda: os.system('cls' if os.name=='nt' else 'clear')
    global unveil
    if play:
        clear()
        print("+---")
        print("| House hand: ['"+str(house[0])+"', COVERED]")
        #print("| House hand: "+str(house)) --> Debug to check house hand
        print("| Your hand:  "+str(hand))
        print("+---")
        print("| House value: "+str(checkHand(h)))
        print("| Your value:  "+str(checkHand(hand)))
        print("+---")
    else:
        if unveil:
            time.sleep(2)
        clear()
        print("+---")
        print("| House hand: "+str(house))
        print("| Your hand:  "+str(hand))
        print("+---")
        print("| House value: "+str(checkHand(house)))
        print("| Your value:  "+str(checkHand(hand)))
        print("+---")
        unveil = 1
        
# --- printing results --- #
def results():
    global play, playH
    global game
    global bust, bustH
    global money, bet
    
    if bust:
        print("| You busted.")
        money -= bet
        lost = int(stats[1]) - bet
        stats[1] = str(lost)
    elif bustH:
        print("| House busted.")
        money += bet
        won = int(stats[0]) + bet
        stats[0] = str(won)
    elif checkHand(hand) < checkHand(house):
        print("| House beats you.")
        money -= bet
        lost = int(stats[1]) - bet
        stats[1] = str(lost)
    elif checkHand(hand) > checkHand(house):
        print("| You beat the house.")
        money += bet
        won = int(stats[0]) + bet
        stats[0] = str(won)
    elif checkHand(hand) == checkHand(house):
        print("| Tie.")
    print("+---")
    updateStat("stats.txt")
    x = input("Want to play again (Y/N)? ")
    if x == 'Y' or x == 'y':
        play, playH = 1, 1
    else:
        game = 0
        
# --- bet --- #
def betting():
    global bet, money
    printBalance()
    x = int(input("| Place your bet: "))
    while (money-x < 0):
        print("+---")
        print("| Your balance is lower than your bet.")
        x = int(input("| Place your bet: "))
    bet = x
    
# --- print balance --- #
def printBalance():
    global money
    balance="| Balance: "+str(money)+"$ |"
    decoration="+"
    for i in range(len(balance)-2):
        decoration+="-"
    decoration+="+"
    print(decoration+"\n"+balance+"\n"+decoration)
    
"""
# --- graphic functions --- #
def init(w, h):
    setup(w, h, None, None)
    bgpic("assets/bg.gif")
    
    # Load card pics
    for suit in suits:
        for value in values:
            addshape("assets/cards/card"+suit+value+".gif")
    addshape("assets/cards/cardBack_blue5.gif")
            
def drawCard(w, h, card, cardNo):
    penup()
    hideturtle()
    x = (-w // 4) + cardNo * 150
    y = h
    speed(0)
    goto(x, y) 
    speed(6)
    shape("assets/cards/cardBack_blue5.gif")
    showturtle()
    x = (-w // 4) + cardNo * 150
    y = -h // 4
    #speed(0)
    goto(x, y)
    pendown()
    delay(100)
    shape("assets/cards/card"+card+".gif")
    stamp()
# ------------------------- #
"""
# --- get game stats from file --- #
def getData(file):
    global money
    for line in open(file):
        data = line.replace("\n", "").split(":")
        if data[0]=="Wallet":
            money = int(data[1])
        else:
            stats.append(data[1])

# --- update game stats --- #
def updateStat(filename):
    global money
    file = open(filename, "r")
    lines = file.readlines()
    file.close()
    
    lines[0]="Wallet:"+str(money)+"\n"
    lines[1]="Won:"+stats[0]+"\n"
    lines[2]="Lost:"+stats[1] +"\n"
        
    file = open(filename, "w")
    file.write("".join(lines))
    file.close()
    
# --- global variables --- #
play, playH, first, game = 1, 1, 1, 1 
bust, bustH, unveil, money, bet = 0, 0, 0, 0, 0
hand, house, stats = [], [], []

# --- main function launching the game --- #
if __name__ == "__main__":
    """w, h = 1200, 600 # w=width, h=height
    init(w, h)
    update()
    """
    getData("stats.txt")    
    while game:
        reset()
        betting()
        while play:
            # initializing
            startGame(first)
            first = 0
            # checking the hand
            if checkHand(hand)<=21:          
                playerMove()
            else:
                busted()
        if not bust:
            displayTable()
            while playH:
                if checkHand(house)<=21:
                    houseMove()
                else:
                    houseBusted()       
        results()