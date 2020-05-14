#import os
# os.system('pip install python-dotenv mcstatus flask discord.py Naked')
import keep_alive
from time import sleep
try:
  keep_alive.keep_alive()
except Exception as e:
  print(e)
try:
  import bot
except Exception as e:
  print(e)
  while True:
    print(e)
    sleep(5)
    import bot