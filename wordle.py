#!/usr/bin/env python3
"""
A simple python3 template with just a main function.
"""

from __future__ import annotations
import curses
import logging
import random
import possible_words

GREEN = 1
YELLOW = 2
CYAN = 3
RED = 4

KEYBOARD = ("q w e r t y u i o p\n"
            " a s d f g h j k l \n"
            "   z x c v b n m   ")


def play_wordle(stdscr: curses._CursesWindow) -> int:
    """
    Function to actually start the game of Wordle in the terminal
    """
    FORMAT = '[%(levelname).4s %(asctime)s] %(message)s'
    logging.basicConfig(filename='test.out', filemode='w', datefmt='%H:%M:%S',
                        level=logging.DEBUG, format=FORMAT)
    logger = logging.getLogger(__name__)

    word_list = possible_words.get_word_list()
    word = random.choice(word_list)

    if curses.has_colors():
        curses.use_default_colors()
        curses.init_pair(GREEN, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(YELLOW, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(CYAN, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(RED, curses.COLOR_BLACK, curses.COLOR_RED)

    guesses = []
    guess = ""
    letters_guessed = set()

    # Cursor coords
    x = 0
    y = 0

    while True:
        stdscr.clear()

        # Cursor coords
        y = 0

        # stdscr.addstr(y, 0, f"The word of the day is: {word}")
        logger.debug(f"{word=}")
        y += 2

        # Print previous guesses (colorized)
        for g in guesses:
            # Figure out which characters are in the right place or not
            available_letters = list(word)
            for idx, ltr in enumerate(g):
                logger.debug(f"{available_letters=}")
                logger.debug(f"comparing {ltr} to {word[idx]}")
                if ltr == word[idx]:
                    logger.debug(f"{ltr} == {word[idx]}  removing {ltr} from {available_letters}")
                    stdscr.addch(y, idx, ltr, curses.color_pair(GREEN))
                    letters_guessed.add((ltr, GREEN))
                    available_letters.remove(ltr)
                elif ltr in available_letters:
                    logger.debug(f"{ltr} in {word}  removing {ltr} from {available_letters}")
                    stdscr.addch(y, idx, ltr, curses.color_pair(YELLOW))
                    letters_guessed.add((ltr, YELLOW))
                    available_letters.remove(ltr)
                else:
                    logger.debug(f"{ltr} not in {word}")
                    stdscr.addch(y, idx, ltr)
                    letters_guessed.add((ltr, RED))
                logger.debug("")
            y += 2

        # If we reach 6 guesses, print endgame
        if len(guesses) == 6 or (guesses and guesses[-1] == word):
            if word not in guesses:
                stdscr.addstr(y, 0, "YOU BAD!", curses.color_pair(RED))
                stdscr.addstr(y+1, 0, "Press any key to continue...", curses.color_pair(RED))
                stdscr.get_wch()
                return 0
            else:
                stdscr.addstr(y, 0, "Winner winner chicken dinner!", curses.color_pair(CYAN))
                stdscr.addstr(y+1, 0, "Press any key to continue...", curses.color_pair(CYAN))
                stdscr.get_wch()
                return 0

        # Print line for user guess
        stdscr.addstr(y, 0, guess)
        for f in range(5):
            stdscr.chgat(y, 0 + f, 1, curses.A_UNDERLINE)
        user_input_x = x
        user_input_y = y

        # Print keyboard under line
        y += 2
        for row in KEYBOARD.splitlines():
            # logger.debug(f"{row=}")
            for idx, key in enumerate(row):
                # logger.debug(f"scanning for {key} in {letters_guessed}")
                gsd_tpl = [item for item in letters_guessed if key in item]
                # logger.debug(f"{gsd_tpl=}")
                if gsd_tpl:
                    stdscr.addch(y, idx, gsd_tpl[0][0], curses.color_pair(gsd_tpl[0][1]))
                else:
                    stdscr.addch(y, idx, key)
            y += 1

            # Get user guess and control cursor
        stdscr.move(user_input_y, user_input_x)
        letter = stdscr.get_wch()
        logger.debug(f"{letter=}")

        # Evaluate keyboard input
        if letter == '\n' and len(guess) == 5 and guess in word_list:
            guesses.append(guess)
            guess = ""
            x = 0
            continue
        elif letter == curses.KEY_BACKSPACE:
            if guess and x > 0:
                guess = guess[:-1]
                x -= 1
                stdscr.move(y, x)
        elif letter.isalpha() and len(guess) < 5:
            guess += letter.lower()
            x += 1
            stdscr.move(y, x)

        # Exit game on "1" or "ESC" key
        if letter == '1' or letter == '\x1b':
            return 0

        # REDRAW


def main() -> int:
    curses.wrapper(play_wordle)


if __name__ == '__main__':
    raise SystemExit(main())
