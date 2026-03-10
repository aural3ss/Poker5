from itertools import count
from player import Player
from pokerhand import PokerHand
from pokercard import PokerCard


class PokerPlayer(Player):
   def __init__(self, name: str, money: int, cards: PokerHand):
       super().__init__(name,money,cards)
       self.bet = 0
       self.fold = False
       # You may add additional player attributes if you'd like...


   def getBet(self) -> int:
       '''
       Returns:
          int: Value of the player's current bet total
       '''
       return(self.bet)


   def resetBet(self) -> None:
       '''
       Resets the bet to 0
       '''
       self.bet = 0


   def addBet(self, money: int) -> None:
       '''
       Add money to the player's current bet


       Args:
          money (int): Amount to add to the bet
       '''
       self.bet = self.bet + money
      
   def setFold(self) -> None:
       '''
       Player has folded, set the fold flag to True
       '''
       self.fold = True


   def getFold(self) -> bool:
       '''
       Returns:
          bool: True if player has folded in the current betting phase
       '''
       return self.fold


   def emptyHand(self) -> bool:
       '''
       Returns:
          bool: True if the player's hand is empty
       '''
       return self.hand.size() == 0


   def replaceCards(self, holdList: list[int], deck: PokerHand):
       '''
       Models the "draw" in poker.  Modify the ``self.hand`` (see parent
       ``Player`` class) according to the index numbers in holdList.
       The holdList will contain numbers 1 - 5. These are which cards
       to "hold" and the other card numbers will be exchanged with
       new cards dealt from the deck.


       Args:
           holdList (list[int]): list of card to hold - valid numbers 1 to 5
           deck (PokerHand): Deal new cards from this deck
       '''
       for i in range(5,0,-1):
           if i not in holdList:
               self.removeCard(i-1)
               newCard = deck.getCard(0)
               deck.deal()
               self.hand.insert(i-1,newCard)


   def sortCards(self) -> None:
       '''
       Sort all of the cards help by player from lowest to highest
       '''
       self.hand.sort()


   def cardsDown(self):
       '''
       Make all the cards in the hand face down
       '''
       for i in range(self.hand.size()):
           self.hand.getCard(i).setFaceDown()
          
   def cardsUp(self):
       '''
       Make all the cards in the hand face up
       '''
       for i in range(self.hand.size()):
           self.hand.getCard(i).setFaceUp()


   def handType(self) -> str:
       '''
       Returns:
           str: The name of the type of hand the player is holding - like
           "Three of a Kind" or "Full House"
       '''
       return self.hand.handType()   
      
   def newHand(self) -> None:
       '''
       Restart with an new empty PokerHand
       Reset fold status to False
       Resets the bet to 0
       '''
       self.hand = PokerHand()
       self.fold = False
       self.bet = 0


   def __str__(self):
       return (super().__str__())




