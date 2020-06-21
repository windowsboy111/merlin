# bot.py
import os
# os.chdir('G:\\My drive\\coding\\py\\KCCS-Official\\')

from discord.ext import commands
from time import sleep
from consolemod import *
from logcfg import logger
from discord.utils import get
import time,botmc,discord,random,asyncio,threading,sys,subprocess,multiprocessing
from io import StringIO, TextIOWrapper, BytesIO
_globals = globals()
_locals = locals()
o_globals = globals()
o_locals = locals()
rt = ''
#console log
logger.info("Program started.")
logger.debug("Finished importing and logger configuration.  Loaded all libraries.")

TOKEN = os.getenv('DISCORD_TOKEN')
# init
bot = commands.Bot(
    command_prefix = '/',
    description="The bot for KCCS Official",
    owner_id=653086042752286730,
    case_insensitive=True
)
runno = 0
lastmsg = []
shell = dict()
shell['sh_out'] = ''
shell['py_out'] = ''
stop = False
statusLs = ['windowsboy111 coding...','vincintelligent searching for ***nhub videos','Useless_Alone._.007 playing with file systems','cat, win, vin, sir!']
cogs = ['fun','utilities','debug','man']
embed=discord.Embed()

def py_shell(message,trash,_globals,_locals):
    global shell
    # if message.content.lower() == "reset-env":
    #     def_g = open('samples/def_globals.txt','r').read()
    #     def_l = open('samples/def_locals.txt','r').read()
        
    #     shell['py_out'] = "Successfully reseted the python shell environment.\n>>>"
    #     return
    if '.fork()' in message.content.lower() or 'import os' in message.content.lower():
        shell['py_out'] = 'Enough fork bomb.\n>>>'
        return
    else:
        msg = message.content
        if '```py' in msg:
            msg = msg[5:-3]
        if '```' in msg:
            msg = msg[3:-3]
        os.system('clear')
        # setup the environment
        old_stdout = sys.stdout
        sys.stdout = TextIOWrapper(BytesIO(), sys.stdout.encoding)
        try:
            exec(msg,_globals,_locals)
        except Exception as e:
            shell['py_out'] = '```\n' + str(e) + '\n>>>```'
            return
        print(end='',flush=True)
        sys.stdout.seek(0)      # jump to the start
        out = sys.stdout.read() # read output
        # restore stdout
        sys.stdout.close()
        sys.stdout = old_stdout
        shell['py_out'] = '```\n' + out + '\n>>>```'
        if len(shell['py_out']) > 1998:
            f = open("samples/pyoutput.txt","w")
            f.write(shell['py_out'])
            f.close()
        return
def load_py(message,shell,_globals,_locals):
    global stop
    t = threading.Thread(target=py_shell,args=[message,shell,_globals,_locals])
    t.start()
    while t.is_alive():
        if stop:
            return

logger.debug("Loaded dotenv, discord_token, bot prefix, custom exceptions, and \"constant\" variables / some global variables.")
def check(person,reason,mod,_globals,_locals):
    result = ''
    if f'u{person.id}' not in _globals and f'u{person.id}' not in _locals:
        result += f"u{person.id} = {{'count': 0, 'reasons': [],'moderator': []}}\n"
    result += f"u{person.id}['reasons'].append(\"{reason}\")\n"
    result += f"u{person.id}['count'] += 1\n"
    result += f"u{person.id}['moderator'].append('{mod}')\n"
    return result
async def warn(message,person:discord.Member=None,*,reason:str='Not specified'):
    msg = await message.channel.send('Reading warnList and writing history to globals')
    rf = open('samples/warnList','r')
    await msg.edit(content='Writing and running script...')
    _globals = globals()
    _locals = locals()
    exec(rf.read(),_globals,_locals)
    result = check(person,reason,message.author.name,_globals,_locals)
    await msg.edit(content='Writing changes...')
    wf = open('samples/warnList','a')
    wf.write(result + '\n')
    rf.close()
    wf.close()
    f = open('samples/warnList','r')
    rs = '\n'.join([i for i in f.read().split('\n') if len(i) > 0])
    f.close()
    f = open('samples/warnList','w')
    f.write(rs + '\n')
    f.close()
    await msg.edit(content=f'{message.author.mention} warned {person.mention}.\nReason: {reason}.')
######################################################################################################################################################################################
@bot.event
async def on_message(message):
    global lastmsg,shell,_globals,_locals,stop
    if message.author.bot and not message.content.startswith('/warn '):
        return
    if message.content.startswith('/warn '):
        if message.author.id == bot.user.id:
            memberid = message.content.split(' ')[1][2:]
            memberid = memberid[:-1]
            member = bot.get_user(int(memberid))
            await warn(message,person=member,reason="spamming")
            await message.delete()
    # if message.author.name == 'Vincintelligent' and message.content.startswith('/'):
    #     await message.channel.send('No.')
    #     return
    if type(message.channel) != discord.DMChannel and message.channel.name == 'python':
        p = threading.Thread(target=load_py,args=[message,shell,_globals,_locals])
        p.start()
        p.join(5)
        if p.is_alive():
            stop = True
            p.join()
            await message.author.create_dm()
            for i in range(3):
                await message.author.dm_channel.send('No more fork bombs')
            shell['py_out'] = "Enough fork bomb."
            
        if len(shell['py_out']) > 1998:
            await message.channel.send(file=discord.File(open("samples/pyoutput.txt","r"),"output.txt"))
            stop=False
            return
        await message.channel.send(shell['py_out'])
        shell['py_out'] = ''
        stop=False
        return
    # if message.server is None and message.startswith('$/'):
    #     logger.info('Received a dm message from ' + message.author.name + 'that starts with $/, it is being treated as a command.')
    #     print(f'dm command from {message.author.name}: {message.content}')
    #     await bot.process_commands(message)
    if message.content.startswith('/'):
        logger.info(f'{message.author.name} has issued command: {message.content}')
        print(f'{message.author.name} has issued command: {message.content}')
#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
    # if 'siriustupid' in message.content.lower():
    #     logger.info(f'Detected "siriustupid" in a message from {message.author.name}')
    #     print(f'Detected "siriustupid" in a message from {message.author.name}')
    #     await message.channel.send('Sirius is so so stupid!', tts=True)
    # elif 'vincidiot' in message.content.lower():
    #     logger.info(f'Detected "vincidiot" in a message from {message.author.name}')
    #     print(f'Detected "vincidiot" in a message from {message.author.name}')
    #     await message.channel.send('Vinci is an idiot!', tts=True)
    # elif 'benz' in message.content.lower():
    #     logger.info(f'Detected "benz" in a message from {message.author.name}')
    #     print(f'Detected "benz" in a message from {message.author.name}')
    #     await message.channel.send('Stupid Benz is a sucker', tts=True)
    # elif 'what?' == message.content.lower():
    #     logger.info(f'Detected "what?" in a message from {message.author.name}')
    #     print(f'Detected "what?" in a message from {message.author.name}')
    #     await message.channel.send('Nothing.')
    if 'invite me' in message.content.lower():
        logger.info('Sending invite link...')
        print('Sending invite link...')
        await message.channel.send('RbBFAfK is the invite code for this server.\nhttps://discord.gg/RbBFAfK')
    await bot.process_commands(message)
@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType(3),name=random.choice(statusLs))
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print(style.cyan(f'Logged in as {bot.user.name} - {bot.user.id}'))
    for cog in cogs:
        bot.load_extension('cogs.' + cog)
    global o_globals
    global o_locals
    o_globals = globals()
    o_locals = locals()
    
    return
@bot.event
async def on_member_join(member):
    logger.info(f"Detected {member.name} joined, welcoming the member in dm...")
    await member.create_dm()
    await member.dm_channel.send(f'Hi {member.name}, welcome to KCCS Official Discord server!\nBy using the guild, you accept the rules.\nPlease answer the following questions:\nAre you a KCCS student?')
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
async def kill(ctx,*,member=None):
    try:
        if member=='@a' or member=='@e':
            a = ""
            for member in ctx.guild.members:
                a += f'{member.display_name} fell out of the world\n'
                a += f'Killed {member.display_name}\n'
                await ctx.send(a)
                a=""
            return
        if member=='@r':
            r = random.choice(ctx.guild.members).display_name
            await ctx.send(f'{r} fell out fo the world')
            await ctx.send(f'Killed {r}')
            return
        if member == '@p' or member == '@s':
            await ctx.send(f'{ctx.message.author.display_name} fell out of the world.\nKilled {ctx.message.author.display_name}')
            return
        if member == None:
            await ctx.send(f'{ctx.message.author.display_name} fell out of the world.\nKilled {ctx.message.author.display_name}')
            return
        rs = ''
        for char in member:
            if char in ['0','1','2','3','4','5','6','7','8','9']:
                rs += char
        member = bot.get_user(int(rs))
        member = member or ctx.message.author
        await ctx.send(f'{member.display_name} fell out of the world.\nKilled {member.display_name}')
        return
    except Exception as e:
        await ctx.send('No entity was found')
        print(e)
@mc.command(name='crash')
async def crash(ctx,*,args=None):
    f=open("samples/mc_crash.txt", "r",encoding='utf-8')
    await ctx.send(f.read())


######### background
async def status():
    await bot.wait_until_ready()
    while True:
        try:
            activity = discord.Activity(type=discord.ActivityType(3),name=random.choice(statusLs))
            await bot.change_presence(status=discord.Status.online, activity=activity)
            await asyncio.sleep(30)
        except:
            pass
bot.loop.create_task(status())

#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_#*_
bot.run(TOKEN,bot=True,reconnect=True)