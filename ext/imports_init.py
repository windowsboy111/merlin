import time, botmc, discord, random, asyncio, threading, contextlib, sys, os, easteregg, csv, traceback, datetime
from discord.ext import commands
from time import sleep
from ext.consolemod import cursor, style
from ext.logcfg import logger
from discord.utils import find, get
from io import StringIO
rt = ''
runno = 0
shell = dict()
shell['py_out'] = ''
stop = False
statusLs = ['windowsboy111 coding...', 'vincintelligent searching for ***nhub videos', 'Useless_Alone._.007 playing with file systems', 'cat, win, vin, sir!']
cogs = []
for cog in os.listdir('cogs/'):
    if cog.endswith('.py'):
        cogs.append(cog[:-3])
embed = discord.Embed()


def py_shell(message, trash, _globals, _locals):
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
                exec(msg, _globals, _locals)
            out = s.getvalue()
        except Exception:
            out = traceback.format_exc()
        shell['py_out'] = '```\n' + out + '\n>>>```'
        if len(shell['py_out']) > 1998:
            f = open("data/pyoutput.txt", "w")
            f.write(shell['py_out'])
            f.close()
        return


def load_py(message: discord.Message, shell: dict, _globals, _locals):
    global stop
    t = threading.Thread(target=py_shell, args=[message, shell, _globals, _locals])
    t.start()
    while t.is_alive():
        if stop:
            return


bot = commands.Bot(
    command_prefix='/',
    description="The bot for KCCS Official",
    owner_id=653086042752286730,
    case_insensitive=True
)
