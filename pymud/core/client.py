import asyncio
import logging
import enum

from . import telnet
from .. import controllers

logger = logging.getLogger(__name__)


class Client(asyncio.Protocol):

    class ReceiveState(enum.IntEnum):
        NORMAL = 0
        TN_IAC = 1
        TN_SB = 2

    def __init__(self):
        self.transport = None
        self.controller = None
        self.buffer = ''

    def data_received(self, data):
        # new data received, reset the state and buffer
        state = self.ReceiveState.NORMAL
        self.buffer = ''

        for byte in [bytes([char]) for char in data]:
            if state == self.ReceiveState.NORMAL:
                if byte == telnet.IAC:
                    state = self.ReceiveState.TN_IAC
                    print('Got IAC')
                    continue

                # CR or LF received, ignore
                if byte in [b'\r', b'\n']:
                    continue

                self.buffer += byte.decode('ascii')

            elif state == self.ReceiveState.TN_IAC:
                if byte == telnet.SB:
                    state = self.ReceiveState.TN_SB
                    print('Got SB')

                elif byte in (telnet.WILL, telnet.WONT, telnet.DO, telnet.DONT):
                    print('Got WILL, WONT, DO, DONT')

                else:
                    # todo: handle the option
                    state = self.ReceiveState.NORMAL

            elif state == self.ReceiveState.TN_SB:
                if byte == telnet.SE:
                    state = self.ReceiveState.NORMAL
                    print('Got SE')

        self.controller.update()

    def connection_lost(self, exc):
        logger.info('Lost connection ', exc)

    def connection_made(self, transport):
        self.transport = transport
        self.controller = controllers.LoginController(self)

    def write(self, data):
        """
        Encodes and writes data to the client.
        """
        self.transport.write(data.encode('utf-8'))

    def write_line(self, data):
        """
        Encodes and writes data to the client with an linebreak at the end.
        """
        self.transport.write('{0}\n'.format(data).encode('utf-8'))
