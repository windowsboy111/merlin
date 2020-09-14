from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
import chatterbot
import chatterbot.response_selection
import os
import threading
import time
import multiprocessing as mp
import asyncio
import discord
doTrain = False
reTrain = False
from chatterbot.conversation import Statement
# more_label = None
# more_data = None
# if an error occurred try this: https://blog.csdn.net/qq_41185868/article/details/83758376


def make_bot(read_only: bool = False):
    bot = ChatBot(
        'Merlin',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        logic_adapters=[
            {
                "import_path":                  "chatterbot.logic.BestMatch",
                "statement_comparison_function":"chatterbot.comparisons.levenshtein_distance",
                "response_selection_method":    chatterbot.response_selection.get_random_response,
                'default_response':             'I am sorry, but I do not understand.',
                'maximum_similarity_threshold': 0.10
            },
            # 'chatterbot.logic.TimeLogicAdapter',
            'chatterbot.logic.MathematicalEvaluation',
            {
                "import_path":  "chatterbot.logic.SpecificResponseAdapter",
                "input_text":   "print('Merlin is the best!')",
                "output_text":  "print('Congratulations! You found an Easter egg!')"
            }
        ],
        preprocessors=[
            'chatterbot.preprocessors.clean_whitespace'
        ],
        # multi_threading=True,
        read_only=read_only,
        database_uri=f'sqlite:///{os.path.dirname(__file__)}/chats.sqlite3'
    )
    return bot


def train(bot: ChatBot):
    bot.set_trainer(ListTrainer)
    conversation = open(f'{os.path.dirname(__file__)}/chats.txt','r').readlines()
    bot.train(conversation)

    bot.set_trainer(ChatterBotCorpusTrainer)
    bot.train('chatterbot.corpus.english')
    return 0


pool = mp.Pool()
bot = make_bot(True)
try:
    open(f'{os.path.dirname(__file__)}/chats.sqlite3').close()
except Exception:
    train(bot)


def proc_res(bot: ChatBot, msg: discord.Message):
    result = bot.get_response(msg.content)
    return await msg.channel.send(result)


async def response(msg: discord.Message):
    global doTrain, reTrain, pool, bot
    async with msg.channel.typing():
        res = ''
        if msg.content.startswith('merlin::'):
            if msg.content == 'merlin::train':
                doTrain = True
                res = "bot is training, please wait for around a minute."
            if msg.content.startswith('merlin::retrain'):
                reTrain = True
                res = "Please wait..."
            res = "`merlin::`?"
        if res:
            return await msg.channel.send(res)
    return pool.apply_async(proc_res, args=(bot, msg))


def proc_save(saveBot, msg: str, prev: str):
    msg = Statement(msg)
    prev = Statement(prev)
    try:
        saveBot.learn_response(msg, prev)
    except:
        saveBot = make_bot()
        saveBot.learn_response(msg, prev)


async def save(msg: str, prev: str):
    global saveBot
    try:
        saveBot
    except NameError:
        saveBot = make_bot() 
    return pool.apply_async(bot.get_response, args=(saveBot, msg, prev))


def init_train(bot: ChatBot):
    os.remove(f'{os.path.dirname(__file__)}/chats.sqlite3')
    bot = make_bot()
    p = mp.Process(target=train, args=(bot, ), name='Merlin chat retrain / reinit')
    p.start()


def loop():
    global doTrain, reTrain, bot
    while True:
        if doTrain:
            doTrain = False
            p = mp.Process(target=train, args=(bot, ), name='Merlin chat train')
            p.start()
        if reTrain:
            reTrain = False
            init_train(bot)
        time.sleep(2)


t = threading.Thread(target=loop)
t.start()
