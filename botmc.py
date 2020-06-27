from mcstatus import MinecraftServer
import discord
from logcfg import logger
from pyTableMaker import modernTable

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
    try:
        temp = MinecraftServer.lookup('2b2s.aternos.me').status()
        status2b2s = "online"
    except OSError:
        status2b2s = "offline"
        
    temp = None or temp
    logger.info("Attempting to return dict from chkmcsrvstatus()...")
    return {"statuskccscomm":statuskccscomm,"statuslopxl": statuslopxl,"statuslopx":statuslopx,"status116": status116,"statussb4": statussb4,"statussmp": statussmp, "status2b2s": status2b2s}





def mcsrv(embed,args):
    logger.info("Started botmc.mc()")
    global hlp
    rtrn = ""
    global mcserverarglist  #chk srv arg
    global tmp
    try:
        if args:
            logger.info("2nd argument detected, searching for same srv_id for override...")
            if args == "kccscomm":
                link = "kccscomm.minehut.gg"
                name = "KCCS Community Survival Server"
                note = "Recommened Survival Server"
            elif args == "lopx":
                link = "lopx.minehut.gg"
                name = "Lopixel on Minehut"
                note = "Help build the minigames server!"
            elif args == "lopxl":
                link = "lopxl.aternos.me"
                name = "Lopixel on Aternos"
                note = "Help build the minigames server!"
            elif args == "116kccs":
                link = "116kccs.aternos.me"
                name = "1.16 Survival Server for KCCS"
                note = "Snapshot version "
            elif args == "sb4kccs":
                link = "sb4kccs.aternos.me"
                name = "Skyblock for KCCS"
                note = "Ruined :("
            elif args == "smpkccs":
                link = "smpkccs.aternos.me"
                name = "Survival Multiplayer KCCS"
                note = "NO CHEATING"
            elif args == "hypixel":
                link = "mc.hypixel.net"
                name = "Hypixel Network"
                note = "Best Minecraft Server Ever!"
            elif args == "earthmc":
                link = "earthmc.net"
                name = "EarthMC"
                note = "A towny server"
            elif args == "pvpwars":
                link = "pvpwars.net"
                name = "PvpWars"
                note = "Null"
            elif args == "crab":
                link = "crabricorn.serv.gs"
                name = "Crabricorn"
                note = "Paper HK survival server"
            elif args == "crabricorn":
                link = "crabricorn.serv.gs"
                name = "Crabricorn"
                note = "Paper HK survival server"
            else:
                logger.info("Not a defined server, will treat 2nd argument as a server link and name.")
                link = args
                name = args
                note = "unknown server :/"
                # try:
                #     note = MinecraftServer(link).query().motd
                # except OSError as e:
                #     note = str(e)
                #     logger.warn('Getting error "{}" while trying to get the motd sf server, error ignored.'.format(str(e)))
                #     logger.info('Query() might not be supported for this server.  Edit server.properties to enable this feature.')
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
    except IndexError:
        pass
    logger.info("Getting IndexError while trying to check 2nd argument, treating request as a basic mc srv list.  Attempting to call chkmcsrvstatus()")
    mcsrvstatus = chkmcsrvstatus()
    logger.info('returned.  Formatting...')
    t = modernTable()
    t.new_column('ID')
    t.new_column('Name')
    t.new_column('Status')
    t.insert('kccscomm.minehut.gg', 'KCCScomm', mcsrvstatus['statuskccscomm'])
    t.insert('lopxl.aternos.me',    'Lopxl',    mcsrvstatus['statuslopxl'])
    t.insert('lopx.minehut.me',     'Lopx',     mcsrvstatus['statuslopx'])
    t.insert('116kccs.aternos.me',  '116kccs',  mcsrvstatus['status116'])
    t.insert('sb4kccs.aternos.me',  'sb4kccs',  mcsrvstatus['statussb4'])
    t.insert('smpkccs.aternos.me',  'smpkccs',  mcsrvstatus['statussmp'])
    t.insert('2b2s.aternos.me',     '2bit2s',   mcsrvstatus['status2b2s'])
    body = '```css\n'
    body += t.get()
    body += '\n```'
    embed = discord.Embed(title="Minecraft servers", description=body,color=0x0000ff)
    logger.info('Attempting to return obj "embed" from srv')
    return embed