import random
from .serial import Alter3Serial


class SerialMock(object):
    def __init__(self):
        super(SerialMock, self).__init__()

    def read(self, n):
        data = bytes([random.randint(0, 255) for i in range(n)] )
        print(f'[serial mock] read {data}')
        return data

    def write(self, data):
        print(f'[serial mock] write {data}')

    def reset_output_buffer(self):
        print(f'[serial mock] reset output buffer')

    def reset_input_buffer(self):
        print(f'[serial mock] reset input buffer')


class Alter3SerialMock(Alter3Serial):
    def __init__(self):
        self._serial = SerialMock()


