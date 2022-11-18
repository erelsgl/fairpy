#!python3
"""
A context for running functions with a time-limit.
Throws an exception if the function does not finish within the limit.

USAGE:

with time_limit(10):
    foo()

NOTE: This does not work on Windows. See:
https://stackoverflow.com/a/8420498/827927
"""

import signal
import contextlib

class TimeoutException(Exception): pass

IS_TIME_LIMIT_SUPPORTED = hasattr(signal, "SIGALRM")  # only works on Linux
is_time_limit_warning_issued = False

@contextlib.contextmanager
def time_limit(seconds):
    if IS_TIME_LIMIT_SUPPORTED:
        def signal_handler(signum, frame):
            raise TimeoutException("Timed out!")
        signal.signal(signal.SIGALRM, signal_handler)
        signal.alarm(seconds)
        try:
            yield
        finally:
            signal.alarm(0)
    else:
        if not is_time_limit_warning_issued:
            import warnings
            warnings.warn("Time-limit is not supported by your operating system.")
            is_time_limit_warning_issued = True
        yield        


if __name__=="__main__":
    with time_limit(1):
        for i in range(1000): print(i)
