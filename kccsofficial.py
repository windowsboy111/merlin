from mcstatus import MinecraftServer
import sys, os
from termcolor import colored, cprint
from kccsofficialmc import mc,mcarglist,hlp,InvalidArgument
from consolemod import style

def clearscreen(): 
    # for windows 
    if os.name == 'nt': 
        _ = os.system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = os.system('clear') 
clearscreen()
print("\033[34m=============================KCCS OFFICIAL=============================\033[0m")

#colors
if sys.platform.lower() == "win32":
    os.system('color')



# functions
def help():
    print(style.grey('To show help, run ' + style.italic("kccsofficial [args] help") + style.reset()) + style.grey('\nTo show minecraft info, run ' + style.italic("kccsofficial minecraft [args]") + "." + style.reset()))
    return 0





# Main section.  Program officially start from here.
try:
    if sys.argv[1] in mcarglist:                                                          #if user indicate minecraft
        print(mc(sys.argv[2:]))
        sys.exit(0)
    elif sys.argv[1] in hlp:                                                              #user indicate help
        print(help())
        sys.exit(0)
    else:
        raise InvalidArgument(("First argument " + style.underline("\"{0}\"") + style.end() + style.red2(" is invalid")).format(sys.argv[1]))
except InvalidArgument as e:
    print(style.red("Error 2: Invalid Argument.  Program terminated.\n") + style.end() + style.red2("Details:  " + str(e)) + style.end())
    print(style.italic(style.grey("To get the usage, include the \"help\" arguments, i.e. \"kccsofficial help\"") + style.reset()))
    sys.exit(2)
except IndexError as e:
    print(style.red("Error 3: IndexError.  " + style.underline("Did you input any arguments?")) + style.reset())
    print(style.grey("To get the usage, include the ") + style.bold("\"help\"") + style.reset() + style.grey(" arguments, i.e. ") + style.bold("\"kccsofficial help\"") + style.reset())
    sys.exit(3)
except Exception as e:
    if e in ["timed out","Server did not respond with any information!"]:
        print(style.red2("Error 4: Runtime Error.  Program terminated.\n" + style.red() + "Details:  " + str(e)) + style.reset())
    else:
        print(style.red(style.bold(style.blink("Error 1: Unknown Error.  Program terminated.\nDetails:  " + str(e)))) + style.reset())
    sys.exit(1)