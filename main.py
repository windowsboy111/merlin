import keep_alive
import traceback
import os
import sys
import time
from dotenv import load_dotenv
load_dotenv(dotenv_path='.env')


def main(port=8080, host="0.0.0.0"):
    try:
        keep_alive.keep_alive(port=port, host=host)
    except Exception:
        os.system(
            "pip3 install chatterbot==0.8.7 discord.py flask mcstatus pytablemaker python-dotenv pyparsing==2.4.7 numpy packaging psutil"
        )
        print(traceback.format_exc())
        print('Retrying in 5 seconds...')
        time.sleep(5)
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)

    try:
        import bot
        bot.start(os.getenv("DISCORD_TOKEN"), bot=True, reconnect=True)
    except Exception:
        print(traceback.format_exc())
        print('Retrying in 5 seconds...')
        time.sleep(5)
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)


if __name__ == '__main__':
    main()
