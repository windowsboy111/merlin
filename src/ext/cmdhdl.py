"""
Message and command handling discord.py extension.

Command processing, command invoking, error handling, and partial command support here.
"""
import json
import traceback
import asyncio
import discord
from discord.ext import commands
from ext import excepts
from ext.const import SETFILE, LASTWRDFILE, STRFILE, fix_settings, get_prefix, cmdHdlLogger, log
from ext.errhdl import errhdl_g
from modules.chat import chat
from modules.consolemod import style
from modules.tools import wrdssep
import special
BOT = None


async def init(bot: commands.Bot):
    # lastword
    try:
        json.load(open(LASTWRDFILE, 'r'))
    except json.JSONDecodeError:
        open(LASTWRDFILE, 'w').write("{}")


async def fix_set(bot: commands.Bot, message: discord.Message):
    settings = json.load(open(SETFILE, 'r'))
    try:
        # test if entry presents
        settings["cmdHdl"]['improveExp']
    except Exception:
        fix_settings(message.guild)  # fix guild settings


async def get_cur_prefix(message):
    settings = json.load(open(SETFILE, 'r'))
    prefix = e = None
    prefixes = settings[f"g{message.guild.id}"]["prefix"]
    for p in prefixes:
        if message.content.startswith(p):
            prefix = p
            break
    return prefix


async def sel_cmd(message: discord.Message):
    msg = message.content
    prefix = await get_cur_prefix(message)
    if not prefix:
        return None
    cmd = BOT.get_command(message.content[len(prefix):])
    if cmd:
        return cmd  # literal cmd name, got found instantly ay
    # then do stuff
    return None


async def proc_cmd(message: discord.Message):
    """
    Process commands.

    Check if it is a valid command, then
    log and invoke it.
    """
    settings = json.load(open(SETFILE, 'r'))
    if message.channel.name == 'merlin-chat':
        return
    cmd = sel_cmd(message)
    if cmd is None:
        return  # not a cmd
    print(f'{message.author} has issued command: {style.green}{message.content}{style.reset}')
    cmdHdlLogger.info(f'{message.author} has issued command: {message.content}')
    try:
        await log(f"{message.channel.mention} {message.author} has issued command: `{message.content}`", guild=message.guild)
    except AttributeError:  # DM
        pass
    try:
        ctx = await bot.get_context(message)
        await ctx.invoke()
        if settings[f'g{message.guild.id}']["cmdHdl"]["delIssue"]:
            await message.delete()
        return 0
    except (discord.ext.commands.errors.CommandNotFound, discord.errors.NotFound):
        pass
    except Exception:
        await message.add_reaction("❌")
        traceback.print_exc(limit=5)


async def save_quote(bot: commands.Bot, message: discord.Message):
    lastword = json.load(open(LASTWRDFILE, 'r'))
    try:
        lastword[f'g{message.guild.id}'][str(message.author.id)] = message.id
    except KeyError:
        lastword[f'g{message.guild.id}'] = {message.author.id: message.id}
    json.dump(lastword, open(LASTWRDFILE, 'w'))


async def chat_hdl(bot: commands.Bot, message: discord.Message):
    settings = json.load(open(SETFILE, 'r'))
    if not isinstance(message.channel, discord.DMChannel) and message.channel.name == 'merlin-chat' and not message.author.bot:
        res, chatbot = await chat.response(message)
        await message.channel.send(res)
    elif not isinstance(message.channel, discord.DMChannel) and not message.author.bot and settings[f'g{message.guild.id}']["cmdHdl"]["improveExp"]:
        msgs = await message.channel.history(limit=2).flatten()
        await asyncio.gather(chat.save(message.content, msgs[1].content))


# discord extension
def setup(bot: commands.Bot):
    """Ext setup."""
    BOT = bot
    bot.loop.create_task(init(bot))  # init chk

    @bot.event
    async def on_message(message: discord.Message):
        # run pre-cmd hooks
        if await special.pre_on_message(message):
            return 0
        # check if settings works
        await fix_set(bot, message)
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
        err_code = await errhdl_g(ctx, e)
        await log(f"FAIL {err_code}: `{ctx.message.content}`", ctx.guild)
