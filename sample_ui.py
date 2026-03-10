from gamedata import GameData
from ui import UI
from player import Player
from ui import debug
import curses

def main(stdscr):
    '''
    You can play around with the UI and Data objects here.
    '''

    ui = UI()
    data = GameData()

    ui.writeMsg("Hello World!!")
    ui.writeStr("Press a key...", 2, 5)
    ui.updateGameWindow()

    debug("Hi, you can print debug messages using debug()")
    debug("Instead of print(), use debug()!!!")

    # Try out other UI methods!!!
    debug("\nTry other UI methods just to see it work")


    ui.waitForKey()

curses.wrapper(main)

