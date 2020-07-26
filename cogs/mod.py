from discord.ext import commands
from discord.utils import get
from datetime import datetime
import discord, pyTableMaker, random, sqlite3, asyncio, json
from ext.dbctrl import close_connection, close_cursor
from ext.imports_share import log, chk_sudo
from exceptions import NoMutedRole
WARNFILE = 'data/warnings.db'
muted = dict()
SETFILE = "data/settings.json"
stringTable = json.load(open('ext/wrds.json', 'r'))
settings = json.load(open(SETFILE, 'r'))


class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='role', aliases=['roles'], help='Get your role rolling automatically.  Possible sub-commands: assign, remove, create, delete')
    @chk_sudo()
    @commands.guild_only()
    async def role(self, ctx):
        if ctx.invoked_subcommand is None:
            return await ctx.send("2 bed idk wat u r toking 'bout, but wut?")

    @role.command(name='assign', aliases=['give', 'set', 'grant', 'add'], help='Possible rolename: 2a, 1b, friends, etc.', pass_context=True)
    async def assign(self, ctx, role: discord.Role, member: discord.Member = None):
        member = member or ctx.message.author
        if role is None:
            await ctx.send(f'Failed to get the role.  Probably role {role} is not a thing.  {ctx.message.author.mention}, please make sure you got it right.')
            return
        await member.add_roles(role)
        await ctx.send(f'Role {role} has been added to {member.mention} by {ctx.message.author.mention}.')

    @role.command(name='remove', aliases=['rm', 'revoke'], help='Possible rolename: 2a, 1b, friends, etc.', pass_context=True)
    async def remove(self, ctx, rolename='', member: discord.Member = None):
        member = member or ctx.message.author
        if rolename == '':
            await ctx.send('apparently this function requires 2 parameters.')
            await ctx.message.delete()
            return
        try:
            role = get(ctx.guild.roles, name=rolename)
            if role is None:
                await ctx.send(f'Failed to get the role.  Probably role {rolename} is not a thing.  '
                               f'{ctx.message.author.mention}, please make sure you got it right.')
                await ctx.message.delete()
                return
            await member.remove_roles(role)
            await ctx.send(f'Role {rolename} has been removed from {member.mention} by {ctx.message.author.mention}.')
        except Exception as e:
            await ctx.send(f'failed to remove role {rolename} from {member} (requested by {ctx.message.author.mention}) with error message:\n{e}')
        await ctx.message.delete()
        return

    @role.command(name='create', aliases=['make', 'mk'], help='Create a new role.')
    async def create(self, ctx, *, rolename=''):
        if rolename == '':
            await ctx.send('apparently this function requires 2 parameters.')
            await ctx.message.delete()
            return
        try:
            await ctx.guild.create_role(name=rolename)
            await ctx.send(f'Role {rolename} created successfully. (Requested by {ctx.message.author.mention})')
        except discord.Forbidden as e:
            await ctx.send(f'Failed to create role {rolename} because the requester {ctx.message.author.mention} has missing permissions.  '
                           f'Administrative privileges are required.\nError message: {e}')
        except Exception as e:
            await ctx.send(f'Failed to create role {rolename} (requested by {ctx.message.author.mention}).\nError message: {e}')
        await ctx.message.delete()
        return

    @role.command(name='delete', aliases=['del'], help='Delete a role (remove from all users)')
    async def delete(self, ctx, *, role: discord.Role):
        if role:
            try:
                await role.delete()
                await ctx.send(f'Role {role.name} deleted successfully. (Requested by {ctx.message.author.mention})')
            except discord.Forbidden as e:
                await ctx.send(f'Failed to delete role {role.name} because the requester {ctx.message.author.mention} '
                               f'has missing permissions.  Administrative privileges are required.\nError message: {e}')
            except Exception as e:
                await ctx.send(f'Failed to create role {role.name} (requested by {ctx.message.author.mention}).\nError message: {e}')
        else:
            await ctx.send(f'Failed to get the role.  Probably role {role.name} is not a thing.  '
                           f'{ctx.message.author.mention}, please make sure you got it right.')
        return

    @commands.command(name='warn', help='Warn a person: /warn @person reason', aliases=['warning'])
    @chk_sudo()
    @commands.guild_only()
    async def warn(self, ctx, person: discord.Member = None, *, reason: str = 'Not specified'):
        if not person:
            await ctx.send('No member has been specified.')
            return
        connection = sqlite3.connect(WARNFILE)
        cursor = connection.cursor()
        rc = cursor.rowcount
        rows = cursor.execute("SELECT MAX(ID) AS len FROM warnings WHERE Person=?;", (str(person.id), )).fetchall()
        if rows == [] or not rows[0][0]:
            cursor.execute("INSERT INTO warnings (ID,Person,Reason,Moderator,WarnedDate) VALUES (1,?,?,?,?);", (
                           str(person.id), reason.replace('\\', '\\\\').replace('"', '\\"'), str(ctx.message.author.id), datetime.now()))
        else:
            cursor.execute("INSERT INTO warnings (ID,Person,Reason,Moderator,WarnedDate) VALUES (?,?,?,?,?);", (
                           str(rows[0][0] + 1), str(person.id), reason.replace('\\', '\\\\').replace('"', '\\"'), str(ctx.message.author.id), datetime.now()))
        if rc == cursor.rowcount:
            return await ctx.send('Failed to warn that bad guy. Unexpected catched error happened '
                                  '(no modification has been made to the db, which is unintended...)')
        cursor.execute("COMMIT;")
        await ctx.send(f'{ctx.message.author.mention} warned {person.mention}.\nReason: {reason}.')
        await log(f'{ctx.message.author.mention} warned {person.mention}.\nReason: {reason}.', guild=ctx.message.channel.guild)

    @commands.command(name='rmwn', help='Remove a warning: /rmwn @person warnNumber')
    @chk_sudo()
    @commands.guild_only()
    async def rmwn(self, ctx, person: discord.Member = None, *, num: int = 0):
        if not person:
            await ctx.send('No member has been specified.')
            return
        connection = sqlite3.connect(WARNFILE)
        cursor = connection.cursor()
        if num == 0:
            cursor.execute("DELETE FROM warnings WHERE Person=?;", (str(person.id), ))
        else:
            cursor.execute("DELETE FROM warnings WHERE Person=? AND ID=?;", (str(person.id), str(num)))
        cursor.execute("COMMIT;")
        close_cursor(cursor)
        close_connection(connection)
        return await ctx.send('Okay!')

    @commands.command(name='chkwrn', aliases=['checkwarn', 'checkwarns', 'checkwarnings', 'ckwn', "chkwn"], help='Show warnings of member')
    @commands.guild_only()
    async def chkwrn(self, ctx, member: discord.Member = None, raw=''):
        member = member or ctx.message.author
        connection = sqlite3.connect(WARNFILE)
        cursor = connection.cursor()
        rows = cursor.execute("SELECT ID,Moderator,Reason,WarnedDate FROM warnings WHERE Person=?;", (str(member.id), )).fetchall()
        if rows == []:
            close_cursor(cursor)
            close_connection(connection)
            return await ctx.send(f"Member {member.mention} does not have any warnings.")
        if raw == 'raw':
            t = pyTableMaker.onelineTable(cellwrap=25)
            t.new_column('Warn No.')
            t.new_column('Reason')
            t.new_column('Moderator')
            t.new_column('Date')
            loopCount = 1
            for warning in rows:
                user = await self.bot.fetch_user(warning[1])
                t.insert(loopCount, warning[2], user.display_name, warning[3])
                loopCount += 1
            embed = discord.Embed(title="Warnings", description='```css\n' + t.get() + '\n```', color=0x00FFBB)
            embed.set_author(name=member, icon_url=ctx.message.author.avatar_url)
            embed.timestamp = datetime.utcnow()
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Warnings", description=f'list of warnings for {member.mention}', color=0x00FFBB)
            embed.timestamp = datetime.utcnow()
            embed.set_author(name=member, icon_url=member.avatar_url)
            loopCount = 1
            for warning in rows:
                user = await self.bot.fetch_user(warning[1])
                embed.add_field(name=user.display_name, value=str(loopCount) + '. ' + warning[2], inline=True)
                loopCount += 1
            await ctx.send(embed=embed)
        close_cursor(cursor)
        return close_connection(connection)

    @commands.command(name='kick', help='/kick @someone [reason]', aliases=['sb', 'softban', 'k'])
    @chk_sudo()
    @commands.guild_only()
    async def kick(self, ctx, member: discord.Member = None, reason: str = 'Not specified'):
        try:
            if not member:
                await ctx.send('Please specify a member.')
                return
            await member.send(f'You have been kicked.\nReason: {reason}')
            await member.kick(reason=reason)
            await ctx.send(
                f'{ctx.message.author.mention} has kicked {member.mention}.\nReason: {reason}\n'
                + random.choice([
                    'https://tenor.com/view/kung-fu-panda-karate-kick-gif-15261593',
                    'https://tenor.com/view/strong-kick-hammer-down-fatal-blow-scarlet-johnny-cage-gif-13863296'])
            )
            return
        except Exception as e:
            await ctx.send(f'Wut happened? {e}')

    @commands.command(name='ban', aliases=["b"], help='/ban @someone [reason]')
    @chk_sudo()
    @commands.guild_only()
    async def ban(self, ctx, member: discord.Member = None, reason: str = 'Not specified'):
        global id
        if not member:
            return await ctx.send('Please specify a member.')
        await member.send(f'You have been banned.\nReason: {reason}')
        await member.ban(reason=reason)
        id = member.id
        await ctx.send(f'{ctx.message.author.mention} has banned {member.mention}.\nReason: {reason}\n' + random.choice([
            'https://imgur.com/V4TVpbC',
            'https://tenor.com/view/thor-banhammer-discord-banned-banned-by-admin-gif-12646581',
            'https://tenor.com/view/cat-red-hammer-bongo-cat-bang-hammer-gif-15733820'
        ]))
        return

    @commands.command(name='unban', help='/unban userID')
    @chk_sudo()
    @commands.guild_only()
    async def unban(self, ctx, userID: int = 0):
        if userID == 0:
            global id
            if id == 0:
                await ctx.send(f'{ctx.message.author.mention} please specify an user id.')
                return
            else:
                userID = id
        user = await self.bot.fetch_user(userID)
        await ctx.guild.unban(user)
        await ctx.send("Fine. There you go.")

    @commands.command(name='mute', help='mute a member')
    @chk_sudo()
    @commands.guild_only()
    async def mute(self, ctx, member: discord.Member, mute_time: str, *, reason=None):
        global muted

        if mute_time.endswith('m'):
            t = int(mute_time[:-1]) * 60
        elif mute_time.endswith('h'):
            t = int(mute_time[:-1]) * 3600
        elif mute_time.endswith('d'):
            t = int(mute_time[:-1]) * 3600 * 24
        elif mute_time.endswith('w'):
            t = int(mute_time[:-1]) * 3600 * 24 * 7
        else:
            try:
                t = int(mute_time)
            except Exception:
                await ctx.send("time should ends with `m`, `h`, `d`, `w`, or no postfix.")
                return

        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if role is None:
            raise NoMutedRole
        await member.add_roles(role)
        await ctx.send(f'**Muted** {member.mention}\n**Reason: **{reason}\n**Duration:** {mute_time}')

        embed = discord.Embed(color=discord.Color.green())
        embed.add_field(name=f"You've been **Muted** in {ctx.guild.name}.", value=f"**Action By: **{ctx.author.mention}\n"
                                                                                  f"**Reason: **{reason}\n**Duration:** {mute_time}")
        await member.send(embed=embed)
        try:
            muted[str(member.id)] += 1
        except Exception:
            muted[str(member.id)] = 1
        muted[str(member.id)]
        await asyncio.sleep(t)

        if muted[str(member.id)] > 1:
            muted[str(member.id)] -= 1
            return
        try:
            await member.remove_roles(role)
        except Exception:
            muted[str(member.id)] -= 1
            return
        await ctx.send(f"**Unmuted {member.mention}**")
        muted[str(member.id)] -= 1
        return

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, NoMutedRole):
            await ctx.send("That command requires creating a @Muted role inside this guild that does not allow members to send messages.")


def setup(bot):
    bot.add_cog(Mod(bot))
