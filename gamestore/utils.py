import functools
import inspect
import logging


class log_with(object):
    """Logging decorator that allows you to log with a specific logger.

    Attributes:
        logger (Logger, optional):
            Instance of a logger

    Todo:
        - loglevel
        - Pretty formatting
        - function call stack level
        - timer
        - args & kwargs
    """

    def __init__(self, logger=None, entry_msg=None, exit_msg=None):
        self.logger = logger
        self.entry_msg = entry_msg
        self.exit_msg = exit_msg

    def __call__(self, function):
        """Returns a wrapper that wraps func. The wrapper will log the entry
        and exit points of the function with logging.INFO level."""
        if not self.logger:
            # If logger is not set, set module's logger.
            self.logger = logging.getLogger(function.__module__)

        # Function signature
        sig = inspect.signature(function)
        arg_names = sig.parameters.keys()

        def message(args, kwargs):
            for i, name in enumerate(arg_names):
                if i < len(args):
                    yield name, args[i]
                elif name in kwargs:
                    yield name, kwargs[name]

        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            d = ', '.join('{}: {}'.format(name, value) for name, value in message(args, kwargs))
            msg = '<' + function.__name__ + '>' + ' ' + '{' + d + '}'
            self.logger.info(msg)
            result = function(*args, **kwargs)
            return result

        return wrapper
