#import os
# os.system('pip install python-dotenv mcstatus flask discord.py Naked')
import keep_alive,threading
from time import sleep
def a():
    while True:
        print(end="")
        sleep(300)
t = threading.Thread(target=a)
t.start()
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