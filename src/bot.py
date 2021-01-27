#!/bin/python3.8
"""
Merlin discord bot.
Startup script.

Copyright windowsboy111 2020 MIT license
https://github.com/windowsboy111/merlin-py
discord.py -- the main module. In fact the main scr.
"""
import os
import sys
import types
from dotenv import load_dotenv
from merlin import Bot, asyncio, discord, commands, root_logger
sys.path.append(os.path.dirname(__file__)) # add this directory to the sys path
# initialize runtime variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = Bot()

@bot.command(name='help', help='Shows this message', aliases=['?', 'cmd', 'cmds', 'commands', 'command'])
async def cmd_help(ctx, *, cmdName: str = ""):
    """The Merlin help command."""
    settings = bot.db['sets']
    prefix = ctx.prefix
    # check if user wants help for global cog
    if cmdName.lower() == "global":
        e = discord.Embed(title='Command list', description='wd: `/`', color=0x0000ff)
        for cmd in bot.walk_commands():
            e.add_field(name=cmd.name, value=cmd.short_doc or "<no help>")
        return await ctx.send(embed=e)
    # check if user wants help for a cog
    for cogName, cog in bot.cogs.items():
        if cogName.lower() == cmdName.lower():
            e = discord.Embed(title='Command list', description=f'wd: `/{cog.qualified_name}`')
            for cmd in cog.walk_commands():
                e.add_field(name=cmd.name, value=cmd.short_doc or "<no help>")
            return await ctx.send(embed=e)
    # show help for command
    if cmdName:
        command = bot.get_command(cmdName)
        if not command or command.hidden: return await ctx.send(':mag: Command not found, please try again.')
        path = "/" + (command.cog.qualified_name if command.cog else "None") + "/" + "/".join(command.full_parent_name.split(" "))
        e = discord.Embed(title=f'Command `{prefix}' + command.qualified_name + '`', description=(path + '\n' + command.description or "<no description>"),color=0x0000ff)
        usage = prefix + command.qualified_name + ' '
        for key, val in command.clean_params.items():
            if val.default:
                usage += f'<{val.name}>'
            else:
                usage += f'<[{val.name}]>'
            usage += ' '
        e.add_field(name='Objective',   value=command.help)
        e.add_field(name='Usage',       value=usage)
        e.add_field(name='Cog',         value="<No cog>" if not command.cog else command.cog.qualified_name)
        e.add_field(name='Aliases',     value=', '.join(command.aliases) or "<No aliases>")
        if hasattr(command, 'commands'):    # it is a group
            e.add_field(name='Sub-Commands', value=''.join([f"`{prefix}{cmd.qualified_name}`: {cmd.short_doc}\n" for cmd in command.commands]))
        await ctx.send(embed=e)
        return
    # no command name supplied, list all cogs
    e = discord.Embed(title="Cogs list")
    for _, cog in bot.cogs.items():
        e.add_field(name=cog.qualified_name, value=cog.description or "<no description>")
    await ctx.send(embed=e)
bot.cmd_help = types.MethodType(cmd_help, bot)

async def main():
    """Main coro. Run this."""
    async with bot:
        bot.MODE = os.getenv('MODE')
        await bot.start(TOKEN)


if __name__ == "__main__":
    loop = bot.loop
    task = loop.create_task(main())
    loop.run_until_complete(task)
