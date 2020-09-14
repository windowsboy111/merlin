from modules import keep_alive
import traceback
import os
import sys
import time
from dotenv import load_dotenv
load_dotenv(dotenv_path='.env')
os.system("python3 -m pip uninstall ddg chatterbot-voice -y && python3 -m pip install --requirement ../requirement.txt")


def main(port=8080, host="0.0.0.0"):
    t = keep_alive.async_run(port=port, host=host)
    try:
        import bot
        bot.start(os.getenv("DISCORD_TOKEN"), bot=True, reconnect=True)
    except Exception:
        print(traceback.format_exc())
        print('Retrying in 5 seconds...')
        time.sleep(5)
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
    print(end=" Trying to stop webserver...\r")
    t.cancel()
    print(" Waiting for it to finish...")
    while not t.cancelled():
        time.sleep(1)
    print(" HALTED")


if __name__ == '__main__':
    main()
