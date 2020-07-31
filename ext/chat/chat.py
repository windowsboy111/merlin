from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os


bot = ChatBot(
    'Merlin',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.BestMatch',
        'chatterbot.logic.MathematicalEvaluation',
    ],
    database_uri=f'sqlite:///{os.path.dirname(__file__)}/chats.sqlite3'
)

bot.set_trainer(ListTrainer)

conversation = open(f'{os.path.dirname(__file__)}/chats.txt','r').readlines()
bot.train(conversation)

def response(msg: str):
    return bot.get_response(msg)

if __name__ == '__main__':
    while True:
        print(response(input('> ')))