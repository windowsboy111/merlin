from flask import Flask
import multiprocessing
app = Flask('')


@app.route('/')
def main():
    return "Hello! Merlin-py is here!"


def run(port=8080, host="0.0.0.0"):
    app.run(host=host, port=port)

def start(port=8080, host="0.0.0.0"):
    p = multiprocessing.Process(target=run, args=(port, host))
    p.start()
    return p
