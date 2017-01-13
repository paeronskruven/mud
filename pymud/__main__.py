import logging

from pymud import core
from pymud import dal

logger = logging.getLogger(__name__)


def main():
    # configure logging
    logging.basicConfig(
        level=logging.DEBUG if core.config.getboolean('server', 'debug') else logging.INFO,
        format='%(asctime)s %(levelname)s %(name)s %(message)s'
    )

    logger.info('Starting server')

    try:
        # connect to the database
        dal.connect()

        # import the controllers here so the global instance of the database is set before the dal modules are loaded
        from pymud import controllers
        # set the starting controller for clients
        core.Client.set_origin_controller(controllers.LoginController)
        core.server.run()
    except Exception as ex:
        logger.error(ex)

    logger.info('Shutting down')


if __name__ == '__main__':
    main()
