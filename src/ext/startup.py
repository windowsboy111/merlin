import os, sys
sys.path.append(os.path.dirname(__file__)) # add this directory to the sys path
with open(f'{os.path.dirname(__file__)}/../discordbot.log', 'w+') as log:
    log.write('')
    log.close()
print("Merlin bot written in python by windowsboy111 :)")
print('==> Importing libraries...')