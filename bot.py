#!/bin/python3
# bot.py
import sys
import os
import random
import traceback
import json
import asyncio
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import find
from ext.consolemod import style
from ext.logcfg import get_logger, logging
from ext.imports_share import log, bot, get_prefix
import easteregg
print("Merlin bot written in python by windowsboy111 :)")
print('==> Starting...')
print(' >> Imported libraries...')
load_dotenv()
print(' >> Defining constant variables...')
exitType = 0
statusLs = ['windowsboy111 coding...', 'vincintelligent searching for ***nhub videos', 'Useless_Alone._.007 playing with file systems', 'cat, win, vin, sir!']
cogs = []
for cog in os.listdir('cogs/'):
    if cog.endswith('.py'):
        cogs.append(cog[:-3])
embed = discord.Embed()
lastmsg = list()
# token is stored inside ".env"
TOKEN = os.getenv('DISCORD_TOKEN')
LASTWRDFILE = "data/lastword.json"
lastword = json.load(open(LASTWRDFILE, 'r'))
SETFILE = "data/settings.json"
stringTable = json.load(open('ext/wrds.json', 'r'))
print(' >> Configuring bot...')
logger = get_logger('Merlin')
eventLogger = get_logger('EVENT')
cmdHdlLogger = get_logger('CMDHDL')
logging.basicConfig(filename='discordbot.log', level=15, format='[%(asctime)s]%(levelname)s - %(name)s: %(message)s')
HINT_LEVEL_NUM = 17
logging.addLevelName(HINT_LEVEL_NUM, "HINT")


def hint(self, message, *args, **kws):
    """hint logging level"""
    if self.isEnabledFor(HINT_LEVEL_NUM):
        # Yes, logger takes its '*args' as 'args'.
        self._log(HINT_LEVEL_NUM, message, args, **kws)

# %%print("hello, world!")
setattr(logging.Logger, 'hint', hint)


def slog(message: str):
    """sub log"""
    print(' >> ' + message)
    logger.hint(message)


def nlog(message: str):
    """new line long"""
    print('\n==> ' + message)
    logger.info(message)


def cmd_handle_log(message: str):
    """logging function for command handling"""
    print('[CMDHDL]\t' + message)
    cmdHdlLogger.info(message)


def event_log(message: str):
    print('[EVENT]\t' + message)
    eventLogger.info(message)


def cmd_handle_warn(message: str):
    print(style.orange + message + style.reset)
    cmdHdlLogger.warning(message)


settings = json.load(open(SETFILE))

# init
bot.remove_command('help')
MODE = os.getenv('MODE')


@bot.event
async def on_message(message: discord.Message):
    global lastmsg
    if await easteregg.easter(message):
        return
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
            try:
                await message.delete()
            except Exception:
                pass
            finally:
                return
        except discord.ext.commands.errors.CommandNotFound:
            return
        except Exception:
            await message.channel.send(f'{message.author.mention}, there was an error trying to execute that command! :(')
            print(traceback.format_exc())
    if isinstance(message.channel, discord.channel.DMChannel):
        return 0
    try:
        global lastword
        lastword[f'g{message.guild.id}'][str(message.author.id)] = message.id
    except KeyError:
        lastword[f'g{message.guild.id}'] = {message.author.id: message.id}
    if (message.author.bot):
        return
    if lastmsg == []:
        lastmsg = [message.content.lower(), message.author, 1, False]
    elif lastmsg[2] == 4 and message.content.lower() == lastmsg[0] and message.author == lastmsg[1] and lastmsg[3]:
        lastmsg[2] += 1
        try:
            await message.delete()
        except Exception:
            pass
        ctx = await bot.get_context(message)
        await ctx.invoke(bot.get_command('warn'), person=lastmsg[1], reason='spamming')
    elif lastmsg[0] == message.content.lower() and lastmsg[1] == message.author:
        lastmsg[2] += 1
        if lastmsg[2] == 4:
            lastmsg[3] = True
    else:
        lastmsg = [message.content.lower(), message.author, 1, False]
    with open(LASTWRDFILE, 'w') as f:
        json.dump(lastword, f)


@bot.event
async def on_ready():
    nlog(f'Logged in as {bot.user.name} - {bot.user.id} in {MODE} mode')
    slog('Telling guilds...')
    if not MODE or MODE == 'NORMAL':
        activity = discord.Activity(type=discord.ActivityType(3), name=random.choice(statusLs))
        await bot.change_presence(status=discord.Status.online, activity=activity)
        await log('Logged in!')
    elif MODE == 'DEBUG':
        await bot.change_presence(status=discord.Status.idle)
        await log('RUNNING IN **DEBUG** MODE!')
    elif MODE == 'FIX':
        await bot.change_presence(status=discord.Status.dnd)
        await log('*RUNNING IN EMERGENCY **FIX** MODE!')
    await log('logged in')
    nlog('Loading Extensions...')
    try:
        for cog in cogs:
            slog(f'Loading {cog}...')
            bot.load_extension('cogs.' + cog)
        await log('loaded extensions / cogs')
    except Exception:
        nlog("An error occurred during loading extension, treat bot start as a reconnect")
        nlog("Reconnected!")
        return 2
    nlog("Ready!")
    return 0


@bot.event
async def on_member_join(member: discord.Member):
    eventLogger.info(f"Detected {member} joined, welcoming the member in dm...")
    try:
        await member.send(f'Hi {member}, welcome to {member.guild.name} Discord server!\nBy using the guild, you accept the rules.')
    except discord.Forbidden:
        eventLogger.warn(f"Failed to send dm to {member}, fallback server welcome")
        await member.guild.send(f'Hi {member}, welcome to {member.guild.name} Discord server!\nBy using the guild, you accept the rules. (Failed to send dm to this user)')
    print(f"{member} has joined the server.")


@bot.event
async def on_guild_join(guild):
    general = find(lambda x: x.name == 'general',  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send(f'Hello {guild.name}! This is Merlin!\nMy prefix is `/` and `$`.\n'
                           'You can create a channel called #merlin-py and I can log my own stuff!\n'
                           'Thanks for supporting! https://github.com/windowsboy111/Merlin-py\n\n'
                           'If I have permissions, the owner of this guild will be informed to setup. Or else, type `/settings`.')
        await guild.owner.send("**SETUP**\nBefore using me, let's spend a few minutes setting up Merlin...\n"
                               "To continue, type (and press enter to send) `y` (300 seconds timeout)")

        ret = await bot.wait_for('message', check=lambda m: m.author == guild.owner and m.content == 'y', timeout=300)
        await guild.owner.send("type prefix: (timeout 30)")
        ret = await bot.wait_for('message', check=lambda m: m.author == guild.owner, timeout=30)
        gprefix = ret.content
        await guild.owner.send("type admin roles, seperated with `, ` and send it (don't do `@`, timeout 60)")
        ret = await bot.wait_for('message', check=lambda m: m.author == guild.owner, timeout=60)
        sudoers = ret.content.split(', ')
        await guild.owner.send("thx! done!")
        f = json.load(open(SETFILE, 'r'))
        f[f'g{guild.id}'] = {"prefix": gprefix, "sudoers": sudoers}
        with open(SETFILE, 'w') as outfile:
            json.dump(f, outfile)
    return


# background
async def status():
    await bot.wait_until_ready()
    while True:
        try:
            if not MODE or MODE == 'NORMAL':
                activity = discord.Activity(type=discord.ActivityType(3), name=random.choice(statusLs))
                await bot.change_presence(status=discord.Status.online, activity=activity)
            elif MODE == 'DEBUG':
                activity = discord.Activity(type=discord.ActivityType(3), name="windowsboy111 debugging me")
                await bot.change_presence(status=discord.Status.idle, activity=activity)
            elif MODE == 'FIX':
                await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType(3), name="windowsboy111 fixing me"))
            await asyncio.sleep(30)
        except Exception:
            pass
try:
    bot.loop.create_task(status())
except Exception:
    pass


@bot.event
async def on_command_error(ctx, error):
    try:
        raise error
    except Exception:
        # This tells the issuer that the command cannot be used in DM
        if isinstance(error, commands.errors.NoPrivateMessage):
            try:
                return await ctx.author.send(f':X::lock: {ctx.command} cannot be used in Private Messages.')
            except discord.HTTPException:
                return
        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        # This prevents any cogs with an overwritten cog_command_error being handled here.
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, commands.errors.CommandNotFound):
            return await ctx.send("Welp, I've no idea. Command not found!")
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.invoke(bot.get_command('help'), cmdName=ctx.command.qualified_name)
        if isinstance(error, commands.BadArgument):
            return await ctx.invoke(bot.get_command('help'), cmdName=ctx.command.qualified_name)

        if isinstance(error, commands.errors.DisabledCommand):
            return await ctx.send(embed=discord.Embed(
                title=f'{ctx.command} has been disabled.',
                description=f':x: `{ctx.message.content}`',
                color=0xff0000
            ))

        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(embed=discord.Embed(
                title='uh oh. An exception has occurred during the execution of the command',
                description=stringTable['CommandInvokeError'].format(content=ctx.message.content),
                color=0xff0000
            ))

        if isinstance(error, discord.ext.commands.errors.NotOwner):
            return await ctx.send(stringTable['notOwner'])

        if isinstance(error, commands.errors.BadArgument):
            return await ctx.send('Whoops. The discord special expression you have specified when issuing that command is invalid. '
                                  'That member / channel / other kinds of object might not exist because I cannot find it.')
        # All other Errors not returned come here. And we can just print the default TraceBack.
        await log(f'Ignoring exception in command {ctx.message.content}:' + '\n\n```' + str(traceback.format_exc()) + '\n```', guild=ctx.guild)

slog("Adding bot commands...")


@bot.command(name='reboot', aliases=['restart'], hidden=True)
@commands.is_owner()
async def _reboot(ctx):
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
async def _shutdown(ctx):
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

# login / start services
slog('Running / logging in...          ')
while True:
    bot.run(TOKEN, bot=True, reconnect=True)
    if exitType == 0:
        nlog("Uh oh whoops, that's awkward... Bot has logged out unexpectedly. trying to relog in...")
        continue
    else:
        nlog('Logged out')
        break
if exitType == 2:
    print("\nExiting...")
    open('discordbot.log', 'w').write('')
    sys.exit(0)
slog('Tidying up...')
for var in dir():
    if var.startswith('__'):
        continue
    if var in ['os', 'sys', 'multiprocessing']:
        continue
    try:
        del globals()[var]
    except KeyError:
        pass
    try:
        del locals()[var]
    except KeyError:
        pass
print('==> Removed all variables\n==> Restarting script...\n\n')
try:
    os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
except PermissionError as e:
    print(f"OPERATION FAILED: {str(e)}")
    open('discordbot.log', 'w').write('')
    sys.exit(2)
