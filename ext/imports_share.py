import discord, datetime
from ext.imports_init import bot
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
