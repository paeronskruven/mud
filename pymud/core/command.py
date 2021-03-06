import logging

logger = logging.getLogger(__name__)


class CommandException(BaseException):
    pass


class CommandNotFoundException(BaseException):
    pass


class CommandInvalidArgumentException(BaseException):
    pass


"""
Dictionary containing all commands that has been added at runtime.
Commands can add themselves with the decorator @core.command.add('cmd name').

Structure as following:
{
    'module name': {
        'cmd': <function>,
        'cmd2: <function>
    }
}
"""
_commands = {}


def log_info():
    logger.info('Available commands:')
    for mod_name, cmds in _commands.items():
        for cmd in cmds:
            logger.info('{0}->{1}'.format(mod_name, cmd))


def parse(data):
    return data.split(None, 1)


def invoke(cmd, **kwargs):
    for key, value in _commands.items():
        if cmd in value:
            try:
                return value[cmd](**kwargs)
            except TypeError:
                raise CommandInvalidArgumentException()
        else:
            raise CommandNotFoundException('Command {0} not found'.format(cmd))


def add(cmd):
    def decorator(func):
        """
        Decorator function for easy way to add commands to the server.
        A reference to the function is stored with the command name as key.
        The structure of the _commands dictionary is described above at its declaration.
        """
        mod_name = func.__module__.rsplit('.', 1)[-1]
        if mod_name not in _commands:
            _commands[mod_name] = {}

        mod_cmds = _commands[mod_name]
        if cmd in mod_cmds:
            raise CommandException('Command {0} already exists'.format(cmd))
        else:
            mod_cmds[cmd] = func

        return func
    return decorator
