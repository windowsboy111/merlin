#!/bin/python3
# bot.py
import ext.startup
# python libs
import sys, os, json, asyncio, traceback, random
from datetime import datetime
# additional libs
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import find
# python external files
from ext.const import statusLs, SETFILE, slog, nlog, logging, eventLogger, style, log, bot, hint
from ext import excepts
# initialize runtime variables
load_dotenv()
exitType, exts, TOKEN, MODE = 0, ['ext.tasks', 'ext.cmdhdl'], os.getenv('DISCORD_TOKEN'), os.getenv('MODE')
lastword = None
setattr(logging.Logger, 'hint', hint)
settings = json.load(open(SETFILE))
# scan the cogs folder
for cog in os.listdir('cogs/'):
    if cog.endswith('.py'):
        exts.append("cogs." + cog[:-3])


@bot.event
async def on_ready():
    nlog(f'Logged in as {style.cyan}{bot.user.name}{style.reset} - {style.italic}{bot.user.id}{style.reset} in {style.magenta}{MODE}{style.reset} mode')
    nlog('Loading Extensions...')
    for extension in exts:
        print(end=f' >> Loading {extension}...\r')
        try:
            bot.load_extension(extension)
            slog(style.green2 + f"Loaded: {extension}" + style.reset + "   ")
        except commands.errors.ExtensionAlreadyLoaded:
            return nlog("Loaded tasks already, continue execution.")
        except Exception as err:
            slog(style.red2 + f"FAILED: {extension}{style.grey} - {style.yellow}{traceback.format_exception_only(err.__class__, err)[0]}{style.reset}")
    slog('Telling guilds...')
    if not MODE or MODE == 'NORMAL':
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=random.choice(statusLs)))
        await log('Logged in!')
    elif MODE == 'DEBUG':
        await bot.change_presence(status=discord.Status.idle)
        await log('RUNNING IN **DEBUG** MODE!')
    elif MODE == 'FIX':
        await bot.change_presence(status=discord.Status.dnd)
        await log('*RUNNING IN EMERGENCY **FIX** MODE!')
    nlog(style.bold + style.blue + "Ready!" + style.reset)
    return 0


def start(token=None, **kwargs):
    # login / start services
    global exitType, settings
    slog('Running / logging in...')
    token = token or os.getenv('DISCORD_TOKEN')
    while True:
        bot.run(token, **kwargs)
        if exitType == 0:
            nlog("Force terminating...")
            os._exit(1)
        nlog('Logged out')
        break
    if exitType == 2:
        print("\nExiting...")
        sys.exit(0)
    nlog('Restarting script...\n\n')
    try:
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
    except PermissionError as e:
        print(f"OPERATION FAILED: {str(e)}", file=sys.stdout)
        sys.exit(3)


if __name__ == '__main__':
    start(TOKEN, bot=True, reconnect=True)
