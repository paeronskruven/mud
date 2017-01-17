import asyncio


class SchedulerException(BaseException):
    pass


async def _task(func, interval):
    while True:
        await asyncio.sleep(interval)
        func()


def schedule_interval(func, interval):
    """
    Schedule a function to be run periodically at the given interval
    :param func: function to schedule
    :param interval: interval in seconds
    """
    if not callable(func):
        raise SchedulerException('{0} is not callable'.format(type(func)))

    asyncio.ensure_future(_task(func, interval))
