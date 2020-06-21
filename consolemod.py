class cursor():
    def position(self,line,column):
        """Move cursor to specified position"""
        print("\033[{line};{column}f".format(line=line,column=column))
    def up(self,lines):
        """Move cursor up specified number of lines"""
        print("\033[{lines}A")
    def down(self,lines):
        """Move cursor down specified number of lines"""
        print("\033[{lines}B")
    def left(self,columns):
        """Move cursor left specified number of columns"""
        print("\033[{columns}C")
    def right(self,columns):
        """Move cursor right specified number of columns"""
        print("\033[{columns}D")
    def cls(self):
        """Clears the screen, and move cursor to 0,0"""
        print("\033[2J")
    def eraseline(self):
        """Erase the whole line (till the end of line)"""
        print("\033[2J")
    def savepos(self):
        """Save current cursor position"""
        print("\033[s")
    def restorepos(self):
        """Restore the saved cursor position"""
        print("\033[u")
class style():
    magenta    = lambda x="": '\33[35m' + str(x)
    cyan       = lambda x="": '\33[36m' + str(x)
    underline  = lambda x="": '\33[4m' + str(x)
    reset      = lambda x="": '\33[0m' + str(x)
    end        = lambda x="": '\33[0m' + str(x)
    bold       = lambda x="": '\33[1m' + str(x)
    italic     = lambda x="": '\33[3m' + str(x)
    url        = lambda x="": '\33[4m' + str(x)
    blink      = lambda x="": '\33[5m' + str(x)
    blink2     = lambda x="": '\33[6m' + str(x)
    selected   = lambda x="": '\33[7m' + str(x)

    black      = lambda x="": '\33[30m' + str(x)
    red        = lambda x="": '\33[31m' + str(x)
    green      = lambda x="": '\33[32m' + str(x)
    yellow     = lambda x="": '\33[33m' + str(x)
    blue       = lambda x="": '\33[34m' + str(x)
    violet     = lambda x="": '\33[35m' + str(x)
    beige      = lambda x="": '\33[36m' + str(x)
    white      = lambda x="": '\33[37m' + str(x)

    blackbg    = lambda x="": '\33[40m' + str(x)
    redbg      = lambda x="": '\33[41m' + str(x)
    greenbg    = lambda x="": '\33[42m' + str(x)
    yellowbg   = lambda x="": '\33[43m' + str(x)
    bluebg     = lambda x="": '\33[44m' + str(x)
    violetbg   = lambda x="": '\33[45m' + str(x)
    beigebg    = lambda x="": '\33[46m' + str(x)
    whitebg    = lambda x="": '\33[47m' + str(x)

    grey       = lambda x="": '\33[90m' + str(x)
    red2       = lambda x="": '\33[91m' + str(x)
    green2     = lambda x="": '\33[92m' + str(x)
    yellow2    = lambda x="": '\33[93m' + str(x)
    blue2      = lambda x="": '\33[94m' + str(x)
    violet2    = lambda x="": '\33[95m' + str(x)
    beige2     = lambda x="": '\33[96m' + str(x)
    white2     = lambda x="": '\33[97m' + str(x)

    greybg     = lambda x="": '\33[100m' + str(x)
    redbg2     = lambda x="": '\33[101m' + str(x)
    greenbg2   = lambda x="": '\33[102m' + str(x)
    yellowbg2  = lambda x="": '\33[103m' + str(x)
    bluebg2    = lambda x="": '\33[104m' + str(x)
    violetbg2  = lambda x="": '\33[105m' + str(x)
    beigebg2   = lambda x="": '\33[106m' + str(x)
    whitebg2   = lambda x="": '\33[107m' + str(x)