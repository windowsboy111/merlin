from discord.ext import commands
from discord.utils import get
import discord, traceback, json, datetime
from ext.imports_share import chk_sudo
import typing
BOTSETFILE = "ext/bot_settings.json"
SETFILE = "data/settings.json"
settings = json.load(open(SETFILE, 'r'))
stringTable = json.load(open('ext/wrds.json', 'r'))


class Core(commands.Cog):
    """\
    Type: discord.ext.commands.Cog  
    The most important commands of the bot are in this cog / extension.  
    Load this extension as an external file with `client.load_extension('cogs.core')`  
    ---
    This cog contains:  
    ## Commands
    - settings
    - help
    - info
    - eval
    - unload
    - reload
    - load
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='settings', help='settings about everything')
    async def settings(self, ctx):
        prefix = settings[f'g{ctx.guild.id}']['prefix']
        sudoers = settings[f'g{ctx.guild.id}']['sudoers']
        if ctx.invoked_subcommand is None:
            e = discord.Embed(title='Settings', description='ayy what settings do you wanna edit?')
            e.add_field(name='Prefix', value=', '.join(prefix))
            e.add_field(name='Moderating roles (sudoers)', value=', '.join([ctx.guild.create_role(name=s).mention if get(ctx.guild.roles, name=s) is None else get(ctx.guild.roles, name=s).mention for s in sudoers]))
            await ctx.send(embed=e)

    @settings.group(name='prefix', help='edit prefix list')
    @chk_sudo()
    async def settings_prefix(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self.bot.get_command('help'), cmdName='settings prefix')

    @settings_prefix.command(name='add', help='add a prefix for this server')
    async def settings_prefix_add(self, ctx, prefix: str):
        prefixes = settings[f'g{ctx.guild.id}']['prefix']
        if prefix in prefixes:
            return ctx.send('That prefix already exists!')
        settings[f"g{ctx.guild.id}"]['prefix'].append(prefix)
        with open(SETFILE, 'w') as outfile:
            json.dump(settings, outfile)
        await ctx.send("Prefixes now avaliable: " + ', '.join(settings[f'g{ctx.guild.id}']['prefix']))

    @settings_prefix.command(name='remove', help='remove a prefix for this server', aliases=['del', 'delete', 'rm'])
    async def settings_prefix_remove(self, ctx, prefix: str):
        prefixes = settings[f'g{ctx.guild.id}']['prefix']
        if prefix not in prefixes:
            return await ctx.send('The specified prefix does not exist in the list!')
        settings[f'g{ctx.guild.id}']['prefix'].remove(prefix)
        with open(SETFILE, 'w') as outfile:
            json.dump(settings, outfile)
        return await ctx.send("Removed the specified prefix")

    @settings.group(name='mods', help='set roles that are moderators / admins', aliases=['mod', 'admin', 'admins'])
    @chk_sudo()
    async def settings_mods(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self.bot.get_command('help'), cmdName='settings mods')

    @settings_mods.command(name='add', help='add a moderating role')
    async def settings_mods_add(self, ctx, role: discord.Role):
        sudoers = settings[f'g{ctx.guild.id}']['sudoers']
        sudoers.append(str(role))
        with open(SETFILE, 'w') as outfile:
            json.dump(settings, outfile)
        return await ctx.send("Moderators roles: " + ', '.join([get(ctx.guild.roles, name=s).mention for s in sudoers]))

    @settings_mods.command(name='remove', help='remove a moderating role', aliases=['del', 'rm', 'delete'])
    async def setings_mod_remove(self, ctx, role: discord.Role):
        sudoers = settings[f'g{ctx.guild.id}']['sudoers']
        sudoers.remove(str(role))
        with open(SETFILE, 'w') as outfile:
            json.dump(settings, outfile)
        return await ctx.send("Moderators roles: " + ', '.join([get(ctx.guild.roles, name=s).mention for s in sudoers]))

    @settings.error
    async def settings_error(self, ctx, error):
        if isinstance(error, KeyError):
            await ctx.send(stringTable['core']['guildSettingsNotFound'])
            settings[f'g{ctx.guild.id}'] = {"prefix": ["/"], "sudoers": []}
            with open(SETFILE, 'w') as outfile:
                json.dump(settings, outfile)
            await ctx.send(stringTable['core']['guildSettingsFixed'])
            return 2

    @commands.command(name='help', help='Shows this message', aliases=['?', 'cmd', 'cmds', 'commands', 'command'])
    async def help(self, ctx, *, cmdName: str = None):
        try: await ctx.message.delete()
        except Exception: pass
        prefix = None
        prefixes = settings[f"g{ctx.guild.id}"]["prefix"]
        for p in prefixes:
            if ctx.message.content.startswith(p):
                prefix = p
                break
        if cmdName:
            command = self.bot.get_command(cmdName)
            if not command or command.hidden: return await ctx.send('Command not found, please try again.')
            e = discord.Embed(title=f'Command `{prefix}' + command.qualified_name + '`', description=(command.description or "<no description>"), color=0x0000ff)
            usage = prefix + command.qualified_name + ' '
            for param in command.clean_params:
                if type(param) is str:
                    usage += f'<{param}> '
                    continue
                if param.default == param.default:
                    usage += f'<{param.name}>'
                else:
                    usage += f'<[{param.name}]>'
                usage += ' '
            e.add_field(name='Objective',   value=command.help)
            e.add_field(name='Usage',       value=usage)
            e.add_field(name='Cog',         value="No cogs" if not command.cog else command.cog.qualified_name)
            if hasattr(command, 'commands'):    # it is a group
                e.add_field(name='Sub-Commands', value=''.join([f"`{prefix}{cmd.qualified_name}`: {cmd.help}\n" for cmd in command.commands]))
            await ctx.send(embed=e)
            return

        all_cmds = self.bot.commands
        e = discord.Embed(title='Command list', description='wd: <GLOBAL>', color=0x0000ff)
        count = 1
        for cmd in all_cmds:
            if cmd.hidden:
                continue
            e.add_field(name=cmd.name, value=cmd.help or "<no help>")
            count += 1
        await ctx.send(embed=e)

    @commands.group(name='info', help='info about everything')
    async def info(self, ctx):
        if ctx.invoked_subcommand is None:
            botinfo = json.load(open(BOTSETFILE))
            embed = discord.Embed(title="Info", description='you can add subcommand after this command so that it will show specific info!')
            embed.add_field(name="Server", value=f"{ctx.guild.id} / `{ctx.guild.name}`")
            embed.add_field(name=self.bot.user, value=f"ver `{botinfo['version']}`")
            embed.add_field(name='Member count', value=len(ctx.guild.members))
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)
            return

    @info.command(name='user', help='info about a user (can be outside of this server!)')
    async def info_user(self, ctx: commands.Context, user: discord.User = None):
        user = user or ctx.author
        other_desc = ""
        if user.discriminator:
            other_desc += f":warning: username has conflict: {user.discriminator}\n"
        embed = discord.Embed(title=f'user {user.display_name}', description=f'```{user.id}{" | BOT" if user.bot else ""}```')
        embed.add_field(name='Mention', value=f"{user.mention} / `{user.mention}`")

        embed.set_author(name=user, icon_url=user.avatar_url)
        embed.set_footer(text='Created')
        embed.timestamp = user.created_at
        await ctx.send(embed=embed)
        return 0

    @info.command(name='member', help='info about a member')
    @commands.guild_only()
    async def info_member(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        other_desc = ""
        if member.discriminator:
            other_desc += f":warning: username has conflict: {member.discriminator}\n"
        embed = discord.Embed(title=f'Member {member.display_name}', description=f'```{member.status} | {member.id}{" | BOT" if member.bot else ""}```')
        embed.add_field(name='Mention', value=f"{member.mention} / `{member.mention}`")
        if member.is_on_mobile():
            embed.add_field(name='Device', value='Mobile')
            if member.mobile_status == discord.Status.online:
                embed.add_field(name='Mobile Status', value='online')
            elif member.mobile_status == discord.Status.idle:
                embed.add_field(name='Mobile Status', value='idle')
            elif member.mobile_status == discord.Status.dnd:
                embed.add_field(name='Mobile Status', value='do not disturb')
            else:
                embed.add_field(name='Mobile Status', value='offline / invisible')
        else:
            embed.add_field(name='Device', value='Desktop / Web App')

        if member.desktop_status == discord.Status.online:
            embed.add_field(name='Desktop status', value='online')
        elif member.desktop_status == discord.Status.idle:
            embed.add_field(name='Desktop Status', value='idle')
        elif member.desktop_status == discord.Status.dnd:
            embed.add_field(name='Desktop Status', value='do not disturb')
        else:
            embed.add_field(name='Desktop Status', value='offline / invisible')

        if member.web_status == discord.Status.online:
            embed.add_field(name='Web App status', value='online')
        elif member.web_status == discord.Status.idle:
            embed.add_field(name='Web App Status', value='idle')
        elif member.web_status == discord.Status.dnd:
            embed.add_field(name='Web App Status', value='do not disturb')
        else:
            embed.add_field(name='Web App Status', value='offline / invisible')

        embed.set_author(name=member, icon_url=member.avatar_url)
        embed.add_field(name='Nickname', value=member.nick or f"<{member.mention} have no nickname>")
        embed.add_field(name='Roles', value=', '.join([r.mention for r in member.roles[1:]]))
        embed.set_footer(text='Joined', icon_url=ctx.guild.icon_url)
        embed.timestamp = member.joined_at
        await ctx.send(embed=embed)
        return 0

    @info.command(name='channel', help='info about a channel')
    @commands.guild_only()
    async def info_channel(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        other_desc = ""
        if channel.is_nsfw():
            other_desc += ":warning: nsfw channel\n"
        if channel.is_news():
            other_desc += ":newspaper: news channel\n"
        if channel.category is not None:
            if channel.permissions_synced:
                other_desc += ":arrows_counterclockwise: :white_check_mark: Permission synced"
            else:
                other_desc += ":arrows_counterclockwise: :negative_squared_cross_mark: Permission outdated"
        embed = discord.Embed(title=f'Text Channel {channel.name}', description=f"```{channel.id}```{other_desc}")
        embed.add_field(name="Category Position", value=channel.position or "<No position>")
        embed.add_field(name='Category', value="<GLOBAL>" if channel.category is None else channel.category.name)
        embed.add_field(name='Mention', value=f"{channel.mention} / `{channel.mention}`")
        if any(await channel.invites()):
            embed.add_field(name='Invites', value=", ".join(f"[{invite.id}]({invite.url})" for invite in channel.invites()))
        embed.add_field(name='Pinned messages', value=len(await channel.pins()))
        embed.set_footer(text="Channel created")
        embed.timestamp = channel.created_at
        await ctx.send(embed=embed)
        return 0

    @info.command(name='server', help='info about the current server', aliases=['guild', 'srv', 'g'])
    @commands.guild_only()
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

    @info.command(name='bot', help='info about this discord bot', aliases=['merlin', 'this', 'self'])
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
        cmd = self.bot.get_command(module)
        if cmd is not None:
            module = cmd.cog.name.lower()
        self.bot.reload_extension(f'cogs.{module}')

    @commands.command(name='unload', help='unload a cog', hidden=True)
    @commands.is_owner()
    async def _unload(self, ctx, module: str):
        cmd = self.bot.get_command(module)
        if cmd is None:
            self.bot.unload_extension(f"cogs.{module}")
        else:
            self.bot.unload_extension(f"cogs.{cmd.cog.name.lower()}")

    @commands.command(name='load', help='load a cog', hidden=True)
    @commands.is_owner()
    async def _load(self, ctx, module: str):
        cmd = self.bot.get_command(module)
        if cmd is None:
            self.bot.load_extension(f"cogs.{module}")
        else:
            self.bot.load_extension(f"cogs.{cmd.cog.name.lower()}")


def setup(bot):
    bot.add_cog(Core(bot))
