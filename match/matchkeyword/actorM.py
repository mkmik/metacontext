class match(object):
    def __init__(self, *args):
        pass

    def __enter__(self):
        pass

    def __exit__(self, *args):
        pass

class case(object):
    def __init__(self, *args):
        pass

    def __enter__(self):
        return ('test', 1)

    def __exit__(self, *args):
        pass

_ = object()
