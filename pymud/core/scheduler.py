import asyncio


class SchedulerException(BaseException):
    pass

_scheduled_tasks = set()


class ScheduledTask:

    def __init__(self, func, interval):
        self._func = func
        self._interval = interval
        asyncio.ensure_future(self._run())
        # todo: add possibility to end tasks on shutdown

    async def _run(self):
        while True:
            await asyncio.sleep(self._interval)
            self._func()


def schedule_interval(func, interval):
    """
    Schedule a function to be run periodically at the given interval
    :param func: function to schedule
    :param interval: interval in seconds
    """
    if not callable(func):
        raise SchedulerException('{0} is not callable'.format(type(func)))
    _scheduled_tasks.add(
        ScheduledTask(func, interval)
    )
