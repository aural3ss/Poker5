import curses
from ui import debug

from pokercard import PokerCard
from pokerhand import PokerHand
from pokerplayer import PokerPlayer
from pokerdata import PokerData
from pokerui import PokerUI

'''
This is a template file for testing ABC functionality of the Poker game.
You can make different test files to test different classes or functions.
'''

def test(stdscr):
    # Write your test code here
    pass

if __name__ == "__main__":
    curses.wrapper(test)

def main(stdscr):
    ui = PokerUI()

    data = PokerData()
    data.makePlayer(1, "Mary", 100)
    data.makePlayer(2, "Joe", 100)


    card = PokerCard('A', '♥')
    for i in range(5):          # just add the same card 5 times into each player
        data.getPlayer(1).addCard(card)
        data.getPlayer(2).addCard(card)

    ui.initPokerRound(data)

    ui.holdCard(1, 1)           # an H should appear for player 1 over card 1
    ui.wait(0.5)
    ui.holdCard(2, 5)           # an H should appear for player 2 over card 5
    ui.waitForKey()             # wait for a key press so you can see the board above

    ui.waitForKey()             # wait for a key press so you can see the board above

if __name__ == "__main__":
    curses.wrapper(main)