from ui import UI
from ui import debug
from card import Card
from pokerplayer import PokerPlayer
from pokerdata import PokerData
from pokerhand import PokerHand




class PokerUI(UI):
  '''
  This is generally done, but you must implement the the ``holdCard`` and
  the ``unholdCard``, and ``showMenu`` methods
   This class has methods that you will be able to use to display features
  of the game that you see in the example.
   You may add additional methods, but do not change any of the already written
  methods.
  '''
  P1_STARTX = 5
  P1_STARTY = 2
  P2_STARTX = 5
  P2_STARTY = 7
  P_DX = 5




  POTX = 15
  POTY = 11




  MENUX = 5
  MENUY = 15




  def initPokerRound(self, data: PokerData) -> None:
      '''
      Clears out the game window. Writes the the name of the players,
      the card numbers and their cards, and their current bet (i.e. 0)
      '''
      self.clearGameWindow()




      p1 = data.getPlayer(1)
      p2 = data.getPlayer(2)
      self.writeStr(p1.getName(), self.P1_STARTX, self.P1_STARTY)
      self.writeStr(p2.getName(), self.P2_STARTX, self.P2_STARTY)




      for i in range(1, 6):
          x = self.P1_STARTX + (i-1) * self.P_DX
          self.writeStr(str(i), x, self.P1_STARTY + 1)
          self.writeStr(str(i), x, self.P2_STARTY + 1)




      self.writePlayerCards(1, data.getHand(1))
      self.writePlayerCards(2, data.getHand(2))




      self.showBets(data)
      self.showPot(data.getPot())




      self.updateGameWindow()




  def writePlayerCards(self, pNum: int, hand: PokerHand) -> None:
      '''
      Write out the hand of an indicated player on the game window.




      Args:
         pNum (int): Either 1 or 2 to indicate which player hand
         hand (PokerHand): The hand to display
      '''




      if pNum == 1:
          x = self.P1_STARTX
          y = self.P1_STARTY
      else:
          x = self.P2_STARTX
          y = self.P2_STARTY




      self.clearLine(y+2)
      i = 0
      for c in hand:
          self.writeStr(str(c), x, y+2)
          i += 1
          x += self.P_DX
      self.updateGameWindow()




  def showBets(self, data: PokerData) -> None:
      '''
      Writes out the current bets of each player on the game window
    
      Args:
          data (PokerData): Contains all the data for the poker game
      '''
      p1 = data.getPlayer(1)
      p2 = data.getPlayer(2)




      x = self.P1_STARTX
      y = self.P1_STARTY + 3
      self.clearLine(y)
      msg = f"Bet: {p1.getBet()}      "
      self.clearLine(y)
      self.writeStr(msg, x, y)




      x = self.P2_STARTX
      y = self.P2_STARTY + 3
      msg = f"Bet: {p2.getBet()}      "
      self.clearLine(y)
      self.writeStr(msg, x, y)




      self.updateGameWindow()




  def showPot(self, amt: int) -> None:
      '''
      Writes out the current pot for the round
    
      Args:
          amt (int): Amount in the pot
      '''
      self.writeStr(f"Pot: {amt}     ", self.POTX, self.POTY)
      self.updateGameWindow()




  def showTurn(self, pNum: int) -> None:
      '''
      Show ``>>>`` next to the player whose turn it is to do something
    
      Args:
          amt (int): Amount in the pot
      '''
      if pNum == 1:
          self.writeStr("   ", 1, self.P2_STARTY)
          self.writeStr(">>>", 1, self.P1_STARTY)
      else:
          self.writeStr("   ", 1, self.P1_STARTY)
          self.writeStr(">>>", 1, self.P2_STARTY)




  def clearMenu(self) -> None:
      self.writeStr(" "*40, 1, self.MENUY)
      for i in range(5):
          self.clearLine(self.MENUY+i+1)
          self.writeStr(" "*40, 1, self.MENUY+i+1)




  def showMenu(self, menu: list[str]) -> None:
      '''
      Write out a menu of actions that the player can do.




      1. Call clearMenu to erase any previous menu
      2. On the line starting from ``MENUX``, ``MENUY``, print the word ``Action:``
      3. For each string in the menu list, print this underneath the
         ``Action:`` title
    
      Args:
         menu (lst[str]): Each string in the list is a line of menu
           to print out for the player's action. The max length of this
           list is 4 just due to window limitations but does not need to
           be checked.
      '''
      self.clearMenu()
      self.writeStr("Action:", self.MENUX, self.MENUY)
      for i, action in enumerate(menu):
          self.writeStr(action, self.MENUX, self.MENUY+1+i)


  def holdCard(self, pNum: int, cardNum: int) -> None:
      '''
      Write an ``H`` character above the card, next to the number
      to indicate that the card is to be held. The line to write
      is on line ``P#_STARTY + 1``.




      Args:
         pNum (int): Either 1 or 2 to indicate which player hand
         cardNum: (int): A number 1 to 5 to indicate which card to hold
      '''
      if pNum == 1:
          x = self.P1_STARTX + (cardNum-1) * self.P_DX+1
          y = self.P1_STARTY + 1
      elif pNum == 2:
          x = self.P2_STARTX + (cardNum-1) * self.P_DX+1
          y = self.P2_STARTY + 1
      self.writeStr("H", x, y)


  def unholdCard(self, pNum: int, cardNum: int) -> None:
      '''
      Write an ' ' character above the card, next to the number
      to erase any hold indication that may have been written for the card.




      Args:
         pNum (int): Either 1 or 2 to indicate which player hand
         cardNum: (int): A number 1 to 5 to indicate which card to unhold
      '''
      if pNum == 1:
          x = self.P1_STARTX + (cardNum-1) * self.P_DX+1
          y = self.P1_STARTY + 1
      elif pNum == 2:
          x = self.P2_STARTX + (cardNum-1) * self.P_DX+1
          y = self.P2_STARTY + 1
      self.writeStr(" ", x, y)





































