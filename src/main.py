from modules import keep_alive
import traceback
import os
import sys
import time
from dotenv import load_dotenv
load_dotenv(dotenv_path='.env')
# os.system("pip3 install chatterbot==0.8.7 discord.py flask mcstatus pytablemaker python-dotenv numpy pyparsing==2.4.7 numpy packaging duckduckgo3 && pip3 uninstall ddg -y")


def main(port=8080, host="0.0.0.0"):
    t = keep_alive.keep_alive(port=port, host=host)
    try:
        import bot
        bot.start(os.getenv("DISCORD_TOKEN"), bot=True, reconnect=True)
    except Exception:
        print(traceback.format_exc())
        print('Retrying in 5 seconds...')
        time.sleep(5)
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
    print(end=" Trying to stop webserver...\r")
    t._stop()
    print(" Waiting for it to finish...")
    t.join()


if __name__ == '__main__':
    main()
