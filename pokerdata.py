from gamedata import GameData
from pokerplayer import PokerPlayer
from pokerhand import PokerHand
from pokercard import PokerCard

class PokerData(GameData):
  '''
  ``PokerData`` is meant to hold all the data/information relevant to the
  poker game. For example - the players, the ante amount, the pot balance
  and any other information you want to store/manipulate for the poker game.
  You are to add any sort of data/attribute and methods you find appropriate
  beyond the required ones below.
  '''

  def __init__(self):
      super().__init__()
      self.pot = 0
      self.ante = 10
      self.betLimit = 0
      self.first_player = 1
      # Add any other sort of data you'd like the PokerData object to hold

  def addPot(self, amt: int) -> None:
      '''
      :param amt: Add amt to the poker pot
      '''
      self.pot += amt

  def getPot(self) -> int:
      '''
      :return: The poker pot
      :rtype: int
      '''
      return self.pot
 
  def getAnte(self) -> int:
      '''
      :return: The ante for the poker game
      :rtype: int
      '''
      return self.ante
 
  def setAnte(self, amt: int) -> None:
      '''
      Set the ante for the poker game to amt
      '''
      self.ante = amt


  def setBetLimit(self, amt: int) -> None:
       '''
       Set the bet limit for the poker game to amt
       '''
       self.betLimit = amt
      
  def getBetLimit(self) -> int:
       '''
       :return: The bet limit for the poker game
       :rtype: int
       '''
       return self.betLimit


  def resetPot(self) -> None:
      '''
      Set the poker pot to 0
      '''
      self.pot = 0

  def makePlayer(self, pNum: int, name: str, money: int) -> None:
      '''
      Creates a PokerPlayer with the given name and money and an empty PokerHand and
      saves it as an attribute of PokerData
    
      :param pNum: Number (1 or 2) of player to make
      :type pNum: int
      :param name: Name of player
      :type name: str
      :param money: Amount of money for the player
      :type money: int
      '''
      hand = PokerHand()
      player = PokerPlayer(name,money,hand)
      if pNum == 1:
          self.player1 = player
      elif pNum == 2:
          self.player2 = player
        
  def getPlayer(self, pNum: int) -> PokerPlayer:
      '''
      :param pNum: Number (1 or 2) of the player to get
      :type pNum: int
      :return: Player 1 or 2 according to pNum
      :rtype: PokerPlayer
      '''
      if pNum == 1:
          return self.player1
      elif pNum == 2:
          return self.player2
  def getHand(self,pNum: int) -> PokerHand:
       if pNum == 1:
          return self.player1.hand
       elif pNum == 2:
          return self.player2.hand

  def bet(self, pNum: int, amt: int) -> None:
      '''
      Add an amount of money to the player's bet and decrease the money balance by
      the same amount
    
      :param pNum: Player number (1 or 2) to adjust
      :type pNum: int
      :param amt: This amount is added to the player's bet and decremented from the
         player's money
      :type amt: int
      '''
      player = self.getPlayer(pNum)
      player.addBet(amt)
      player.money -= amt
      self.pot += amt

  def flipCards(self, pNum: int) -> None:
      '''
      Flip all the cards held in the hand of the player. If the card is up, then
      make it face down and vice versa
    
      :param pNum: Player number (1 or 2) to flip cards
      :type pNum: int
      '''
      if pNum == 1:
          for card in self.player1.hand:
              card.flipUpDown()
      else:
          for card in self.player2.hand:
              card.flipUpDown()
  def flipDown(self, pNum: int) -> None:
      '''
      Flip all the cards held in the hand of the player face down
    
      :param pNum: Player number (1 or 2) to flip cards
      :type pNum: int
      '''
      if pNum == 1:
          for card in self.player1.hand:
              card.setFaceDown()
      else:
          for card in self.player2.hand:
              card.setFaceDown()
  def flipUp(self, pNum: int) -> None:
      '''
      Flip all the cards held in the hand of the player face up
    
      :param pNum: Player number (1 or 2) to flip cards
      :type pNum: int
      '''
      if pNum == 1:
          for card in self.player1.hand:
              card.setFaceUp()
      else:
          for card in self.player2.hand:
              card.setFaceUp()
        
  def whoIsWinner(self) -> int:
      '''
      Determine the winner between player 1 and player 2 by comparing their
      poker hand
      :return: 1 if player 1 won; or 2 if player 2 won; or 0 if a tie
      '''
      h1 = self.player1.hand
      h2 = self.player2.hand
      result = h1.compare(h2)
      return result





















