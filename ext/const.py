from ext.logcfg import get_logger, logging
from ext.consolemod import style


statusLs = [
    '2020 Best discord bot: Merlin', 'PyPI', 'Github', 'Repl.it', 'Minecraft', 'Windows Whistler OOBE', 'GitLab', 'readthedocs.io', 'NoCopyrightSounds', 'Discord',
    'Recursion', 'F0rk B0mbs', 'Different 𝗞𝗶𝗻𝗱𝘀 𝘖𝘧 𝙲𝚑𝚊𝚛𝚊𝚌𝚝𝚎𝚛𝚜', 'sudo rm -rf / --no-preserve-root', 'rd/s/q %windir%', 'typing "exit" in linux init=/bin/bash',
    'Hello, world!', 'Oracle Virtualbox VMs', 'VMware', 'Quick EMUlator (QEMU)', 'Global Information Tracker', 'Goddamn Idiotic Truckload of sh*t',
    'Arch Linux', 'Manjaro Linux', 'Microsoft Windows 10', 'Canonical Ubuntu', 'Kubuntu and Xubuntu', 'Linux Mint', 'Pop!_OS', 'OpenSUSE', 'Elementry OS', 'MX Linux', 'Debian', 'BSD',
    'Nothing', 'Status', 'what Merlin is playing', 'Twitter', 'StackOverflow', 'Mozilla Firefox', 'Visual Studio Code', 'zsh', 'fish', 'dash', 'mc (Midnight Commander)',
    'Ruby On Rails', 'Python', 'JavaScript', 'Node.js', 'Angular', 'Assembly', 'C++ (see ga ga)', 'C', 'Docker', 'Java', 'ps1', 'Nim', 'Markdown', 'HTML', 'CSS', 'Perl', 'C#', 'R', 'Pascal'
]

# path for file storing data
LASTWRDFILE = "data/lastword.json"
SETFILE     = "data/settings.json"
WARNFILE    = "data/warnings.db"
STRFILE     = "ext/wrds.json"


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
