import discord
from discord.ext import commands
from datetime import datetime
import traceback
import psutil
import os
SANDBOX_TRACEBACK = 'samples/traceback.sndbx'


class Debug(commands.Cog):
    """\
    Type: discord.ext.commands.Cog  
    Most of the debug commands are stored in this cog  
    Load this extension as an external file with `client.load_extension('cogs.debug')`
    ---
    This cog contains:  
    ## Commands
    - ping
    - msgstats
    - sandbox
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(pass_context=True, help='Tells you the ping from discord to the bot', name='ping')
    async def ping(self, ctx: commands.Context):
        t = datetime.now()
        msg = await ctx.send('`Ping!`')
        sendTime = datetime.now() - t
        t = datetime.now()
        await msg.edit(content='`Pong!`')
        editTime = datetime.now() - t
        t = datetime.now()
        await msg.delete()
        delTime = datetime.now() - t
        await ctx.send(
            embed=discord.Embed(title=':ping_pong: Pong!')
            .add_field(name='Bot Latency', value=f"{self.bot.latency * 1000}ms")
            .add_field(name='Send Message', value=f"{sendTime.total_seconds() * 1000}ms")
            .add_field(name="Edit Message", value=f"{editTime.total_seconds() * 1000}ms")
            .add_field(name="Del Message", value=f"{delTime.total_seconds() * 1000}ms")
        )

    @commands.command(name='sandbox', help='check if a command runs properly')
    async def sandbox(self, ctx, *, commandName: str):
        command = None
        ret = None
        startTime = None
        errorCode = int()
        try:
            command = self.bot.get_command(commandName)
            if command is None:
                await ctx.send(f"msh: command not found: `{commandName}`")
                return 3
            startTime = datetime.now()  
            ret = await ctx.invoke(command)
        except Exception as err:
            timeElapsed = datetime.now() - startTime
            e = discord.Embed(title='Task Failed Succefully', description=f":x: `{ctx.message.content.split()[0][:-7]}{commandName}`", color=0xff0000)
            e.add_field(name='command name', value=command.qualified_name)
            e.add_field(name='time used', value=timeElapsed)
            try:
                errorCode = str(int(ret))
            except Exception:
                try:
                    errorCode = str(ret)
                except Exception:
                    errorCode = str("return value cannot be converted to string")
            e.add_field(name='Return value', value=errorCode)
            e.add_field(name='Error type', value=type(err).__name__)
            e.add_field(name='Error message', value=str(err))
            e.timestamp = datetime.utcnow()
            with open(SANDBOX_TRACEBACK, 'w') as f:
                f.write(traceback.format_exc())
            await ctx.send(embed=e, file=discord.File(open(SANDBOX_TRACEBACK, 'r'), 'traceback.txt'))
            return 0
        timeElapsed = datetime.now() - startTime
        e = discord.Embed(title='the command runs without any error!', description=f":white_check_mark: `{ctx.message.content.split()[0][:-7]}{commandName}`", color=0x00ff00)
        e.add_field(name='command name', value=command.qualified_name)
        e.add_field(name='time used', value=timeElapsed)
        try:
            errorCode = str(int(ret))
        except Exception:
            try:
                errorCode = str(ret)
            except Exception:
                errorCode = str("return value cannot be converted to string")
        e.add_field(name='Return value', value=errorCode)
        e.timestamp = datetime.utcnow()
        await ctx.send(embed=e)

    @commands.command(name='resources', help='show cpu, ram usages etc', aliases=['usage', 'res'])
    async def res(self, ctx):
        proc = psutil.Process(os.getpid())
        embed = discord.Embed(title='Bot Resources usage', color=0xff8700)
        embed.add_field(name='CPU Usage', value=f"```{proc.cpu_percent()}%```")
        embed.add_field(name='Used RAM', value=f"```{round(psutil.virtual_memory().used // 1048576)} MiB / "
                                               f"{round(psutil.virtual_memory().total // 1048576)} MiB ║ "
                                               f"proc {proc.memory_percent()}%```")
        cpu = psutil.cpu_stats()
        freq = psutil.cpu_freq()
        proc.memory_full_info()
        embed.add_field(name=f'{psutil.cpu_count()} CPUs', value=f'```{cpu.syscalls} Syscalls | {round(cpu.ctx_switches // 1000000)}M Switches```')
        embed.add_field(name=f'CPU Interrupts', value=f"```{round(cpu.interrupts // 1000000)}M ({round(cpu.soft_interrupts // 1000000)}M soft)```")
        embed.add_field(name=f'CPU Frequency', value=f"```Currently {round(freq.current)}Mhz | Max {round(freq.max)}Mhz | Mix {round(freq.min)}Mhz```")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Debug(bot))
