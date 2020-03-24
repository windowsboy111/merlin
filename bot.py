# bot.py
from dotenv import load_dotenv
from mcstatus import MinecraftServer
from discord.ext import commands
from discord.ext.commands import has_permissions,MissingPermissions
from consolemod import *
from logcfg import logger
from discord.utils import get
import threading,datetime,time,botmc,discord,os,random,asyncio,json
from concurrent.futures import ThreadPoolExecutor

#console log
logger.info("Program started.")
logger.debug("Finished importing and logger configuration.  Loaded all libraries.")

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# init
bot = commands.Bot(command_prefix = '/')
runno = -1
logger.debug("Loaded dotenv, discord_token, bot prefix, custom exceptions, and \"constant\" variables / some global variables.")
embed=discord.Embed()


with open('G:/my drive/coding/python/kccs-official/reports.json', encoding='utf-8') as f:
  try:
    report = json.load(f)
  except ValueError:
    report = {}
    report['users'] = []  
@bot.command(pass_context = True)
@has_permissions(manage_roles=True, ban_members=True)
async def warn(ctx,user:discord.User,*reason:str):
    if not reason:
        await ctx.say("Please provide a reason")
        return
    reason = ' '.join(reason)
    for current_user in report['users']:
        if current_user['name'] == user.name:
            current_user['reasons'].append(reason)
            break
        else:
            report['users'].append({
                'name':user.name,
                'reasons': [reason,]
            })
    with open('reports.json','w+') as f:
        json.dump(report,f)
    await ctx.say(f"{user.mention} has been warned by {ctx.message.author.mention} with reason: {reason}")
@bot.command(pass_context = True)
async def warnings(ctx,user:discord.User):
  for current_user in report['users']:
    if user.name == current_user['name']:
      await ctx.say(f"{user.name} has been reported {len(current_user['reasons'])} times : {','.join(current_user['reasons'])}")
      break
  else:
    await ctx.say(f"{user.name} has never been reported")  
@warn.error
async def kick_error(error, ctx):
  if isinstance(error, MissingPermissions):
      text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
      await ctx.send_message(ctx.message.channel, text)


@bot.listen
async def listen(message):
    user = discord.utils.get(message.guild.members, id=message.author.id)
    logger.info("{user}: {message.content}")
    print(style.green(f"{user}: {message.content}") + style.reset())


@bot.on_message
async def on_message(message):
    if message.author == bot.user.name or message.author.bot:
        return


@bot.event
async def on_ready():
    logger.info("Bot is now ready!")
    print(style.cyan(f'\33[2J{bot.user.name} has connected to Discord!') + style.reset())
    return


@bot.command(name='cough',help="Simulate cough. :)")
async def cough(ctx):
    logger.info(ctx.message.author.name + "has issued command /cough")
    lolcough = ["What? You being infected coronavirus?",str(bot.get_emoji(684291327818596362)),"Please don't:\nSneeze on me;\nCough on me;\nTalk to me,\nNo oh oh!","🤢",
    "Run, run, until it's done, done, until the sun comes up in the morn'."]
    response = random.choice(lolcough)
    logger.info("Result / response: " + response)
    msg = await ctx.send(response)
    await msg.add_reaction('👀')
    return

@bot.command(name='test', help="Respond with test messages!")
async def test(ctx):
    loltest = ["!urban MEE6","Am I a joke to you?","!8ball Siriu-smart?","What? Are you a developer?{}".format(ctx.message.author.mention),
    "Didn't expect anyone would use this command, but there it is!","No test.","Ping Pong!","No.","?????","Siriusly, What did you expect?",
    "Stop.","!8ball are you stupid?","Vincidiot"]
    logger.info(ctx.message.author.name + "has issued command /test")
    response = random.choice(loltest)
    logger.info("Result / response: " + response)
    msg = await ctx.send(response)
    await msg.add_reaction('👍')
    return

@bot.command(pass_context=True)
async def ping(ctx):
    await ctx.send(embed=discord.Embed(title="Pong!", description='The latency is {} ms.'.format(bot.latency*1000), color=0x3333ff))

@bot.command(name='emojis',help='Print all emojis')
async def emojis(ctx):
    for emoji in ctx.guild.emojis:
        await ctx.send(str(bot.get_emoji(emoji.id)) + str(emoji.id) + f" {emoji.name}")

@bot.command(name='stupid',help='Shout at stupid things')
async def stupid(ctx,*,args='that'):
    logger.info(ctx.message.author.name + 'has issued command /stupid')
    await ctx.send(random.choice([f'{args} is so so stupid!',f"I can't believe how stupid {args} is!",f"Seriously, {args}'s the stupidest thing I've ever heard!",f"STUPID STUPID STUPID STUPID STUPID STUPID STUPID STUPID {args}!",f"I can't believe {args}'s even a thing."]))





class threadMC (threading.Thread):
   def __init__(self, threadID, name, ctx,args):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.args = args
        self.ctx = ctx
   def run(self):
        logger.info("Starting " + self.name)
        procMC(self.ctx,self.args)
        logger.info("Exiting " + self.name)
@bot.command(name='mc',help="Same as kccsofficial.exe mc <args>\nUsage: /mc srv hypixel",pass_context=True)
async def mc(ctx,*,args=""):
    async with ctx.typing():
        loop = asyncio.get_event_loop()
        loop.run_in_executor(ThreadPoolExecutor(), mainmc(ctx,args))
    await ctx.send(embed=embed)
def mainmc(ctx,args):
    global runno,embed,rtc
    enduser = ctx.message.author.name
    runno += 1
    starttime = datetime.datetime.now()
    try:
        fetchMC = threadMC(runno,"FetchMC_{}".format(str(runno)),ctx,args)
        fetchMC.start()
        logger.info(enduser + " has issued command /mc " + args)
        print("{} has issued command /mc {}".format(enduser,args))
        fetchMC.join()
        endtime = datetime.datetime.now()
        timeElapsed = endtime - starttime
        embed.set_footer(text='Exit code: {}, Time elapsed: {} ms'.format(rtc,str(int(timeElapsed.total_seconds() * 1000))))
        time.sleep(0.5)
        if runno == 100:
            runno = 0
    except RuntimeError:
        pass
    except TypeError:
        pass
    return embed
def procMC(ctx,args):
    global embed
    global rtc
    logger.info("procMC started as a new thread.")
    rtc=0
    try:
        if args=="":
            raise discord.ext.commands.errors.MissingRequiredArgument(ctx.command)
        logger.info("Attempting to call botmc.mc()")
        embed = botmc.mc(embed,args)
    except botmc.InvalidArgument as e:
        rtrn = "Panic 2: InvalidArgument. Send gud args!!!!!!!?\n""Details:  " + str(e) + "\n"
        rtrn += "2 get da usage, includ da \"help\" args, i.e. `/mc help`\n"
        rtc = 2
        time.sleep(0.5)
    except discord.ext.commands.errors.MissingRequiredArgument as e:
        rtrn = "Panic 3: MissingRequiredArgument.  Plz send args!!!\nDetails:  {}\n".format(str(e))
        rtrn += "2 get da usage, includ da \"help\" args, i.e. `/mc help`\n"
        rtc = 3
        time.sleep(0.5)
    except botmc.OfflineServer as e:
        rtrn = "Panic 4: OfflineServer.  Details: {}\n2 get da usage, includ da \"help\" args, i.e. `/mc help`\n".format(str(e))
        rtc = 4
    # except Exception as e:
        # rtrn = "Panic 1: Unknun Era.  Program kthxbai.\nDetails:  " + str(e) + "\n"
        # rtc = 1
    if rtc != 0:
        embed = discord.Embed(title="ERROR",description=str(rtrn),color=0xFF0000)
        if rtc == 1:
            logger.error("Exit code: " + str(rtc))
        else:
            logger.warn("Exit code: " + str(rtc))
    else:
        logger.info("Exit code: " + str(rtc))
    embed.set_footer(text="kthxbai code: {}.".format(rtc))





@bot.group(pass_context=True)
async def vote(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send(f"2 bed idk wat u r toking 'bout, but wut?")

@vote.command(name='create',help='Create a vote: /vote create <name> <choices>')
async def create(ctx,name,*,args):
    try:
        async with ctx.typing():
            args = args.split(",")
            import votes
            ebd = discord.Embed(title=f'Poll: {name}\n',color=0xaaff00,description=ctx.author.mention)
            ebd.set_author(name=ctx.author.name,url=f'https://cdn.discordapp.com/{ctx.author.id}',icon_url=ctx.author.avatar_url)
            regional_indicator = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟']
            for choice in args:
                ebd.add_field(name=regional_indicator[args.index(choice)],value=choice)
            msg = await ctx.send(embed=ebd)
            for choice in args:
                await msg.add_reaction(regional_indicator[args.index(choice)])
        f = open('votes.py','a')
        f.writelines("\nvotes['{name}'] = {{\n'choices': {args}, 'author': {author}, 'msg': {msg}}}".format(name=name,args=args,author=ctx.author,msg=msg))
        f.close()
    except discord.ext.commands.errors.MissingRequiredArgument as e:
        await ctx.send(f'ERA: MissingRequiredArgument: {e}.\n2 bed idk wat u r tokin \'bout, but wut?')
@vote.command(name='end',help='End a vote: /vote end <name>')
async def end(ctx,*,n):
        async with ctx.typing():
            import votes
            data = votes.votes['"' + str(n) + '"']
            choices = data['choices']
            author = data['author']
            msg = data['msg']
            ebd = discord.Embed(title=n,description='Poll ended',color=0x00ffbb)
            ebd.set_author(name=author.name,url=author.url,icon_url=author.avatar_url)
            regional_indicator = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟']
            for choice in choices:
                ebd.add_field(name=regional_indicator[choices.index(choice)],value=get(msg.reactions, emoji=regional_indicator[choices[choice]]).count - 1)
            await msg.delete()
            await ctx.send(embed=ebd)
        f = open('votes.py','a')
        f.write("\nvotes.del('{}')".format(n))
        f.close()
        return

        
        
        
        





console = cursor()
console.cls()
bot.run(TOKEN)