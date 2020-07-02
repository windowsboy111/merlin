import time,botmc,discord,random,asyncio,threading,sys,subprocess,multiprocessing,contextlib,sys,os,easteregg,contextlib,csv
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
        except Exception as e:
            out = str(e)
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
def check(person:discord.Member,reason:str,mod,_globals,_locals):
    result = ''
    if f'u{person.id}' not in _globals and f'u{person.id}' not in _locals:
        result += f"u{person.id} = {{'count': 0, 'reasons': [],'moderator': []}}\n"
    result += "u{id}['reasons'].append(\"{r}\")\n".format(r=reason.replace('"','\\"'),id=person.id)
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
