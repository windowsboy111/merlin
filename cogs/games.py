import discord
from discord.ext import commands
import enum
import random


class Rps:
    ROCK = 0
    PAPER = 1
    SCISSORS = 2

    @classmethod
    def get_emoji(cls, num: int):
        if num == cls.ROCK:
            return ":punch:"
        elif num == cls.PAPER:
            return ":hand_splayed:"
        elif num == cls.SCISSORS:
            return ":v:"
    
    @classmethod
    async def convert(cls, ctx, arg: str):
        """return paper, rock or scissors, intended to be a function argument converter (function annotation)"""
        if arg.lower() not in ('rock', 'paper', 'scissors'):
            raise commands.BadArgument('Either rock, paper or scissors.')
        return ('rock', 'paper', 'scissors').index(arg.lower())


class Games(commands.Cog):
    """\
    This cog store games :) you can play with it.
    ---
    ## Commands
    - rps (rock paper scissors)
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['rockpaperscissors', 'rock_paper_scissors', 'rock-paper-scissors'])
    async def rps(self, ctx, val: Rps):
        """Enjoy your rock paper scissors"""
        myChoice = random.choice((0, 1, 2))
        embed = None
        desc = f'Me: {Rps.get_emoji(myChoice)}\nYou: {Rps.get_emoji(val)}'
        if myChoice == val:
            embed = discord.Embed(title="Draw!",        description=desc, color=0xffff00)
        elif myChoice - val == 1 or (myChoice + 2) == val:
            embed = discord.Embed(title="You lose!",    description=desc, color=0xff0000)
        else:
            embed = discord.Embed(title="You win!",     description=desc, color=0x00ff00)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Games(bot))
