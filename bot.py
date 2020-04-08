# bot.py
from dotenv import load_dotenv
from mcstatus import MinecraftServer
from discord.ext import commands
from discord.ext.commands import has_permissions,MissingPermissions
from consolemod import *
from logcfg import logger
from discord.utils import get
import threading,datetime,time,botmc,discord,os,random,asyncio,json
from concurrent.futures import ThreadPoolExecutor
#console log
logger.info("Program started.")
logger.debug("Finished importing and logger configuration.  Loaded all libraries.")
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
# init
bot = commands.Bot(
    command_prefix = '/',
    description="The bot for KCCS Official",
    case_insensitive=True)
runno = 0
lastmsg = []
cogs = ['fun','utilities','debug','man']
embed=discord.Embed()
logger.debug("Loaded dotenv, discord_token, bot prefix, custom exceptions, and \"constant\" variables / some global variables.")


@bot.listen
async def listen(message):
    user = discord.utils.get(message.guild.members, id=message.author.id)
    logger.info("{user}: {message.content}")
    print(style.green(f"{user}: {message.content}") + style.reset())
@bot.on_message
async def on_message(message):
    global lastmsg
    if message.author == bot.user.name or message.author.bot:
        return
    # if message.server is None and message.startswith('$/'):
    #     logger.info('Received a dm message from ' + message.author.name + 'that starts with $/, it is being treated as a command.')
    #     print(f'dm command from {message.author.name}: {message.content}')
    #     await bot.process_commands(message)

    if message.startswith('/'):
        logger.info(f'{message.author.name} has issued command: {message.content}')
        print(f'{message.author.name} has issued command: {message.content}')

    if 'siriustupid' in message.content.lower():
        logger.info(f'Detected "siriustupid" in a message from {message.author.name}')
        print(f'Detected "siriustupid" in a message from {message.author.name}')
        await message.channel.send('Sirius is so so stupid!', tts=True)
    elif 'vincidiot' in message.content.lower():
        logger.info(f'Detected "vincidiot" in a message from {message.author.name}')
        print(f'Detected "vincidiot" in a message from {message.author.name}')
        await message.channel.send('Vinci is an idiot!', tts=True)
    elif 'benz' in message.content.lower():
        logger.info(f'Detected "benz" in a message from {message.author.name}')
        print(f'Detected "benz" in a message from {message.author.name}')
        await message.channel.send('Stupid Benz is a sucker', tts=True)
    elif 'what?' == message.content.lower():
        logger.info(f'Detected "what?" in a message from {message.author.name}')
        print(f'Detected "what?" in a message from {message.author.name}')
        await message.channel.send('Nothing.')
    if not lastmsg:
        lastmsg=[message.content.lower(),message.author,1,False]
    elif lastmsg[2] == 2 and message.content.lower() == lastmsg[0] and message.author == lastmsg[1] and lastmsg[3]:
        logger.info(f'Detected the same message has been sent from {message.author.name} for 3 times!')
        print(f'Detected the same message has been sent from {message.author.name} for five times!')
        await message.channel.send(f'OK BOOMER {message.author.mention}')
    elif lastmsg[0] == message.content.lower() and lastmsg[1] == message.author:
        lastmsg[2]+=1
        if lastmsg[2] == 2:
            lastmsg[3]=True
    else:
        lastmsg=[message.content.lower(),message.author,1,False]
@bot.event
async def on_ready():
    print(style.cyan(f'Logged in as {bot.user.name} - {bot.user.id}'))
    for cog in cogs:
        bot.load_extension('cogs.' + cog)
    return
@bot.event
async def on_member_join(member):
    logger.info(f"Detected {member.name} joined, welcoming the member in dm...")
    await member.create_dm()
    await member.dm_channel.send(f'Hi {member.name}, welcome to KCCS Official Discord server!  I am the KCCS Official bot, lemme guide you through:\n'
    'Before the 10 minutes pass, READ THE RULES.\nThis is an English discord server after all, only English is allowed unless you are in a voice channel.\n'
    'To assign a identity role, run the following command in the server: `/role assign [e.g. 1a]`.\nIf you are not in KCCS, run `/role assign friends` instead.\n')
    ment = member.mention
    embed = discord.Embed(title=f"Welcome {ment}!",color=0xFFBB00)
    embed.set_author(name=member,icon_url=member.avatar_url)
    embed.set_footer(text=f"User id: {member.id}")
    await bot.get_channel(664091944082997278).send()
    print(f"{member} has joined the server.")


class threadMC (threading.Thread):
   def __init__(self, threadID, name, ctx,args):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.args = args
        self.ctx = ctx
   def run(self):
        logger.info("Starting " + self.name)
        procMC(self.ctx,self.args)
        logger.info("Exiting " + self.name)
@bot.command(name='mc',help="Same as kccsofficial.exe mc <args>\nUsage: /mc srv hypixel",pass_context=True)
async def mc(ctx,*,args=""):
    async with ctx.typing():
        loop = asyncio.get_event_loop()
        loop.run_in_executor(ThreadPoolExecutor(), mainmc(ctx,args))
    await ctx.send(embed=embed)
def mainmc(ctx,args):
    global runno,embed,rtc
    enduser = ctx.message.author.name
    runno += 1
    starttime = datetime.datetime.now()
    try:
        fetchMC = threadMC(runno,"FetchMC_{}".format(str(runno)),ctx,args)
        fetchMC.start()
        logger.info(enduser + " has issued command /mc " + args)
        print("{} has issued command /mc {}".format(enduser,args))
        fetchMC.join()
        endtime = datetime.datetime.now()
        timeElapsed = endtime - starttime
        embed.set_footer(text='Exit code: {}, Time elapsed: {} ms'.format(rtc,str(int(timeElapsed.total_seconds() * 1000))))
        time.sleep(0.5)
        if runno == 100:
            runno = 0
    except RuntimeError:
        pass
    except TypeError:
        pass
    return embed
def procMC(ctx,args):
    global embed
    global rtc
    logger.info("procMC started as a new thread.")
    rtc=0
    try:
        if args=="":
            raise discord.ext.commands.errors.MissingRequiredArgument(ctx.command)
        logger.info("Attempting to call botmc.mc()")
        embed = botmc.mc(embed,args)
    except botmc.InvalidArgument as e:
        rtrn = "Panic 2: InvalidArgument. Send gud args!!!!!!!?\n""Details:  " + str(e) + "\n"
        rtrn += "2 get da usage, includ da \"help\" args, i.e. `/mc help`\n"
        rtc = 2
        time.sleep(0.5)
    except discord.ext.commands.errors.MissingRequiredArgument as e:
        rtrn = "Panic 3: MissingRequiredArgument.  Plz send args!!!\nDetails:  {}\n".format(str(e))
        rtrn += "2 get da usage, includ da \"help\" args, i.e. `/mc help`\n"
        rtc = 3
        time.sleep(0.5)
    except botmc.OfflineServer as e:
        rtrn = "Panic 4: OfflineServer.  Details: {}\n2 get da usage, includ da \"help\" args, i.e. `/mc help`\n".format(str(e))
        rtc = 4
    # except Exception as e:
        # rtrn = "Panic 1: Unknun Era.  Program kthxbai.\nDetails:  " + str(e) + "\n"
        # rtc = 1
    if rtc != 0:
        embed = discord.Embed(title="ERROR",description=str(rtrn),color=0xFF0000)
        if rtc == 1:
            logger.error("Exit code: " + str(rtc))
        else:
            logger.warn("Exit code: " + str(rtc))
    else:
        logger.info("Exit code: " + str(rtc))
    embed.set_footer(text="kthxbai code: {}.".format(rtc))



console = cursor()
console.cls()
bot.run(TOKEN,bot=True,reconnect=True)