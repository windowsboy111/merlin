from mcstatus import MinecraftServer
import discord

# constant variables!!!
mcarglist=["minecraft","Minecraft","MINECRAFT","mc","Mc","MC"]  #The args you type in order to indicate you wanna get minecraft info
mcserverarglist=["srv","Srv","SRV","Server","server","SERVER"]  #The args you type in order to indicate you wanna get minecraft servers info
hlp=["Help","help","hlp","HELP"]                                #The args you type in order to indicate you wanna get help

# user-defined exceptions
class Error(Exception):
   """Base class for other exceptions"""
   pass
class InvalidArgument(Error):
    """Argument passed from the command line is invalid"""
    pass

def chkmcsrvstatus():
    try:
        temp = MinecraftServer.lookup("kccscomm.minehut.gg:25565")
        statuskccscomm = "online"
    except OSError:
        statuskccscomm = "offline"
    try:
        temp = MinecraftServer.lookup("lopxl.aternos.me")
        statuslopxl = "online"
    except OSError:
        statuslopxl = "offline"
    try:
        temp = MinecraftServer.lookup("lopx.minehut.gg")
        statuslopx = "online"
    except OSError:
        statuslopx = "offline"
    try:
        temp = MinecraftServer.lookup("116kccs.aternos.me")
        status116 = "online"
    except OSError:
        status116 = "offline"
    try:
        temp = MinecraftServer.lookup("sb4kccs.aternos.me")
        statussb4 = "online"
    except OSError:
        statussb4 = "offline"
    try:
        temp = MinecraftServer.lookup("smpkccs.aternos.me")
        statussmp = "online"
    except OSError:
        statussmp = "offline"
        temp += ""
    return {"statuskccscomm":statuskccscomm,"statuslopxl": statuslopxl,"statuslopx":statuslopx,"status116": status116,"statussb4": statussb4,"statussmp": statussmp}
def mc(embed,argv):
    global hlp
    rtrn = ""
    global mcserverarglist  #chk srv arg
    global tmp
    args = argv.split(" ")
    if args[0] in hlp:
        rtrn = 'Args: help, server\n'
        return rtrn
    elif args[0] in mcserverarglist:
        try:
            if args[1]:
                if args[1] == "kccscomm":
                    link = "kccscomm.minehut.gg"
                    name = "KCCS Community Survival Server"
                    note = "Recommened Survival Server"
                elif args[1] == "lopx":
                    link = "lopx.minehut.gg"
                    name = "Lopixel on Minehut"
                    note = "Help build the minigames server!"
                elif args[1] == "lopxl":
                    link = "lopxl.aternos.me"
                    name = "Lopixel on Aternos"
                    note = "Help build the minigames server!"
                elif args[1] == "116kccs":
                    link = "116kccs.aternos.me"
                    name = "1.16 Survival Server for KCCS"
                    note = "Snapshot version "
                elif args[1] == "sb4kccs":
                    link = "sb4kccs.aternos.me"
                    name = "Skyblock for KCCS"
                    note = "Ruined :("
                elif args[1] == "smpkccs":
                    link = "smpkccs.aternos.me"
                    name = "No Cheat Survival Multiplayer"
                    note = "NO CHEATING"
                elif args[1] == "hypixel":
                    link = "mc.hypixel.net"
                    name = "Hypixel Network"
                    note = "Best Minecraft Server Ever!"
                elif args[1] == "earthmc":
                    link = "earthmc.net"
                    name = "EarthMC"
                    note = "A towny server"
                elif args[1] == "pvpwars":
                    link = "pvpwars.net"
                    name = "PvpWars"
                    try:
                        note = MinecraftServer(link).query().motd
                    except OSError as e:
                        note = str(e)
                else:
                    link = args[1]
                    name = args[1]
                    try:
                        note = MinecraftServer(link).query().motd
                    except OSError as e:
                        note = str(e)
                try:
                    tmp=MinecraftServer(args[1]).query()
                    status="online"
                    players=tmp.players.online
                    playerls=tmp.players.names
                except OSError as e:
                    status="offline"
                    players=0
                    playerls=[str(e)]
                except KeyError as e:
                    raise InvalidArgument("Invalid server id: " + str(e))
                try:
                    ping=str(MinecraftServer(link).ping()) + " ms"
                except OSError as e:
                    ping=str(e)
                embed = discord.Embed(title="Minecraft KCCS Official",description="")
                embed.add_field(name = "Server name: ", value=name, inline=True)
                embed.add_field(name = "Server link: ", value=link, inline=True)
                embed.add_field(name = "Server status: ", value=status, inline=True)
                embed.add_field(name = "Note: ", value=note, inline=True)
                embed.add_field(name = "Latency (Ping): ", value=ping, inline=True)
                embed.add_field(name = "Number of players: ", value=players, inline=True)
                embed.add_field(name = "Players Online: ", value=", ".join(playerls), inline=True)
                return embed
            else:
                raise InvalidArgument("Invalid argument \"" + args[1] + "\" for the third argument.")
        except IndexError:
            pass
        mcsrvstatus = chkmcsrvstatus()
        mcsrvlis = {"kccscomm": {
                        "name":             "KCCS Community",
                        "link":             "kccscomm.minehut.gg",
                        "status":           mcsrvstatus["statuskccscomm"],
                        "note":             "Recommened"
                    },
                    "lopxl":{
                        "name":             "Lopixel on Aternos",
                        "link":             "lopxl.aternos.me",
                        "status":           mcsrvstatus["statuslopxl"],
                        "note":             "Inactive"
                    },
                    "lopx":{
                        "name":             "Lopixel on Minehut",
                        "link":             "lopx.minehut.gg",
                        "status":           mcsrvstatus["statuslopx"],
                        "note":             "Ignored"
                    },
                    "116kccs":{
                        "name":             "1.16 server for KCCS",
                        "link":             "116kccs.aternos.me",
                        "status":           mcsrvstatus["status116"],
                        "note":             "Active"
                    },
                    "sb4kccs":{
                        "name":             "Skyblock for KCCS",
                        "link":             "sb4kccs.aternos.me",
                        "status":           mcsrvstatus["statussb4"],
                        "note":             "Ruined"
                    },
                    "smpkccs":{
                        "name":             "Survival Multiplayer",
                        "link":             "smpkccs.aternos.me",
                        "status":           mcsrvstatus["statussmp"],
                        "note":             "Active, NO CHEATING"
                    }
        }
        rtrn += "Name\t\t\t\tLink\t\t\t\tStatus\n"
        for srv in mcsrvlis:                        #print the stuff in the outer dict
            for key in mcsrvlis[srv]:               #print the value from the key with a for-loop in the inter dict
                rtrn += str(mcsrvlis[srv][key]) + "\t\t"
                if mcsrvlis[srv][key] in ["KCCS Community", "lopx.minehut.gg"]:
                    rtrn += "\t"
            rtrn += "\n"
        rtrn += "\n"
        embed = discord.Embed(title="Minecraft Servers", description=rtrn)
        return embed