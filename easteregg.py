# This is a template for your eastereggs
# This is not the real easter egg in the repl.it version of Merlin
# It only exists or else the code will not run correctly
import discord

async def easter(message: discord.Message):
    """
	The easter egg function that will ran in on_message()  
	If you want the command to invoke, return False.
	If you want to stop everything after the easter egg, return True.
	This will prevents invoking the command, spam checking, etc.
	"""
	msg = message.content
	if msg.startswith("I need easter egg!"):
		# An example, if the message starts with the string it will run the following code
		await message.channel.send("There you go. Have fun.")
		return True # if it is True, on_message will return after running this easter egg
	return False # remember to add this line at the end!
