import discord


async def easter(message: discord.Message):
    msg = str(message.content)
    if msg.lower().startswith('/recursion'):
        await message.channel.send(f'{message.author.mention}, command `{message.content}` not found!\nTry `$recursion`.')
        return True
    if msg.lower().startswith('/warn ') and msg.lower().endswith(' stupid'):
        await message.channel.send(f'YES STUPID WARN IT, IT DESERVES A WARN, IT\'S SO SO STUPID!')
        return False
    if msg.lower().startswith('/stupid'):
        await message.channel.send(f'YES YOU ARE STUPID, HOW STUPID YOU ARE')
        return False
    if msg.lower().startswith('/hello, world'):
        await message.channel.send(f'How could you found this?')
        return False
    if msg.lower().startswith('/whatis stupid benz'):
        await message.channel.send(f'What is Stupid Benz, Why you ask me? Ask Stupid Benz, ||Because Stupid Benz is **STUPID**||')
        return False
    return False
