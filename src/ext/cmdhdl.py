"""
Message and command handling discord.py extension.

Command processing, command invoking, error handling, and partial command support here.
"""
import json
import warnings
import traceback
import asyncio
import discord
from discord.ext import commands
from ext import excepts
from ext.const import SETFILE, LASTWRDFILE, STRFILE, get_prefix, cmdHdlLogger
from modules.chat import chat
from modules.consolemod import style
from modules.tools import wrdssep
import merlin
import special
BOT = None


async def get_cur_prefix(message):
    settings = json.load(open(SETFILE, 'r'))
    prefix = e = None
    prefixes = settings[f"g{message.guild.id}"]["prefix"]
    for p in prefixes:
        if message.content.startswith(p):
            prefix = p
            break
    return prefix


async def proc_cmd(message: discord.Message):
    """
    Process commands.

    Check if it is a valid command, then
    log and invoke it.
    """
    if message.channel.name == 'merlin-chat':
        return
    prefix = None
    prefixes = await BOT.get_prefix(message)
    for p in prefixes:
        if message.content.startswith(p):
            prefix = p
            break
    if prefix is None:
        return  # not a cmd
    with warnings.catch_warnings(record=True) as w:
        cmd = BOT.get_command(message.content[len(prefix):], last_gud=True)
        if len(w) == 1:
            # if issubclass(w[-1].category, excepts.AmbiguousSearchQuery):
            #     return await message.channel.send(w[-1].message)
            await message.channel.send(w[-1].message)
        if cmd is None:
            return  # not a cmd
        cmdHdlLogger.info(f'{message.author} has issued command: {message.content}')
        try:
            await BOT.netLogger(f"{message.channel.mention} {message.author} has issued command: `{message.content}`", guild=message.guild)
        except AttributeError:  # DM
            pass
        try:
            ctx = await BOT.get_context(message)
            await BOT.invoke(ctx)
            if BOT.db['sets'][f'g{message.guild.id}']["cmdHdl"]["delIssue"]:
                await message.delete()
            return 0
        except (discord.ext.commands.errors.CommandNotFound, discord.errors.NotFound):
            pass
        except Exception:
            await message.add_reaction("❌")
            cmdHdlLogger.debug(traceback.format_exc(limit=5))


async def save_quote(bot: merlin.Bot, message: discord.Message):
    lastword = bot.db['lastwrds']
    try:
        lastword[f'g{message.guild.id}'][str(message.author.id)] = message.id
    except KeyError:
        lastword[f'g{message.guild.id}'] = {message.author.id: message.id}


async def chat_hdl(bot: merlin.Bot, message: discord.Message):
    settings = bot.db['sets']
    chatChannelID = settings[f'g{message.guild.id}']['chatChannel']
    if not isinstance(message.channel, discord.DMChannel) and (message.channel.id == chatChannelID) and not message.author.bot:
        await chat.response(bot, message)
    elif not isinstance(message.channel, discord.DMChannel) and not message.author.bot and settings[f'g{message.guild.id}']["cmdHdl"]["improveExp"]:
        msgs = await message.channel.history(limit=2).flatten()
        await asyncio.gather(chat.save(message.content, msgs[1].content))


# discord extension
def setup(bot: merlin.Bot):
    """Ext setup."""
    global BOT
    BOT = bot

    @bot.event
    async def on_message(message: discord.Message):
        # run pre-cmd hooks
        if await special.pre_on_message(message):
            return 0
        # gather and run in parallel (nowait)
        await asyncio.gather(save_quote(bot, message), proc_cmd(message), chat_hdl(bot, message))
        await special.post_on_message(message)   # set fn for callback when done

    @bot.event
    async def on_command_error(ctx, e):
        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return
        # This prevents any cogs with an overwritten cog_command_error being handled here.
        if ctx.cog and ctx.cog._get_overridden_method(ctx.cog.cog_command_error) is not None:
            return
        err_code = await BOT.errhdl_g(ctx, e)
        if err_code:
            await BOT.netLogger(f"FAIL {err_code}: `{ctx.message.content}`", ctx.guild)
