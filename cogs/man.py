from discord.ext import commands
from discord.utils import get
from logcfg import logger
from fileman import *
from datetime import datetime
import discord,os,pyTableMaker,random,sqlite3
from ext.dbctrl import close_connection

def is_sudoers(member):
    if get(member.guild.roles,name="Moderators") not in member.roles and get(member.guild.roles,name='Administrators') not in member.roles:
        return False
    return True

class man(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    @commands.group(name='role',aliases=['roles'],help='Get your role rolling automatically.  Possible sub-commands: assign, remove, create, delete')
    async def role(self,ctx):
        if is_sudoers(ctx.author):
            await ctx.send('g3t r3kt, u r not admin!!')
            await ctx.message.delete()
            return
        if ctx.invoked_subcommand is None:
            await ctx.send(f"2 bed idk wat u r toking 'bout, but wut?")
            await ctx.message.delete()
            return
    @role.command(name='assign',aliases=['give','set','grant','add'],help=r'Possible rolename: 2a, 1b, friends, etc.',pass_context=True)
    async def assign(self,ctx,rolename: discord.Role,member: discord.Member=None):
        member = member or ctx.message.author
        if rolename == '':
            await ctx.send('apparently this function requires 2 parameters.')
            await ctx.message.delete()
            return
        try:
            role = get(ctx.guild.roles, name=rolename)
            if role is None:
                await ctx.send( f'Failed to get the role.  Probably role {rolename} is not a thing.  {ctx.message.author.mention}, please make sure you got it right.')
                await ctx.message.delete()
                return
            await member.add_roles(role)
            await ctx.send( f'Role {rolename} has been added to {member.mention} by {ctx.message.author.mention}.')
        except Exception as e:
            await ctx.send( f'failed to add role {rolename} to {member} (requested by {ctx.message.author.mention}) with error message:\n{e}')
        await ctx.message.delete()
        return


    @role.command(name='remove',aliases=['rm','revoke'],help=r'Possible rolename: 2a, 1b, friends, etc.',pass_context=True)
    async def remove(self,ctx,rolename='',member: discord.Member=None):
        member = member or ctx.message.author
        if rolename == '':
            await ctx.send('apparently this function requires 2 parameters.')
            await ctx.message.delete()
            return
        try:
            role = get(ctx.guild.roles, name=rolename)
            if role is None:
                await ctx.send( f'Failed to get the role.  Probably role {rolename} is not a thing.  {ctx.message.author.mention}, please make sure you got it right.')
                await ctx.message.delete()
                return
            await member.remove_roles(role)
            await ctx.send( f'Role {rolename} has been removed from {member.mention} by {ctx.message.author.mention}.')
        except Exception as e:
            await ctx.send( f'failed to remove role {rolename} from {member} (requested by {ctx.message.author.mention}) with error message:\n{e}')
        await ctx.message.delete()
        return



    @role.command(name='create',aliases=['make','mk'],help=r'Create a new role.')
    async def create(self,ctx,*,rolename=''):
        if rolename == '':
            await ctx.send('apparently this function requires 2 parameters.')
            await ctx.message.delete()
            return
        try:
            await ctx.guild.create_role(name=rolename)
            await ctx.send( f'Role {rolename} created successfully. (Requested by {ctx.message.author.mention})')
        except discord.Forbidden:
            await ctx.send( f'Failed to create role {rolename} because the requester {ctx.message.author.mention} has missing permissions.  Administrative privileges are required.\n'
                            'Error message: {e}')
        except Exception as e:
            await ctx.send( f'Failed to create role {rolename} (requested by {ctx.message.author.mention}).\nError message: {e}')
        await ctx.message.delete()
        return


    @role.command(name='delete',aliases=['del'],help='Delete a role (remove from all users)')
    async def delete(self,ctx,*,rolename):
        if rolename == '':
            await ctx.send('apparently this function requires 2 parameters.')
            await ctx.message.delete()
            return
        role = discord.utils.get(ctx.guild.roles, name=rolename)
        if role:
            try:
                await role.delete()
                await ctx.send(f'Role {rolename} deleted successfully. (Requested by {ctx.message.author.mention})')
            except discord.Forbidden as e:
                await ctx.send( f'Failed to delete role {rolename} because the requester {ctx.message.author.mention} '
                                f'has missing permissions.  Administrative privileges are required.\nError message: {e}')
            except Exception as e:
                await ctx.send( f'Failed to create role {rolename} (requested by {ctx.message.author.mention}).\nError message: {e}')
        else:
            await ctx.send( f'Failed to get the role.  Probably role {rolename} is not a thing.  {ctx.message.author.mention}, please make sure you got it right.')
        await ctx.message.delete()
        return


    @commands.command(name='nickname',help='Change the nickname')
    async def nickname(self,ctx, newNick='', member: discord.Member=None):
        async with ctx.typing():
            member = member or ctx.message.author
        if newNick=='':
            await ctx.send('Nickname cannot be blank.')
            return
        try:
            await ctx.message.guild.get_member(member.id).edit(nick=newNick)
            await ctx.send(f'Operation completed successfully.')
            return
        except Exception as e:
            await ctx.send( f'An error occurred while trying to assign {member.mention} a new nickname (requested by {ctx.message.author.mention})\nError message: {e}')
            return
    @commands.command(name='warn',help='Warn a person: /warn @person reason',aliases=['warning'])
    async def warn(self,ctx,person:discord.Member=None,*,reason:str='Not specified'):
        if not person:
            await ctx.send('No member has been specified.')
            return
        connection = sqlite3.connect("samples/warnings.db")
        cursor = connection.cursor()
        rows = cursor.execute("SELECT MAX(ID) AS len FROM warnings WHERE Person=?;", (str(person.id)), ).fetchall()
        if rows==[] or not rows[0][0]:  cursor.execute("INSERT INTO warnings (ID,Person,Reason,Moderator,WarnedDate) VALUES (0,?,?,?,?);", (                        str(person.id), reason.replace('\\','\\\\').replace('"','\\"'), str(ctx.message.author.id), datetime.now()))
        else:                           cursor.execute("INSERT INTO warnings (ID,Person,Reason,Moderator,WarnedDate) VALUES (?,?,?,?,?);", (str(rows[0][0] + 1),    str(person.id), reason.replace('\\','\\\\').replace('"','\\"'), str(ctx.message.author.id),  datetime.now()))
        close_connection(connection)
        await ctx.send(f'{ctx.message.author.mention} warned {person.mention}.\nReason: {old_reason}.')
        await log(f'{ctx.message.author.mention} warned {person.mention}.\nReason: {old_reason}.',guild=ctx.message.channel.guild)
    @commands.command(name='rmwn',help='Remove a warning: /rmwn @person warnNumber')
    async def rmwn(self,ctx,person:discord.Member=None,*,num:int=0):
        if not person:
            await ctx.send('No member has been specified.')
            return
        connection = sqlite3.connect("samples/warnings.db")
        cursor = connection.cursor()
        if num==0:  cursor.execute("DELETE FROM warnings WHERE Person=?;", (str(person.id)))
        else:       cursor.execute("DELETE FROM warnings WHERE Person=? AND ID=?;", (str(person.id), str(num)))
        close_connection(connection)
        return await ctx.send('Okay!')
    @commands.command(name='chkwrn',aliases=['checkwarn','checkwarns','checkwarnings','ckwn',"chkwn"],help='Show warnings of member: /chkwrn @person [raw]')
    async def chkwrn(self,ctx,member:discord.Member=None,raw=''):
        member = member or ctx.message.author
        connection = sqlite3.connect("samples/warnings.db")
        cursor = connection.cursor()
        rows = cursor.execute("SELECT ID,Moderator,Reason,WarnedDate FROM warnings WHERE Person=?;", (str(member.id), )).fetchall()
        if rows==[]:    return await ctx.send(f"Member {member.mention} does not have any warnings.")
        if raw=='raw':
            t = table.onelineTable()
            col_no = t.new_column('Warn No.')
            col_reason = t.new_column('Reason')
            col_mod = t.new_column('Moderator')
            col_date = t.new_column('Date')
            loopCount = 1
            for warning in rows:
                t.insert(str(warning[0]),warning[2],self.bot.fetch_user(warning[1]),warning[3])
                loopCount += 1
            embed = discord.Embed(title="Warnings", description='```css\n'+t.get()+'\n```',color=0x00FFBB)
            embed.set_author(name=member,icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Warnings", description=f'list of warnings for {member.mention}',color=0x00FFBB)
            embed.set_author(name=member,icon_url=member.avatar_url)
            loopCount = 1
            for warning in rows:
                embed.add_field(name=self.bot.fetch_user(warning[1]).mention,value=str(warning[0])+'. '+warning[2],inline=True)
                loopCount += 1
            await ctx.send(embed=embed)
        return close_connection(connection)
    @commands.command(name='kick',help='/kick @someone [reason]',aliases=['sb','softban','k'])
    async def kick(self,ctx,member:discord.Member=None,reason:str='Not specified'):
        try:
            if not member:
                await ctx.send('Please specify a member.')
                return
            await member.send(f'You have been kicked.\nReason: {reason}')
            await member.kick()
            await ctx.send(f'{ctx.message.author.mention} has kicked {member.mention}.\nReason: {reason}\n' + random.choice(['https://tenor.com/view/kung-fu-panda-karate-kick-gif-15261593','https://tenor.com/view/strong-kick-hammer-down-fatal-blow-scarlet-johnny-cage-gif-13863296']))
            return
        except Exception as e:
            await ctx.send(f'Wut happened? {e}')
    @commands.command(name='ban',aliases=["b"],help='/ban @someone [reason]')
    async def ban(self,ctx,member:discord.Member=None,reason:str='Not specified'):
        global id
        try:
            if not member:
                await ctx.send('Please specify a member.')
                return
            dm = await member.create_dm()
            await dm.send(f'You have been banned.\nReason: {reason}')
            await member.ban()
            id = member.id
            await ctx.send(f'{ctx.message.author.mention} has banned {member.mention}.\nReason: {reason}\n' + random.choice(['https://imgur.com/V4TVpbC','https://tenor.com/view/thor-banhammer-discord-banned-banned-by-admin-gif-12646581','https://tenor.com/view/cat-red-hammer-bongo-cat-bang-hammer-gif-15733820']))
            return
        except Exception as e:
            await ctx.send(f'Wut happened? {e}')
    @commands.command(name='unban',help='/unban userID')
    async def unban(self,ctx,userID:int=0):
        if userID==0:
            global id
            if id == 0:
                await ctx.send(f'{ctx.message.author.mention} please specify an user id.')
                return
            else:
                userID = id
        try:
            user = await self.bot.fetch_user(userID)
            await ctx.guild.unban(user)
        except:
            await ctx.send('Failed to unban the user.')
        return




def setup(bot):
    bot.add_cog(man(bot))
