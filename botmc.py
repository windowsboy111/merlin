from mcstatus import MinecraftServer
import discord
from logcfg import logger

# constant variables!!!
mcserverarglist=["srv","Srv","SRV","Server","server","SERVER"]  #The args you type in order to indicate you wanna get minecraft servers info
hlp=["Help","help","hlp","HELP"]                                #The args you type in order to indicate you wanna get help

# user-defined exceptions
class Error(Exception):
   """Base class for other exceptions"""
   pass
class InvalidArgument(Error):
    """Argument passed from the command line is invalid"""
    pass
class OfflineServer(Error):
    """The specified minecraft server has been detected as offline"""
    pass

def chkmcsrvstatus():
    logger.info("Started chkmcsrvstatus(), try-excepting if servers are online...")
    try:
        temp = MinecraftServer.lookup("kccscomm.minehut.gg:25565").status()
        statuskccscomm = "online"
    except OSError:
        statuskccscomm = "offline"
    try:
        temp = MinecraftServer.lookup("lopxl.aternos.me").status()
        statuslopxl = "online"
    except OSError:
        statuslopxl = "offline"
    try:
        temp = MinecraftServer.lookup("lopx.minehut.gg").status()
        statuslopx = "online"
    except OSError:
        statuslopx = "offline"
    try:
        temp = MinecraftServer.lookup("116kccs.aternos.me").status()
        status116 = "online"
    except OSError:
        status116 = "offline"
    try:
        temp = MinecraftServer.lookup("sb4kccs.aternos.me").status()
        statussb4 = "online"
    except OSError:
        statussb4 = "offline"
    try:
        temp = MinecraftServer.lookup("smpkccs.aternos.me").status()
        statussmp = "online"
    except OSError:
        statussmp = "offline"
        
    logger.info("Attempting to return dict from chkmcsrvstatus()...")
    return {"statuskccscomm":statuskccscomm,"statuslopxl": statuslopxl,"statuslopx":statuslopx,"status116": status116,"statussb4": statussb4,"statussmp": statussmp}





def mc(embed,argv):
    logger.info("Started botmc.mc()")
    global hlp
    rtrn = ""
    global mcserverarglist  #chk srv arg
    global tmp
    args = argv.split(" ")
    if args[0] in hlp:
        logger.info("Help arguments detected")
        rtrn = 'Args: help, server\n'
        embed = discord.Embed(title="help",description=rtrn)
        logger.info('Attempting to return obj "embed" from hlp')
        return embed
    elif args[0] in mcserverarglist:
        logger.info('server argument detected')
        try:
            if args[1]:
                logger.info("2nd argument detected, searching for same srv_id for override...")
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
                    name = "Survival Multiplayer KCCS"
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
                    note = "Null"
                else:
                    logger.info("Not a defined server, will treat 2nd argument as a server link and name.")
                    link = args[1]
                    name = args[1]
                    try:
                        note = MinecraftServer(link).query().motd
                    except OSError as e:
                        note = str(e)
                        logger.warn('Getting error "{}" while trying to get the motd sf server, error ignored.'.format(str(e)))
                        logger.info('Query() might not be supported for this server.  Edit server.properties to enable this feature.')
                try:
                    tmp=MinecraftServer.lookup(link).status()
                    status="online"
                    players=str(tmp.players.online) + "/" + str(tmp.players.max)
                    ping=tmp.latency
                except OSError as e:
                    status='offline'
                    logger.warn('Getting error "{}" while trying to detect if server is online, treat server as an offline server.'.format(str(e)))
                    raise OfflineServer("Server {} (link {}) has been detected as offline.".format(name,link))
                try:
                    if tmp.players.sample:
                        playerls = ', '.join(p.name for p in tmp.players.sample)
                    else:
                        playerls = 'Unknown'
                except OSError as e:
                    playerls=[str(e)]
                    if status == "online":
                        logger.warn('Getting error "{}" while trying to get ping even server is online, error ignored.'.format(str(e)))
                if tmp.description:
                    dscrp = tmp.description
                else:
                    dscrp = "No description / Unknown"
                if tmp.version.name:
                    ver = tmp.version.name
                else:
                    ver = "Unknown"
                embed = discord.Embed(title="Minecraft KCCS Official",description="Here's da info",color=0x00b9ff)
                embed.add_field(name = "Server name: ",         value=name,         inline=True)
                embed.add_field(name = "Server link: ",         value=link,         inline=True)
                embed.add_field(name = "Server status: ",       value=status,       inline=True)
                embed.add_field(name = "Server version: ",      value=ver,          inline=True)
                embed.add_field(name = "Note: ",                value=note,         inline=True)
                embed.add_field(name = "Latency (Ping): ",      value=ping,         inline=True)
                embed.add_field(name = "Number of players: ",   value=players,      inline=True)
                embed.add_field(name = "Players Online: ",      value=playerls,     inline=True)
                embed.add_field(name = "Description: ",         value=dscrp,        inline=True)
                logger.info('Attempting to return obj "embed" from srv <id/link>')
                return embed
            else:
                raise InvalidArgument("Invalid argument \"" + args[1] + "\" for the third argument.")
        except IndexError:
            pass
        logger.info("Getting IndexError while trying to check 2nd argument, treating request as a basic mc srv list.  Attempting to call chkmcsrvstatus()")
        mcsrvstatus = chkmcsrvstatus()
        logger.info('Creating dict "mcsrvlis" based on the dict returned from chkmcsrvstatus()')
        mcsrvlis = {
            "kccscomm": {
                "name":     "KCCS Community",
                "link":     "kccscomm.minehut.gg",
                "status":   mcsrvstatus["statuskccscomm"],
                "note":     "Recommened"
            },
            "lopxl":{
                "name":     "Lopixel on Aternos",
                "link":     "lopxl.aternos.me",
                "status":   mcsrvstatus["statuslopxl"],
                "note":     "Inactive"
            },
            "lopx":{
                "name":     "Lopixel on Minehut",
                "link":     "lopx.minehut.gg",
                "status":   mcsrvstatus["statuslopx"],
                "note":     "Ignored"
            },
            "116kccs":{
                "name":     "1.16 server for KCCS",
                "link":     "116kccs.aternos.me",
                "status":   mcsrvstatus["status116"],
                "note":     "Active"
            },
            "sb4kccs":{
                "name":     "Skyblock for KCCS",
                "link":     "sb4kccs.aternos.me",
                "status":   mcsrvstatus["statussb4"],
                "note":     "Ruined"
            },
            "smpkccs":{
                "name":     "Survival Multiplayer",
                "link":     "smpkccs.aternos.me",
                "status":   mcsrvstatus["statussmp"],
                "note":     "Active, NO CHEATING"
            }
        }
        logger.info('Formatting the dict so that it will be a little bit human-readable')
        rtrn += "Name\t\t\t\tLink\t\t\t\tStatus\n"
        for srv in mcsrvlis:                        #print the stuff in the outer dict
            for key in mcsrvlis[srv]:               #print the value from the key with a for-loop in the inter dict
                rtrn += str(mcsrvlis[srv][key]) + "\t\t"
                if mcsrvlis[srv][key] in ["KCCS Community", "lopx.minehut.gg"]:
                    rtrn += "\t"
            rtrn += "\n"
        rtrn += "\n"
        embed = discord.Embed(title="Minecraft Servers", description=rtrn,color=0x0000ff)
        logger.info('Attempting to return obj "embed" from srv')
        return embed
    else:
        raise InvalidArgument("1st Arg '{}' is invalid!".format(argv[0]))