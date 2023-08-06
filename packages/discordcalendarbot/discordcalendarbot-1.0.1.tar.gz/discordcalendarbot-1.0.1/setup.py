
"""discordcalendarbot bot for Discord."""

from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='discordcalendarbot',
    packages = ['discordcalendarbot'],
    version='1.0.1',
    description='Discord bot that handle a Google calendar',
    long_description=long_description,
    author='Axel Rieben & Johnny Da Costa',
    author_email='axel.rieben@he-arc.ch, johnny.dacosta@he-arc.ch',
    url='https://github.com/johndacost/PyBot',
    license='MIT',
    keywords=['discord', 'asyncio', 'bot', 'google calendar'],
    install_requires=(
        'aiohttp>=2.0.0',
        'arrow',
        'httplib2',
        'feedparser',
        'google-api-python-client',
        'discord.py'
    )
)
