from discord.ext import commands
from discord.utils import get
from logcfg import logger
from dotenv import load_dotenv
import discord
import os
load_dotenv()
guild_id = int(os.getenv('DISCORD_GUILD'))

suRole = ['Administrators', 'Seniors', 'CathayChannelAccess', 'F2OfficialChannelAccess', 'DJ', 'MCdiscSRV', 'Groovy', 'MEE6', 'Dyno', 'KCCS Official', 'Muted']

class manage(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.group(name='role',aliases=['roles'],help='Get your role rolling automatically.  Possible sub-commands: assign, remove, create, delete')
    async def role(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f"2 bed idk wat u r toking 'bout, but wut?")
            await ctx.message.delete()
            return
    @role.command(name='assign',aliases=['give','set','grant','add'],help=r'Usage: /role assign {rolename} [member].  Possible rolename: 2a, 1b, friends, etc.',pass_context=True)
    async def assign(self,ctx,rolename='',member: discord.Member=None):
        member = member or ctx.message.author
        if rolename == '':
            await ctx.send('apparently this function requires 2 parameters.')
            await ctx.message.delete()
            return
        global suRole
        if rolename in suRole and not get(ctx.guild.roles, name='Administrators') in ctx.message.author.roles:
            await ctx.send('g3t r3kt, u r not admin!!')
            await ctx.message.delete()
            return
        try:
            role = get(ctx.guild.roles, name=rolename)
            if role is None:
                await ctx.send( f'Failed to get the role.  Probably role {rolename} is not a thing.  {ctx.message.author.mention}, please make sure you got it right.')
                print(          f'Failed to get the role.  Probably role {rolename} is not a thing.  Did {ctx.message.author} got it right?')
                logger.info(    f'Failed to get the role.  Probably role {rolename} is not a thing.  Did {ctx.message.author} got it right?')
                await ctx.message.delete()
                return
            await member.add_roles(role)
            logger.info(    f'Role {rolename} has been added to {member} by {ctx.message.author}.')
            print(          f'Role {rolename} has been added to {member} by {ctx.message.author}.')
            await ctx.send( f'Role {rolename} has been added to {member.mention} by {ctx.message.author.mention}.')
        except Exception as e:
            logger.warn(    f'failed to add role {rolename} to {member} (requested by {ctx.message.author}) with error message:\n{e}')
            await ctx.send( f'failed to add role {rolename} to {member} (requested by {ctx.message.author.mention}) with error message:\n{e}')
            print(          f'failed to add role {rolename} to {member} (requested by {ctx.message.author}) with error message:\n{e}')
        await ctx.message.delete()
        return


    @role.command(name='remove',aliases=['rm','revoke'],help=r'Usage: /role remove {rolename} [member].  Possible rolename: 2a, 1b, friends, etc.',pass_context=True)
    async def remove(self,ctx,rolename='',member: discord.Member=None):
        member = member or ctx.message.author
        if rolename == '':
            await ctx.send('apparently this function requires 2 parameters.')
            await ctx.message.delete()
            return
        global suRole
        if rolename in suRole and not get(ctx.guild.roles, name='Administrators') in ctx.message.author.roles:
            await ctx.send('g3t r3kt, u r not admin!!')
            await ctx.message.delete()
            return
        try:
            role = get(ctx.guild.roles, name=rolename)
            if role is None:
                await ctx.send( f'Failed to get the role.  Probably role {rolename} is not a thing.  {ctx.message.author.mention}, please make sure you got it right.')
                print(          f'Failed to get the role.  Probably role {rolename} is not a thing.  Did {ctx.message.author} got it right?')
                logger.info(    f'Failed to get the role.  Probably role {rolename} is not a thing.  Did {ctx.message.author} got it right?')
                await ctx.message.delete()
                return
            await member.remove_roles(role)
            logger.info(    f'Role {rolename} has been removed from {member} by {ctx.message.author}.')
            print(          f'Role {rolename} has been removed from {member} by {ctx.message.author}.')
            await ctx.send( f'Role {rolename} has been removed from {member.mention} by {ctx.message.author.mention}.')
        except Exception as e:
            logger.warn(    f'failed to remove role {rolename} from {member} (requested by {ctx.message.author}) with error message:\n{e}')
            await ctx.send( f'failed to remove role {rolename} from {member} (requested by {ctx.message.author.mention}) with error message:\n{e}')
            print(          f'failed to remove role {rolename} from {member} (requested by {ctx.message.author}) with error message:\n{e}')
        await ctx.message.delete()
        return
    


    @role.command(name='create',aliases=['make','mk'],help=r'Create a new role. /role create {role name}')
    async def create(self,ctx,*,rolename=''):
        if rolename == '':
            await ctx.send('apparently this function requires 2 parameters.')
            await ctx.message.delete()
            return
        try:
            await ctx.guild.create_role(name=rolename)
            await ctx.send( f'Role {rolename} created successfully. (Requested by {ctx.message.author.mention})')
            logger.info(    f'Role {rolename} created successfully. (Requested by {ctx.message.author})')
            print(          f'Role {rolename} created successfully. (Requested by {ctx.message.author})')
        except discord.Forbidden:
            await ctx.send( f'Failed to create role {rolename} because the requester {ctx.message.author.mention} has missing permissions.  Administrative privileges are required.\n'
                            'Error message: {e}')
            print(          f'Failed to create role {rolename} because the requester {ctx.message.author} has missing permissions.  Administrative privileges are required.\n'
                            'Error message: {e}')
            logger.warn(    f'Failed to create role {rolename} because the requester {ctx.message.author} has missing permissions.  Administrative privileges are required.\n'
                            'Error message: {e}')
        except Exception as e:
            await ctx.send( f'Failed to create role {rolename} (requested by {ctx.message.author.mention}).\nError message: {e}')
            print(          f'Failed to create role {rolename} (requested by {ctx.message.author}).\nError message: {e}')
            logger.warn(    f'Failed to create role {rolename} (requested by {ctx.message.author}).\nError message: {e}')
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
                print(f'Role {rolename} deleted successfully. (Requested by {ctx.message.author})')
                logger.info(f'Role {rolename} deleted successfully. (Requested by {ctx.message.author})')
            except discord.Forbidden as e:
                await ctx.send( f'Failed to delete role {rolename} because the requester {ctx.message.author.mention} has missing permissions.  Administrative privileges are required.\n'
                                f'Error message: {e}')
                print(          f'Failed to delete role {rolename} because the requester {ctx.message.author} has missing permissions.  Administrative privileges are required.\n'
                                f'Error message: {e}')
                logger.warn(    f'Failed to delete role {rolename} because the requester {ctx.message.author} has missing permissions.  Administrative privileges are required.\n'
                                f'Error message: {e}')
            except Exception as e:
                await ctx.send( f'Failed to create role {rolename} (requested by {ctx.message.author.mention}).\nError message: {e}')
                print(          f'Failed to create role {rolename} (requested by {ctx.message.author}).\nError message: {e}')
                logger.warn(    f'Failed to create role {rolename} (requested by {ctx.message.author}).\nError message: {e}')
        else:
            await ctx.send( f'Failed to get the role.  Probably role {rolename} is not a thing.  {ctx.message.author.mention}, please make sure you got it right.')
            print(          f'Failed to get the role.  Probably role {rolename} is not a thing.  Did {ctx.message.author} got it right?')
            logger.info(    f'Failed to get the role.  Probably role {rolename} is not a thing.  Did {ctx.message.author} got it right?')
        await ctx.message.delete()
        return




def setup(bot):
    bot.add_cog(manage(bot))