import discord, datetime, json
from discord.ext import commands


def get_prefix(bot: commands.Bot, message):
    with open('data/settings.json', 'r') as f:
        settings = json.load(f)
        prefix = None
        try:
            prefix = settings['g' + str(message.guild.id)]['prefix']
        except KeyError:
            settings['g' + str(message.guild.id)] = {'prefix': ["/"]}
            prefix = ['/']
        result = prefix.copy()
        result.append('<@690839099648638977> ')
        return result


bot = discord.ext.commands.Bot(
    command_prefix=get_prefix,
    description="The bot for KCCS Official",
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
