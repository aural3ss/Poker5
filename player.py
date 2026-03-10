###############
# DO NOT EDIT #
###############
from stack_of_cards import StackOfCards
from card import Card

class Player:
    '''
    A generic card player. The generic card player has a name, an amount
    of money and a hand of cards.

    Args:
       name (str): Name of player
       amount (int): Amount of money player has
       cards (StackOfCards): The players hand of cards
    '''
    def __init__(self, name: str, amount: int, cards: StackOfCards):
        '''
        Constructor
        '''
        self.name = name
        self.money = amount
        self.hand = cards
     
    # prints out name and the hand of stack_of_cards    
    def __str__(self):
        return("{}: {}".format(self.name, self.hand))
    
    def getName(self) -> str:
        '''
        Return:
           str: The name of player
        '''
        return(self.name)
    
    def getMoney(self) -> int:
        '''
        Return:
           int: Money balance of player
        '''
        return self.money

    def setMoney(self, amt: int) -> None:
        '''
        Args:
           amt (int): Change money balance to this amount
        '''
        self.money = amt

    def addMoney(self, amount):
        '''
        Args:
           amount (int): Change money balance by this amount - can be negative
           to subtract
        '''
        self.money += amount
    
    def addCard(self, card):
        '''
        Args:
           card (Card): Add this card to the end of the player's hand of cards
        '''
        self.hand.add(card)
        
    def getCard(self, pos) -> Card:
        '''
        Args:
           pos (int): Position (starting from 0) of card in the stack to return

        Return:
           Card: A single card from the hand
        '''
        return self.hand.getCard(pos)

    def removeCard(self, pos) -> None:
        '''
        Args:
           pos (int): Position (starting from 0) of card in the stack to remove
        '''
        return self.hand.remove(pos)

    def setHand(self, cards) -> None:
        '''
        Args:
           cards (StackOfCards): Replace player's hand with this one
        '''
        self.hand = cards

    def getHand(self) -> StackOfCards:
        '''
        Return:
           StackOfCards: The player's hand of cards
        '''
        return self.hand

###############
# DO NOT EDIT #
###############