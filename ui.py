import curses
import time
from typing import List


'''
**DO NOT MODIFY THIS CLASS - FOR REFERENCE ONLY**
'''


class Debugger:


   def __init__(self) -> None:


       self.ui: UI | None = None


   def __call__(self, *args) -> None:


       if self.ui is not None:
           self.ui.writeDebug(*args)


debug = Debugger()


class UI:
   '''
   UI is a curses-based 3-paned window - a message window, a game window and a message window
   with methods to write to different windows on the screen.


   When you create a UI instance, you will immediately see the screen appear (as long as your
   console is tall enough...). All locations are defined as (x, y).


   ┌────────────────────────────────────────┐
   │ Header Window - 40 x 1                 │
   ├────────────────────────────────────────┤
   │x <-- Top left position (1, 1)          │
   │                                        │
   │                                        │
   │                                        │
   │                                        │
   │                                        │
   │                                        │
   │                                        │
   │                                        │
   │ Game Window - 40(w) x 20(h)            │
   │                                        │
   │                                        │
   │                                        │
   │                                        │
   │                                        │
   │                                        │
   │                                        │
   │                                        │
   │                                        │
   │   Bottom Right Character (40, 20) --> x│
   ├────────────────────────────────────────┤
   │ Message Window - 40(w) x 5(h)          │
   │                                        │
   │                                        │
   │                                        │
   └────────────────────────────────────────┘
   '''
   WIDTH = 40
   HEADER_HEIGHT = 1
   GAME_HEIGHT = 20
   MSG_HEIGHT = 5
   DBG_WIDTH = 50


   # total height with the 4 horizontal border lines
   TOTAL_HEIGHT = GAME_HEIGHT + HEADER_HEIGHT + MSG_HEIGHT + 4


   # total width with the 2 vertical border lines
   TOTAL_WIDTH = WIDTH + 2


   def __init__(self, testMode: bool = False):


       # Set this flag to True when doing unit test w/o the curses really running
       self.testMode = testMode


       # special UI modes
       self.keyIn = None       # used for testing purposes
       self.pauseMode = False  # default
       self.testAnswerQ = None # default off


       self.playerKeys = [ [], [] ]    # initialize for 2 players
       self.playerMoves = [ [], [] ]
       self.playerKeyDef = [ {}, {} ]


       if self.testMode:
           # initialize a "fake" display that is a 2D array of characters
           self.fakeGameWindow = [ [' ' for _ in range(self.WIDTH+2) ] for y in range(self.GAME_HEIGHT+2) ]
           return


       # curses related code - skip in testMode
       self.stdscr = curses.initscr()
       curses.curs_set(0)          # make cursor invisible
       curses.start_color()
       curses.use_default_colors()
       self.stdscr.keypad(True)    # handle keypad
       self.stdscr.nodelay(1)      # make getch() non-blocking


       self.height, self.width = self.stdscr.getmaxyx()


       # ask for a minimum size on the console before starting
       while self.height < self.TOTAL_HEIGHT or self.width < self.TOTAL_WIDTH:
           self.stdscr.addstr(0, 0, f"Please resize your console to at least {self.TOTAL_HEIGHT} wide and {self.TOTAL_WIDTH} tall")
           self.stdscr.addstr(1, 0, f"Console size is {self.width} x {self.height}")
           self.stdscr.getch()
           self.wait(0.2)
           self.stdscr.clear()
           self.height, self.width = self.stdscr.getmaxyx()
           self.stdscr.refresh()


       # make overall game window and the 3 sub-windows for header/game/message
       self.mainWindow = curses.newwin(self.TOTAL_HEIGHT, self.TOTAL_WIDTH, 0, 0)
       self.headerWindow = curses.newwin(self.HEADER_HEIGHT, self.WIDTH, 1, 1)
       self.gameWindow = curses.newwin(self.GAME_HEIGHT+2, self.TOTAL_WIDTH, self.HEADER_HEIGHT+1, 0)
       self.gameWindow.nodelay(1)
       self.msgWindow = curses.newwin(self.MSG_HEIGHT, self.WIDTH,
               self.TOTAL_HEIGHT-self.MSG_HEIGHT-1, 1)
       self.msgWindow.scrollok(True)
      
       # make a debug window next to the game windows
       self.dbgWindow = curses.newwin(self.TOTAL_HEIGHT - 1, self.DBG_WIDTH, 1, self.TOTAL_WIDTH + 1)
       self.dbgWindow.scrollok(True)       


       self.mainWindow.border()
       self.mainWindow.refresh()


       # draw the game boarders with the Tee's so that it looks nice inside the game border
       self.gameBorder()         


       global debug


       debug.ui = self


   def setAutoKeyInput(self, keyIn: list[str]):
       '''
       For test mode
       ex. setAutoKeyInput(['w-d','--kjkl'])
       '''
       self.keyIn = keyIn


   def setAutoAnswerQ(self, answers: list[str]):
       '''
       For test mode
       '''
       self.testAnswerQ = answers


   def setPauseMode(self, mode: bool):
       '''
       Enables a pause mode where a space can be used to stop play
       '''
       self.pauseMode = mode


   def getHeight(self) -> int:
       '''
       Returns the height of the Game window - it is better to call this method
       than to depend on the fact that it is 20 high.


       Returns:
           int: The height of the Game window
       '''
       return self.GAME_HEIGHT
  
   def getWidth(self) -> int:
       '''
       Returns the width of the Game window - it is better to call this method
       than to depend on the fact that it is 40 wide.


       Returns:
           int: The width of the Game window
       '''
       return self.WIDTH


   def getPlayerMove(self, playerNum: int = 1) -> str:
       '''
       Return the next move for ``playerNum``.
       Uses the playerKeyDef map that maps a key press to a
       move command string - like ``w`` -> ``u``. The ``UI`` class can be defined to look for
       keys associated with a player and return the move string associated with that key.


       If the player has not yet pressed a key, it will return ``None``.


       Args:
           playerNum (int): The player number - 1 or 2
       '''


       # Test Mode: use keyIn strings for input
       if self.keyIn != None:
           p = playerNum - 1
           keyInputStr = self.keyIn[p]
           key = keyInputStr[0:1]          # get next ch from input string
           self.keyIn[p] = keyInputStr[1:] # remove ch from input string
           if key in self.playerKeyDef[p]:
               return(self.playerKeyDef[p][key])
           else:
               return None


       # Normal user key input - gather any key inputs into a player input Q
       p = playerNum - 1
       ch = self.gameWindow.getch(1,1)
       while ch != -1:


           # pause on ' '
           if self.pauseMode and chr(ch) == ' ':
               self.waitForKey()


           if chr(ch) in self.playerKeyDef[p]:
               move = self.playerKeyDef[p][chr(ch)]
               # ignore auto-repeat of a key press when a key is held down
               if len(self.playerMoves[p]) == 0 or move != self.playerMoves[p][-1]:
                   self.playerMoves[p].append(move)
         
           ch = self.gameWindow.getch(1,1)
      
       # get next player move from queue
       if len(self.playerMoves[p]) == 0:
           return None
       else:
           return self.playerMoves[p].pop(0)


   def getKey(self):
       if self.testMode:
           return


       return self.gameWindow.getch()


   def setPlayerKeyMap(self, playerNum: int, keyDefs: list[ tuple[str, str] ]):
       '''
       Define a set of key mappings for each player.
       For example, [ ('q', 'q'), ('d', 'r'), ('w', 'u') ] defines three key mappings for
       the player.


       Args:
           playerNum (int): The player number
           keyDefs ([list[ tuple(str, str)]]): List of a key mappings
       '''
       p = playerNum - 1
       for (key, what) in keyDefs:
           if key not in self.playerKeyDef[p]:
               self.playerKeyDef[p][key] = what


   def resetWindows(self):
       '''
       Clears out the Game and Message windows. Redraws borders nicely.
       Keep the message window with whatever was already there.
       '''
       if self.testMode:
           return


       self.clearHeaderWindow()
       self.clearGameWindow()
       self.gameBorder()
       self.clearMsgWindow()


   def clearMainWindow(self):
       if self.testMode:
           return


       self.mainWindow.clear()
       self.mainWindow.refresh()


   def clearHeaderWindow(self) -> None:
       '''
       Clears out the header window
       '''
       if self.testMode:
           return


       self.headerWindow.clear()
       self.headerWindow.refresh()


   def clearGameWindow(self) -> None:
       '''
       Clears out the Game window
       '''
       if self.testMode:
           return


       self.clearRect(self.gameWindow, 1, 1, self.GAME_HEIGHT, self.WIDTH)


   def clearMsgWindow(self) -> None:
       '''
       Clears out the message window
       '''
       self.msgWindow.clear()
       self.msgWindow.refresh()


   def clearLine(self, y: int) -> None:
       '''
       Clears the indicated line


       Args:
           y (int): The line to clear from 1 to GAME_HEIGHT
       '''
       if self.testMode:
           return


       if y < 1 or y > self.GAME_HEIGHT:
           return


       self.gameWindow.addstr(y, 1, ' '* self.WIDTH)
       self.gameWindow.refresh()


   def clearRect(self, win, start_y, start_x, height, width):
       if self.testMode:
           return


       for y in range(start_y, start_y + height):
           win.addstr(y, start_x, ' ' * width)
       win.refresh()


   def gameBorder(self) -> None:
       if self.testMode:
           return


       self.gameWindow.border()
       maxX = self.gameWindow.getmaxyx()[1] - 1
       maxY = self.gameWindow.getmaxyx()[0] - 1
       self.gameWindow.addch(0, 0, curses.ACS_LTEE)
       self.gameWindow.addch(maxY, 0, curses.ACS_LTEE)
       self.gameWindow.addch(0, maxX, curses.ACS_RTEE)
       self.gameWindow.insch(maxY, maxX, curses.ACS_RTEE)
       self.gameWindow.refresh()


   def writeDebug(self, *args) -> None:
       if self.testMode:
           return


       self.dbgWindow.addstr(" ".join(str(x) for x in args) + "\n")
       self.dbgWindow.refresh()


   def writeStr(self, s: str, x: int, y: int) -> None:
       '''
       Writes a character (or string) to the Game window buffer at (x, y).
       It does not draw it to the screen, so a ``updateGameWindow()`` call needs to
       be done to display it to actually see it on the screen.


       Args:
           s (str): The string to write
           x (int): The x position to write - 1 to ``getWidth()``
           y (int): The y position to write - 1 to ``getHeight()``
       '''
       if self.testMode:
           for i, ch in enumerate(s):
               self.fakeGameWindow[y][x + i] = ch
           return


       self.gameWindow.addstr(y, x, s)


   def getGameWinCh(self, x: int, y: int) -> str:
       '''
       Test Mode feature to return the character at position x, y
       '''
       return self.fakeGameWindow[y][x]


   def updateGameWindow(self) -> None:
       '''
       Draw the changes to the Game window made by ``writeStr()``.
       '''
       if self.testMode:
           return


       self.gameWindow.refresh()


   def wait(self, sec) -> None:
       '''
       Wait for sec seconds
      
       Args:
           sec (int): seconds to wait
       '''
       if self.testMode:
           return


       time.sleep(sec)


   def waitForKey(self) -> None:
       if self.testMode:
           return


       while self.stdscr.getch() == -1:
           pass


   def writeHeaderMsg(self, text: str) -> None:
       '''
       Write the text message to the Header window.
       '''
       if self.testMode:
           return


       self.headerWindow.addstr(text)
       self.headerWindow.refresh()


   def writeMsg(self, text: str) -> None:
       '''
       Write ``text`` message to the message window.
       It will automatically add a '\\\\n' and go to the next line of the message window.
       The message window scrolls automatically. It is somewhat like a ``print()`` function,
       but it can only accept a single string as an input.
       '''
       if self.testMode:
           return


       self.msgWindow.addstr(text + '\n')
       self.msgWindow.refresh()


   def askMsg(self, prompt: str) -> str:
       '''
       Write out a prompt to the Message window and wait for the user to type in a response.
       Return the response string.


       Similar in use to the console's ``input()`` function but for this UI window framework.
       '''


       # Test Mode - get answer from the answer queue
       if self.testAnswerQ != None:
           answer = self.testAnswerQ.pop(0)
           return answer


       # clear out the key presses before prompting
       while self.stdscr.getch() != -1:
           pass


       # Normal Mode
       self.msgWindow.addstr(prompt + " ")
       curses.curs_set(1)          # make cursor visible
       curses.echo()
       self.msgWindow.nodelay(0)   # wait for the <ENTER>


       userInput = self.msgWindow.getstr().decode('utf-8')


       curses.curs_set(0)          # make cursor invisible again
       curses.noecho()
       self.msgWindow.nodelay(1)


       return userInput


   def writePlayerNames(self, n1: str, n2: str) -> None:
       '''
       Write ``n1`` / ``n2`` names to the Header window with spacing that allows for the score
       to be next to the names


       Args:
           n1 (str): Player 1 name
           n2 (str): Player 2 name
       '''
       if self.testMode:
           return


       self.headerWindow.addstr(0, 7, n1)
       self.headerWindow.addstr(0, self.WIDTH - 7 - len(n2), n2)
       self.headerWindow.refresh()


   def writeScore(self, pNum: int, score: int) -> None:
       '''
       Write the score of player pNum into the Header window.
       Player 1 appears on the left and player 2 score appears on the right.
       If the score is bigger than 99999 it will not display nicely...


       Args:
           pNum (int): Player number
           score (int): Score to write
       '''
       if self.testMode:
           return


       if pNum == 1:
           self.headerWindow.addstr(0, 1, str(score).rjust(5, " "))
       elif pNum == 2:
           self.headerWindow.addstr(0, self.WIDTH - 6, str(score).rjust(5, " "))
       self.headerWindow.refresh()


      





