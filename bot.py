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
    loltest = ["What? Are you a developer?{}".format(ctx.message.author.mention),"Didn't expect anyone would use this command, but there it is!","No test.","Ping Pong!","No.","?????","Siriusly, What did you expect?","Stop.","!8ball are you stupid?","Vincidiot"]
    response = random.choice(loltest)
    logger.info("Result / response: " + response)
    msg = await ctx.send(response)
    await msg.add_reaction('👍')
    return


@bot.command(name='mc',help="Same as kccsofficial.exe mc <args>\nUsage: /mc srv hypixel")
async def mc(ctx,*,args=""):
    logger.info(ctx.message.author.name + " has issued command /mc " + args)
    print("{} has issued command /mc {}.".format(ctx.message.author.name,args))
    try:
        if args=="":
            raise discord.ext.commands.errors.MissingRequiredArgument("")
        embed = discord.Embed(title="Minecraft KCCS Official",description="Loading...")
        msg = await ctx.send(embed=embed)
        embed = botmc.mc(embed,str(args))

    except botmc.InvalidArgument as e:
        rtrn = "Error 2: Invalid Argument.  Program terminated.\n""Details:  " + str(e) + "\n"
        rtrn += "To get the usage, include the \"help\" arguments, i.e. `/mc help`\n"
        rtc = 2
    except discord.ext.commands.errors.MissingRequiredArgument as e:
        rtrn = "Error 3: MissingRequiredArgument.  Did you input any arguments?\n"
        rtrn += "To get the usage, include the \"help\" arguments, i.e. `/mc help`\n"
        rtc = 3
    except Exception as e:
        if e in ["timed out","Server did not respond with any information!"]:
            rtrn = "Error 4: Runtime Error.  Program terminated.\nDetails:  " + str(e) + "\n"
            rtc = 4
        else:
            rtrn = "Error 1: Unknown Error.  Program terminated.\nDetails:  " + str(e) + "\n"
            rtc = 1
    if rtc != 0:
        if rtc == 1:
            logger.error("Error exit code: " + str(rtc))
        else:
            logger.warn("Exit code: " + str(rtc))
    else:
        logger.info("Exit code: " + str(rtc))
    embed = discord.Embed(title="ERROR",description=str(rtrn))
    embed.set_footer(text="Program exited with code {}.".format(rtc))
    await msg.edit(embed=embed)
    return



console = cursor()
console.cls()
bot.run(TOKEN)