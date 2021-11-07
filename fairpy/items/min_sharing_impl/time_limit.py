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

@contextlib.contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
