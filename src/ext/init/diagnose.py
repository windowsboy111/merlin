class _Getch:
    """Gets a single character from standard input.  Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()


def main():
    print("This python script diagnoses why merlin does not work properly for you")
    print("to continue, press y.")
    ch = getch()
    if ch not in ['y', 'Y']:
        return 2
    try:
        import ext
    except ImportError:
        print("cannot import ext. be sure you run the script in the src/ directory of the repository.")
    try:
        import easteregg
    except ImportError:
        print("cannot import easteregg external python module. you have to create an easteregg.py file and include an async `easter(msg: discord.Message)' function.")
    try:
        import discord
        import duckduckgo
        import psutil
        import dotenv
        import pytablemaker
        import chatterbot
        import chatterbot_corpus
        import mcstatus
        import numpy
        import flask
    except:
        print("Please run the following command and try again: pip install --requirement requirement.txt")
    print("no errors found.")

if __name__ == '__main__':
    main()