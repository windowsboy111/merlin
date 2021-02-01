import asyncio
import traceback
from discord.ext import commands
from discord.utils import get
import discord, traceback, json, datetime
from ext import excepts
from ext.const import chk_sudo, SETFILE, BOTSETFILE, DEFAULT_SETTINGS, is_sudoers
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
    description = "The important / basic commands."
    def __init__(self, bot):
        self.bot = bot

    async def init_sets(self, guild: discord.Guild):
        settings = self.bot.db['sets']
        try:
            settings[f"g{guild.id}"]['cmdHdl']
        except KeyError:
            settings[f"g{guild.id}"] = DEFAULT_SETTINGS.copy()
            with open(SETFILE, 'w') as outfile:
                json.dump(settings, outfile)
            return
        # fix cmdHdl
        cmdHdl = DEFAULT_SETTINGS['cmdHdl'].copy()          # the following code will leave entrys already
        cmdHdl.update(settings[f'g{guild.id}']['cmdHdl'])   # exists and add the missing entrys so that
        settings[f'g{guild.id}']['cmdHdl'] = cmdHdl         # overwriting can be prevented
        default = DEFAULT_SETTINGS.copy()
        default.update(settings[f'g{guild.id}'])            # we can also do the same thing for the whole settings
        settings[f'g{guild.id}'].update(default)


    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        await self.init_sets(guild)
        for role in guild.roles:
            if role.permissions.administrator:
                self.bot.db['sets'][f'g{guild.id}']['sudoers'].append(role.id)

    async def sett_proc(self, ctx, base, entry: str, val: str):  # process settings assignments
        # coro, might be overengineered, but whatever
        try:
            base[entry]
        except KeyError:  # cannot access
            raise excepts.HaltInvoke(":x: Entry does not exist!")
        if not val:  # def'
            raise excepts.HaltInvoke(base[entry])
        if isinstance(base[entry], list):  # process the []s
            if ' ' not in val or not val.startswith(("add", "rm", "remove", "del")):
                raise excepts.HaltInvoke(base[entry])
            op = val.split()[0]
            val = " ".join(val.split()[1:])
            if op == 'add':
                if val in base[entry]:
                    raise excepts.HaltInvoke(":x: Already exists!")
                try:
                    return base[entry].append(int(val))
                except ValueError:
                    return base[entry].append(val)
            if op in ('rm', "remove", "delete", "del"):
                if val not in base[entry]:
                    raise excepts.HaltInvoke(":x: Does not exists!")
                try:
                    return base[entry].remove(int(val))
                except ValueError:
                    return base[entry].remove(val)
        if isinstance(base[entry], dict):  # proess the {}s, feed back into itself
            if " " not in val:
                raise excepts.HaltInvoke(base[entry])
            entry_ = val.split()
            val_ = " ".join(val.split()[1:])
            return await self.sett_proc(ctx, base[entry], entry_, val_)  # recursion
        try:
            base[entry] = int(val)
        except ValueError:
            base[entry] = val

    @commands.guild_only()
    @commands.group(name='settings', aliases=['configure'])
    async def cmd_settings(self, ctx: commands.Context, entry:str="", *, val:str=""):
        """Configure Merlin for this discord server."""
        sets = self.bot.db['sets']
        gset = sets[f'g{ctx.guild.id}']
        if entry == "" or entry not in list(gset.keys()):
            return await ctx.send("```json\n" + json.dumps(gset, sort_keys=True, indent=2) + "\n```")
        await self.sett_proc(ctx, gset, entry, val)
        await ctx.message.add_reaction("✅")

    @cmd_settings.error
    async def settings_error(self, ctx, error):
        if isinstance(error, (KeyError, AssertionError)):
            await self.init_sets(ctx.guild)
            return await ctx.reinvoke()
        await self.bot.errhdl_g(ctx, error)

    @commands.group(name='info', help='info about everything')
    async def info(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            botinfo = json.load(open(BOTSETFILE))
            embed = discord.Embed(
                title="Info", description='you can add subcommand after this command so that it will show specific info!')
            embed.add_field(
                name="Server", value=f"{ctx.guild.id} / `{ctx.guild.name}`")
            embed.add_field(name=self.bot.user,
                            value=f"ver `{botinfo['version']}`")
            embed.add_field(name='Member count', value=len(ctx.guild.members))
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)
            

    @info.command(name='user', help='info about a user (can be outside of this server!)')
    async def info_user(self, ctx: commands.Context, user: discord.User = None):
        user = user or ctx.author
        other_desc = ""
        if user.discriminator:
            other_desc += f":warning: username has conflict: {user.discriminator}\n"
        embed = discord.Embed(
            title=f'user {user.display_name}', description=f'```{user.id}{" | BOT" if user.bot else ""}```')
        embed.add_field(
            name='Mention', value=f"{user.mention} / `{user.mention}`")
        embed.set_author(name=user, icon_url=user.avatar_url)
        embed.set_footer(text='Account created at')
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
        embed = discord.Embed(title=f'Member {member.display_name}',
                              description=f'```{member.status} | {member.id}{" | BOT" if member.bot else ""}```')
        embed.add_field(
            name='Mention', value=f"{member.mention} / `{member.mention}`")
        if member.is_on_mobile():
            embed.add_field(name='Device', value='Mobile')
            if member.mobile_status == discord.Status.online:
                embed.add_field(name='Mobile Status', value='online')
            elif member.mobile_status == discord.Status.idle:
                embed.add_field(name='Mobile Status', value='idle')
            elif member.mobile_status == discord.Status.dnd:
                embed.add_field(name='Mobile Status', value='do not disturb')
            else:
                embed.add_field(name='Mobile Status',
                                value='offline / invisible')
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
        embed.add_field(
            name='Nickname', value=member.nick or f"<{member.mention} have no nickname>")
        embed.add_field(name='Roles', value=', '.join(
            [r.mention for r in member.roles[1:]]) or "<None>")
        embed.set_footer(text='Member joined at', icon_url=ctx.guild.icon_url)
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
        embed = discord.Embed(
            title=f'Text Channel {channel.name}', description=f"```{channel.id}```{other_desc}")
        embed.add_field(name="Category Position",
                        value=channel.position or "<No position>")
        embed.add_field(
            name='Category', value="<GLOBAL>" if channel.category is None else channel.category.name)
        embed.add_field(
            name='Mention', value=f"{channel.mention} / `{channel.mention}`")
        if any(await channel.invites()):
            embed.add_field(name='Invites', value=", ".join(
                f"[{invite.id}]({invite.url})" async for invite in channel.invites()))
        embed.add_field(name='Pinned messages', value=len(await channel.pins()))
        embed.set_footer(text="Channel created")
        embed.timestamp = channel.created_at
        await ctx.send(embed=embed)
        return 0

    @info.command(name='server', help='info about the current server', aliases=['guild', 'srv', 'g'])
    @commands.guild_only()
    async def info_server(self, ctx):
        settings = self.bot.db['sets']
        embed = discord.Embed(title='Server info', description=ctx.guild.description or "<description not set>")
        embed.add_field(name="Server", value=f"{ctx.guild.name} - {ctx.guild.id}")
        embed.add_field(name='Members count', value=ctx.guild.member_count)
        embed.add_field(name='Roles count', value=len(ctx.guild.roles))
        embed.add_field(name='Channels count',
                        value=f"{len(ctx.guild.text_channels)} text / {len(ctx.guild.voice_channels)} voice - total {len(ctx.guild.channels)}")
        embed.add_field(name='Categories count',
                        value=len(ctx.guild.categories))
        embed.add_field(name='Sudoers', value=", ".join([discord.utils.get(
            ctx.guild.roles, name=r).mention for r in settings[f'g{ctx.guild.id}']["sudoers"]]) or "<None>")
        embed.add_field(name='Rules channel',
                        value=ctx.guild.rules_channel.mention if ctx.guild.rules_channel else "Not set")
        embed.add_field(name='System channel',
                        value=ctx.guild.system_channel.mention if ctx.guild.system_channel else "Not set")
        embed.add_field(name='Region', value=str(
            ctx.guild.region) or "Not set / found")
        embed.add_field(
            name='afk', value=f"{ctx.guild.afk_timeout or '<no afk timeout>'} sec / {ctx.guild.afk_channel.name if ctx.guild.afk_channel else '<no afk channel>'}")
        embed.add_field(name='Public updates channel',
                        value=ctx.guild.public_updates_channel.mention if ctx.guild.public_updates_channel else "Not a public server / not set")
        None if not ctx.guild.icon_url else embed.set_image(
            url=ctx.guild.icon_url)
        embed.add_field(name='Owner', value=ctx.guild.owner.mention)
        embed.set_footer(text="Created at")
        embed.timestamp = ctx.guild.created_at
        await ctx.send(embed=embed)
        return

    @info.command(name='bot', help='info about this discord bot', aliases=['merlin', 'this', 'self'])
    async def info_bot(self, ctx):
        settings = self.bot.db['botsets']
        embed = discord.Embed(title='Merlin info', description='an open-source discord.py bot')
        for key in settings.keys():
            embed.add_field(name=key, value=settings[key])
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)
        return


def setup(bot: discord.ext.commands.Bot):
    bot.add_cog(Core(bot))
