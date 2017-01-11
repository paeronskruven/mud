import enum
import logging

from . import core
from .dal import account


logger = logging.getLogger(__name__)


class Controller:
    """
    Base class for all controllers.

    The update() method on controllers gets invoked when the client has sent data to the server.
    """

    def __init__(self, client):
        self._client = client

    def update(self):
        raise NotImplementedError()


class LoginController(Controller):

    class States(enum.IntEnum):
        ASK_FOR_USERNAME = 0
        ASK_FOR_PASSWORD = 1

    def __init__(self, *args):
        super().__init__(*args)

        self._state = self.States.ASK_FOR_USERNAME
        self._username = ''
        self._password = ''

        self._render()

    def update(self):
        if self._state == self.States.ASK_FOR_USERNAME:
            self._username = self._client.buffer
            self._state = self.States.ASK_FOR_PASSWORD

        elif self._state == self.States.ASK_FOR_PASSWORD:
            self._password = self._client.buffer

            if account.authenticate(self._username, self._password):
                # todo: authenticate client and get character
                self._client.controller = GameController(self._client)
                return
            else:
                self._client.write_line('Invalid details')
                self._state = self.States.ASK_FOR_USERNAME

        self._render()

    def _render(self):
        if self._state == self.States.ASK_FOR_USERNAME:
            self._client.write_line('Enter your username:')
        elif self._state == self.States.ASK_FOR_PASSWORD:
            self._client.write_line('Enter your password:')


class GameController(Controller):

    def __init__(self, *args):
        super().__init__(*args)

    def update(self):
        parts = core.command.parse(self._client.buffer)
        cmd = parts[0]

        kwargs = {'client': self._client}
        try:
            kwargs['data'] = parts[1]
        except IndexError:
            # the command was sent without any arguments
            pass

        try:
            core.command.invoke(cmd, **kwargs)
        except core.command.CommandNotFoundException:
            self._client.write_line('{0} is not a valid command'.format(cmd))
        except core.command.CommandInvalidArgumentException:
            self._client.write_line('{0} contained invalid arguments'.format(cmd))
