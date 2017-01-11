import asyncio
import logging

from . import client

logger = logging.getLogger(__name__)


class Server:

    def __init__(self):
        self._host = ''
        self._port = 3127
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
        logger.info('Starting server on port: {0}'.format(self._port))
        self._server = self._event_loop.create_server(client.Client, host=self._host, port=self._port)
        self._event_loop.run_until_complete(self._server)
        try:
            self._event_loop.run_forever()
        finally:
            logger.info('Server is shutting down')
            self._server.close()
            self._event_loop.close()

server = Server()
