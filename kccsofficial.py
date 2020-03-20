from mcstatus import MinecraftServer
import sys

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


# functions
def help():
    print('To show help, run "kccsofficial [args] help"\nTo show minecraft info, run "kccsofficial minecraft [args]"')



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
            if sys.argv[3] in mcsrvlis:
                print(mcsrvlis[sys.argv[3]])
                return 0
            else:
                raise InvalidArgument("Invalid argument \"" + sys.argv[3] + "\" for the third argument.")
        except IndexError:
            pass
        print("Name\t\t\t\tLink\t\t\t\tStatus")
        for srv in mcsrvlis:                        #print the stuff in the outer dict
            for key in mcsrvlis[srv]:               #print the value from the key with a for-loop in in the inter dict
                if key in ["playersOnline","note"]:
                    continue
                print(str(mcsrvlis[srv][key]) + "\t\t", end="")
                if mcsrvlis[srv][key] in ["KCCS Community", "lopx.minehut.gg"]:
                    print("\t",end="")
            print("")
        return 0
    elif sys.argv[2] in hlp:
        print('Args: help, server')


# Main section.  Program officially start from here.
print("====================KCCS OFFICIAL====================")
try:
    if sys.argv[1] in mcarglist:                                                          #if user indicate minecraft
        sys.exit(mc())
    elif sys.argv[1] in hlp:                                                              #user indicate help
        sys.exit(help())
    else:
        raise InvalidArgument
except InvalidArgument as e:
    print("Error 2: Invalid Argument.  Program terminated.\nDetails:  " + str(e))
    print("To get the usage, include the \"help\" arguments, i.e. \"kccsofficial help\"")
    sys.exit(2)
except IndexError as e:
    print("Error 3: IndexError.  Did you input any arguments?\nDetails:  " + str(e))
    print("To get the usage, include the \"help\" arguments, i.e. \"kccsofficial help\"")
    sys.exit(3)
except Exception as e:
    print("Error 1: Unknown Error.  Pragram terminated.  Details:  " + str(e))
    sys.exit(1)