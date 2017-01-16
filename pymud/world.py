import logging


logger = logging.getLogger(__name__)

TICK_INTERVAL = 5 * 60


def tick():
    logger.info('World tick started')
    # todo: add things that needs updating
    logger.info('World tick ended')


