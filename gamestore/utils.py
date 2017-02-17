import functools
import inspect
import logging


class log_with(object):
    """Logging decorator that allows you to log with a specific logger.

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
                try:
                    value = args[i]
                except IndexError:
                    # FIXME: Default values in kwargs
                    try:
                        value = kwargs[name]
                    except KeyError:
                        continue
                yield str(name) + ': ' + str(value)

        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            self.logger.info('<' + function.__name__ + '>' + '\n' +
                             '\n'.join(message(args, kwargs)))

            result = function(*args, **kwargs)

            return result
        return wrapper
