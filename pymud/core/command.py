class CommandException(BaseException):
    pass

"""
Following variable contains all commands that has been added at runtime.
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


def parse(data):
    return data.split(None, 1)


def invoke(cmd, **kwargs):
    for key, value in _commands.items():
        if cmd in value:
            return value[cmd](**kwargs)
        else:
            raise CommandException('Command {0} not found'.format(cmd))


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
