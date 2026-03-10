from card import Card


class PokerCard(Card):
   '''
   A PokerCard has some additional features to the standard card.
   The Ace has a value of 14 instead of 1. The card can be up or down
   and prints out differently depending on whether it is face up or down.
   Also, a PokerCard is comparable based on its value.


   Args:
      rank (str): Rank of card - like 'A'
      suit (str): Suit of card - like '♥'
      factUp (bool): Optional parameter - defaults to ``False``. Defines
        whether the card is facing up or down
   '''


   def __init__(self, rank: str, suit: str, faceUp: bool = False):
       super().__init__(rank,suit)
       self.faceUp = faceUp
  
   def getValue(self) -> int:
       '''
       Return:
          A numerical value from 1-14 where Ace is 14, Jack is 11, Queen is 12 and
          King is 13, etc.
       '''
       if self.rank == "A":
           return 14
       elif self.rank == "K":
           return 13
       elif self.rank == "Q":
           return 12
       elif self.rank == "J":
           return 11
       else:
           return int(self.rank) 


   def getFaceUp(self) -> bool:
       '''
       Return:
          bool: ``True`` if card is face up
       '''
       return self.faceUp


   def setFaceUp(self) -> None:
       self.faceUp = True
  
   def setFaceDown(self) -> None:
       self.faceUp = False


   def flipUpDown(self) -> None:
       '''
       Flip the card - if face was up, then make it face down; vice versa
       '''
       if self.faceUp == True:
           self.setFaceDown()
       else:
           self.setFaceUp()
  
   def __eq__(self, other) -> bool:
       '''
       Return:
          Equal based on the value of the two cards
       '''
       return self.getValue() == other.getValue()
  
   def __lt__(self, other) -> bool:
       '''
       Return:
          If ``self`` is less than ``other`` based on the value of the two cards
       '''
       if self.getValue() < other.getValue():
           return True
       else:
           return False
  
   def __str__(self) -> str:
       '''
       Return:
          If face up, just return the normal string value of the card,
          otherwise return '████'


       '''
       if self.faceUp == True:
           return '{}{}'.format(self.rank,self.suit)
       else:
           return "████"






