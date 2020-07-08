import time,botmc,discord,random,asyncio,threading,sys,subprocess,multiprocessing,contextlib,sys,os,easteregg,contextlib,csv,traceback,datetime
from discord.ext import commands
from time import sleep
from consolemod import * # pylint: disable=unused-wildcard-import
from logcfg import logger
from discord.utils import get
from io import StringIO, TextIOWrapper, BytesIO
_globals = globals()
_locals = locals()
o_globals = globals()
o_locals = locals()
rt = ''
runno = 0
lastmsg = []
shell = dict()
shell['py_out'] = ''
stop = False
statusLs = ['windowsboy111 coding...','vincintelligent searching for ***nhub videos','Useless_Alone._.007 playing with file systems','cat, win, vin, sir!']
cogs = ['fun','utilities','debug','man']
embed=discord.Embed()

def py_shell(message,trash,_globals,_locals):
    global shell
    if '.fork()' in message.content.lower():
        shell['py_out'] = 'Enough fork bomb.\n>>>'
        return
    else:
        msg = message.content
        if '```py' in msg:
            msg = msg[5:-3]
        if '```' in msg:
            msg = msg[3:-3]
        # setup the environment
        @contextlib.contextmanager
        def stdoutIO(stdout=None):
            old = sys.stdout
            if stdout is None:
                stdout = StringIO()
            sys.stdout = stdout
            yield stdout
            sys.stdout = old
        out = ''
        try:
            with stdoutIO() as s:
                exec(msg,_globals,_locals)
            out = s.getvalue()
        except Exception:
            out = traceback.format_exc()
        shell['py_out'] = '```\n' + out + '\n>>>```'
        if len(shell['py_out']) > 1998:
            f = open("samples/pyoutput.txt","w")
            f.write(shell['py_out'])
            f.close()
        return
def load_py(message:discord.Message,shell:dict,_globals,_locals):
    global stop
    t = threading.Thread(target=py_shell,args=[message,shell,_globals,_locals])
    t.start()
    while t.is_alive():
        if stop:
            return


bot = commands.Bot(
    command_prefix = '/',
    description="The bot for KCCS Official",
    owner_id=653086042752286730,
    case_insensitive=True
)

async def log(message:str,*,guild: discord.Guild=None,guild_id: int=None):
    if not guild:
        for guild in bot.guilds:
            for channel in guild.channels:
                if channel.name == 'merlin-py':
                    await channel.send(f"[{datetime.datetime.now()}] {message}")
                    return
    else:
        if not guild and guild_id:
            try:
                guild = await bot.fetch_guild(guild_id)
            except:
                return 1
        for channel in guild.channels:
            if channel.name == 'merlin-py':
                await channel.send(f"[{datetime.datetime.now()}] {message}")
    return