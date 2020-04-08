from discord.ext import commands
from logcfg import logger
import random
class fun(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name='cough',help="Simulate cough. :)")
    async def cough(self,ctx):
        logger.info(ctx.message.author.name + "has issued command /cough")
        lolcough = ["What? You being infected coronavirus?",str(self.bot.get_emoji(684291327818596362)),"Please don't:\nSneeze on me;\nCough on me;\nTalk to me,\nNo oh oh!","🤢",
        "Run, run, until it's done, done, until the sun comes up in the morn'."]
        response = random.choice(lolcough)
        logger.info("Result / response: " + response)
        msg = await ctx.send(response)
        await msg.add_reaction('👀')
        return

    @commands.command(name='test', help="Respond with test messages!")
    async def test(self,ctx):
        loltest = ["!urban MEE6","Am I a joke to you?","!8ball Siriu-smart?","What? Are you a developer?{}".format(ctx.message.author.mention),
        "Didn't expect anyone would use this command, but there it is!","No test.","Ping Pong!","No.","?????","Siriusly, What did you expect?",
        "Stop.","!8ball are you stupid?","Vincidiot"]
        logger.info(ctx.message.author.name + "has issued command /test")
        response = random.choice(loltest)
        logger.info("Result / response: " + response)
        msg = await ctx.send(response)
        await msg.add_reaction('👍')
        return

    @commands.command(name='stupid',help='Shout at stupid things')
    async def stupid(self,ctx,*,args='that'):
        logger.info(ctx.message.author.name + 'has issued command /stupid')
        await ctx.send(random.choice([f'{args} is so so stupid!',f"I can't believe how stupid {args} is!",f"Seriously, {args}'s the stupidest thing I've ever heard!",f"STUPID STUPID STUPID STUPID STUPID STUPID STUPID STUPID {args}!",f"I can't believe {args}'s even a thing."]))

    @commands.command(name='whatis',help='Tells you what the input is. /whatis minecraft')
    async def whatis(self,ctx,*,args=""):
        logger.info(ctx.message.author.name + f'has issued command /whatis {args}')
        if args=="":
            await ctx.send("Bruh, where's the argument???")
            return
        await ctx.send(random.choice([f"{args} is generally {args}.",f"Technically, {args} is {args}!",f"To know what {args} is, please run `!urban {args}`",
        f"Well, not in a nutshell, {args} as {args} is {args} in {args} on {args} at {args} from {args} to {args}...It's just...{args}!!!!!",
        f"You are so dumb that you even don't know what {args} is!"]))

    @commands.command(name='boomer',help="/boomer [person]",aliases=['boom','okboomer'])
    async def boomer(self,ctx,*,person=""):
        logger.info(ctx.message.author.name + 'has issued command /boomer ' + str(person))
        if person == "":
            person = ctx.message.author
            await ctx.send(f'OK BOOMER {person.mention}')
            return
        await ctx.send(f'OK BOOMER {person}')



def setup(bot):
    bot.add_cog(fun(bot))
    # Adds the Fun commands to the bot
    # Note: The "setup" function has to be there in every cog file