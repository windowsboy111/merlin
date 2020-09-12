import discord, json, traceback, sys, asyncio
from discord.ext import commands
from ext.const import SETFILE, LASTWRDFILE, STRFILE, fix_settings, get_prefix, cmdHdlLogger, log
import special
from ext import excepts
from modules.chat import chat
from datetime import datetime
from modules.consolemod import style


async def fix_set(bot: commands.Bot, message: discord.Message):
    settings = json.load(open(SETFILE, 'r'))
    try:
        # test if entry presents
        settings["cmdHdl"]['improveExp']
    except Exception:
        fix_settings(message.guild)  # fix guild settings


async def proc_cmd(bot: commands.Bot, message: discord.Message):
    settings = json.load(open(SETFILE, 'r'))
    if message.content.startswith(get_prefix(bot, message)) and message.channel.name != 'merlin-chat':
        msgtoSend = f'{message.author} has issued command: '
        print(msgtoSend + style.green + message.content + style.reset)
        cmdHdlLogger.info(msgtoSend + message.content)
        try:
            await log(message.channel.mention + ' ' + msgtoSend + '`' + message.content + '`', guild=message.channel.guild)
        except AttributeError:
            pass
        try:
            await bot.process_commands(message)
            if settings[f'g{message.guild.id}']["cmdHdl"]["delIssue"]:
                await message.delete()
            return 0
        except discord.ext.commands.errors.CommandNotFound:
            pass
        except discord.errors.NotFound:
            pass
        except Exception:
            await message.channel.send(f'{message.author.mention}, there was an error trying to execute that command! :(')
            print(traceback.format_exc())


async def save_quote(bot: commands.Bot, message: discord.Message):
    lastword = json.load(open(LASTWRDFILE, 'r'))
    try:
        lastword[f'g{message.guild.id}'][str(message.author.id)] = message.id
    except Exception:
        lastword[f'g{message.guild.id}'] = {message.author.id: message.id}
    json.dump(lastword, open(LASTWRDFILE, 'w'))


async def chat_hdl(bot: commands.Bot, message: discord.Message):
    settings = json.load(open(SETFILE, 'r'))
    if not isinstance(message.channel, discord.DMChannel) and message.channel.name == 'merlin-chat' and not message.author.bot:
        await chat.response(message)
        return 0
    elif not isinstance(message.channel, discord.DMChannel) and not message.author.bot and settings[f'g{message.guild.id}']["cmdHdl"]["improveExp"]:
        msgs = await message.channel.history(limit=2).flatten()
        await chat.save(message.content, msgs[1].content)


def setup(bot: commands.Bot):
    @bot.event
    async def on_message(message: discord.Message):
        # run pre-cmd hooks
        if await special.pre_on_message(message):
            return 0
        await fix_set(bot, message)
        await asyncio.gather(save_quote(bot, message), proc_cmd(bot, message), chat_hdl(bot, message))
        await special.post_on_message(message) # run post-cmd hooks


    @bot.event
    async def on_command_error(ctx, error):
        settings = json.load(open(SETFILE, 'r'))
        stringTable = json.load(open(STRFILE, 'r'))
        try:
            raise error
        except Exception:
            # This tells the issuer that the command cannot be used in DM
            if isinstance(error, commands.errors.NoPrivateMessage):
                try:
                    await ctx.author.send(f':x::lock: {ctx.command} cannot be used in Private Messages.')
                    return 3
                except discord.HTTPException:
                    return 3
            # This prevents any commands with local handlers being handled here in on_command_error.

            # This prevents any cogs with an overwritten cog_command_error being handled here.
            if ctx.cog and ctx.cog._get_overridden_method(ctx.cog.cog_command_error) is not None:
                return

            # Anything in ignored will return and prevent anything happening.
            if isinstance(error, commands.errors.CommandNotFound):
                try:
                    if settings[f'g{ctx.guild.id}']['cmdHdl']['cmdNotFound']:
                        await ctx.send(":interrobang: Welp, I've no idea. Command not found!")
                except KeyError:
                    await ctx.send(":interrobang: :two: :x:\n<:err:740034702743830549> Command not found!\n<:warn:739838316374917171> something went wrong, please run `/settings`")
                return 2
            if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
                return await ctx.invoke(bot.get_command('help'), cmdName=ctx.command.qualified_name)

            if isinstance(error, commands.errors.DisabledCommand):
                return await ctx.send(embed=discord.Embed(
                    title=f':no_entry: {ctx.command} has been disabled.',
                    description=f':x: `{ctx.message.content}`',
                    color=0xff0000
                ))

            if isinstance(error, excepts.NotMod):
                await ctx.send(f"`{ctx.author} is not in the sudoers file.  This incident will be reported.`")

            if hasattr(ctx.command, 'on_error'):
                return

            if isinstance(error, commands.errors.CommandInvokeError):
                await ctx.send(embed=discord.Embed(
                    title='<:err:740034702743830549> uh oh. An exception has occurred during the execution of the command',
                    description=stringTable['CommandInvokeError'].format(
                        content=ctx.message.content),
                    timestamp=datetime.utcnow(),
                    color=0xff0000
                ))

            if isinstance(error, commands.errors.NotOwner):
                await ctx.send(stringTable['notOwner'])
                return 6
            if isinstance(error, commands.errors.ConversionError):
                await ctx.send(
                    ':bangbang: Hey bud, seems like you tried to input some invalid type of arguments to the command call!\n'
                    'Either CoNsUlT a PsYcHiAtRiSt or check the usage. Please!')
                return 4

            if isinstance(error, commands.errors.BadArgument):
                await ctx.send(
                    ':grey_question: Whoops. The discord special expression you have specified when issuing that command is invalid.'
                    ':mag: This error occurrs usually because of the bot fails to find the object.')
                return 4
            if isinstance(error, excepts.NotMod):
                return await ctx.send(str(error))

            # All other Errors not returned come here. And we can just print the default TraceBack.
            print(f"{style.red2}Ignoring exception in command {ctx.message.content}:\n{style.red}{traceback.format_exc()}{style.reset}", file=sys.stderr)
            await log(f'Ignoring exception in command `{ctx.message.content}`:\n\n```{str(traceback.format_exc())}\n```', guild=ctx.guild)
            return 1
