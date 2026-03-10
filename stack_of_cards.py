###############
# DO NOT EDIT #
###############
import random

#===========================================================================
# Description: A list of Card; used for a player's hand or a deck of cards
#
# State Attributes
#     - cards - list of card; starts out empty
# Methods
#     - shuffle() - randomly shuffle all the card in the list
#     - deal() - deal the 'top' card from the hand/deck
#     - add(card) - add Card to the list of cards
#     - remove(pos) - remove and return Card at pos number
#     - size() - size of hand
#     - getCard(pos) - returns a Card at the 'pos'
#     - __str__() - returns string of all the cards in the hand like '4♣ 10♥ A♠'
#===========================================================================
class StackOfCards:
    '''
    Models a stack of cards - can be used to hold a player's hand of 5 cards
    or a deck of 52 cards
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.cards = []
        
    def __str__(self) -> str:
        '''
        Prints out all the cards in a single line
        '''
        s = ''
        for card in self.cards:
            if s == '':
                s = str(card)
            else:
                s = s + ' ' + str(card)
        return s

    def __len__(self) -> int:
        return len(self.cards)

    def __iter__(self):
        return iter(self.cards)
    
    # Add card to the 'bottom' of the deck of cards
    def add(self, card):
        '''
        Add card tot the end/bottom of the deck of cards
        '''
        self.cards.append(card)
                
    def remove(self, pos: int):
        '''
        Remove a card at given position (0 to size - 1)
        
        :param pos: Position of card to remove
        '''
        card = self.cards.pop(pos)
        return card
               
    # Deal card from the 'top' of the deck of cards
    def deal(self):
        '''
        :return: Deal the top card (at index 0) of the card deck
        :rtype: Card
        '''
        return self.cards.pop(0)
        
    def shuffle(self) -> None:
        '''
        Shuffle all of the cards in the deck
        '''
        random.shuffle(self.cards)
        
    def size(self) -> int:
        '''
        :return: The number of cards in the deck
        :rtype: int
        '''
        return(len(self.cards))
    
    def getCard(self, pos:int):
        '''
        :param pos: Get the card at the indicated position (0 to size-1)
        :return: The card at the provided posision
        '''
        return(self.cards[pos])
    
    def copy(self):
        '''
        :return: A full copy of the stack of cards 
        '''
        stack = StackOfCards()
        stack.cards = self.cards[:]
        return stack

    def setCards(self, cards):
        '''
        Replace the hand with an brand new set of cards

        Args:
            cards (list[Cards]): Set the hand to the new set of cards
        '''
        self.cards = list(cards)
    
###############
# DO NOT EDIT #
###############
        