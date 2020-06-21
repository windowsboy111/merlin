from discord.ext import commands
from logcfg import logger


class debug(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name='emojis',help='Print all emojis')
    async def emojis(self,ctx):
        for emoji in ctx.guild.emojis:
            await ctx.send(str(self.bot.get_emoji(emoji.id)) + str(emoji.id) + f" {emoji.name}")


def setup(bot):
    bot.add_cog(debug(bot))