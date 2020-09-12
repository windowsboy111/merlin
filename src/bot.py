#!/bin/python3
# bot.py
import ext.startup
# python libs
import sys
import os
import traceback
import random
import json
import asyncio
from datetime import datetime
# additional libs
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import find
# python external files
import special
from modules.chat import chat
from ext.const import log, bot, get_prefix, fix_settings
from ext.const import statusLs, LASTWRDFILE, STRFILE, SETFILE, slog, nlog, hint, logging, cmdHdlLogger, eventLogger, style
from ext import excepts
# initlize runtime variables
load_dotenv()
exitType, exts, TOKEN, MODE = 0, ['ext.tasks', 'ext.cmdhdl'], os.getenv('DISCORD_TOKEN'), os.getenv('MODE')
lastword = stringTable = None
setattr(logging.Logger, 'hint', hint)
settings = json.load(open(SETFILE))
# scan the cogs folder
for cog in os.listdir('cogs/'):
    if cog.endswith('.py'):
        exts.append("cogs." + cog[:-3])
stringTable = json.load(open(STRFILE, 'r'))
try:
    lastword = json.load(open(LASTWRDFILE, 'r'))
except json.JSONDecodeError:
    # "format" / initlize the json files
    lastword = {}
    f = open(LASTWRDFILE, 'w')
    f.write("{}")
    f.close()

slog("Adding bot commands...")


@bot.command(name='reboot', aliases=['restart'], hidden=True)
@commands.is_owner()
async def cmd_reboot(ctx):
    global exitType
    print('Bot going to log out in 10 seconds [owner disc rq] type: reboot')
    await log('***__WARNING! BOT WILL RESTART IN 10 SECONDS!__***')
    await ctx.send('Bot will restart in 10 seconds.')
    await asyncio.sleep(10)
    await ctx.send('Logging out...')
    await log('Logging out...')
    print('Logging out...')
    exitType = 1
    await bot.logout()


@bot.command(name='shutdown', aliases=['stop', 'sdwn', 'kthxbai', 'halt'], hidden=True)
@commands.is_owner()
async def cmd_shutdown(ctx):
    global exitType
    nlog('Bot going to log out in 10 seconds [owner disc rq] type: shutdown')
    await log('***__WARNING! BOT WILL RESTART IN 10 SECONDS!__***')
    await ctx.send('Bot will shutdown in 10 seconds.')
    await asyncio.sleep(10)
    await ctx.send('Logging out...')
    await log('Logging out...')
    nlog('Logging out...')
    exitType = 2
    await bot.logout()


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
            slog(style.red2 + f"FAILED: {extension}{style.grey} - {style.yellow}{traceback.format_exception_only(err.__class__, err)}{style.reset}")
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
    global exitType, settings, stringTable, lastword
    slog('Running / logging in...')
    token = token or os.getenv('DISCORD_TOKEN')
    while True:
        bot.run(token, **kwargs)
        if exitType == 0:
            nlog("Force terminating...")
            os._exit(1)
        nlog('Logged out')
        break
    slog('Writing changes and saving data...')
    lastword, stringTable = json.load(
        open(LASTWRDFILE, 'r')), json.load(open('ext/wrds.json', 'r'))
    settings.update(json.load(open(SETFILE, 'r')))
    json.dump(settings, open(SETFILE, 'w'))
    if exitType == 2:
        print("\nExiting...")
        sys.exit(0)
    print('==> Restarting script...\n\n')
    try:
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
    except PermissionError as e:
        print(f"OPERATION FAILED: {str(e)}")
        sys.exit(3)


if __name__ == '__main__':
    start(TOKEN, bot=True, reconnect=True)
