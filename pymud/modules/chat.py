import logging

from pymud import core

logger = logging.getLogger(__name__)


@core.command.add('say')
async def say(client, data):
    client.write_line('testing \033[3m color\033[0m')
    pass


@core.command.add('noargs')
async def noargs(client):
    logger.info('no args')
