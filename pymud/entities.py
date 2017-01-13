from pymud import controllers


class Player:

    def __init__(self, client):
        self.client = client
        #self.controller = controllers.LoginController()

    def on_data_received(self, data):
        print(data)
