"""
This script contains constant paths and objects,
and also global functions
"""
import json
import asyncio
from datetime import datetime
import discord
from discord.ext import commands
from ext import excepts
from ext.logcfg import gLogr
from modules.consolemod import style
__all__ = [
    "fix_settings", "DEFAULT_SETTINGS", "chk_sudo", "log", "bot", "get_prefix",
    "STATUSES", "BOTSETFILE", "LASTWRDFILE", "SETFILE", "WARNFILE", "STRFILE", "TAGFILE"
]


STATUSES = [
    'Best discord bot: Merlin', 'PyPI', 'Github', 'Repl.it', 'Minecraft', 'Windows Whistler OOBE', 'GitLab', 'readthedocs.io', 'NoCopyrightSounds', 'Discord',
    'Recursion', 'F0rk B0mbs', 'Different 𝗞𝗶𝗻𝗱𝘀 𝘖𝘧 𝙲𝚑𝚊𝚛𝚊𝚌𝚝𝚎𝚛𝚜', 'sudo rm -rf / --no-preserve-root', 'rd/s/q %windir%', 'typing "exit" in linux init=/bin/bash',
    'Hello, world!', 'Oracle Virtualbox VMs', 'VMware', 'Quick EMUlator (QEMU)', 'Global Information Tracker', 'Goddamn Idiotic Truckload of sh*t',
    'Arch Linux', 'Manjaro Linux', 'Microsoft Windows 10', 'Canonical Ubuntu', 'Kubuntu and Xubuntu', 'Linux Mint', 'Pop!_OS', 'OpenSUSE', 'Elementry OS', 'MX Linux', 'Debian', 'BSD',
    'Nothing', 'Status', 'what Merlin is playing', 'Twitter', 'StackOverflow', 'Mozilla Firefox', 'Visual Studio Code', 'zsh', 'fish', 'dash', 'mc (Midnight Commander)',
    'Ruby On Rails', 'Python', 'JavaScript', 'Node.js', 'Angular', 'Assembly', 'C++ (see ga ga)', 'C', 'Docker', 'Java', 'ps1', 'Nim', 'Markdown', 'HTML', 'CSS', 'Perl', 'C#', 'R', 'Pascal']



# path for file storing data
BOTSETFILE = "ext/bot_settings.json"
LASTWRDFILE = "data/lastword.json"
SETFILE = "data/settings.json"
WARNFILE = "data/warnings.db"
STRFILE = "ext/wrds.json"
BOTSETFILE = "ext/bot_settings.json"
SETFILE = "data/settings.json"
TAGFILE = "data/tags.db"
RANKFILE = "data/rank.db"


<<<<<<< HEAD
logger, eventLogger, cmdHdlLogger = get_logger(
    'Merlin'), get_logger('EVENT'), get_logger('CMDHDL')
logging.basicConfig(filename='discordbot.log', level=15,
                    format='[%(asctime)s]%(levelname)s - %(name)s: %(message)s')
HINT_LEVEL_NUM = 17
logging.addLevelName(HINT_LEVEL_NUM, "HINT")

def hint(self, message, *args, **kws):
    """hint logging level"""
    if self.isEnabledFor(HINT_LEVEL_NUM):
        # Yes, logger takes its '*args' as 'args'.
        self._log(HINT_LEVEL_NUM, message, args, **kws)

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

=======
logger, eventLogger, cmdHdlLogger = gLogr('Merlin.root', 'Merlin.event', 'Merlin.cmdHdl')
>>>>>>> master

def get_prefix(bot: commands.Bot, message: discord.Message):
    """Get prefix for guild"""
    if isinstance(message.channel, discord.channel.DMChannel):
        return (f'{bot.user.mention} ', '/')
    with open(SETFILE, 'r') as f:
        settings = json.load(f)
        prefix = None
        try:
            prefix = settings['g' + str(message.guild.id)]['prefix']
        except KeyError:
            settings['g' + str(message.guild.id)] = {'prefix': ["/"]}
            json.dump(settings, open(SETFILE, 'w'))
            prefix = ['/']
        prefixes = prefix.copy()
        prefixes.append(f'<@!{bot.user.id}> ')
        prefixes.append(f'<@{bot.user.id}> ')
        return tuple(prefixes)


<<<<<<< HEAD
bot = discord.ext.commands.Bot(
    command_prefix=get_prefix,
    description="an awesome discord bot coded in discord.py",
    owner_id=653086042752286730,
    case_insensitive=True)


class Log:
=======
class Log:
    def __init__(self, bot):
        self.bot = bot
>>>>>>> master
    @staticmethod
    async def worker_log(name, queue):
        slept = 0
        while True:
            if slept >= 10:
                return  # timeout
            if queue.empty():
                slept += 0.1
                await asyncio.sleep(0.1)  # come back and check later
                continue
            channel, msg = await queue.get()
            await channel.send(f"[{datetime.utcnow().time()}] {msg}")
            queue.task_done()
            slept = 0  # reset timeout

<<<<<<< HEAD
    @classmethod
    async def __call__(cls, message: str, *, guild: discord.Guild = None):
=======
    async def __call__(self, message: str, guild: discord.Guild = None):
>>>>>>> master
        if guild:
            for channel in guild.channels:
                if channel.name == 'merlin-py':
                    await channel.send(f"[{datetime.now()}] {message}")
                    return
        queue = asyncio.Queue()
        tasks = []
        for i in range(5):
<<<<<<< HEAD
            tasks.append(asyncio.create_task(cls.worker_log(f'worker-log-{i}', queue)))
        for guild in bot.guilds:
=======
            tasks.append(asyncio.create_task(self.worker_log(f'worker-log-{i}', queue)))
        for guild in self.bot.guilds:
>>>>>>> master
            for channel in guild.channels:
                if channel.name == 'merlin-py':
                    queue.put_nowait((channel, message))
                    break
<<<<<<< HEAD
log = Log()
=======

>>>>>>> master

def is_sudoers(member: discord.Member):
    """\
    Type: function
    Checks if the provided member has admin roles (has moderating priviledges)
    This function fetches the Admin roles list from the settings `dict()`
    ---
    return: bool
    """
    settings = json.load(open(SETFILE, 'r'))
    if member.guild.owner == member:
        return True
    for role in member.roles:
        try:
            if role.name in settings[f'g{member.guild.id}']['sudoers']:
                return True
        except KeyError:
            settings[f'g{member.guild.id}'] = {"sudoers": [], "prefix": ["/"]}
            with open(SETFILE, 'w') as outfile:
                json.dump(settings, outfile)
    return False

def chk_sudo():
    """\
    Type: decorator
    The command will only be able to be executed by the author if the author is owner or have permissions
    """
    async def predicate(ctx):
        if is_sudoers(ctx.author):
            return True
        await ctx.message.add_reaction("🛑")
        return False
    return commands.check(predicate)


DEFAULT_SETTINGS = {
    "prefix": ["/"],
    "sudoers": [],
    "cmdHdl": {
        "cmdNotFound": 0,
        "delIssue": 0,
        "improveExp": 0}}


<<<<<<< HEAD
def fix_settings(guild: discord.Guild):


    settings = None
    try:
        settings = json.load(open(SETFILE, 'r'))
    except Exception:
        settings = {}
        open(SETFILE, 'w').write("{}")
    try:
        settings[f"g{guild.id}"]['cmdHdl']
    except KeyError:
        settings[f"g{guild.id}"] = DEFAULT_SETTINGS.copy()
        with open(SETFILE, 'w') as outfile:
            json.dump(settings, outfile)
        return
    # fix cmdHdl
    cmdHdl = DEFAULT_SETTINGS['cmdHdl'].copy()          # the following code will leave entrys already
    cmdHdl.update(settings[f'g{guild.id}']['cmdHdl'])   # exists and add the missing entrys so that
    settings[f'g{guild.id}']['cmdHdl'] = cmdHdl         # overwriting can be prevented
    default = DEFAULT_SETTINGS.copy()
    default.update(settings[f'g{guild.id}'])            # we can also do the same thing for the whole settings
    settings[f'g{guild.id}'].update(default)
    with open(SETFILE, 'w') as outfile:
        json.dump(settings, outfile)
=======
>>>>>>> master
