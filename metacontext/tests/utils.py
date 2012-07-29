import sys

from cStringIO import StringIO


class intercept_stdout(object):
    def __init__(self):
        self.buf = StringIO()

    def __enter__(self):
        self.old_stdout = sys.stdout
        sys.stdout = self.buf
        return self.buf

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self.old_stdout
        self.buf.flush()
