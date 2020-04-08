from discord.ext import commands
from logcfg import logger
from quickpoll import QuickPoll as qp
import discord

class utils(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    @commands.command(pass_context=True, help='Tells you the ping from discord to the bot', name='ping')
    async def ping(self,ctx):
        await ctx.send(embed=discord.Embed(title="Pong!", description='The latency is {} ms.'.format(self.bot.latency*1000), color=0x3333ff))

    @commands.group(pass_context=True,help="/help vote",aliases=['poll','voting'])
    async def vote(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f"2 bed idk wat u r toking 'bout, but wut?")
    @vote.command(name='create',help='Create a vote: /vote create <name> <choices>')
    async def create(self,ctx,name,*options: str):
        logger.info(f"{ctx.message.author.name} has issued command /vote create {name} " + str(options))
        poll = qp(self.bot)
        await poll.quickpoll(poll,ctx=ctx,question=name,options=options)
        logger.info(f'finished request /vote create {name} {str(options)} from {ctx.author.name}.')
        return
    @vote.command(name='end',help='End a vote: /vote end <name>')
    async def end(self,ctx,*,id):
        poll = qp(self.bot)
        await poll.tally(poll,ctx=ctx,id=id)
        return


def setup(bot):
    bot.add_cog(utils(bot))