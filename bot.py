#!/bin/python3
# bot.py

# python libs
import bot_imports
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
from ext.imports_share import log, bot, get_prefix
from ext.const import statusLs, LASTWRDFILE, STRFILE, SETFILE, slog, nlog, hint, logging, cmdHdlLogger, eventLogger, style
from ext import excepts
import easteregg
from ext.chat import chat
load_dotenv()
cogs = []
for cog in os.listdir('cogs/'):
    if cog.endswith('.py'):
        cogs.append(cog[:-3])
# token is stored inside ".env"
TOKEN = os.getenv('DISCORD_TOKEN')
lastword = stringTable = None
try:
    lastword    = json.load(open(LASTWRDFILE, 'r'))
    stringTable = json.load(open(STRFILE, 'r'))
except json.JSONDecodeError:
    lastword = {}
    f = open(LASTWRDFILE, 'w')
    f.write("{}")
    f.close()
    stringTable = json.load(open('ext/wrds.json', 'r'))


setattr(logging.Logger, 'hint', hint)


settings = json.load(open(SETFILE))

# init
bot.remove_command('help')
MODE = os.getenv('MODE')

slog("Adding bot commands...")


# ---------
# background tasks
async def status():
    await bot.wait_until_ready()
    while True:
        try:
            if not MODE or MODE == 'NORMAL':
                activity = discord.Game(name=random.choice(statusLs))
                await bot.change_presence(status=discord.Status.online, activity=activity)
            elif MODE == 'DEBUG':
                activity = discord.Activity(type=discord.ActivityType(
                    3), name="windowsboy111 debugging me")
                await bot.change_presence(status=discord.Status.idle, activity=activity)
            elif MODE == 'FIX':
                await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType(3), name="windowsboy111 fixing me"))
            await asyncio.sleep(30)
        except Exception:
            pass


async def update():
    global settings, stringTable, lastword
    lastword, stringTable = json.load(
        open(LASTWRDFILE, 'r')), json.load(open(STRFILE, 'r'))
    settings.update(json.load(open(SETFILE, 'r')))
    json.dump(settings, open(SETFILE, 'w'))


async def task_update():
    await update()
    await asyncio.sleep(60)

bot.loop.create_task(status())
bot.loop.create_task(task_update())


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


# ------
# events
@bot.event
async def on_message(message: discord.Message):
    if await easteregg.easter(message):
        return
    try:
        global lastword
        lastword[f'g{message.guild.id}'][str(message.author.id)] = message.id
    except Exception:
        lastword[f'g{message.guild.id}'] = {message.author.id: message.id}
    if not isinstance(message.channel, discord.DMChannel) and message.channel.name == 'merlin-chat' and not message.author.bot:
        async with message.channel.typing():
            await message.channel.send(chat.response(message.content))
            return 0
    await update()
    if message.content.startswith(get_prefix(bot, message)):
        msgtoSend = f'{message.author} has issued command: '
        print(msgtoSend + style.green + message.content + style.reset)
        cmdHdlLogger.info(msgtoSend + message.content)
        try:
            await log(message.channel.mention + ' ' + msgtoSend + '`' + message.content + '`', guild=message.channel.guild)
        except AttributeError:
            pass
        try:
            await bot.process_commands(message)
            return 0
        except discord.ext.commands.errors.CommandNotFound:
            return 2
        except discord.errors.NotFound:
            return 2
        except Exception:
            print(traceback.format_exc(), file=sys.stderr)


@bot.event
async def on_ready():
    nlog(f'Logged in as {bot.user.name} - {bot.user.id} in {MODE} mode')
    nlog('Loading Extensions...')
    try:
        for cog in cogs:
            slog(f'Loading {cog}...')
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


@bot.event
async def on_member_join(member: discord.Member):
    eventLogger.info(f"{member} has joined {member.guild}")
    print(f"{member} has joined {member.guild}")
    return 0


@bot.event
async def on_guild_join(guild: discord.Guild):
    sudoers = []
    for name in [role.name for role in guild.owner.roles]:
        if ['admin', 'mod', 'owner'] in name.lower():
            sudoers.append(name)
    f = json.load(open(SETFILE, 'r'))
    f[f'g{guild.id}'] = {"prefix": ['/'],
                         "cmdHdl": {"cmdNotFound": 0}, "sudoers": sudoers}
    with open(SETFILE, 'w') as outfile:
        json.dump(f, outfile)
    return 0


@bot.event
async def on_command_error(ctx, error):
    try:
        raise error
    except Exception:
        # This tells the issuer that the command cannot be used in DM
        if isinstance(error, commands.errors.NoPrivateMessage):
            try:
                await ctx.author.send(f':x::lock: {ctx.command} cannot be used in Private Messages.')
                return 3
            except discord.HTTPException:
                return 3
        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        # This prevents any cogs with an overwritten cog_command_error being handled here.
        if ctx.cog and ctx.cog._get_overridden_method(ctx.cog.cog_command_error) is not None:
            return

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, commands.errors.CommandNotFound):
            try:
                if settings[f'g{ctx.guild.id}']['cmdHdl']['cmdNotFound']:
                    await ctx.send(":interrobang: Welp, I've no idea. Command not found!")
            except KeyError:
                await ctx.send(":interrobang: :two: :x:\n<:err:740034702743830549> Command not found!\n<:warn:739838316374917171> something went wrong, please run `/settings`")
            return 2
        if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
            return await ctx.invoke(bot.get_command('help'), cmdName=ctx.command.qualified_name)

        if isinstance(error, commands.errors.DisabledCommand):
            return await ctx.send(embed=discord.Embed(
                title=f':no_entry: {ctx.command} has been disabled.',
                description=f':x: `{ctx.message.content}`',
                color=0xff0000
            ))
            return 5

        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(embed=discord.Embed(
                title='<:err:740034702743830549> uh oh. An exception has occurred during the execution of the command',
                description=stringTable['CommandInvokeError'].format(
                    content=ctx.message.content),
                timestamp=datetime.utcnow(),
                color=0xff0000
            ))

        if isinstance(error, commands.errors.NotOwner):
            await ctx.send(stringTable['notOwner'])
            return 6
        if isinstance(error, commands.errors.ConversionError):
            await ctx.send(
                ':bangbang: Hey bud, seems like you tried to input some invalid type of arguments to the command call!\n'
                'Either CoNsUlT a PsYcHiAtRiSt or check the usage. Please!')
            return 4

        if isinstance(error, commands.errors.BadArgument):
            await ctx.send(
                ':grey_question: Whoops. The discord special expression you have specified when issuing that command is invalid.'
                ':mag: This error occurrs usually because of the bot fails to find the object.')
            return 4
        if isinstance(error, excepts.NotMod):
            return await ctx.send(str(error))

        # All other Errors not returned come here. And we can just print the default TraceBack.
        await log(f'Ignoring exception in command {ctx.message.content}:' + '\n\n```' + str(traceback.format_exc()) + '\n```', guild=ctx.guild)
        return 1

slog("Adding bot commands...")


@bot.command(name='reboot', aliases=['restart'], hidden=True)
@commands.is_owner()
async def _reboot(ctx):
    global exitType
    print('Bot going to log out in 10 seconds [owner disc rq] type: reboot')
    await log('***__WARNING! BOT WILL RESTART IN 10 SECONDS!__***')
    await ctx.send(':arrows_counterclockwise: Bot will restart in 10 seconds.')
    await asyncio.sleep(10)
    await ctx.send('Logging out...')
    await log('Logging out...')
    print('Logging out...')
    exitType = 1
    await bot.logout()


@bot.command(name='shutdown', aliases=['stop', 'sdwn', 'kthxbai', 'halt'], hidden=True)
@commands.is_owner()
async def _shutdown(ctx):
    global exitType
    nlog('Bot going to log out in 10 seconds [owner disc rq] type: shutdown')
    await log('***__WARNING! BOT WILL RESTART IN 10 SECONDS!__***')
    await ctx.send(':octagonal_sign: Bot will shutdown in 10 seconds.')
    await asyncio.sleep(10)
    await ctx.send('Logging out...')
    await log('Logging out...')
    nlog('Logging out...')
    exitType = 2
    await bot.logout()


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
