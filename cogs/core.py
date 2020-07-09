from discord.ext import commands
import discord

class Core(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name='help', help='Shows this message')
    async def help(self,ctx,*,args=None):
        try: await ctx.message.delete()
        except: pass
        if args:
            command = None
            for cmd in self.bot.commands:
                if cmd.name == args and not cmd.hidden:
                    command = cmd
                    break
            if not command: return await ctx.send('Command not found, please try again.')
            e = discord.Embed(title=f'Command `/' + ((' '.join(command.parents) + ' ' + command.name) if (command.parents) else (command.name)) + '`', description=(command.description or "<no description>"))
            e.add_field(name='Objective',   value=command.help)
            e.add_field(name='Usage',       value=command.usage)
            e.add_field(name='Cog',         value="No cog" if not command.cog else command.cog.qualified_name)
            try:
                if command.commands:
                    e.add_field(name='Sub-Commands',value=', '.join([cmd.name for cmd in command.commands]))
            except: pass
            msg = await ctx.send('Type a command name in 30 seconds to get info about the command. [awaiting...]',embed=e)
            names = [(None if cmd.hidden else cmd.name) for cmd in self.bot.commands] # loop over all commands, if not hidden, append its string name
            cogs = bot.cogs
            def check(m): return m.author == ctx.message.author and m.channel == ctx.message.channel and (m.content in names or m.content in cogs)
            try:
                rt = await bot.wait_for('message', check=check, timeout=30)
                if rt:
                    return await ctx.invoke(self.bot.get_command('help'), args=rt.content)
                return
            except asyncio.exceptions.TimeoutError: return

        all_cmds = self.bot.commands
        e = discord.Embed(title='Command list',description='wd: <GLOBAL>')
        count = 1
        for cmd in all_cmds:
            e.add_field(name=cmd.name,value=cmd.help or "<no help>")
            count += 1
        msg = await ctx.send('Type a command name in 30 seconds to get info about the command. [awaiting...]',embed=e)
        names = [(None if cmd.hidden else cmd.name) for cmd in bot.commands]
        cogs = self.bot.cogs
        def check(m):
            return m.author == ctx.message.author and m.channel == ctx.message.channel and (m.content in names or m.content in cogs)
        try:
            rt = await self.bot.wait_for('message', check=check, timeout=30)
            if rt:
                return await ctx.invoke(self.bot.get_command('help'), args=rt.content)
            return
        except asyncio.exceptions.TimeoutError: return


    @commands.command(name='eval',help='it is eval', hidden=True)
    @commands.is_owner()
    async def _eval(self, ctx, *, code='"bruh wat to eval"'):
        try:    await ctx.send(eval(code))
        except Exception:   await ctx.send('uh oh. there\'s an error in your code:\n```\n' + traceback.format_exc() + '\n```')

    @commands.command(name='reload', help='reload a cog', hidden=True)
    @commands.is_owner()
    async def _reload(self, ctx, cog: str):
        self.bot.unload_extension(f"cogs.{cog}")
        self.bot.load_extension(f"cogs.{cog}")

    @commands.command(name='unload', help='unload a cog', hidden=True)
    @commands.is_owner()
    async def _unload(self, ctx, cog: str):   self.bot.unload_extension(f"cogs.{cog}")

    @commands.command(name='load', help='load a cog', hidden=True)
    @commands.is_owner()
    async def _load(self, ctx, cog: str):     self.bot.load_extension(f"cogs.{cog}")
def setup(bot):
    bot.add_cog(Core(bot))
