import warnings
import socket
from ..constants import *
from .base import AlterMiddlewareBase, warn


class GeminoidServer(AlterMiddlewareBase):
    def __init__(self, address='127.0.0.1', port=12000):
        raise Exception("Gemionoidserver mode is not implemented yet.")
        super(GeminoidServer, self).__init__()
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((address, port))
        self._socket.settimeout(0.1)

    def get_axes(self):
        warn('get_axes is not work with geminoidserver. return value is filled with None')
        return [None] * AXIS_NUM

    def set_axes(self, value_list, axis_index=None):
        if axis_index is None:
            axis_index = range(1, len(value_list)+1)
        req = 'moveaxes'
        for i, v in zip(axis_index, value_list):
            req += f' {i+1} {v} 1 1000'
        # for i, v in enumerate(value_list):
        #     req += f' {i+1} {v} 1 1000'
        req += '\n'
        try:
            self._socket.sendall(req.encode())
            response = self._socket.makefile().readline()
        except Exception as e:
            warn(f'error on set_axes ({e})')


class Alter2GeminoidServer(AlterMiddlewareBase):
    def __init__(self, address='127.0.0.1', port=12000):
        super(Alter2GeminoidServer, self).__init__()
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((address, port))
        self._socket.settimeout(0.1)

    def get_axes(self):
        warn('get_axes is not work with geminoidserver. return value is filled with None')
        return [None] * AXIS_NUM

    def set_axes(self, value_list):
        req = ""
        for a3idx, a2idx in ALTER3_TO_ALTER2_AXIS_MAP:
            v = value_list[a3idx-1]
            req += f'moveaxis {a2idx} {v} 9\n'
        try:
            self._socket.sendall(req.encode())
            response = self._socket.makefile().readline()
        except Exception as e:
            warn(f'error on set_axes ({e})')
