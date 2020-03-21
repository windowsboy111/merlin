from mcstatus import MinecraftServer
import sys, os
from termcolor import colored, cprint

# user-defined exceptions
class Error(Exception):
   """Base class for other exceptions"""
   pass
class InvalidArgument(Error):
    """Argument passed from the command line is invalid"""
    pass

# constant variables!!!
mcarglist=["minecraft","Minecraft","MINECRAFT","mc","Mc","MC"]  #The args you type in order to indicate you wanna get minecraft info
mcserverarglist=["srv","Srv","SRV","Server","server","SERVER"]  #The args you type in order to indicate you wanna get minecraft servers info
hlp=["Help","help","hlp","HELP"]                                #The args you type in order to indicate you wanna get help
#colors
if sys.platform.lower() == "win32":
    os.system('color')

# Group of Different functions for different styles
class style():
    black      = lambda x="": '\033[30m' + str(x)
    red        = lambda x="": '\033[31m' + str(x)
    green      = lambda x="": '\033[32m' + str(x)
    yellow     = lambda x="": '\033[33m' + str(x)
    blue       = lambda x="": '\033[34m' + str(x)
    magenta    = lambda x="": '\033[35m' + str(x)
    cyan       = lambda x="": '\033[36m' + str(x)
    white      = lambda x="": '\033[37m' + str(x)
    underline  = lambda x="": '\033[4m' + str(x)
    reset      = lambda x="": '\033[0m' + str(x)
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


# functions
def help():
    print(style.grey('To show help, run ' + style.italic("kccsofficial [args] help") + style.reset()) + style.grey('\nTo show minecraft info, run ' + style.italic("kccsofficial minecraft [args]") + "." + style.reset()))
    return 0


def chkmcsrvstatus():
    global hlp
    try:
        temp = MinecraftServer.lookup("kccscomm.minehut.gg:25565").status()
        statuskccscomm = "online"
        playerskccscomm = temp.players.online
    except OSError:
        statuskccscomm = "offline"
        playerskccscomm = 0
    try:
        temp = MinecraftServer.lookup("lopxl.aternos.me").status()
        statuslopxl = "online"
        playerslopxl = temp.players.online
    except OSError:
        statuslopxl = "offline"
        playerslopxl = 0
    try:
        temp = MinecraftServer.lookup("lopx.minehut.gg").status()
        statuslopx = "online"
        playerslopx = temp.players.online
    except OSError:
        statuslopx = "offline"
        playerslopx = 0
    try:
        temp = MinecraftServer.lookup("116kccs.aternos.me").status()
        status116 = "online"
        players116 = temp.players.online
    except OSError:
        status116 = "offline"
        players116 = 0
    try: 
        temp = MinecraftServer.lookup("sb4kccs.aternos.me").status()
        statussb4 = "online"
        playerssb4 = temp.players.online
    except OSError:
        statussb4 = "offline"
        playerssb4 = 0
    try:
        temp = MinecraftServer.lookup("smpkccs.aternos.me").status()
        statussmp = "online"
        playerssmp = temp.players.online
    except OSError:
        statussmp = "offline"
        playerssmp = 0
    return {"statuskccscomm":statuskccscomm,
            "playerskccscomm": playerskccscomm,
            "statuslopxl": statuslopxl,
            "playerslopxl": playerslopxl,
            "statuslopx":statuslopx,
            "playerslopx": playerslopx,
            "status116": status116,
            "players116": players116,
            "statussb4": statussb4,
            "playerssb4": playerssb4,
            "statussmp": statussmp,
            "playerssmp": playerssmp}


def mc():
    global mcserverarglist  #chk srv arg

    if sys.argv[2] in mcserverarglist:
        mcsrvstatus = chkmcsrvstatus()

        mcsrvlis = {"kccscomm": {
                        "name":             "KCCS Community",
                        "link":             "kccscomm.minehut.gg",
                        "status":           mcsrvstatus["statuskccscomm"],
                        "playersOnline":    mcsrvstatus["playerskccscomm"],
                        "note":             "Recommened"
                    },
                    "lopxl":{
                        "name":             "Lopixel on Aternos",
                        "link":             "lopxl.aternos.me",
                        "status":           mcsrvstatus["statuslopxl"],
                        "playersOnline":    mcsrvstatus["playerslopxl"],
                        "note":             "Inactive"
                    },
                    "lopx":{
                        "name":             "Lopixel on Minehut",
                        "link":             "lopx.minehut.gg",
                        "status":           mcsrvstatus["statuslopx"],
                        "playersOnline":    mcsrvstatus["playerslopx"],
                        "note":             "Ignored"
                    },
                    "116kccs":{
                        "name":             "1.16 server for KCCS",
                        "link":             "116kccs.aternos.me",
                        "status":           mcsrvstatus["status116"],
                        "playersOnline":    mcsrvstatus["players116"],
                        "note":             "Active"
                    },
                    "sb4kccs":{
                        "name":             "Skyblock for KCCS",
                        "link":             "sb4kccs.aternos.me",
                        "status":           mcsrvstatus["statussb4"],
                        "playersOnline":    mcsrvstatus["playerssb4"],
                        "note":             "Ruined"
                    },
                    "smpkccs":{
                        "name":             "Survival Multiplayer",
                        "link":             "smpkccs.aternos.me",
                        "status":           mcsrvstatus["statussmp"],
                        "playersOnline":    mcsrvstatus["playerssmp"],
                        "note":             "Active, NO CHEATING"
                    }
        }
        try:
            try:
                playerls=MinecraftServer(mcsrvlis[sys.argv[3]]["link"]).query().players.names
            except OSError as e:
                playerls=[str(e)]
            except KeyError as e:
                raise InvalidArgument("Invalid server id: " + str(e))
            if sys.argv[3] in mcsrvlis:
                if mcsrvlis[sys.argv[3]]["status"]=="offline":
                    players="No players!"
                elif playerls == []:
                    players="No players!"
                else:
                    try:
                        players=", ".join(MinecraftServer(mcsrvlis[sys.argv[3]]["link"]).query().players.names)
                    except OSError as e:
                        players=str(e)
                try:
                    ping=str(MinecraftServer(mcsrvlis[sys.argv[3]]["link"]).ping()) + " ms"
                except OSError as e:
                    ping=str(e)
                print((style.yellow("Server name:\t\t")         + style.green("{0}\n") 
                        + style.yellow("Server link:\t\t")      + style.green("{1}\n") 
                        + style.yellow("Server status:\t\t")    + style.green("{2}\n") 
                        + style.yellow("Note:\t\t\t")           + style.green("{3}\n") 
                        + style.yellow("Latency (Ping):\t\t")   + style.green("{4}\n") 
                        + style.yellow("Number of players:\t")  + style.green("{5}\n") 
                        + style.yellow("Players Online:\t\t")   + style.green("{6}\n") + style.reset())
                    .format(mcsrvlis[sys.argv[3]]["name"],      #format it with the stuff from mcsrvlis and minecraft servers libraries
                            mcsrvlis[sys.argv[3]]["link"],
                            mcsrvlis[sys.argv[3]]["status"],
                            mcsrvlis[sys.argv[3]]["note"],          
                            ping,
                            mcsrvlis[sys.argv[3]]["playersOnline"],
                            players))
                return 0
            else:
                raise InvalidArgument("Invalid argument \"" + sys.argv[3] + "\" for the third argument.")
        except IndexError:
            pass
        print(style.black(style.greenbg2("Name                            Link                            Status")) + style.reset() + style.blue2())
        for srv in mcsrvlis:                        #print the stuff in the outer dict
            for key in mcsrvlis[srv]:               #print the value from the key with a for-loop in in the inter dict
                if key in ["playersOnline","note"]:
                    continue
                print(str(mcsrvlis[srv][key]) + "\t\t", end="")
                if mcsrvlis[srv][key] in ["KCCS Community", "lopx.minehut.gg"]:
                    print("\t",end="")
            print()
        print(style.reset())
        return 0
    elif sys.argv[2] in hlp:
        print(style.grey('Args: ' + style.italic('help, server')) + style.reset())





# Main section.  Program officially start from here.
print(style.blue("\n=============================KCCS OFFICIAL=============================") + style.reset())
try:
    if sys.argv[1] in mcarglist:                                                          #if user indicate minecraft
        sys.exit(mc())
    elif sys.argv[1] in hlp:                                                              #user indicate help
        sys.exit(help())
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