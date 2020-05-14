from discord.ext import commands
from logcfg import logger
from quickpoll import QuickPoll as qp
import discord,os,table
verbose=True
async def output(message,msg:discord.Message=None,ctx=None,dcmsg=True):
    print(message)
    logger.info(message)
    if verbose and dcmsg:
        if msg:
            await msg.edit(content=message)
        else:
            return ctx.send(message)

class utils(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    @commands.command(pass_context=True, help='Tells you the ping from discord to the bot', name='ping')
    async def ping(self,ctx):
        await ctx.send(embed=discord.Embed(title="Pong!", description='The latency is {} ms.'.format(self.bot.latency*1000), color=0x3333ff))
    @commands.command(name='msgstats',help='info of a message')
    async def msgstats(self,ctx,*,args=''):
        await ctx.send(f'args: {args}\nLength: {len(args)}')
    @commands.group(pass_context=True,help="/help vote",aliases=['poll','voting'],name='vote')
    async def vote(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f"2 bed idk wat u r toking 'bout, but wut?")
            return
    @vote.command(name='create',help='Create a vote: /vote create <name> <choices>',aliases=['make','mk','new'])
    async def create(self,ctx,name='',*options: str):
        if name=='':
            await ctx.send('Bruh, wuts da title of the poll?')
            return
        msg = await ctx.send('Once apon a time, there was a poll, that YOU SHOULDN\'T SEE DIS MESSAGE! OR ELSE DISCORD IS LAGGY!')
        poll = qp(self.bot)
        await poll.quickpoll(poll,msg=msg,ctx=ctx,question=name,options=options)
        await msg.edit(content='')
        return
    @vote.command(name='end',help='End a vote: /vote end <id>')
    async def end(self,ctx,*,id=0,id2=0):
        msg = await ctx.send('deleting `system32`...')
        if id==0:
            await msg.edit('bruh i need da poll id')
            return
        poll = qp(self.bot)
        await poll.tally(poll,msg=msg,ctx=ctx,id=id)
        await msg.edit(content='')
        return


    @commands.group(pass_context=True,help='create, show, edit tables.',name='table')
    async def table(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f"2 bed idk wat u r toking 'bout, but wut?")
            return
    @table.command(name='make',aliases=['new','create','mk'],help='create new table.  /table create tabletype tablename')
    async def make(self,ctx,ttype=None,*,name:str='table'):
        msg = await ctx.send('Writing script...')
        if not ttype:
            await msg.edit(content='Possible type of table: modernTable, classicTable, onelineTable.')
            return
        try:
            scr = f'def gettable():\n\timport table\n\t{name} = table.{ttype}()\n'
            f = open(f'samples/table_{name}.py','w+')
            f.write(scr)
            f.close()
            await msg.edit(content='Operation completed successfully.')
            return
        except Exception as e:
            await msg.edit(content=f'Task failed successfully.\nError message: {e}')
    @table.command(name='insert',help='insert rows to table.  /table insert tablename content1 content2 content3...')
    async def insert(self,ctx,name:str='table',*,content=None):
        msg = await ctx.send('Writing script...')
        if not content:
            await msg.edit(content='Bruh, content?')
            return
        try:
            if not os.path.exists(f'samples/table_{name}.py'):
                await msg.edit(content='Operashun terminated.  Table has not been created yet.')
                return
            rs = '\''
            a = content.split(',')
            tmp = "','"
            rs += tmp.join(a)
            rs += "'"
            content = rs
            scr = f'\t{name}.insert({content})\n'
            f = open(f'samples/table_{name}.py','a')
            f.write(scr)
            f.close()
            await msg.edit(content='Operation completed successfully.')
            return
        except Exception as e:
            await msg.edit(content=f'Task failed successfully.\nError message: {e}')
    @table.group(name='column',help='column methods.  possible args: create,delete,rename,moveToEnd',pass_context=True)
    async def column(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f'2 bed idk wat u r toking \'bout, but wut?')
            return
    @column.command(name='add',help='add a column.  /table column add tablename identity name', aliases=['create','make','mk'])
    async def add(self,ctx,table=None,identity=None,name=None):
        msg = await ctx.send('Writing script...')
        if not table or not identity or not name:
            await msg.edit(content="I nEeD aRgUmEnTs! `/help table column add`")
            return
        try:
            if not os.path.exists(f'samples/table_{table}.py'):
                await msg.edit(content='Operashun terminated.  Table has not been created yet.')
                return
            scr = f'\t{identity} = {table}.new_column("{name}")\n'
            f = open(f'samples/table_{table}.py','a')
            f.write(scr)
            f.close()
            await msg.edit(content='Operation completed successfully.')
            return
        except Exception as e:
            await msg.edit(content=f'Task failed successfully.\nError message: {e}')
    @column.command(name='delete',aliases=['rm','remove','del'],help='Delete a column: /table column delete tablename identity')
    async def delete(self,ctx,table=None,identity=None):
        msg = await ctx.send('Writing script...')
        if not table or not identity:
            await msg.edit(content='CMON!!!`/help table column del`')
            return
        try:
            if not os.path.exists(f'samples/table_{table}.py'):
                await msg.edit(content='Operashun terminated.  Table has not been created yet.')
                return
            scr = f'\t{identity}.delete()\n'
            f = open(f'samples/table_{table}.py','a')
            f.write(scr)
            f.close()
            await msg.edit(content='Operation completed successfully.')
            return
        except Exception as e:
            await msg.edit(content=f'Task failed successfully.\nError message: {e}')
    @column.command(name='rename',aliases=['ren'],help='Rename a column: /table column rename tablename identity newname')
    async def rename(self,ctx,table,identity,*,newname):
        msg = await ctx.send('Writing script...')
        if not table or not identity or not newname:
            await msg.edit(content='Tell me how to rename a column without tablename, id, or a new name. `/help table column rename`')
            return
        try:
            if not os.path.exists(f'samples/table_{table}.py'):
                await msg.edit(content='Operashun terminated.  Table has not been created yet.')
                return
            scr = f'\t{identity}.rename("{newname}")\n'
            f = open(f'samples/table_{table}.py','a')
            f.write(scr)
            f.close()
            await msg.edit(content='Operation completed successfully.')
            return
        except Exception as e:
            await msg.edit(content=f'Task failed successfully.\nError message: {e}')
    @column.command(name='moveToEnd',aliases=['mv','move','mte'],help='Move a column to rhs: /table column mte tablename identity')
    async def moveToEnd(self,ctx,table=None,identity=None):
        msg = await ctx.send('Writing script...')
        if not table or not identity:
            msg.edit(content='Aha! Moving a null column to the end! `/help column mte`')
            return
        try:
            if not os.path.exists(f'samples/table_{table}.py'):
                await msg.edit(content='Operashun terminated.  Table has not been created yet.')
                return
            scr = f'\t{identity}.moveToEnd()\n'
            f = open(f'samples/table_{table}.py','a')
            f.write(scr)
            f.close()
            await msg.edit(content='Operation completed successfully.')
            return
        except Exception as e:
            await msg.edit(content=f'Task failed successfully.\nError message: {e}')
    @table.command(name='show',aliases=['get'],help='Show the table: /table show tablename')
    async def show(self,ctx,table=None):
        msg = await ctx.send('Writing script...')
        if not table:
            await msg.edit(content='PLEASE SEEK HELP `/help table show`')
            return
        try:
            if not os.path.exists(f'samples/table_{table}.py'):
                await msg.edit(content='Operashun terminated.  Table has not been created yet.')
                return
            scr = f'\treturn {table}.get()\n'
            f = open(f'samples/table_{table}.py','r')
            await output('Executing script...',msg=msg)
            _locals = locals()
            exec(f.read() + scr,globals(),_locals)
            ans = _locals['gettable']()
            await ctx.send('```css\n' + ans + '```   ')
            f.close()
            await output('Operation completed successfully.',msg=msg)
            return
        except Exception as e:
            await output(f'Task failed successfully.\nError message: {e}',msg=msg)
    @table.command(name='drop',help='Delete a table completely: /table drop tablename')
    async def drop(self,ctx,table=None):
        msg = await ctx.send('Deleting script...')
        if not table:
            msg.edit(content='idk table. `/help table drop`')
            return
        try:
            if not os.path.exists(f'samples/table_{table}.py'):
                await msg.edit(content='Operashun terminated.  Table does not exist anymore.')
                return
            os.remove(f'samples/table_{table}.py')
            await msg.edit(content='Operation completed successfully.')
            return
        except Exception as e:
            await msg.edit(content=f'Task failed successfully.\nError message: {e}')


def setup(bot):
    bot.add_cog(utils(bot))