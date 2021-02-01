from modules import keep_alive
import traceback
import asyncio
import os
import sys
import time
from dotenv import load_dotenv
load_dotenv(dotenv_path='.env')
os.system("python3 -m pip uninstall ddg chatterbot-voice -y && python3 -m pip install --requirement ../requirement.txt")


def main(port=8080, host="0.0.0.0"):
    p = keep_alive.start(port=port, host=host)
    try:
        import bot
        bot.bot.MODE = os.getenv('MODE')
        bot.bot.run(os.getenv("DISCORD_TOKEN"), bot=True, reconnect=True)
    except Exception:
        print(traceback.format_exc())
        print('Retrying in 5 seconds...')
        time.sleep(5)
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
    print(end=" Trying to stop webserver...\r")
    p.terminate()
    p.join()
    print(" HALTED")


if __name__ == '__main__':
    main()
