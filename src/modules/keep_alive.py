from flask import Flask
import asyncio
app = Flask('')


@app.route('/')
def main():
    return "Hello! Merlin-py is here!"


def run(port=8080, host="0.0.0.0"):
    app.run(host=host, port=port)

def async_run(port=8080, host="0.0.0.0"):
    async def run(port, host):
        app.run(host=host, port=port)
    return asyncio.create_task(run(port, host))