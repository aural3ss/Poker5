from stack_of_cards import StackOfCards
from pokercard import PokerCard
from itertools import combinations
from ui import debug
WINNING_HANDS = ["Straight Flush", \
                "Four of a Kind", \
                "Full House", \
                "Flush", \
                "Straight", \
                "3 of a Kind", \
                "Two Pairs", \
                "Pair", \
                "Nothing" ]




HAND_RANK = {v : i for (i, v) in enumerate(reversed(WINNING_HANDS))}




class PokerHand(StackOfCards):
  '''
  A Poker Hand is meant to be a StackOfCards that has 5 Cards




  Key methods are to determine what type of hand it is and to compare
  2 PokerHands and determine the larger one
  '''
  def getValueDict(self) -> dict:
      '''
      key: rank of card -> value: number of appearances of the rank
      '''
      d = {}
      for card in self.cards:
          v = card.getValue()
          if v in d:
              d[v] += 1
          else:
              d[v] = 1
      return d




  def sort(self) -> None:
      '''
      Sort the hand using the PokerCard's ``__eq__`` and ``__lt__``
      '''
      self.cards.sort()
    
  def insert(self, pos: int, card: PokerCard) -> None:
      '''
      Insert the card at the indicated position
    
      :param pos: Position to insert card
      :param card: The PokerCard that is to be inserted
      '''
      self.cards.insert(pos, card)

  def handType(self) -> str:
      '''
      :return: Return a string that is the hand type - it should be one of the
         WINNING_HANDS strings - or "Nothing" if it is not even a pair
      :rtype: str
      '''
    
      value_dict = self.getValueDict()
      card_counts = list(value_dict.values())
      card_counts.sort()
      if self.isFlush() and self.isStraight():
          return "Straight Flush"
      if card_counts == [1, 4]:
          return "Four of a Kind"
      if card_counts == [2, 3]:
          return "Full House"
      if self.isFlush():
          return "Flush"
      if self.isStraight():
          return "Straight"
      if card_counts == [1, 1, 3]:
          return "3 of a Kind"
      if card_counts == [1, 2, 2]:
          return "Two Pairs"
      if card_counts == [1, 1, 1, 2]:
          return "Pair"
      if card_counts == [1, 1, 1, 1, 1]:
          return "Nothing"
      else:
          raise ValueError('{} hand is of unknown type'.format(self.cards))

  def isPair(self) -> bool:
      '''
      :return: Returns ``True`` if the hand is a pair
      :rtype: bool
      '''
      return self.handType() == "Pair"    
  
  def isFlush(self):
      '''
      :return: Returns ``True`` if the hand is a flush
      :rtype: bool
      '''
      card_types = set(card.getSuit() for card in self.cards)
      return len(card_types) == 1

  def isStraight(self):
      '''
      :return: Returns ``True`` if the hand is a straignt
      :rtype: bool
      '''
      card_values = [card.getValue() for card in self.cards]
      card_values.sort()
      if card_values == [2, 3, 4, 5, 14]:
          return True
      i = 4
      while i > 0 and card_values[i] - card_values[i - 1] == 1:
          i -= 1
      return i == 0




  def generateCompareTuple(self, item:tuple[int, int]):
      '''
      first compare counts (item[1]), then compare ranks (item[0])
      used in sortHand()
      '''
      return (-item[1], -item[0])




  def sortedHand(self):
      '''
      given a poker hand, return a list of ranks based on amt
      if two amounts are the same, they are organized by rank (high -> low)
      '''
      value_dict = self.getValueDict()
      value_to_count = list(value_dict.items())
      value_to_count.sort(key = self.generateCompareTuple)
      return [item[0] for item in value_to_count]




  def compareFourOfKind(self, other: "PokerHand") -> int:
      '''
      Compare two poker hands - ``self`` vs. ``other`` that are 4 of a kind




      :param other: Another hand (PokerHand) to compare against self
      :type other: PokerHand
      :return: Return 1 if ``self`` is higher. Return 2 if ``other`` is higher.
         Return 0 if they are both equal (tie).
      :rtype: int
      '''
      return self.compare(other)




  def compareFullHouse(self, other: "PokerHand") -> int:
      '''
      Compare two poker hands - ``self`` vs. ``other`` that are both
      a full house.




      :param other: Another hand (PokerHand) to compare against self
      :type other: PokerHand
      :return: Return 1 if ``self`` is higher. Return 2 if ``other`` is higher.
         Return 0 if they are both equal (tie).
      :rtype: int
      '''
      return self.compare(other)
    
  def comparePair(self, other: "PokerHand") -> int:
      '''
      Compare two poker hands - ``self`` vs. ``other`` that are both
      a **just** a pair.




      :param other: Another hand (PokerHand) to compare against self
      :type other: PokerHand
      :return: Return 1 if ``self`` is higher. Return 2 if ``other`` is higher.
         Return 0 if they are both equal (tie).
      :rtype: int
      '''
      return self.compare(other)




  def compare(self, other: "PokerHand") -> int:
      '''
      Compare the two 5-card hands of poker
    
      Return: 1 if player 1 wins, 2 if player 2 winds, 0 in the case of a tie
      '''
      type1 = self.handType()
      type2 = other.handType()
      if HAND_RANK[type1] != HAND_RANK[type2]:
          return 1 if HAND_RANK[type1] > HAND_RANK[type2] else 2
      # types are the same
      hand1 = self.sortedHand()
      hand2 = other.sortedHand()
      return 1 if hand1 > hand2 else 0 if hand1 == hand2 else 2








def test1():
  h1 = PokerHand()
  h1.add(PokerCard(suit = PokerCard.SUIT[0], rank = PokerCard.RANK[0], faceUp = True))
  h1.add(PokerCard(suit = PokerCard.SUIT[1], rank = PokerCard.RANK[3], faceUp = True))
  h1.add(PokerCard(suit = PokerCard.SUIT[0], rank = PokerCard.RANK[9], faceUp = True))
  h1.add(PokerCard(suit = PokerCard.SUIT[3], rank = PokerCard.RANK[11], faceUp = True))
  h1.add(PokerCard(suit = PokerCard.SUIT[2], rank = PokerCard.RANK[8], faceUp = True))
  h2 = PokerHand()
  h2.add(PokerCard(suit = PokerCard.SUIT[0], rank = PokerCard.RANK[1], faceUp = True))
  h2.add(PokerCard(suit = PokerCard.SUIT[1], rank = PokerCard.RANK[4], faceUp = True))
  h2.add(PokerCard(suit = PokerCard.SUIT[0], rank = PokerCard.RANK[9], faceUp = True))
  h2.add(PokerCard(suit = PokerCard.SUIT[3], rank = PokerCard.RANK[10], faceUp = True))
  h2.add(PokerCard(suit = PokerCard.SUIT[2], rank = PokerCard.RANK[12], faceUp = True))
  assert h1.compare(h2) == 2, (
      "h1 = {h1}, h2 = {h2}, winner is player {p}".format(
          h1=h1,
          h2=h2,
          p=h1.compare(h2),
      )
  )




if __name__ == "__main__":
  test1()












