import asyncio
import logging
import enum

from pymud.core import telnet
from pymud.core.controller import Controller

logger = logging.getLogger(__name__)


class Client(asyncio.Protocol):

    _origin_controller = None

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

        # iterate the received bytes
        # todo: handle telnet protocol elsewhere?
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

        # update the current controller if we have anything in the buffer
        if self.buffer:

            asyncio.ensure_future(self.controller.update())

    def connection_lost(self, exc):
        logger.info('Lost connection')

    def connection_made(self, transport):
        self.transport = transport
        self.controller = self._origin_controller(self)

    @classmethod
    def set_origin_controller(cls, controller):
        if issubclass(controller, Controller):
            cls._origin_controller = controller
        else:
            raise TypeError('Expected type: {0}, got: {1}'.format(Controller, controller))

    def write(self, data):
        """
        Encodes and writes data to the client.
        """
        self.transport.write(data.encode('utf-8'))

    def write_line(self, data):
        """
        Encodes and writes data to the client with an linebreak at the end.
        """
        self.transport.write('{0}\n'.format(data).encode('ascii'))
