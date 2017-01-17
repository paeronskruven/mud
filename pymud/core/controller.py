class Controller:
    """
    Base class for all controllers.

    The update() method on controllers gets invoked when the client has sent data to the server.
    """

    def __init__(self, client):
        self._client = client

    async def update(self, buffer):
        raise NotImplementedError()
