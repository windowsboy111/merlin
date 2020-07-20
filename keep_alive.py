from flask import Flask
from threading import Thread
app = Flask('')


@app.route('/')
def main():
    return "Hello! Merlin-py is here!"


def run(port=8080, host="0.0.0.0"):
    app.run(host=host, port=port)


def keep_alive():
    server = Thread(target=run)
    server.start()
