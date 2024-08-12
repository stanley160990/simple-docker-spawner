from socket import socket

class Port(object):
    def __init__(self) -> None:
        pass

    def gen(self):
        with socket() as s:
            s.bind(('',0))
            free_socket = s.getsockname()[1]

        return free_socket
