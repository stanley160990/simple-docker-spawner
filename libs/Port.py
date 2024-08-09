import socket

class Port(object):
    def __init__(self) -> None:
        pass

    def gen(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('localhost', 0))
        port = s.getsockname()[1]
        s.listen(1)
        s.close()

        return port
