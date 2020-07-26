from discord.ext import commands
from ext.quickpoll import QuickPoll as qp
import discord
import csv
import random
import botmc
import traceback
from datetime import datetime
SANDBOX_TRACEBACK = 'samples/traceback.sndbx'


class Utils(commands.Cog):
    """\
    Type: discord.ext.commands.Cog  
    Most of the utilities are stored in this cog  
    Load this extension as an external file with `client.load_extension('cogs.utils')`
    ---
    This cog contains:  
    ## Commands  
    - vote / poll
    - mc
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
                except discord.NotFound: continue
            return
        msg = await ctx.send('deleting `system32`...')
        if id == '0':       return await msg.edit(content='bruh i need da poll id')
        poll = qp(self.bot)
        await poll.tally(poll, msg=msg, ctx=ctx, id=id)
        try:                return await msg.edit(content='')
        except Exception:   return

    @commands.group(name='mc', help="Same as kccsofficial.exe mc <args>\nUsage: /mc srv hypixel", pass_context=True, aliases=['minecraft'])
    async def mc(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("2 bed idk wat u r toking 'bout, but wut?")
            return

    @mc.command(name='srv', help='list servers', aliases=['server'])
    async def srv(self, ctx, *, args: str = None):
        global embed
        global rtc
        embed = discord.Embed(title='Spinning \'round...', description='Gift me a sec')
        msg = await ctx.send(embed=embed)
        await msg.add_reaction(self.bot.get_emoji(687495401661661324))
        rtc = 0
        try:
            embed = botmc.mcsrv(embed, args)
        except botmc.InvalidArgument as e:
            rtrn = "Panic 2: InvalidArgument. Send gud args!!!!!!!?\n""Details:  " + str(e) + "\n"
            rtrn += "2 get da usage, includ da \"help\" args, i.e. `/mc help`\n"
            rtc = 2
        except botmc.OfflineServer as e:
            rtrn = "Panic 4: OfflineServer.  Details: {}\n2 get da usage, includ da \"help\" args, i.e. `/mc help`\n".format(str(e))
            rtc = 3
        except Exception as e:
            rtrn = "Panic 1: Unknun Era.  Program kthxbai.\nDetails:  " + str(e) + "\n"
            rtc = 1
        if rtc != 0:
            embed = discord.Embed(title="ERROR", description=str(rtrn), color=0xFF0000)
        embed.set_footer(text="kthxbai code: {}.".format(rtc))
        await msg.edit(embed=embed)
        await msg.remove_reaction(self.bot.get_emoji(687495401661661324), self.bot.user)

    @mc.command(name='addsrv', help='add a shortcut looking for a server', aliases=['asv'])
    async def addsrv(self, ctx, link: str = None, name: str = None, note: str = None):
        if not link or not name or not note:
            return await ctx.send('Missing required arguments :/')
        with open('data/mcsrvs.csv', mode='w') as csv_f:
            w = csv.writer(csv_f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            w.writerow([link, name, note])
            return await ctx.send('Operation completed successfully.')

    @mc.command(name='kill', help='cmd /kill')
    async def kill(self, ctx, *, member=None):
        try:
            if member == '@a' or member == '@e':
                a = ""
                for member in ctx.guild.members:
                    a += f'{member.display_name} fell out of the world\n'
                    a += f'Killed {member.display_name}\n'
                    await ctx.send(a)
                    a = ""
                return
            if member == '@r':
                r = random.choice(ctx.guild.members).display_name
                await ctx.send(f'{r} fell out fo the world.\nKilled {r}')
                return
            if member == '@p' or member == '@s':
                await ctx.send(f'{ctx.message.author.display_name} fell out of the world.\nKilled {ctx.message.author.display_name}')
                return
            if not member:
                await ctx.send(f'{ctx.message.author.display_name} fell out of the world.\nKilled {ctx.message.author.display_name}')
                return
            rs = ''
            for char in member:
                if char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    rs += char
            member = self.bot.get_user(int(rs))
            member = member or ctx.message.author
            await ctx.send(f'{member.display_name} fell out of the world.\nKilled {member.display_name}')
            return
        except Exception as e:
            await ctx.send('No entity was found')
            print(e)

    @mc.command(name='crash')
    async def crash(self, ctx, *, args=None):
        f = open("samples/mc_crash.txt", "r", encoding='utf-8')
        await ctx.send(f.read())

    @commands.command(name='invite', help='get server invite link')
    async def invite(self, ctx):
        await ctx.send((await ctx.guild.invites())[0].url)

    @commands.command(name='sandbox', help='check if a command runs properly')
    async def sandbox(self, ctx, *, commandName: str):
        command = None
        rt = None
        startTime = None
        errorCode = int()
        try:
            command = self.bot.get_command(commandName)
            if command is None:
                await ctx.send(f"msh: command not found: `{commandName}`")
                return 3
            startTime = datetime.now()
            rt = await ctx.invoke(command)
        except Exception as err:
            timeElapsed = datetime.now() - startTime
            e = discord.Embed(title='Task Failed Succefully', description=f":x: `{ctx.message.content.split()[0][:-7]}{commandName}`", color=0xff0000)
            e.add_field(name='command name', value=command.qualified_name)
            e.add_field(name='time used', value=timeElapsed)
            try:
                errorCode = str(int(rt))
            except Exception:
                try:
                    errorCode = str(rt)
                except Exception:
                    errorCode = str("return value cannot be converted to string")
            e.add_field(name='Return value', value=errorCode)
            e.add_field(name='Error type', value=type(err).__name__)
            e.add_field(name='Error message', value=str(err))
            e.timestamp = datetime.utcnow()
            with open(SANDBOX_TRACEBACK, 'w') as f:
                f.write(traceback.format_exc())
            await ctx.send(embed=e, file=discord.File(open(SANDBOX_TRACEBACK, 'r'), 'traceback.txt'))
            return 0
        timeElapsed = datetime.now() - startTime
        e = discord.Embed(title='the command runs without any error!', description=f":white_check_mark: `{ctx.message.content.split()[0][:-7]}{commandName}`", color=0x00ff00)
        e.add_field(name='command name', value=command.qualified_name)
        e.add_field(name='time used', value=timeElapsed)
        try:
            errorCode = str(int(rt))
        except Exception:
            try:
                errorCode = str(rt)
            except Exception:
                errorCode = str("return value cannot be converted to string")
        e.add_field(name='Return value', value=errorCode)
        e.timestamp = datetime.utcnow()
        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Utils(bot))
