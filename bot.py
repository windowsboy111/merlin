#!/bin/python3
# bot.py
from dotenv import load_dotenv
from ext.imports_init import bot, traceback, commands, discord, asyncio, statusLs, random, csv, logger, botmc, find, cogs, style, threading, load_py, easteregg, os
import json
from ext.imports_share import log
_globals = globals()
_locals = locals()
lastmsg = list()
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SETFILE = "data/settings.json"
# token is stored inside ".env"

# console log
logger.info("Program started.")
logger.debug("Finished importing and logger configuration.  Loaded all libraries.")

# init
bot.remove_command('help')
logger.debug("Loaded env, custom exceptions, and \"constant\" variables / some global variables.")
MODE = os.getenv('MODE')
print(f"running in {MODE} mode...")


@bot.event
async def on_message(message: discord.Message):
    global lastmsg, shell, _globals, _locals, stop
    if await easteregg.easter(message): return
    if type(message.channel) != discord.DMChannel and message.channel.name == 'python' and message.author != bot.user:
        p = threading.Thread(target=load_py, args=[message, shell, _globals, _locals])
        p.start()
        p.join(5)
        if p.is_alive():
            stop = True
            p.join()
            for i in range(3):  await message.author.send('No more fork bombs')
            shell['py_out'] = "Enough fork bomb."
        if len(shell['py_out']) > 1998:
            await message.channel.send(file=discord.File(open("data/pyoutput.txt", "r"), "output.txt"))
            stop = False
            return
        await message.channel.send(shell['py_out'])
        shell['py_out'] = ''
        stop = False
        return
    if message.content.startswith('/') and message.author != bot.user:
        isCmd = False
        for cmd in bot.commands:
            if message.content.lower().split(' ')[0] == '/' + cmd.name:
                isCmd = True
                break
            for alias in cmd.aliases:
                if message.content.lower().split(' ')[0] == '/' + alias:
                    isCmd = True
                    break
        if isCmd:
            msgtoSend = f'{message.author.name} has issued command: {message.content}'
            logger.info(msgtoSend)
            print(msgtoSend)
            await log(message.channel.mention + ' ' + msgtoSend, guild=message.channel.guild)
            try:
                await bot.process_commands(message)
                try:    await message.delete()
                except Exception: pass
                finally: return
            except discord.ext.commands.errors.CommandNotFound: return
            except Exception as e:
                await message.channel.send(f'{message.author.mention}, there was an error trying to execute that command! :(')
                print(str(e))
    if 'invite me' in message.content.lower():  await message.channel.send('RbBFAfK is the invite code for this server.\nhttps://discord.gg/RbBFAfK\n')
    if (message.author.bot): return
    if lastmsg == []:   lastmsg = [message.content.lower(), message.author, 1, False]
    elif lastmsg[2] == 4 and message.content.lower() == lastmsg[0] and message.author == lastmsg[1] and lastmsg[3]:
        lastmsg[2] += 1
        await message.delete()
        ctx = await bot.get_context(message)
        await ctx.invoke(bot.get_command('warn'), person=lastmsg[1], reason='spamming')
    elif lastmsg[0] == message.content.lower() and lastmsg[1] == message.author:
        lastmsg[2] += 1
        if lastmsg[2] == 4: lastmsg[3] = True
    else:   lastmsg = [message.content.lower(), message.author, 1, False]


@bot.event
async def on_ready():
    print(style.cyan(f'Logged in as {bot.user.name} - {bot.user.id}'))
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
    for cog in cogs:
        bot.load_extension('cogs.' + cog)
    await log('loaded extensions / cogs')
    return


@bot.event
async def on_member_join(member):
    logger.info(f"Detected {member.name} joined, welcoming the member in dm...")
    await member.send(f'Hi {member.name}, welcome to KCCS Official Discord server!\nBy using the guild, you accept the rules.')
    print(f"{member} has joined the server.")


@bot.event
async def on_guild_join(guild):
    general = find(lambda x: x.name == 'general',  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send(f'Hello {guild.name}! This is Merlin!\nMy prefix is `/` and `$`.\n'
                           'You can create a channel called #merlin-py and I can log my own stuff!\n'
                           'Thanks for supporting! https://github.com/windowsboy111/Merlin\n\n'
                           'If I have permissions, the owner of this guild will be informed to setup. Or else, type `/settings`.')
        await guild.owner.send("**SETUP**\nBefore using me, let's spend a few minutes setting up Merlin...\n"
                               "To continue, type (and press enter to send) `y` (300 seconds timeout)")

        def check(m):   return m.author == guild.owner and m.content == 'y'
        rt = await bot.wait_for('message', check=check, timeout=300)
        await guild.owner.send("type prefix: (timeout 30)")
        del check
        def check(m):   return m.author == guild.owner
        rt = await bot.wait_for('message', check=check, timeout=30)
        gprefix = rt.content
        await guild.owner.send("type admin roles, seperated with `, ` and send it (don't do `@`, timeout 60)")
        rt = await bot.wait_for('message', check=check, timeout=60)
        sudoers = rt.content.split(', ')
        await guild.owner.send("thx! done!")
        f = json.load(open(SETFILE, 'r'))
        f[f'g{guild.id}'] = {"prefix": gprefix, "sudoers": sudoers}
        with open(SETFILE, 'w') as outfile:
            json.dump(f, outfile)
    return


@bot.group(name='mc', help="Same as kccsofficial.exe mc <args>\nUsage: /mc srv hypixel", pass_context=True, aliases=['minecraft'])
async def mc(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("2 bed idk wat u r toking 'bout, but wut?")
        return


@mc.command(name='srv', help='list servers', aliases=['server'])
async def srv(ctx, *, args: str = None):
    global embed
    global rtc
    embed = discord.Embed(title='Spinning \'round...', description='Gift me a sec')
    msg = await ctx.send(embed=embed)
    await msg.add_reaction(bot.get_emoji(687495401661661324))
    rtc = 0
    try:
        logger.info("Attempting to call botmc.mcsrv()")
        embed = botmc.mcsrv(embed, args)
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
        embed = discord.Embed(title="ERROR", description=str(rtrn), color=0xFF0000)
        if rtc == 1:
            logger.error("Exit code: " + str(rtc))
        else:
            logger.warn("Exit code: " + str(rtc))
    else:
        logger.info("Exit code: " + str(rtc))
    embed.set_footer(text="kthxbai code: {}.".format(rtc))
    await msg.edit(embed=embed)
    await msg.remove_reaction(bot.get_emoji(687495401661661324), bot.user)


@mc.command(name='addsrv', help='add a shortcut looking for a server', aliases=['asv'])
async def addsrv(ctx, link: str = None, name: str = None, note: str = None):
    if not link or not name or not note:
        return await ctx.send('Missing required arguments :/')
    with open('data/mcsrvs.csv', mode='w') as csv_f:
        w = csv.writer(csv_f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow([link, name, note])
        return await ctx.send('Operation completed successfully.')


@mc.command(name='kill', help='cmd /kill')
async def kill(ctx, *, member=None):
    try:
        if member == '@a' or member == '@e':
            a = ""
            for member in ctx.guild.members:
                a += f'{member.display_name} fell out of the world\n'
                a += f'Killed {member.display_name}\n'
                await ctx.send(a)
                a = ""
            return
        if member == '@r':
            r = random.choice(ctx.guild.members).display_name
            await ctx.send(f'{r} fell out fo the world.\nKilled {r}')
            return
        if member == '@p' or member == '@s':
            await ctx.send(f'{ctx.message.author.display_name} fell out of the world.\nKilled {ctx.message.author.display_name}')
            return
        if not member:
            await ctx.send(f'{ctx.message.author.display_name} fell out of the world.\nKilled {ctx.message.author.display_name}')
            return
        rs = ''
        for char in member:
            if char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                rs += char
        member = bot.get_user(int(rs))
        member = member or ctx.message.author
        await ctx.send(f'{member.display_name} fell out of the world.\nKilled {member.display_name}')
        return
    except Exception as e:
        await ctx.send('No entity was found')
        print(e)


@mc.command(name='crash')
async def crash(ctx, *, args=None):
    f = open("samples/mc_crash.txt", "r", encoding='utf-8')
    await ctx.send(f.read())


# background
async def status():
    await bot.wait_until_ready()
    while True:
        try:
            if not MODE or MODE == 'NORMAL':
                activity = discord.Activity(type=discord.ActivityType(3), name=random.choice(statusLs))
                await bot.change_presence(status=discord.Status.online, activity=activity)
            elif MODE == 'DEBUG':
                await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType(3), name="windowsboy111 debugging me"))
            elif MODE == 'FIX':
                await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType(3), name="windowsboy111 fixing me"))
            await asyncio.sleep(30)
        except Exception:
            pass
bot.loop.create_task(status())


@bot.event
async def on_command_error(ctx, error):
    try:
        raise error
    except Exception:
        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            await log(f'`{ctx.content}` caused an error: ```\n{traceback.format_exc()}```')
            return await log("Note that the error has been passed to the global command error handler unexpectedly")

        # This prevents any cogs with an overwritten cog_command_error being handled here.
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, commands.errors.CommandNotFound):  return await ctx.send("Welp, I've no idea. Command not found!")
        if isinstance(error, commands.MissingRequiredArgument): return await ctx.invoke(bot.get_command('help'), cmdName=ctx.command.qualified_name)
        if isinstance(error, commands.BadArgument):             return await ctx.invoke(bot.get_command('help'), cmdName=ctx.command.qualified_name)

        if isinstance(error, commands.errors.DisabledCommand):  return await ctx.send(f'{ctx.command} has been disabled.')

        if isinstance(error, commands.errors.NoPrivateMessage):
            try:                                                return await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except discord.HTTPException:                       return

        if isinstance(error, commands.errors.CommandInvokeError):      await ctx.send('uh oh. An exception has occurred during the execution of the command. Check the log for more details.')

        if isinstance(error, commands.errors.BadArgument):      return await ctx.send('Whoops. The discord special expression you have specified when issuing that command is invalid. That member / channel / other kinds of object might not exist because I cannot find it.')
        # All other Errors not returned come here. And we can just print the default TraceBack.
        await log(f'Ignoring exception in command {ctx.message.content}:' + '\n\n```' + str(traceback.format_exc()) + '\n```', guild=ctx.guild)


bot.run(TOKEN, bot=True, reconnect=True)
