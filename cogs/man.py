from discord.ext import commands
from discord.utils import get
from logcfg import logger

import discord,os,table,random

guild_id = int(os.getenv('DISCORD_GUILD'))
id=0
issu = False
suMode = []
suRole = ['Administrators', 'Seniors', 'CathayChannelAccess', 'F2OfficialChannelAccess', 'DJ', 'MCdiscSRV', 'Groovy', 'MEE6', 'Dyno', 'KCCS Official', 'Muted','Bots',"moderators"]

def delete_line_by_full_match(original_file, line_to_delete):
    """ In a file, delete the lines at line number in given list"""
    is_skipped = False
    dummy_file = original_file + '.tmp'
    # Open original file in read only mode and dummy file in write mode
    with open(original_file, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        # Line by line copy data from original file to dummy file
        for line in read_obj:
            line_to_match = line
            if line[-1] == '\n':
                line_to_match = line[:-1]
            # if current line matches with the given line then skip that line
            if line_to_match != line_to_delete:
                write_obj.write(line)
            else:
                is_skipped = True
    # If any line is skipped then rename dummy file as original file
    if is_skipped:
        os.remove(original_file)
        os.rename(dummy_file, original_file)
    else:
        os.remove(dummy_file)
    return is_skipped
def delete_line_by_full_match2(original_file, line_to_delete,count=1):
    """ In a file, delete the lines at line number in given list"""
    is_skipped = False
    dummy_file = original_file + '.tmp'
    # Open original file in read only mode and dummy file in write mode
    l=0
    with open(original_file, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        # Line by line copy data from original file to dummy file
        for line in read_obj:
            line_to_match = line
            if line[-1] == '\n':
                line_to_match = line[:-1]
            # if current line matches with the given line then skip that line
            if line_to_match != line_to_delete or count==l:
                write_obj.write(line)
            else:
                l+=1
                is_skipped = True
    # If any line is skipped then rename dummy file as original file
    if is_skipped:
        os.remove(original_file)
        os.rename(dummy_file, original_file)
    else:
        os.remove(dummy_file)
    return is_skipped
def delete_line_by_condition(original_file, condition):
    """ In a file, delete the lines at line number in given list"""
    dummy_file = original_file + '.tmp'
    is_skipped = False
    # Open original file in read only mode and dummy file in write mode
    with open(original_file, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        # Line by line copy data from original file to dummy file
        for line in read_obj:
            # if current line matches the given condition then skip that line
            if condition(line) == False:
                write_obj.write(line)
            else:
                is_skipped = True
    # If any line is skipped then rename dummy file as original file
    read_obj.close()
    write_obj.close()
    if is_skipped:
        os.remove(original_file)
        os.rename(dummy_file, original_file)
    else:
        os.remove(dummy_file)
def delete_line_with_word(file_name, word):
    """Delete lines from a file that contains a given word / sub-string """
    delete_line_by_condition(file_name, lambda x : word in x )

class manage(commands.Cog):
    global suMode
    def __init__(self,bot):
        self.bot = bot
    @commands.group(name='sudo',aliases=['su'],help='SUDOOOOOOO')
    async def sudo(self,ctx,func='',*,args=''):
        if get(ctx.guild.roles,name="Moderators") not in ctx.message.author.roles and get(ctx.guild.roles,name='Administrators') not in ctx.message.author.roles:
            await ctx.send('password...wait, no.')
            return
        suMode.append(ctx.message.author)
        if func == 'role':
            await self.role(ctx,args)
        elif func == 'nickname':
            await self.nickname(ctx,args)
        elif func == 'warn':
            try:
                await self.warn(ctx,discord.Member(args[0]),args[1])
            except:
                await self.warn(ctx,discord.Member(args[0]))
        elif func == 'rmwn':
            try:
                await self.rmwn(ctx,args.split(' ')[0],args.split(' ')[1])
            except:
                await self.rmwn(ctx,args.split(' ')[0])
        elif func == 'ckwn':
            await self.ckwn(ctx,args)
        elif func == 'kick':
            try:
                await self.kick(ctx,args.split(' ')[0],args.split(' ')[1])
            except:
                await self.kick(ctx,args.split(' ')[0])
        elif func == 'ban':
            await self.ban(ctx,args.split(' ')[0],args.split(' ')[1])
        elif func == 'unban':
            await self.unban(ctx,args.split(' ')[0])
        elif func == 'su':
            await self.su(ctx)
        else:
            await ctx.send('kthxbai')
        issu = False
        suMode.remove(ctx.message.author)
    @sudo.command(name='su',help='Gets into sudo mode. Everything will be in sudo')
    async def su(self,ctx):
        global issu
        global suMode
        if ctx.message.author.mention in suMode:
            ctx.send(f'----- Nothing changed, already in superuser mode {ctx.message.author.mention} -----')
        suMode.append(ctx.message.author)
        issu = True
        await ctx.send(f'##### Activated superuser mode {ctx.message.author.mention} #####')
    @commands.command(name='exit',aliases=['quit'],help='Exit sudo mode')
    async def exit(self,ctx):
        global suMode
        if ctx.message.author in suMode:
            suMode.remove(ctx.message.author)
            await ctx.send(f'$$$$$ Exited superuser mode {ctx.message.author.mention} $$$$$')
        else:
            await ctx.send(f'----- Nothing changed, not in superuser mode {ctx.message.author.mention} -----')
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
        if ctx.message.author not in suMode:
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
        if ctx.message.author not in suMode:
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
        if ctx.message.author not in suMode:
            await ctx.send('g3t r3kt, u r not admin!!')
            await ctx.message.delete()
            return
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
        if ctx.message.author not in suMode:
            await ctx.send('g3t r3kt, u r not admin!!')
            await ctx.message.delete()
            return
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
                await ctx.send( f'Failed to delete role {rolename} because the requester {ctx.message.author.mention} '
                                f'has missing permissions.  Administrative privileges are required.\nError message: {e}')
                print(          f'Failed to delete role {rolename} because the requester {ctx.message.author} '
                                f'has missing permissions.  Administrative privileges are required.\nError message: {e}')
                logger.warn(    f'Failed to delete role {rolename} because the requester {ctx.message.author} '
                                f'has missing permissions.  Administrative privileges are required.\nError message: {e}')
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


    @commands.command(name='nickname',help='Change the nickname')
    async def nickname(self,ctx, newNick='', member: discord.Member=None):
        async with ctx.typing():
            member = member or ctx.message.author
        if (ctx.message.author not in suMode) and member != ctx.message.author:
            await ctx.send('g3t r3kt, u r not admin!!')
            await ctx.message.delete()
            return
        if newNick=='':
            await ctx.send('Nickname cannot be blank.')
            return
        try:
            await ctx.message.guild.get_member(member.id).edit(nick=newNick)
            await ctx.send(f'Operation completed successfully.')
            return
        except Exception as e:
            await ctx.send( f'An error occurred while trying to assign {member.mention} a new nickname (requested by {ctx.message.author.mention})\nError message: {e}')
            print(          f'An error occurred while trying to assign {member} a new nickname (requested by {ctx.message.author})\nError message: {e}')
            logger.warn(    f'An error occurred while trying to assign {member} a new nickname (requested by {ctx.message.author})\nError message: {e}')
            return
    def check(self,person,reason,mod,_globals,_locals):
        result = ''
        if f'u{person.id}' not in _globals and f'u{person.id}' not in _locals:
            result += f"u{person.id} = {{'count': 0, 'reasons': [],'moderator': []}}\n"
        result += f"u{person.id}['reasons'].append(\"{reason}\")\n"
        result += f"u{person.id}['count'] += 1\n"
        result += f"u{person.id}['moderator'].append('{mod}')\n"
        return result
    @commands.command(name='warn',help='Warn a person: /warn @person reason',aliases=['warning'])
    async def warn(self,ctx,person:discord.Member=None,*,reason:str='Not specified'):
        if not person:
            await ctx.send('No member has been specified.')
            return
        if ctx.message.author not in suMode and not ctx.message.author.bot:
            await ctx.send('g3t r3kt, u r not admin!!')
            await ctx.message.delete()
            return
        rf = open('samples/warnList','r')
        _globals = globals()
        _locals = locals()
        exec(rf.read(),_globals,_locals)
        result = self.check(person,reason,ctx.message.author.name,_globals,_locals)
        wf = open('samples/warnList','a')
        wf.write(result + '\n')
        rf.close()
        wf.close()
        f = open('samples/warnList','r')
        rs = '\n'.join([i for i in f.read().split('\n') if len(i) > 0])
        f.close()
        f = open('samples/warnList','w')
        f.write(rs + '\n')
        f.close()
        await ctx.send(f'{ctx.message.author.mention} warned {person.mention}.\nReason: {reason}.')
    @commands.command(name='rmwn',help='Remove a warning: /rmwn @person warnNumber')
    async def rmwn(self,ctx,person:discord.Member=None,*,num:int=0):
        if not person:
            await ctx.send('No member has been specified.')
            return
        if ctx.message.author not in suMode:
            await ctx.send('g3t r3kt, u r not admin!!')
            await ctx.message.delete()
            return
        # try:
        rf = open('samples/warnList','r')
        _locals = locals()
        _globals = globals()
        exec(rf.read(),_globals,_locals)
        if (f'u{person.id}' not in _locals and f'u{person.id}' not in _globals) or _locals[f'u{person.id}']['count'] == 0:
            await ctx.send(f'Either {person.mention} is not a thing, or he/she does not have any warning.')
            rf.close()
            return
        if num==0:
            rf.close()
            delete_line_with_word('samples/warnList',f'u{person.id}')
            await ctx.send(f'Removed all warnings for {person.mention}')
            return
        word = f'u{person.id}['
        rf.close()
        toRemove = []
        num *= 3
        num -= 2
        l = 1
        with open('samples/warnList') as rf:
            for line in rf:
                if word in line:
                    if l == num or l == num+1 or l == num+2:
                        toRemove.append(line[:-1])
                    l += 1
        for line in toRemove:
            delete_line_by_full_match2('samples/warnList',line,1)
        await ctx.send(f'Removed warning number {str(int((num + 2)/3))} for {person.mention}\n')
        return
        # except Exception as e:
        #     await msg.edit(content='An error has occurred: ' + str(e))
        #     return
    @commands.command(name='chkwrn',aliases=['checkwarn','checkwarns','checkwarnings','ckwn',"chkwn"],help='Show warnings of member: /chkwrn @person [raw]')
    async def chkwrn(self,ctx,member:discord.Member=None,raw=''):
        member = member or ctx.message.author
        rf = open('samples/warnList','r')
        _globals = globals()
        _locals = locals()
        exec(rf.read(),_globals,_locals)
        rf.close()
        try:
            warnObj = _locals[f'u{member.id}']
        except:
            await ctx.send(f"Member {member.mention} does not have any warnings.")
            return
        if raw=='raw':
            t = table.onelineTable()
            col_no = t.new_column('Warn No.')
            col_reason = t.new_column('Reason')
            col_mod = t.new_column('Moderator')
            loopCount = 1
            for reason in warnObj['reasons']:
                t.insert(str(loopCount),reason,warnObj['moderator'][loopCount-1])
                loopCount += 1
            embed = discord.Embed(title="Warnings", description='```css\n'+t.get()+'\n```',color=0x00FFBB)
            embed.set_author(name=member,icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=embed)
            return
        else:
            embed = discord.Embed(title="Warnings", description=f'list of warnings for {member.mention}',color=0x00FFBB)
            embed.set_author(name=member,icon_url=member.avatar_url)
            loopCount = 1
            for reason in warnObj['reasons']:
                embed.add_field(name=loopCount,value=reason,inline=True)
                loopCount += 1
            await ctx.send(embed=embed)
            return
    @commands.command(name='kick',help='/kick @someone [reason]',aliases=['sb','softban','k'])
    async def kick(self,ctx,member:discord.Member=None,reason:str='Not specified'):
        try:
            if not member:
                await ctx.send('Please specify a member.')
                return
            if ctx.message.author not in suMode:
                await ctx.send('g3t r3kt, u r not admin!!')
                await ctx.message.delete()
                return
            await member.kick()
            dm = await member.create_dm()
            await dm.send(f'You have been kicked.\nReason: {reason}')
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
            if ctx.message.author not in suMode:
                await ctx.send('g3t r3kt, u r not admin!!')
                await ctx.message.delete()
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
        if ctx.message.author not in suMode:
            await ctx.send('g3t r3kt, u r not admin!!')
            await ctx.message.delete()
            return
        user = await self.bot.fetch_user(userID)
        await ctx.guild.unban(user)
        return




def setup(bot):
    bot.add_cog(manage(bot))