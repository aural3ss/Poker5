#Version 1.0:PokerCard,PokerPlayer,PokerData,PokerHand completed and debugged
#Version 2.0: Completed and tested PokerUI
#Version 3.0: game.py finished, ready to begin full debugging
#Version 4.0: Everything has been debugged, the full game without external features has been completed
#Version 5.0: Ignore the 5th snapshot, this is the real 5th snapshot with all of the update comments.
#Version 5.0 is the final version, with all of the extra features fully implemented and tested
#The extra features include: setting a custom ante after every game, setting a custom balance after every game, and a custom betting limit after each game
#Version 6.0: This is just some extra cleanup of functions, to make sure everything is spot on.
import curses
from ui import debug
from pokercard import PokerCard
from pokerhand import PokerHand
from pokerplayer import PokerPlayer
from pokerdata import PokerData
from pokerui import PokerUI
from stack_of_cards import StackOfCards

def playRound(ui: PokerUI, data: PokerData, deck: PokerHand, roundNum: int) -> int:
 '''
 Play one round - make/shuffle deck, deal 5 cards, bet, draw, bet, pay winner.
 1. Make and shuffle a PokerHand deck of 52 PokerCards
 2. Each player puts the ante of 10 into the pot
 3. Deal 5 cards - one at a time alternating between player 1 and player 2
 4. Bet - starting with designated starting player
 5. Draw - Each player declares which cards they want to keep and are given
    new cards from the deck. This starts with the designated starting player
 6. Bet - starting with the designated player again
 7. Determine winner who wins the pot
 
 Args:
     ui (PokerUI): User interface for Poker game
     data (PokerData): All the data in Poker game
  Return:
     int: The player number (1 or 2) of the winner, 0 if tie
 '''
 
 second_player = 3 - data.first_player
 # player_order gives the order of the players
 player_order = [data.first_player, second_player]
 player1 = data.getPlayer(1)
 player2 = data.getPlayer(2)
 players = [player1, player2]

 for player in players:
     player.resetBet()
     player.newHand()
 data.resetPot()

 # step 1: shuffle a deck of 52 cards
 deck.shuffle()

 # step 2: start with the ante of the players choice
 data.getPlayer(1).money -= data.getAnte()
 data.getPlayer(2).money -= data.getAnte()
 data.pot += 2 * data.getAnte()

 # step 3: deal the cards one at a time alternating between player 1 and player 2
 for card_num in range(5):
     for p_num in player_order:
         card = deck.deal()
         data.getPlayer(p_num).addCard(card)

 #initialize ui window
 ui.initPokerRound(data)
 ui.showTurn(data.first_player)
 ui.showBets(data)
 ui.showPot(data.pot)
 ui.writePlayerNames(data.getPlayer(1).getName(), data.getPlayer(2).getName())
 ui.writeScore(1, data.getPlayer(1).getMoney())
 ui.writeScore(2, data.getPlayer(2).getMoney())
 ui.updateGameWindow()

 # step 4: bet starting with the designated player
 bet(ui, data, data.first_player)
 if data.getPlayer(second_player).getFold() == True:
   player1.addMoney(data.getPot())
   ui.writeMsg(
         "{name} won the game, winning {amt} dollars.".format(
             name = data.getPlayer(data.first_player).getName(),
             amt = data.getPot()
         )
     )
   data.resetPot()
   return data.first_player

 # step 5: hold cards starting with the designated player
 for p_num in player_order:
     held_cards = hold(ui, data, p_num)
     data.getPlayer(p_num).replaceCards(held_cards, deck)
     ui.writePlayerCards(p_num, data.getPlayer(p_num).getHand())
     ui.updateGameWindow()
 # step 6: bet starting with the designated player again
 bet(ui, data, data.first_player)
 if player2.getFold() == True:
     player1.addMoney(data.getPot())
     ui.writeMsg(
         "{name} won the game, winning {amt} dollars.".format(
             name = data.getPlayer(data.first_player).getName(),
             amt = data.getPot()
         )
     )
     data.resetPot()
     return data.first_player
  # step 7
 hand1 = player1.hand
 hand2 = player2.hand
 winner = hand1.compare(hand2)
 if winner == 1:
     player1.addMoney(data.getPot())
     ui.writeMsg("{name} won the game!".format(name = player1.getName()))
 elif winner == 2:
     player2.addMoney(data.getPot())
     ui.writeMsg("{name} won the game!".format(name = player2.getName()))
 else:
     player1.addMoney(player1.getBet())
     player2.addMoney(player2.getBet())
     ui.writeMsg("The game is a tie!")

 data.flipUp(1)
 ui.writePlayerCards(1, data.getPlayer(1).getHand())
 data.flipUp(2)
 ui.writePlayerCards(2, data.getPlayer(2).getHand())
 nextRound = ui.askMsg("Press enter to continue.")
 ui.updateGameWindow()
 if nextRound != None:
        return winner

def bet(ui: PokerUI, data: PokerData, pNum: int) -> None:
 '''
 Handle the bet sequence starting from the designated player.
 1. Designated player starts. Either presses ``?`` to toggle cards
    up or down or ``b`` to bet.
 2. Ask player how much he will bet making sure it is a legal amount.
 3. Next player decides to call or fold by pressing ``c`` or ``f`` or ``?``.


 At the end of betting, the pot will include both player's bet.


 Args:
     ui (PokerUI): User interface for Poker game
     data (PokerData): All the data in Poker game
     pNum (int): player number that starts the bet (1 or 2)
 '''
 #step 1: designated player starts with actions
 ui.showTurn(pNum)
 if pNum == data.first_player:
     options = ("bet")
     actions = ["? - show/hide cards", "b - bet"]
     ui.showMenu(actions)
     while True:
       move = ui.getPlayerMove(pNum)
       if move is None:
           continue
       elif move == "flip":
           data.flipCards(pNum)
           ui.writePlayerCards(pNum, data.getHand(pNum))
           ui.updateGameWindow()
           continue
       elif move in options:
           break
 #step 2: designated player decides how much to bet
     while True:
       data.setBetLimit(data.getPlayer(pNum).getMoney())
       amt_str = ui.askMsg("What would you like to bet, {name}?(0-{limit})".
       format(name = data.getPlayer(data.first_player).getName(), limit = data.getBetLimit()))
       try:
           amount = int(amt_str)
       except ValueError:
           ui.writeMsg("Please enter a number.")
           continue
       if amount < 0:
           ui.writeMsg("Please enter a positive integer.")
           continue
       if amount > data.getBetLimit():
           ui.writeMsg("Your bet of {amt} exceeds the bet limit.".format(amt = amount))
           continue
       if amount > data.getPlayer(pNum).money:
           ui.writeMsg("Your bet of {amt} exceeds your available funds.".format(amt = amount))
           continue
       if amount == 0 and data.getPlayer(pNum).money == 0:
           ui.writeMsg("Since you have no more money, we made an all-in bet of 0 on your behalf.")
       data.bet(pNum, amount)
       data.flipDown(pNum)
       ui.writePlayerCards(pNum, data.getPlayer(pNum).getHand())
       ui.showBets(data)
       ui.writeScore(pNum, data.getPlayer(pNum).getMoney())
       ui.updateGameWindow()
       break
     
     second_player = 3 - pNum
     options = ("call", "fold")
     actions = ["? - show/hide cards", "c - call", "f - fold"]
     ui.showMenu(actions)
     ui.showTurn(second_player)
     while True:
      move = ui.getPlayerMove(second_player)
      if move is None:
         continue
      elif move == "flip":
         data.flipCards(second_player)
         ui.writePlayerCards(second_player, data.getPlayer(second_player).getHand())
         ui.updateGameWindow()
      elif move == "call":
         call_amount = data.getPlayer(pNum).getBet()               
         if call_amount > data.getPlayer(second_player).money:
             call_amount = data.getPlayer(second_player).money
             ui.writeMsg("Since you cannot afford to call, we made an all-in on your behalf.")
         data.bet(second_player, call_amount)
         data.flipDown(second_player)
         ui.writePlayerCards(second_player, data.getPlayer(second_player).getHand())
         ui.showBets(data)
         ui.writeScore(second_player, data.getPlayer(second_player).getMoney())
         ui.updateGameWindow()
         break
      elif move == "fold":
         data.getPlayer(second_player).setFold()
         ui.updateGameWindow()
         break
     ui.showPot(data.getPot())
     for player in [data.getPlayer(1), data.getPlayer(2)]:
        player.resetBet()
        ui.showBets(data)
        ui.updateGameWindow()
    
def hold(ui: PokerUI, data: PokerData, pNum: int) -> list[int]:
 '''
 The designated player will decide which cards they want to hold by
 pressing ``1``/``2``/``3``/``4``/``5``. The ``?`` will show/hide their cards.
 Pressing one of the card numbers will toggle a ``H`` designation on that card.
 Pressing ``d`` will commit their hold selection. At end of this, the
 player's cards will automatically be hidden face down.


 Args:
     ui (PokerUI): User interface for Poker game
     data (PokerData): All the data in Poker game
     pNum (int): player number that is being asked which cards to hold (1 or 2)
 Return:
     list[int]: A list of integers representing the cards the player wants
     to hold. Ex. [1, 3, 4]
 '''
 hold_selection = set()
 actions = ["? - show/hide cards", "1/2/3/4/5 - toggle hold/unhold card", "d - done with hold selection"]
 ui.showMenu(actions)
 ui.showTurn(pNum)
 while True:
     move = ui.getPlayerMove(pNum)
     if move == None:
         continue
     if move != None and move in ("1", "2", "3", "4", "5"):
         card_number = int(move)
         if card_number in hold_selection:
             hold_selection.remove(card_number)
             ui.unholdCard(pNum, card_number)
         else:
             hold_selection.add(card_number)
             ui.holdCard(pNum, card_number)
         ui.updateGameWindow()
     elif move != None and move == "flip":
         data.flipCards(pNum)
         ui.writePlayerCards(pNum, data.getPlayer(pNum).getHand())
         ui.updateGameWindow()
     elif move != None and move == "done":
         held_cards = list(hold_selection)
         data.flipDown(pNum)
         ui.writePlayerCards(pNum, data.getPlayer(pNum).getHand())
         for card in held_cards:
            ui.unholdCard(pNum, card)
         ui.updateGameWindow()
         held_cards.sort()
         return held_cards
      
def playGame(ui: PokerUI, data: PokerData) -> None:
 '''
 1. Designate player 1 to start the first round of betting.
 2. Repeatedly call playRound() until one player does not have any
    more money (or enough to even ante for the next round of play).
    At the end of each round, swap the person who will start the bet
    in the next round.
 3. Write a message at the end declaring who won.
 Args:
     ui (PokerUI): User interface for Poker game
     data (PokerData): All the data in Poker game
 '''
 data.first_player = 1
 player1 = data.getPlayer(1)
 player2 = data.getPlayer(2)
 roundNum = 1
 while player1.getMoney() >= 10 and player2.getMoney() >= 10:
     deck = makeDeck()
     playRound(ui, data, deck, roundNum)
     data.first_player = 3 - data.first_player
     roundNum += 1
 if player1.getMoney() > player2.getMoney():
     winner = 1
 else:
     winner = 2
 ui.writeMsg("{name} has won the game with a {hand}!".format(name = data.getPlayer(winner).getName(), hand = data.getHand(winner)))


def makeDeck() -> PokerHand:
 '''
 Make a deck of all 52 PokerCards - no specific order required.
 Return:
     PokerHand: All 52 PokerCards
 '''
 deck = PokerHand()
 for  suit in PokerCard.SUIT:
     for rank in PokerCard.RANK:
         deck.add(PokerCard(suit = suit, rank = rank, faceUp = False))
 return deck

def main(stdscr):
 '''
 1. Get player names and starting money balance.
 2. Call playGame() and when done see if players want to play again.
    If yes, reset the money to the original starting money balance and play again.
    If no, then end.
 '''
 # initialize ui and data
 ui = PokerUI()
 ui.setPlayerKeyMap(1, [('?', 'flip'), ('b', 'bet'), ('c', 'call'), ('f', 'fold'),
                        ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('d', 'done') ])
 ui.setPlayerKeyMap(2, [('?', 'flip'), ('b', 'bet'), ('c', 'call'), ('f', 'fold'),
                        ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('d', 'done') ])                    
 data = PokerData()
 data.setData('mode', 'basic')
 data.setData('numPlayers', 2)

# starts by asking for player names and money balance, and then calls playGame. 
 ui.writeMsg("Let's play 5-card Draw")
 name1 = ui.askMsg("Player 1 name?")
 # sets player 1s money, making sure they enter a valid positive integer
 while True:
    money1 = ui.askMsg("How much are you bringing to the table, {name}?".format(name=name1))
    try:
        money1 = int(money1)
        if money1 > 0:
            break
        else:
            ui.writeMsg("Please enter a positive integer for the amount of money.")
    except ValueError:
        ui.writeMsg("Please enter a valid number.")

 name2 = ui.askMsg("Player 2 name?")
 # sets player 2s money, making sure they enter a valid positive integer
 while True:
    money2 = ui.askMsg("How much are you bringing to the table, {name}?".format(name=name2))
    try:
        money2 = int(money2)
        if money2 > 0:
            break
        else:
            ui.writeMsg("Please enter a positive integer for the amount of money.")
    except ValueError:
        ui.writeMsg("Please enter a valid number.")
 # sets the ante, making sure they enter a valid positive integer
 while True:
    try:
        ante = int(ui.askMsg("What is the ante for each round?"))
        if ante > 0:
            data.setAnte(ante)
            break
        else:
            ui.writeMsg("Please enter a positive integer for the ante.")
    except ValueError:
        ui.writeMsg("Please enter a valid number.")
# if the ante is invalid, it will tell the user to input a new amount of money
 while money1 < data.getAnte() or money2 < data.getAnte():
    ui.writeMsg("One or more players does not have enough money to ante. Please enter new amounts.")
    while True:
        try:
            money1 = int(ui.askMsg("How much are you bringing to the table, {name}?".format(name=name1)))
            if money1 > 0:
                break
            else:
                ui.writeMsg("Please enter a positive integer.")
        except ValueError:
            ui.writeMsg("Please enter a valid number.")
    while True:
        try:
            money2 = int(ui.askMsg("How much are you bringing to the table, {name}?".format(name=name2)))
            if money2 > 0:
                break
            else:
                ui.writeMsg("Please enter a positive integer.")
        except ValueError:
            ui.writeMsg("Please enter a valid number.")
 # if the bet limit is invalid, it will tell the user to input a new bet limit. 
 # If the bet limit is 0, it will set the bet limit to the maximum possible bet (the smaller of the two player's money minus the ante).
 while True:
    try:
        betLimit = int(ui.askMsg("What is the bet limit for each round? (0 = no limit)"))
        
        if betLimit < 0:
            ui.writeMsg("Please enter a non-negative integer.")
            continue

        if betLimit == 0:
            betLimit = min(money1 - data.getAnte(), money2 - data.getAnte())

        data.setBetLimit(betLimit)
        break

    except ValueError:
        ui.writeMsg("Please enter a valid number.")
 ui.writeMsg("Great! Let's start the game!")
 data.makePlayer(1, name1, int(money1))
 data.makePlayer(2, name2, int(money2))
 ui.updateGameWindow()
 playGame(ui, data)
 playAgain = ui.askMsg("Do you want to play again? (y/n)")
 while playAgain == "y":
     while True:
        money1 = ui.askMsg("How much are you bringing to the table, {name}?".format(name=name1))
        try:
            money1 = int(money1)
            if money1 > 0:
                break
            else:
                ui.writeMsg("Please enter a positive integer for the amount of money.")
        except ValueError:
            ui.writeMsg("Please enter a valid number.")
     while True:
        money2 = ui.askMsg("How much are you bringing to the table, {name}?".format(name=name2))
        try:
            money2 = int(money2)
            if money2 > 0:
                break
            else:
                ui.writeMsg("Please enter a positive integer for the amount of money.")
        except ValueError:
            ui.writeMsg("Please enter a valid number.")
     data.getPlayer(1).setMoney(int(money1))
     data.getPlayer(2).setMoney(int(money2))
     # sets the ante, making sure they enter a valid positive integer
     while True:
        try:
            ante = int(ui.askMsg("What is the ante for each round?"))
            if ante > 0:
                data.setAnte(ante)
                break
            else:
                ui.writeMsg("Please enter a positive integer for the ante.")
        except ValueError:
            ui.writeMsg("Please enter a valid number.")
  # if the ante is invalid, it will tell the user to input a new amount of money
     while money1 < data.getAnte() or money2 < data.getAnte():
        ui.writeMsg("One or more players does not have enough money to ante. Please enter new amounts.")
        while True:
            try:
                money1 = int(ui.askMsg("How much are you bringing to the table, {name}?".format(name=name1)))
                if money1 > 0:
                    break
                else:
                    ui.writeMsg("Please enter a positive integer.")
            except ValueError:
                ui.writeMsg("Please enter a valid number.")
        while True:
            try:
                money2 = int(ui.askMsg("How much are you bringing to the table, {name}?".format(name=name2)))
                if money2 > 0:
                    break
                else:
                    ui.writeMsg("Please enter a positive integer.")
            except ValueError:
                ui.writeMsg("Please enter a valid number.")
     # if the bet limit is invalid, it will tell the user to input a new bet limit. 
 # If the bet limit is 0, it will set the bet limit to the maximum possible bet (the smaller of the two player's money minus the ante).
     while True:
        try:
            betLimit = int(ui.askMsg("What is the bet limit for each round? (0 = no limit)"))
        
            if betLimit < 0:
                ui.writeMsg("Please enter a non-negative integer.")
                continue

            if betLimit == 0:
                betLimit = min(money1 - data.getAnte(), money2 - data.getAnte())

            data.setBetLimit(betLimit)
            break

        except ValueError:
            ui.writeMsg("Please enter a valid number.")
     ui.writeMsg("Great! Let's start the game!")
     playGame(ui, data)
     playAgain = ui.askMsg("Do you want to play again? (y/n)")
 if playAgain == "n":
     ui.writeMsg("Thanks for playing! Press any key to exit.")
     ui.waitForKey()
     ui.updateGameWindow()


# DO NOT CHANGE/DELETE THIS LINE BELOW
if __name__ == "__main__":
 curses.wrapper(main)





