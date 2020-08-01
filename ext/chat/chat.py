from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
import chatterbot
import chatterbot.response_selection
import os
import threading
import time
import multiprocessing as mp
doTrain = False
reTrain = False
# more_label = None
# more_data = None
# if an error occurred try this: https://blog.csdn.net/qq_41185868/article/details/83758376


def make_bot():
    return ChatBot(
        'Merlin',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        logic_adapters=[
            {
                "import_path":                  "chatterbot.logic.BestMatch",
                "statement_comparison_function":"chatterbot.comparisons.levenshtein_distance",
                "response_selection_method":    chatterbot.response_selection.get_random_response,
                # 'default_response':             'I am sorry, but I do not understand.',
                # 'maximum_similarity_threshold': 0.40
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
        # read_only=True,
        database_uri=f'sqlite:///{os.path.dirname(__file__)}/chats.sqlite3'
    )


def train(bot: ChatBot):
    trainer = ListTrainer(bot)
    conversation = open(f'{os.path.dirname(__file__)}/chats.txt','r').readlines()
    trainer.train(conversation)

    cTrainer = ChatterBotCorpusTrainer(bot)
    cTrainer.train('chatterbot.corpus.english')
    try:
        cTrainer.train('chatterbot.corpus.tchinese')
    except FileNotFoundError:
        cTrainer.train('chatterbot.corpus.traditionalchinese')
    return 0

try:
    open(f'{os.path.dirname(__file__)}/chats.sqlite3').close()
    bot = make_bot()
except Exception:
    bot = make_bot()
    train(bot)

def response(msg: str):
    global doTrain, reTrain
    if msg.startswith('merlin::'):
        if msg == 'merlin::train':
            doTrain = True
            return "bot is training, please wait for around a minute."
        if msg.startswith('merlin::retrain'):
            reTrain = True
            return "Please wait..."
        return "`merlin::`?"
    res = bot.get_response(msg)
    if res != 'I am sorry, but I do not understand.':
        bot.learn_response(res)
    return res


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


if __name__ == '__main__':
    while True:
        print(response(input('> ')))
