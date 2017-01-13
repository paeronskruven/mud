import asyncio
import logging
import configparser

from pymud.core import command
from pymud.core import client

logger = logging.getLogger(__name__)

config = configparser.ConfigParser()
config.read('config.ini')


class Server:

    def __init__(self):
        self._host = config.get('server', 'host')
        self._port = config.getint('server', 'port')
        self._server = None
        self._client_handles = []
        # todo: implement uvloop when not running on windows for performance
        self._event_loop = asyncio.get_event_loop()

    def add_client_handle(self, handle):
        self._client_handles.append(handle)

    def broadcast(self, data):
        for handle in self._client_handles:
            handle.write(data)

    def run(self):
        logger.info('Trying to bind {0}:{1}'.format(self._host, self._port))

        self._server = self._event_loop.create_server(client.Client, host=self._host, port=self._port)
        self._event_loop.run_until_complete(self._server)
        logger.info('Binding success')
        # log info about commands that have been added
        command.log_info()

        try:
            logger.info('Waiting for connections...')
            self._event_loop.run_forever()
        finally:
            self._server.close()
            self._event_loop.close()

server = Server()
