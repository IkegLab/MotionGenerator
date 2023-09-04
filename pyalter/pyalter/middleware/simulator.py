import socket
from ..constants import *
from .base import AlterMiddlewareBase, warn


class Alter3Simulator(AlterMiddlewareBase):
    def __init__(self, address='127.0.0.1', port=11000):
        super(Alter3Simulator, self).__init__()
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((address, port))
        self._socket.settimeout(0.1)

    def get_axes(self):
        try:
            self._socket.sendall(f'getaxis\n'.encode())
            f = self._socket.makefile()
            response = f.readline()
            status = f.readline()
            data = [int(float(v)) for v in response.split()[:ALTER3_AXIS_NUM]]
            return data
        except Exception as e:
            warn(f'error on get_axes: {e}')
            return [None] * AXIS_NUM

    def set_axes(self, value_list):
        req = 'moveaxes'
        for i, v in enumerate(value_list):
            req += f' {i+1} {v} 1 1000'
        req += '\n'
        try:
            self._socket.sendall(req.encode())
            response = self._socket.makefile().readline()
        except Exception as e:
            warn(f'error on set_axes ({e})')
