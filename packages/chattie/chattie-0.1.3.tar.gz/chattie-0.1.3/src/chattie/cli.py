"""The cli for the chattie command."""

import click
import os

from inspect import getdoc
from chattie.bot import Bot
from chattie.tricks import helpcmd
from chattie.plugins import get_connectors
from chattie.plugins import get_commands


@click.group()
def chattie():
    """Helpful commands for running a chattie bot."""
    pass


@chattie.command()
def connectors():
    """Show all installed connectors."""
    connectors = get_connectors()
    for c in connectors:
        print(c.name)


@chattie.command()
@click.argument('connector_name')
def doc(connector_name):
    """View the doc for the given connector."""
    connectors = get_connectors()
    for c in connectors:
        if c.name == connector_name:
            print(getdoc(c.load()))


@chattie.command()
def commands():
    """Show all installed commands."""
    import chattie.connectors.term as term
    bot = Bot('Chattie', term, get_commands())
    print(helpcmd(bot, ''))


@chattie.command()
@click.argument('bot_name')
def new(bot_name):
    """Create a new bot."""
    os.mkdir(bot_name)
    # Create the tricks directory
    os.mkdir(os.path.join(bot_name, 'tricks'))
    with open(os.path.join(bot_name, 'tricks', '__init__.py'), 'w') as f:
        f.write("commands = {}")
    # Create the handlers directory
    os.mkdir(os.path.join(bot_name, 'handlers'))
    with open(os.path.join(bot_name, 'handlers', '__init__.py'), 'w') as f:
        f.write("handlers = []")

    with open(os.path.join(bot_name, 'envfile'), 'w') as f:
        f.write("""export BOT_NAME=%s

######################################################################
                    Telegram Connector Config
######################################################################
# Make sure you install python-telegram-bot first with
# pip3 install python-telegram-bot
# export TELEGRAM_API_TOKEN='your token here'

######################################################################
                    Matrix Connector Config
######################################################################
# Make sure you install matrix_client first with
# pip3 install matrix_client
# export MATRIX_URL='https://matrix.org'
# export MATRIX_USERNAME=%s
# export MATRIX_PASSWORD='my_bots_password'
# Comma seperated list of rooms to join
# export MATRIX_ROOMS='#thorin-test:matrix.org'""" % bot_name)

    with open(os.path.join(bot_name, 'README'), 'w') as f:
        f.write("""How to use your new bot!

First you can write new commands or 'tricks' in the tricks folder and
new handlers in the handlers folder. If that doesn't make sense to you
you can view the documentation at:

https://github.com/chasinglogic/Chattie

Now if you want to just run your bot you need to first pick a
connector. To view installed connectors run:

chattie connectors

Once you've picked a connector then set the appropriate environment
variables in envfile then activate it with:

source envfile

Finally:

chattie run --connector connector_name

and you're good to go!
""")


@chattie.command()
@click.option('--name',
              default=os.getenv('BOT_NAME', 'Chattie'),
              help='The name of your bot.')
@click.option('--connector',
              default='terminal_connector',
              help='Which connector to use, see "chattie connectors"')
def run(name, connector):
    """Run the bot.

    By default will run with the first available connector.
    """
    conn = None
    available = get_connectors()
    for c in available:
        if c.name == connector:
            conn = c.load()

    commands = get_commands()
    print('comm', commands)
    bot = Bot(name, conn, commands)
    bot.run()


if __name__ == '__main__':
    chattie()
