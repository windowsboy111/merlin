import discord
async def easter(message:discord.Message):
    msg = str(message.content)
    if msg.lower().startswith('/recursion'):
        await message.channel.send(f'{message.author.mention}, command `{message.content}` not found!\nTry `$recursion`.')
        return True
    if msg.lower().startswith('/warn ') and msg.lower().endswith(' stupid'):
        await message.channel.send(f'YES STUPID WARN IT, IT DESERVES A WARN, IT\'S SO SO STUPID!')
        return False
    return False