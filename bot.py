# bot.py
from dotenv import load_dotenv
from mcstatus import MinecraftServer
from discord.ext import commands
from discord.ext.commands import has_permissions,MissingPermissions
from consolemod import *
from logcfg import logger
from discord.utils import get
import threading,datetime,time,botmc,discord,os,random,asyncio,json,quickpoll
from concurrent.futures import ThreadPoolExecutor

#console log
logger.info("Program started.")
logger.debug("Finished importing and logger configuration.  Loaded all libraries.")

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# init
bot = commands.Bot(command_prefix = '/')
runno = 0
logger.debug("Loaded dotenv, discord_token, bot prefix, custom exceptions, and \"constant\" variables / some global variables.")
embed=discord.Embed()



@bot.listen
async def listen(message):
    user = discord.utils.get(message.guild.members, id=message.author.id)
    logger.info("{user}: {message.content}")
    print(style.green(f"{user}: {message.content}") + style.reset())


@bot.on_message
async def on_message(message):
    if message.author == bot.user.name or message.author.bot:
        return


@bot.event
async def on_ready():
    logger.info("Bot is now ready!")
    print(style.cyan(f'\33[2J{bot.user.name} has connected to Discord!') + style.reset())
    return


@bot.command(name='cough',help="Simulate cough. :)")
async def cough(ctx):
    logger.info(ctx.message.author.name + "has issued command /cough")
    lolcough = ["What? You being infected coronavirus?",str(bot.get_emoji(684291327818596362)),"Please don't:\nSneeze on me;\nCough on me;\nTalk to me,\nNo oh oh!","🤢",
    "Run, run, until it's done, done, until the sun comes up in the morn'."]
    response = random.choice(lolcough)
    logger.info("Result / response: " + response)
    msg = await ctx.send(response)
    await msg.add_reaction('👀')
    return

@bot.command(name='test', help="Respond with test messages!")
async def test(ctx):
    loltest = ["!urban MEE6","Am I a joke to you?","!8ball Siriu-smart?","What? Are you a developer?{}".format(ctx.message.author.mention),
    "Didn't expect anyone would use this command, but there it is!","No test.","Ping Pong!","No.","?????","Siriusly, What did you expect?",
    "Stop.","!8ball are you stupid?","Vincidiot"]
    logger.info(ctx.message.author.name + "has issued command /test")
    response = random.choice(loltest)
    logger.info("Result / response: " + response)
    msg = await ctx.send(response)
    await msg.add_reaction('👍')
    return

@bot.command(pass_context=True, help='Tells you the ping from discord to the bot', name='ping')
async def ping(ctx):
    await ctx.send(embed=discord.Embed(title="Pong!", description='The latency is {} ms.'.format(bot.latency*1000), color=0x3333ff))

@bot.command(name='emojis',help='Print all emojis')
async def emojis(ctx):
    for emoji in ctx.guild.emojis:
        await ctx.send(str(bot.get_emoji(emoji.id)) + str(emoji.id) + f" {emoji.name}")

@bot.command(name='stupid',help='Shout at stupid things')
async def stupid(ctx,*,args='that'):
    logger.info(ctx.message.author.name + 'has issued command /stupid')
    await ctx.send(random.choice([f'{args} is so so stupid!',f"I can't believe how stupid {args} is!",f"Seriously, {args}'s the stupidest thing I've ever heard!",f"STUPID STUPID STUPID STUPID STUPID STUPID STUPID STUPID {args}!",f"I can't believe {args}'s even a thing."]))

@bot.command(name='whatis',help='Tells you what the input is. /whatis minecraft')
async def whatis(ctx,*,args=""):
    logger.info(ctx.message.author.name + f'has issued command /whatis {args}')
    if args=="":
        await ctx.send("Bruh, where's the argument???")
        return
    await ctx.send(random.choice([f"{args} is generally {args}.",f"Technically, {args} is {args}!",f"To know what {args} is, please run `!urban {args}`",
    f"Well, not in a nutshell, {args} as {args} is {args} in {args} on {args} at {args} from {args} to {args}...It's just...{args}!!!!!",
    f"You are so dumb that you even don't know what {args} is!"]))



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





@bot.group(pass_context=True)
async def vote(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send(f"2 bed idk wat u r toking 'bout, but wut?")
@vote.command(name='create',help='Create a vote: /vote create <name> <choices>')
async def create(ctx,name,*options: str):
    logger.info(f"{ctx.message.author.name} has issued command /vote create {name} " + str(options))
    poll = quickpoll.QuickPoll(bot)
    await poll.quickpoll(poll,ctx,name,options)
    logger.info(f'finished request /vote create {name} {str(options)} from {ctx.author.name}.')
    return
@vote.command(name='end',help='End a vote: /vote end <name>')
async def end(ctx,*,id):
    poll = quickpoll.QuickPoll(bot)
    await poll.tally(poll,ctx,id)
    return

        
        
        
        





console = cursor()
console.cls()
bot.run(TOKEN)