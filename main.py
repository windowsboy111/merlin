import keep_alive
import traceback
import os
import sys
import time
os.system("pip3 install chatterbot==0.8.7 discord.py flask mcstatus pytablemaker python-dotenv numpy pyparsing==2.4.7 numpy packaging")


def main(port=8080, host="0.0.0.0"):
    try:
        keep_alive.keep_alive(port=port, host=host)
    except Exception:
        print(traceback.format_exc())
        print('Retrying in 5 seconds...')
        from dotenv import load_dotenv
        load_dotenv('.env')
        time.sleep(5)
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
    try:
        import bot
        bot.start(bot=True, reconnect=True)
    except Exception:
        print(traceback.format_exc())
        print('Retrying in 5 seconds...')
        time.sleep(5)
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)


if __name__ == '__main__':
    main()
