from discord.ext import commands
import discord
import random
lolpwd = 'samples/'


class Fun(commands.Cog):
    """\
    This cog is for fun only. Most of the commands here are for the author to
    experiment with discord.py. Most of them are out of support and contains
    hard-coded strings and objects which isn't great.
    ---
    ## Commands
    - cough
    - test
    - stupid
    - whatis
    - boomer
    - media
    - say
    - send
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='cough', help="Simulate cough. :)")
    async def cough(self, ctx):
        lolcough = ["What? You being infected coronavirus?", str(self.bot.get_emoji(684291327818596362)), "Please don't:\nSneeze on me;\nCough on me;\nTalk to me,\nNo oh oh!", "🤢", "Run, run, until it's done, done, until the sun comes up in the morn'."]
        response = random.choice(lolcough)
        msg = await ctx.send(response)
        await msg.add_reaction('👀')
        return

    @commands.command(name='test', help="Respond with test messages!")
    async def test(self, ctx):
        loltest = ["!urban MEE6", "Am I a joke to you?", "!8ball Siriu-smart?", f"What? Are you a developer?{ctx.message.author.mention}",
                   "Didn't expect anyone would use this command, but there it is!", "No test.", "Ping Pong!", "No.", "?????", "Siriusly, What did you expect?",
                   "Stop.", "!8ball are you stupid?", "Vincidiot"]
        response = random.choice(loltest)
        msg = await ctx.send(response)
        await msg.add_reaction('👍')
        return

    @commands.command(name='stupid', help='Shout at stupid things')
    async def stupid(self, ctx, *, args='that'):
        await ctx.send(random.choice([f'{args} is so so stupid!', f"I can't believe how stupid {args} is!", f"Seriously, {args}'s the stupidest thing I've ever heard!", f"STUPID STUPID STUPID STUPID STUPID STUPID STUPID STUPID {args}!", f"I can't believe {args}'s even a thing."]))

    @commands.command(name='whatis', help='Tells you what the input is. /whatis minecraft')
    async def whatis(self, ctx, *, args=""):
        if args == "":
            await ctx.send("Bruh, where's the argument???")
            return
        await ctx.send(random.choice([f"{args} is generally {args}.", f"Technically, {args} is {args}!", f"To know what {args} is, please run `!urban {args}`",
                                      f"Well, not in a nutshell, {args} as {args} is {args} in {args} on {args} at {args} from {args} to {args}...It's just...{args}!!!!!",
                                      f"You are so dumb that you even don't know what {args} is!"]))

    @commands.command(name='boomer', help="/boomer [person]", aliases=['boom', 'okboomer'])
    async def boomer(self, ctx, *, person=""):
        if person == "":
            person = ctx.message.author
            await ctx.send(f'OK BOOMER {person.mention}')
            return
        await ctx.send(f'OK BOOMER {person}')

    @commands.group(name='media', help='/media [sub-commands]', aliases=['sent'])
    async def media(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f"2 bed idk wat u r toking 'bout, but wut?")
            return

    @media.command(name='no', help='/media no, will give you file related to "no"', aliases=['nope', 'nah', 'np'])
    async def no(self, ctx, *, args=''):
        async with ctx.typing():
            global lolpwd
            rtrn = random.choice([
                discord.File(f"{lolpwd}Mumbo Jumbo - No No No.mp3"),
                discord.File(f"{lolpwd}Keralis and Xisuma - No No No.mp3")])
            await ctx.send(file=rtrn)

    @media.command(name='fool', help='/media stupid, will give you file related to "stupid"', aliases=['stupid', 'foolish', 'stupidity'])
    async def fool(self, ctx, *, args=''):
        global lolpwd
        async with ctx.typing():
            await ctx.send(file=discord.File(f"{lolpwd}Mumbo Jumbo - Stupid.mp3"))

    @media.command(name='discord', help='/media discord, will give you file related to "discord"', aliases=['disc', 'dc'])
    async def discord(self, ctx, *, args=""):
        global lolpwd
        async with ctx.typing():
            await ctx.send(file=discord.File(f"{lolpwd}Discord_3WIP.ogg"))

    @media.command(name='afk', help='/media afk, will give you file related to "afk"', aliases=['mumboafk'])
    async def afk(self, ctx, *, args=""):
        global lolpwd
        async with ctx.typing():
            await ctx.send(file=discord.File(f"{lolpwd}Grian - Mumbo AFK.mp3"))

    @commands.command(name='say', help='the bot is talking!')
    async def say(self, ctx, *, args=""):
        if args == '':
            return
        await ctx.send(args, tts=True)
        await ctx.message.delete()
        return

    @commands.command(name='send', help='The bot is sending messages!')
    async def send(self, ctx, *, args=""):
        if args == "":
            return
        await ctx.send(args)
        await ctx.message.delete()
        return


def setup(bot):
    bot.add_cog(Fun(bot))
    # Adds the Fun commands to the bot
    # Note: The "setup" function has to be there in every cog file
