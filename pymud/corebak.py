import os
import asyncio


def load_modules():
    mods = []
    f = os.listdir('pymud/modules')
    for m in f:
        if m.startswith('__'):
            continue
        mods.append(
            __import__("pymud.modules." + m.split('.')[0], fromlist=["pymud.modules"])
        )
    return mods

class CommandRouter:

    def __init__(self):
        self._routes = {}

    def add_route(self, cmd, func):
        self._routes[cmd] = func

    def route(self, cmd, data):
        print(self._routes)
        if cmd in self._routes:
            self._routes[cmd](data)

cmd_router = CommandRouter()


def add_command(cmd):
    def decorator(func):
        cmd_router.add_route(cmd, func)
        return func
    return decorator


