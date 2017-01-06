import logging

from .. import core

logger = logging.getLogger(__name__)


@core.command.add('say')
def say(**kwargs):
    logger.info(kwargs)
    kwargs['client'].write_line('testing \033[3m color\033[0m')


@core.command.add('noargs')
def noargs(**kwargs):
    logger.info(kwargs)
