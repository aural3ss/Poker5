###############
# DO NOT EDIT #
###############

class Card:
    '''
    A single standard card with a rank and suit - like Ace of Spades. It is
    very generic so technically the rank is any string and the suit is any
    string. The value of the A is 1 and the King is 13.

    Args:
       rank (str): The card rank - like 'A' or '5' or 'J'
       suit (str): One of the suits
    '''
    
    SUIT = ['♥', '♦', '♣', '♠']
    RANK = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

    def __init__(self, rank: str, suit: str):
        '''
        Intializes the Card.
        
        Args:
           rank (str): The card rank - like 'A' or '5' or 'J'
           suit (str): One of the suits
        '''
        self.rank = rank
        self.suit = suit
        
    def getValue(self) -> int:
        '''
        Return:
           A numerical value from 1-13 where Ace is 1, Jack is 11, Queen is 12 and
           King is 13.
        '''
        if self.rank == 'A':
            return(1)
        elif self.rank == 'J':
            return(11)
        elif self.rank == 'Q':
            return(12)
        elif self.rank == 'K':
            return(13)
        elif self.rank in '23456789' or self.rank == '10':
            return(int(self.rank))
        else:
            raise ValueError('{} is of unkwown value'.format(self.rank))
    
    
    def getRank(self) -> str:   
        '''
        Return:
            The rank of the card
        '''
        return(self.rank)
    
    def getSuit(self) -> str:   
        '''
        Return:
            The suit of the card
        '''
        return(self.suit)
    
    def __str__(self):
        return('{}{}'.format(self.rank, self.suit)) 

###############
# DO NOT EDIT #
###############