from discord.ext import commands
from ext.quickpoll import QuickPoll as qp
import discord


class Utils(commands.Cog):
    """\
    Type: discord.ext.commands.Cog
    Most of the utilities are stored in this cog
    Load this extension as an external file with `client.load_extension('cogs.utils')`
    ---
    This cog contains:
    ## Commands
    - vote / poll
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True, help="/help vote", aliases=['poll', 'voting'], name='vote')
    async def vote(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("2 bed idk wat u r toking 'bout, but wut?")
            return

    @vote.command(name='create', help='Create a vote: /vote create <name> <choices>', aliases=['make', 'mk', 'new'])
    async def create(self, ctx, name='', *options: str):
        if name == '':
            await ctx.send('Bruh, wuts da title of the poll?')
            return
        msg = await ctx.send('Once apon a time, there was a poll, that YOU SHOULDN\'T SEE DIS MESSAGE! OR ELSE DISCORD IS LAGGY!')
        poll = qp(self.bot)
        await poll.quickpoll(poll, msg=msg, ctx=ctx, question=name, options=options)
        await msg.edit(content='')
        return

    @vote.command(name='check', help='Check polls that has not ended', aliases=['chk'])
    async def check(self, ctx, *, num='0'):
        if num == '0':
            num = 0xFFFFFF
        result = ''
        result2 = list()
        id = list()
        msg = await ctx.send('You have forgotten something...')
        messages = None
        if not num:
            messages = await ctx.message.channel.history(limit=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF).flatten()
        else:
            messages = await ctx.message.channel.history(limit=int(num)).flatten()
        for message in messages:
            if message.author != ctx.message.guild.me:
                continue
            if not message.embeds:
                continue
            embed = message.embeds[0]
            try:
                if 'Poll ID: ' not in embed.footer.text:
                    continue
            except Exception:
                continue
            if embed.title.startswith('Results of the poll for "'): continue
            if embed.description != 'Poll ended':
                link = f'[{message.created_at}]({message.jump_url})\n'
                result += link
                result2.append(embed.title)
                id.append(message.id)
        if result == '':
            await msg.edit(content='No unended polls detected.')
            return
        rs = result.split('\n')
        embed = discord.Embed(title='Running polls')
        loopCount = 0
        for r in rs:
            if loopCount == len(result2):
                break
            embed.add_field(name=result2[loopCount], value=r)
            loopCount += 1
        await msg.edit(content='Results: ' + str(len(result2)), embed=embed)
        return id

    @vote.command(name='end', help='End a vote or poll')
    async def end(self, ctx, *, id='0'):
        if id == 'all':
            ctx = await self.bot.get_context(ctx.message)
            ids = await self.check(num=None, ctx=ctx)
            for msgid in ids:
                channel = ctx.message.channel
                try:
                    ctx = await self.bot.get_context(await channel.fetch_message(msgid))
                    await self.end(ctx=ctx, id=msgid)
                except discord.NotFound:    continue
            return
        msg = await ctx.send('deleting `system32`...')
        if id == '0':       return await msg.edit(content='bruh i need da poll id')
        poll = qp(self.bot)
        await poll.tally(poll, msg=msg, ctx=ctx, id=id)
        try:                return await msg.edit(content='')
        except Exception:   return


def setup(bot):
    bot.add_cog(Utils(bot))
