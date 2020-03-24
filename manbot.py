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


client = discord.ext.commands.Bot(command_prefix = '/')


   



client.run(TOKEN)