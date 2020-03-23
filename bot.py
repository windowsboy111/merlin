# bot.py
import os
import random
from dotenv import load_dotenv
from mcstatus import MinecraftServer
from discord.ext import commands
import discord
from consolemod import *
import botmc
from logcfg import logger
from discord.utils import get
import threading
import datetime
import time

#console log
logger.info("Program started.")
logger.debug("Finished importing and logger configuration.  Loaded all libraries.")

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# init
bot = commands.Bot(command_prefix='/')
runno = -1
logger.debug("Loaded dotenv, discord_token, bot prefix, custom exceptions, and \"constant\" variables / some global variables.")



@bot.listen
async def listen(message):
    user = discord.utils.get(message.guild.members, id=message.author.id)
    logger.info("{user}: {message.content}")
    print(style.green(f"{user}: {message.content}") + style.reset())


@bot.on_message
async def on_message(message):
    if message.author == bot.user.name:
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




class threadMC (threading.Thread):
   def __init__(self, threadID, name, ctx,embed,args):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.args = args
        self.ctx = ctx
        self.embed = embed
   def run(self):
        logger.info("Starting " + self.name)
        procMC(self.ctx,self.args)
        logger.info("Exiting " + self.name)
@bot.command(name='mc',help="Same as kccsofficial.exe mc <args>\nUsage: /mc srv hypixel",pass_content=True)
async def mc(ctx,*,args=""):
    global runno,embed
    enduser = ctx.message.author.name
    runno += 1
    starttime = datetime.datetime.now()
    embed = discord.Embed(title="Minecraft KCCS Official",description="uh......")
    msg = await ctx.send("Spinnin' around...")
    ebd = await ctx.send(embed=embed)
    try:
        fetchMC = threadMC(runno,"FetchMC_{}".format(str(runno)),ctx,embed,args)
        fetchMC.start()
        logger.info(enduser + " has issued command /mc " + args)
        print("{} has issued command /mc {}".format(enduser,args))
        await msg.add_reaction(bot.get_emoji(687495401661661324))
        fetchMC.join()
        await msg.remove_reaction(bot.get_emoji(687495401661661324),bot.user)
        endtime = datetime.datetime.now()
        timeElapsed = endtime - starttime
        await msg.edit(content='Time elapsed: {} ms'.format(str(int(timeElapsed.total_seconds() * 1000))))
        await ebd.edit(embed=embed)
        time.sleep(0.5)
        if threading.active_count == 4:
            runno = -1
    except RuntimeError:
        pass
    return
def procMC(ctx,args):
    global embed
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
    except Exception as e:
        rtrn = "Panic 1: Unknun Era.  Program kthxbai.\nDetails:  " + str(e) + "\n"
        rtc = 1
    if rtc != 0:
        embed = discord.Embed(title="ERROR",description=str(rtrn))
        if rtc == 1:
            logger.error("Exit code: " + str(rtc))
        else:
            logger.warn("Exit code: " + str(rtc))
    else:
        logger.info("Exit code: " + str(rtc))
    embed.set_footer(text="kthxbai code: {}.".format(rtc))






console = cursor()
console.cls()
bot.run(TOKEN)