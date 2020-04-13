# bot.py
import os
os.chdir('G:\\My drive\\coding\\py\\KCCS-Official\\')
from dotenv import load_dotenv
from mcstatus import MinecraftServer
from discord.ext import commands
from consolemod import *
from logcfg import logger
from discord.utils import get
import time,botmc,discord,random
#console log
logger.info("Program started.")
logger.debug("Finished importing and logger configuration.  Loaded all libraries.")
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
# init
bot = commands.Bot(
    command_prefix = '/',
    description="The bot for KCCS Official",
    case_insensitive=True
)
runno = 0
lastmsg = []
cogs = ['fun','utilities','debug','man']
embed=discord.Embed()
logger.debug("Loaded dotenv, discord_token, bot prefix, custom exceptions, and \"constant\" variables / some global variables.")

######################################################################################################################################################################################
@bot.on_message
async def on_message(message):
    user = discord.utils.get(message.guild.members, id=message.author.id)
    print(style.green(f"{user}: {message.content}") + style.reset())
    global lastmsg
    channels = ['bot-talk']
    if message.author == bot.user.name or message.author.bot or message.channel.id not in channels:
        return
    bad_words = ["fuck", "shit", "bitch"]
    for word in bad_words:
        if message.content.count(word) > 0:
            print(f"{message.author.mention}, no bad words please! \"{word}\" is not allowed!")
            await message.channel.purge(limit=1)
    # if message.server is None and message.startswith('$/'):
    #     logger.info('Received a dm message from ' + message.author.name + 'that starts with $/, it is being treated as a command.')
    #     print(f'dm command from {message.author.name}: {message.content}')
    #     await bot.process_commands(message)
    if message.startswith('/'):
        logger.info(f'{message.author.name} has issued command: {message.content}')
        print(f'{message.author.name} has issued command: {message.content}')
#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
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
    # ment = member.mention
    # embed = discord.Embed(title=f"Welcome {ment}!",color=0xFFBB00)
    # embed.set_author(name=member,icon_url=member.avatar_url)
    # embed.set_footer(text=f"User id: {member.id}")
    # await bot.get_channel(664091944082997278).send(embed=embed)
    print(f"{member} has joined the server.")

#######################################################################################################################################################################################


@bot.group(name='mc',help="Same as kccsofficial.exe mc <args>\nUsage: /mc srv hypixel",pass_context=True,aliases=['minecraft'])
async def mc(ctx):
   if ctx.invoked_subcommand is None:
        await ctx.send(f"2 bed idk wat u r toking 'bout, but wut?")
        return
@mc.command(name='srv',help='list servers',aliases=['server'])
async def srv(ctx,*,args:str=None):
    global embed
    global rtc
    embed = discord.Embed(title='Spinning \'round...',description='Gift me a sec')
    msg = await ctx.send(embed=embed)
    await msg.add_reaction(bot.get_emoji(687495401661661324))
    rtc=0
    try:
        logger.info("Attempting to call botmc.mcsrv()")
        embed = botmc.mcsrv(embed,args)
    except botmc.InvalidArgument as e:
        rtrn = "Panic 2: InvalidArgument. Send gud args!!!!!!!?\n""Details:  " + str(e) + "\n"
        rtrn += "2 get da usage, includ da \"help\" args, i.e. `/mc help`\n"
        rtc = 2
    except botmc.OfflineServer as e:
        rtrn = "Panic 4: OfflineServer.  Details: {}\n2 get da usage, includ da \"help\" args, i.e. `/mc help`\n".format(str(e))
        rtc = 3
    except Exception as e:
        rtrn = "Panic 1: Unknun Era.  Program kthxbai.\nDetails:  " + str(e) + "\n"
        rtc = 1
    if rtc != 0:
        embed = discord.Embed(title="ERROR",description=str(rtrn),color=0xFF0000)
        if rtc == 1:
            logger.error("Exit code: " + str(rtc))
        else:
            logger.warn("Exit code: " + str(rtc))
    else:
        logger.info("Exit code: " + str(rtc))
    embed.set_footer(text="kthxbai code: {}.".format(rtc))
    await msg.edit(embed=embed)
    await msg.remove_reaction(bot.get_emoji(687495401661661324), bot.user)
@mc.command(name='kill',help='cmd /kill')
async def kill(ctx,member:discord.Member=None):
    if member=='@a' or member=='@e':
        for member in ctx.guild.members:
            await ctx.send(f'{member.display_name} fell out of the world')
            await ctx.send(f'Killed {member.display_name}')
            return
    if member=='@r':
        await ctx.send(f'{random.choice(ctx.guild.members).display_name} fell out fo the world')
        await ctx.send(f'Killed {member.display_name}')
        return
    if member == '@p' or member == '@s':
        await ctx.send(f'{ctx.message.author.display_name} fell out of the world.')
        await ctx.send(f'Killed {member.display_name}')
        return
    member = member or ctx.message.author
    await ctx.send(f'{member.display_name} fell out of the world.')
    await ctx.send(f'Killed {member.display_name}')
    return
@mc.command(name='crash')
async def crash(ctx,*,args=None):
    f=open("samples/mc_crash.txt", "r",encoding='utf-8')
    await ctx.send(f.read())

#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_
console = cursor()
console.cls()
bot.run(TOKEN,bot=True,reconnect=True)