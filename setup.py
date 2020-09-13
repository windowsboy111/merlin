from setuptools import setup
import json
long_description = ''
cfg = json.load(open('src/ext/bot_settings.json', 'r'))
with open("README.md", "r") as fh:
    long_description = fh.read()
stage = None
if cfg["stage"] == "stable":
    stage = 'Development Status :: 5 - Production/Stable'
elif cfg["stage"] == "beta":
    stage = 'Development Status :: 4 - Beta'
elif cfg['stage'] == "alpha":
    stage = 'Development Status :: 3 - Alpha'
setup(
    name='Merlin-bot',
    packages=['src'],
    version=cfg['version'],
    license='MIT',
    description=cfg['description'],
    long_description_content_type="text/markdown",
    long_description=long_description,
    author=cfg['author name'],
    author_email='cyruschan0111@gmail.com',
    url='https://github.com/windowsboy111/Merlin-py/',
    download_url=f'https://github.com/windowsboy111/Merlin-py/archive/{cfg["version"]}.tar.gz',
    keywords=['discord', 'bot', 'discord.py'],
    install_requires=['pytablemaker', 'discord.py', 'chatterbot==0.8.7', 'mcstatus', 'flask', 'python-dotenv', 'psutil', 'duckduckgo3', 'asynchronizer'],
    classifiers=[
        stage,
        'Intended Audience :: Developers',
        'Topic :: Communications',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Natural Language :: Cantonese',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
)
