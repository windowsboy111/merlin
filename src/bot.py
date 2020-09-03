#!/bin/python3
# bot.py
# python libs
import ext.startup
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
from ext.const import log, bot, get_prefix
from ext.const import statusLs, LASTWRDFILE, STRFILE, SETFILE, slog, nlog, hint, logging, cmdHdlLogger, eventLogger, style
from ext import excepts
load_dotenv()
cogs = []
for cog in os.listdir('cogs/'):
    if cog.endswith('.py'):
        cogs.append(cog[:-3])
# token is stored inside ".env"
TOKEN = os.getenv('DISCORD_TOKEN')
lastword = stringTable = None
try:
    lastword = json.load(open(LASTWRDFILE, 'r'))
    stringTable = json.load(open(STRFILE, 'r'))
except json.JSONDecodeError:
    lastword = {}
    f = open(LASTWRDFILE, 'w')
    f.write("{}")
    f.close()
    stringTable = json.load(open('ext/wrds.json', 'r'))


# configs (post startup)
MODE = os.getenv('MODE')
setattr(logging.Logger, 'hint', hint)
settings = json.load(open(SETFILE))

async def update():
    global settings, stringTable, lastword
    lastword, stringTable = json.load(
        open(LASTWRDFILE, 'r')), json.load(open(STRFILE, 'r'))
    settings.update(json.load(open(SETFILE, 'r')))
    json.dump(settings, open(SETFILE, 'w'))
# ---------
# background tasks

async def task_update():
    await update()
    await asyncio.sleep(60)

bot.loop.create_task(task_update())

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


@bot.command(name='update', hidden=True)
@commands.is_owner()
async def cmd_update(ctx):
    await update()


@bot.event
async def on_ready():
    nlog(f'Logged in as {bot.user.name} - {bot.user.id} in {MODE} mode')
    nlog('Loading Extensions...')
    slog('Loading ext.tasks...')
    bot.load_extension("ext.tasks")
    slog('Loading ext.cmdhdl...')
    bot.load_extension("ext.cmdhdl")
    try:
        for cog in cogs:
            slog(f'Loading cogs.{cog}...')
            bot.load_extension('cogs.' + cog)
    except Exception:
        nlog("An error occurred during loading extension, treat bot start as a reconnect")
        nlog("Reconnected!")
        return 2
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
    nlog("Ready!")
    return 0


def start(token=None, **kwargs):
    # login / start services
    global exitType, settings, stringTable, lastword
    slog('Running / logging in...')
    token = token or os.getenv('DISCORD_TOKEN')
    while True:
        bot.run(token, **kwargs)
        if exitType == 0:
            nlog("Uh oh whoops, that's awkward... Bot has logged out unexpectedly. trying to relog in...")
            continue
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
        sys.exit(2)


if __name__ == '__main__':
    start(TOKEN, bot=True, reconnect=True)
