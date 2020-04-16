from discord.ext import commands
from discord.utils import get
from logcfg import logger
from dotenv import load_dotenv
import discord,os,table
load_dotenv()
guild_id = int(os.getenv('DISCORD_GUILD'))
suRole = ['Administrators', 'Seniors', 'CathayChannelAccess', 'F2OfficialChannelAccess', 'DJ', 'MCdiscSRV', 'Groovy', 'MEE6', 'Dyno', 'KCCS Official', 'Muted']
id=0

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
    def __init__(self,bot):
        self.bot = bot
    def check(self,person,reason,mod,_globals,_locals):
        result = ''
        if f'u{person.id}' not in _globals and f'u{person.id}' not in _locals:
            result += f"u{person.id} = {{'count': 0, 'reasons': [],'moderator': []}}\n"
        result += f"u{person.id}['reasons'].append('{reason}')\n"
        result += f"u{person.id}['count'] += 1\n"
        result += f"u{person.id}['moderator'].append('{mod}')\n"
        return result
    @commands.command(name='warn',help='Warn a person: /warn @person reason',aliases=['warning'])
    async def warn(self,ctx,person:discord.Member=None,*,reason:str='Not specified'):
        if not person:
            await ctx.send('No member has been specified.')
            return
        role = discord.utils.find(lambda r: r.name == 'Administrators', ctx.message.guild.roles)
        if role not in ctx.message.author.roles:
            await ctx.send('Administrative priviledges are required.')
            return
        msg = await ctx.send('Reading warnList and writing history to globals')
        rf = open('samples/warnList','r')
        await msg.edit(content='Writing and running script...')
        _globals = globals()
        _locals = locals()
        exec(rf.read(),_globals,_locals)
        result = self.check(person,reason,ctx.message.author.name,_globals,_locals)
        await msg.edit(content='Writing changes...')
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
        await msg.edit(content=f'{ctx.message.author.mention} warned {person.mention}.\nReason: {reason}')
    @commands.command(name='rmwn',help='Remove a warning: /rmwn @person warnNumber')
    async def rmwn(self,ctx,person:discord.Member=None,*,num:int=0):
        if not person:
            await ctx.send('No member has been specified.')
            return
        role = discord.utils.find(lambda r: r.name == 'Administrators', ctx.message.guild.roles)
        if role not in ctx.message.author.roles:
            await ctx.send('Administrative priviledges are required.')
            return
        msg = await ctx.send('Reading warnList...')
        # try:
        rf = open('samples/warnList','r')
        _locals = locals()
        _globals = globals()
        exec(rf.read(),_globals,_locals)
        if (f'u{person.id}' not in _locals and f'u{person.id}' not in _globals) or _locals[f'u{person.id}']['count'] == 0:
            await msg.edit(content=f'Either {person.mention} is not a thing, or he/she does not have any warning.')
            rf.close()
            return
        await msg.edit(content='Checking file, writing changes...')
        if num==0:
            rf.close()
            delete_line_with_word('samples/warnList',f'u{person.id}')
            await msg.edit(content=f'Removed all warnings for {person.mention}')
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
        await msg.edit(content=f'Removed warning number {num} for {person.mention}\n')
        return
        # except Exception as e:
        #     await msg.edit(content='An error has occurred: ' + str(e))
        #     return
    @commands.command(name='chkwrn',aliases=['checkwarn','checkwarns','checkwarnings','ckwn'],help='Show warnings of member: /chkwrn @person [raw]')
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
            embed.set_author(name=ctx.message.author,icon_url=ctx.message.author.avatar_url)
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
            role = discord.utils.find(lambda r: r.name == 'Administrators', ctx.message.guild.roles)
            if role not in ctx.message.author.roles:
                await ctx.send(f'You don\'t have permissions to do so, {ctx.message.author.mention}!')
                return
            dm = await member.create_dm()
            await dm.send(f'You have been kicked.\nReason: {reason}')
            await ctx.send(f'{ctx.message.author.mention} has kicked {member.mention}.\nReason: {reason}')
            await member.ban()
            await member.unban()
            return
        except Exception as e:
            await ctx.send(f'Wut happened? {e}')
    @commands.command(name='ban',help='/ban @someone [reason]')
    async def ban(self,ctx,member:discord.Member=None,reason:str='Not specified'):
        try:
            if not member:
                await ctx.send('Please specify a member.')
                return
            role = discord.utils.find(lambda r: r.name == 'Administrators', ctx.message.guild.roles)
            if role not in ctx.message.author.roles:
                await ctx.send(f'You don\'t have permissions to do so, {ctx.message.author.mention}!')
                return
            dm = await member.create_dm()
            await dm.send(f'You have been banned.\nReason: {reason}')
            global id
            id = member.id
            await ctx.send(f'{ctx.message.author.mention} has banned {member.mention}.\nReason: {reason}')
            await member.ban()
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
        role = discord.utils.find(lambda r: r.name == 'Administrators', ctx.message.guild.roles)
        if role not in ctx.message.author.roles:
            await ctx.send(f'You don\'t have permissions to do so, {ctx.message.author.mention}!')
            return
        user = await self.bot.fetch_user(userID)
        await ctx.guild.unban(user)
        return





def setup(bot):
    bot.add_cog(manage(bot))