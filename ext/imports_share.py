import discord, datetime, json
from discord.ext import commands
import ext.excepts
SETFILE = "data/settings.json"


def get_prefix(bot: commands.Bot, message: discord.Message):
    """Get prefix for guild"""
    if isinstance(message.channel, discord.channel.DMChannel):
        return (f'{bot.user.mention} ', '/')
    with open('data/settings.json', 'r') as f:
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


bot = discord.ext.commands.Bot(
    command_prefix=get_prefix,
    description="an awesome discord bot coded in discord.py",
    owner_id=653086042752286730,
    case_insensitive=True
)


async def log(message: str, *, guild: discord.Guild = None, guild_id: int = None):
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
            except Exception:
                return 1
        for channel in guild.channels:
            if channel.name == 'merlin-py':
                await channel.send(f"[{datetime.datetime.now()}] {message}")
    return


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
        else:
            raise exceptions.NotMod(f"{ctx.author} is not a moderator / administrator in the given guild")
    return commands.check(predicate)
