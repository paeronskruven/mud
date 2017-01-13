import enum
import logging

from pymud import core
from pymud.dal import account


logger = logging.getLogger(__name__)


class LoginController(core.Controller):

    class States(enum.IntEnum):
        ASK_FOR_USERNAME = 0
        ASK_FOR_PASSWORD = 1

    def __init__(self, *args):
        super().__init__(*args)

        self._state = self.States.ASK_FOR_USERNAME
        self._username = ''
        self._password = ''

        self._render()

    async def update(self):
        if self._state == self.States.ASK_FOR_USERNAME:
            self._username = self._client.buffer
            self._state = self.States.ASK_FOR_PASSWORD

        elif self._state == self.States.ASK_FOR_PASSWORD:
            self._password = self._client.buffer

            if await account.authenticate(self._username, self._password):
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


class GameController(core.Controller):

    def __init__(self, *args):
        super().__init__(*args)

    async def update(self):
        parts = core.command.parse(self._client.buffer)
        cmd = parts[0]

        kwargs = {'client': self._client}
        try:
            kwargs['data'] = parts[1]
        except IndexError:
            # the command was sent without any arguments
            pass

        try:
            await core.command.invoke(cmd, **kwargs)
        except core.command.CommandNotFoundException:
            self._client.write_line('{0} is not a valid command'.format(cmd))
        except core.command.CommandInvalidArgumentException:
            self._client.write_line('{0} contained invalid arguments'.format(cmd))
