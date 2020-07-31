from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
import chatterbot
import chatterbot.comparisons
import chatterbot.response_selection
import os

bot = ChatBot(
    'Merlin',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        {
            "import_path":                  "chatterbot.logic.BestMatch",
            "statement_comparison_function":"chatterbot.comparisons.levenshtein_distance",
            "response_selection_method":    chatterbot.response_selection.get_random_response,
            'default_response':             'I am sorry, but I do not understand.',
            'maximum_similarity_threshold': 0.90
        },
        'chatterbot.logic.TimeLogicAdapter',
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
    multi_threading=True,
    read_only=True,
    database_uri=f'sqlite:///{os.path.dirname(__file__)}/chats.sqlite3'
)

trainer = ListTrainer(bot)
corpusTrainer = ChatterBotCorpusTrainer(bot)

conversation = open(f'{os.path.dirname(__file__)}/chats.txt','r').readlines()
trainer.train(conversation)
corpusTrainer.train('chatterbot.corpus.english')
corpusTrainer.train('chatterbot.corpus.traditionalchinese')

def response(msg: str):
    return bot.get_response(msg)

if __name__ == '__main__':
    while True:
        print(response(input('> ')))