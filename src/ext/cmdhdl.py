"""
This file is a discord extension. Load it on startup (both pre and post is okay).
Contains command handling
"""
import discord
import asyncio
from discord.ext import commands
from modules.chat import chat
import special
from ext.const import SETFILE, STRFILE, LASTWRDFILE, get_prefix, style, cmdHdlLogger, log
from datetime import datetime
from ext import excepts
import traceback
import json


# ---------
# background tasks
async def update():
    global stringTable, lastword
    lastword, stringTable = json.load(
        open(LASTWRDFILE, 'r')), json.load(open(STRFILE, 'r'))
    # settings.update(json.load(open(SETFILE, 'r')))
    # json.dump(settings, open(SETFILE, 'w'))


async def task_update():
    await update()
    await asyncio.sleep(60)


def set_on_message(bot: commands.Bot):
    async def on_message(message: discord.Message):
        lastword = json.load(open(LASTWRDFILE, 'r'))
        if await special.pre_on_message(message):
            return
        try:
            lastword[f'g{message.guild.id}'][str(message.author.id)] = message.id
        except Exception:
            lastword[f'g{message.guild.id}'] = {message.author.id: message.id}
        if not isinstance(message.channel, discord.DMChannel) and message.channel.name == 'merlin-chat' and not message.author.bot:
            async with message.channel.typing():
                await message.channel.send(chat.response(message.content))
            return 0
        await update()
        if message.content.startswith(get_prefix(bot, message)):
            msgtoSend = f'{message.author} has issued command: '
            print(msgtoSend + style.green + message.content + style.reset)
            cmdHdlLogger.info(msgtoSend + message.content)
            try:
                await log(message.channel.mention + ' ' + msgtoSend + '`' + message.content + '`', guild=message.channel.guild)
            except AttributeError:
                pass
            try:
                await bot.process_commands(message)
                return 0
            except discord.ext.commands.errors.CommandNotFound:
                pass
            except discord.errors.NotFound:
                pass
            except Exception:
                await message.channel.send(f'{message.author.mention}, there was an error trying to execute that command! :(')
                print(traceback.format_exc())
        await special.post_on_message(message)
    return on_message


def set_on_cmd_err(bot: commands.Bot):
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
            if hasattr(ctx.command, 'on_error'):
                return

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
            await log(f'Ignoring exception in command {ctx.message.content}:' + '\n\n```' + str(traceback.format_exc()) + '\n```', guild=ctx.guild)
            return 1
    return on_command_error


def setup(bot: commands.Bot):
    bot.loop.create_task(task_update())
    bot.event(set_on_cmd_err(bot))