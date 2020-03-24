#botbot.py
from dotenv import load_dotenv
from mcstatus import MinecraftServer
from discord.ext import commands
from consolemod import *
from botclientlog import logger
from discord.utils import get
import threading,datetime,time,botmc,discord,os,random,json
from discord.ext.commands import has_permissions, MissingPermissions

#console log
logger.info("Program started.")
logger.debug("Finished importing and logger configuration.  Loaded all libraries.")

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_GUILD = os.getenv('DISCORD_GUILD')
client = discord.Client()
lastmsg=[]



@client.event
async def on_message(message):
    global lastmsg
    if message.author == client.user or message.author.bot:
        return
    if 'siriustupid' in message.content.lower():
        await message.channel.send('Sirius is so so stupid!', tts=True)
    elif 'vincidiot' in message.content.lower():
        await message.channel.send('Vinci is an idiot!', tts=True)
    elif 'benz' in message.content.lower():
        await message.channel.send('Stupid Benz is a sucker', tts=True)
    elif 'what?' == message.content.lower():
        await message.channel.send('Nothing.')
    if not lastmsg:
        lastmsg=[message.content.lower(),message.author,1,False]
    elif lastmsg[2] == 4 and message.content.lower() == lastmsg[0] and message.author == lastmsg[1] and lastmsg[3]:
        await message.channel.send(f'OK BOOMER {message.author.mention}')
    elif lastmsg[0] == message.content.lower() and lastmsg[1] == message.author:
        lastmsg[2]+=1
        if lastmsg[2] == 4:
            lastmsg[3]=True
    else:
        lastmsg=[message.content.lower(),message.author,1,False]



@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    member.create_dm()
    member.dm_channel.send(f'Hi {member.name}, welcome to KCCS Official Discord server!')


client.run(TOKEN)
