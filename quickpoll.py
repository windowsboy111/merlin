import discord
from discord.ext import commands


class QuickPoll:
    """"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def quickpoll(self, ctx, question, options: str):
        if len(options) <= 1:
            await ctx.send('You need more than one option to make a poll!')
            return
        if len(options) > 10:
            await ctx.send('You cannot make a poll for more than 10 things!')
            return

        if len(options) == 2 and options[0] == 'yes' and options[1] == 'no':
            reactions = ['✅', '❌']
        else:
            reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

        description = []
        for x, option in enumerate(options):
            description += '\n {} {}'.format(reactions[x], option)
        embed = discord.Embed(title=question, description=''.join(description),color=0x00FFBB)
        embed.set_author(name=ctx.message.author,icon_url=ctx.message.author.avatar_url)
        react_message = await ctx.send(embed=embed)
        for reaction in reactions[:len(options)]:
            await react_message.add_reaction(reaction)
        embed.set_footer(text='Poll ID: {}'.format(react_message.id))
        await react_message.edit(embed=embed)

    @commands.command(pass_context=True)
    async def tally(self, ctx, id):
        poll_message = await discord.TextChannel.fetch_message(ctx.message.channel, id)
        if not poll_message.embeds:
            return
        embed = poll_message.embeds[0]
        if poll_message.author != ctx.message.guild.me:
            return
        unformatted_options = [x.strip() for x in embed.description.split('\n')]
        opt_dict = {x[:2]: x[3:] for x in unformatted_options} if unformatted_options[0][0] == '1' \
            else {x[:1]: x[2:] for x in unformatted_options}
        # check if we're using numbers for the poll, or x/checkmark, parse accordingly
        voters = [ctx.message.guild.me.id]  # add the bot's ID to the list of voters to exclude it's votes

        tally = {x: 0 for x in opt_dict.keys()}
        for reaction in poll_message.reactions:
            if reaction.emoji in opt_dict.keys():
                reactions = poll_message.reactions
                for reaction in reactions:
                    async for reactor in reaction.users():
                        if reactor.id not in voters:
                            tally[reaction.emoji] += 1
                            voters.append(reactor.id)

        output = discord.Embed(title='Results of the poll for "{}":\n'.format(embed.title),color=0xb6ff00)
        for key in tally.keys():
            output.add_field(name=opt_dict[key],value=tally[key])
            output.set_footer(text='Poll ID: {}'.format(id))
        msg = await ctx.send(embed=output)
        edited = discord.Embed(title=embed.title,description='Poll ended',color=0xFFC300)
        edited.add_field
        edited.set_footer(text=f"Result id: {msg.id}")
        await poll_message.edit(embed=edited)


def setup(bot):
    bot.add_cog(QuickPoll(bot))