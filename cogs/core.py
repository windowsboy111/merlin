from discord.ext import commands
import discord, traceback, json, datetime
BOTSETFILE = "ext/bot_settings.json"
SETFILE = "data/settings.json"


class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', help='Shows this message')
    async def help(self, ctx, *, cmdName: str = None):
        try: await ctx.message.delete()
        except Exception: pass
        if cmdName:
            command = self.bot.get_command(cmdName)
            if not command or command.hidden: return await ctx.send('Command not found, please try again.')
            e = discord.Embed(title='Command `/' + ((' '.join([p.name for p in command.parents]) + ' ' + command.name) if (command.parents) else (command.name)) + '`', description=(command.description or "<no description>"))
            e.add_field(name='Objective',   value=command.help)
            e.add_field(name='Usage',       value=command.usage)
            e.add_field(name='Cog',         value="No cogs" if not command.cog else command.cog.qualified_name)
            if hasattr(command, 'commands'):    # it is a group
                e.add_field(name='Sub-Commands', value=', '.join([cmd.name for cmd in command.commands]))
            await ctx.send(embed=e)
            return

        all_cmds = self.bot.commands
        e = discord.Embed(title='Command list', description='wd: <GLOBAL>')
        count = 1
        for cmd in all_cmds:
            e.add_field(name=cmd.name, value=cmd.help or "<no help>")
            count += 1
        await ctx.send(embed=e)

    @commands.group(name='info', help='info about everything')
    async def _info(self, ctx):
        if ctx.invoked_subcommand is None:
            botinfo = json.load(open(BOTSETFILE))
            embed = discord.Embed(title="Info", description='you can add subcommand after this command so that it will show specific info!')
            embed.add_field(name="Server", value=f"{ctx.guild.id} / `{ctx.guild.name}`")
            embed.add_field(name=self.bot.user, value=f"ver `{botinfo['version']}`")
            embed.add_field(name='Member count', value=len(ctx.guild.members))
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)
            return

    @_info.command(name='server', help='info about the current server', aliases=['guild', 'srv', 'g'])
    async def info_server(self, ctx):
        settings = json.load(open(SETFILE, 'r'))
        embed = discord.Embed(title='Server info', description=ctx.guild.description or "<description not set>")
        embed.add_field(name="Server", value=f"{ctx.guild.name} - {ctx.guild.id}")
        embed.add_field(name='Members count', value=ctx.guild.member_count)
        embed.add_field(name='Roles count', value=len(ctx.guild.roles))
        embed.add_field(name='Channels count', value=f"{len(ctx.guild.text_channels)} text / {len(ctx.guild.voice_channels)} voice - total {len(ctx.guild.channels)}")
        embed.add_field(name='Categories count', value=len(ctx.guild.categories))
        embed.add_field(name='Sudoers', value=", ".join([discord.utils.get(ctx.guild.roles, name=r).mention for r in settings[f'g{ctx.guild.id}']["sudoers"]]))
        embed.add_field(name='Rules channel', value=ctx.guild.rules_channel.mention if ctx.guild.rules_channel else "Not set")
        embed.add_field(name='System channel', value=ctx.guild.system_channel.mention if ctx.guild.system_channel else "Not set")
        embed.add_field(name='Region', value=str(ctx.guild.region) if ctx.guild.region else "Not set / found")
        embed.add_field(name='afk', value=f"{ctx.guild.afk_timeout or '<no afk timeout>'} sec / {ctx.guild.afk_channel.name if ctx.guild.afk_channel else '<no afk channel>'}")
        # embed.add_field(name='Public updates channel', value=ctx.guild.public_updates_channel.mention if ctx.guild.public_updates_channel else "Not a public server / not set")
        # new in discord.py version 1.4
        None if not ctx.guild.icon_url else embed.set_image(url=ctx.guild.icon_url)
        embed.add_field(name='Owner', value=ctx.guild.owner.mention)
        embed.set_footer(text="Created on")
        embed.timestamp = ctx.guild.created_at
        await ctx.send(embed=embed)
        return

    @_info.command(name='bot', help='info about this discord bot', aliases=['merlin', 'this', 'self'])
    async def info_bot(self, ctx):
        settings = json.load(open(BOTSETFILE, 'r'))
        embed = discord.Embed(title='Merlin info', description='an open-source discord.py bot')
        for key in settings.keys():
            embed.add_field(name=key, value=settings[key])
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)
        return

    @commands.command(name='eval', help='it is eval', hidden=True)
    @commands.is_owner()
    async def _eval(self, ctx, *, code='"bruh wat to eval"'):
        try: await ctx.send(eval(code))
        except Exception: await ctx.send('uh oh. there\'s an error in your code:\n```\n' + traceback.format_exc() + '\n```')

    @commands.command(name='reload', help='reload a cog', hidden=True)
    @commands.is_owner()
    async def _reload(self, ctx, module: str):
        await ctx.invoke(self.bot.get_command('_unload'), module=module)
        await ctx.invoke(self.bot.get_command('_load'), module=module)

    @commands.command(name='unload', help='unload a cog', hidden=True)
    @commands.is_owner()
    async def _unload(self, ctx, module: str):
        cmd = self.bot.get_command(module)
        if cmd is None:
            self.bot.unload_extension(f"cogs.{module}")
        else:
            self.bot.unload_extension(f"cogs.{cmd.cog.name}")

    @commands.command(name='load', help='load a cog', hidden=True)
    @commands.is_owner()
    async def _load(self, ctx, module: str):
        cmd = self.bot.get_command(module)
        if cmd is None:
            self.bot.load_extension(f"cogs.{module}")
        else:
            self.bot.load_extension(f"cogs.{cmd.cog.name}")


def setup(bot):
    bot.add_cog(Core(bot))
