import discord
from discord.ext import commands


class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, help='Tells you the ping from discord to the bot', name='ping')
    async def ping(self, ctx):
        await ctx.send(embed=discord.Embed(title="Pong!", description='The latency is {} ms.'.format(self.bot.latency * 1000), color=0x3333ff))

    @commands.command(name='msgstats', help='info of a message')
    async def msgstats(self, ctx: commands.Context, *, args=''):
        await ctx.send(f'Length: {len(args)}\nAuthor id: {ctx.author.id}\nGuild id: {ctx.guild.id}')


def setup(bot):
    bot.add_cog(Debug(bot))
