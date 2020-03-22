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
import valstore

#console log
logger.info("Program started.")
logger.debug("Finished importing and logger configuration.  Loaded all libraries.")


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# init
bot = commands.Bot(command_prefix='/')

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
    logger.debug("Bot is now ready!")
    print(style.cyan(f'\33[2J{bot.user.name} has connected to Discord!') + style.reset())
    return




@bot.command(name='test', help="Respond with test messages!")
async def test(ctx):
    logger.info(ctx.message.author.name + "has issued command /test")
    response = random.choice(valstore.loltest)
    logger.info("Result / response: " + response)
    msg = await ctx.send(response)
    await msg.add_reaction('👍')
    return


@bot.command(name='mc',help="Same as kccsofficial.exe mc <args>\nUsage: /mc srv hypixel",pass_content=True)
async def mc(ctx,*,args=""):
    logger.info(ctx.message.author.name + " has issued command /mc " + args)
    print("{} has issued command /mc {}.".format(ctx.message.author.name,args))
    rtrn = 0
    msg = await ctx.send("Spinnin' around...")
    await msg.add_reaction(bot.get_emoji(687495401661661324))
    rtc=0
    try:
        if args=="":
            raise discord.ext.commands.errors.MissingRequiredArgument("")
        embed = discord.Embed(title="Minecraft KCCS Official",description="uh......")
        await msg.edit(embed=embed)
        embed = botmc.mc(embed,args)
    except botmc.InvalidArgument as e:
        rtrn = "Panic 2: InvalidArgument. Send gud args!!!!!!!?\n""Details:  " + str(e) + "\n"
        rtrn += "2 get da usage, includ da \"help\" args, i.e. `/mc help`\n"
        rtc = 2
    except discord.ext.commands.errors.MissingRequiredArgument as e:
        rtrn = "Panic 3: MissingRequiredArgument.  Plz send args!!!\nDetails:  {}\n".format(str(e))
        rtrn += "2 get da usage, includ da \"help\" args, i.e. `/mc help`\n"
        rtc = 3
    except Exception as e:
        if e in ["timed out","Server did not respond with any information!"]:
            rtrn = "Panic 4: Runclock Era.  Program kthxbai.\nDetails:  " + str(e) + "\n"
            rtc = 4
        else:
            rtrn = "Panic 1: Unknown Era.  Program kthxbai.\nDetails:  " + str(e) + "\n"
            rtc = 1
    if rtc != 0:
        embed = discord.Embed(title="ERROR",description=str(rtrn))
        if rtc == 1:
            logger.error("Panic kthxbai code: " + str(rtc))
        else:
            logger.warn("kthxbai code: " + str(rtc))
    else:
        logger.info("Exit code: " + str(rtc))
    embed.set_footer(text="kthxbai code: {}.".format(rtc))
    await msg.edit(embed=embed)
    await msg.remove_reaction(bot.get_emoji(687495401661661324),bot.user)
    return




@bot.command(name='cough',help="Simulate cough. :)")
async def cough(ctx):
    logger.info(ctx.message.author.name + "has issued command /cough")
    response = random.choice(valstore.lolcough)
    logger.info("Result / response: " + response)
    msg = await ctx.send(response)
    await msg.add_reaction('👀')
    return





console = cursor()
console.cls()
bot.run(TOKEN)