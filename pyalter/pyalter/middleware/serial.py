import serial
from .. import constants
from .base import AlterMiddlewareBase, warn


class SerialBase(AlterMiddlewareBase):
    def __init__(self, 
                 serial_port,
                 axis_num,
                 set_axis_data_num,
                 get_axis_return_data_num,
                 get_axis_parse_map, 
                 serial_timeout=0.2):
        super(SerialBase, self).__init__()
        if serial_timeout < 0.2:
            warn(f'serial timeout smaller than 0.2 will be take many errors. (got {serial_timeout})')
        self._serial = serial.Serial(serial_port, 500000, timeout=serial_timeout)
        self._AXIS_NUM = axis_num
        self._SET_AXIS_DATA_NUM = set_axis_data_num
        self._GET_AXIS_RETURN_DATA_NUM = get_axis_return_data_num
        self._GET_AXIS_RETURN_DATA_LEN = constants.GET_AXIS_RETURN_DATA_LEN
        self._GET_AXIS_RETURN_DATA_TOTAL_SIZE = self._GET_AXIS_RETURN_DATA_NUM * self._GET_AXIS_RETURN_DATA_LEN
        self._GET_AXIS_PARSE_MAP = get_axis_parse_map

    def get_axes(self):
        cmd = [0x39, 0x00, self._GET_AXIS_RETURN_DATA_NUM]
        crc = self._crc16(cmd)
        cmd = [0x5A] + cmd + [crc & 0x00FF, (crc & 0xFF00) >> 8] + [0xA5]
        self._send_command(cmd)
        res = self._serial.read(self._GET_AXIS_RETURN_DATA_TOTAL_SIZE)
        return self._parse_get_axes_response(res)

    def _parse_get_axes_response(self, response):
        if len(response) != self._GET_AXIS_RETURN_DATA_TOTAL_SIZE:
            warn(f'GET_AXES can not get correct data length ({len(response)} < {self._GET_AXIS_RETURN_DATA_TOTAL_SIZE}). Part of the data is filled by None.')
        data = [[None] * 8 for _ in range(self._GET_AXIS_RETURN_DATA_NUM)]
        for res in self._split_get_axes_response(response):
            if self._crc16(res[1:12]) != (res[12] | (res[13] << 8)):
                warn('GET_AXES respons CRC value is not correct. Part of the data is filled by None.')
            elif res[0] != 0x5A or res[1] != 0xB9:
                warn('GET_AXES response headder or command value is not correct. Part of the data is filled by None.')
            elif res[2] + res[3] != self._GET_AXIS_RETURN_DATA_NUM - 1:
                warn('GET_AXES board number is not correct. Part of the data is filled by None.')
            else:
                board_number = res[2]
                data[board_number] = res[4:12]
        result = [None] * self._AXIS_NUM
        for i, j, k in self._GET_AXIS_PARSE_MAP:
            result[i-1] = data[j-1][k-1]  # axis index start from 1, but data index start from 0.
        return result

    def _split_get_axes_response(self, response):
        idx = len(response) // self._GET_AXIS_RETURN_DATA_LEN
        return [response[i*self._GET_AXIS_RETURN_DATA_LEN:(i+1)*self._GET_AXIS_RETURN_DATA_LEN] for i in range(idx)]

    def set_axes(self, value_list):
        if len(value_list) != self._SET_AXIS_DATA_NUM:
            warn('SET_AXIS number of data is not correct. The command will be failed.')
        cmd = [0x30, self._SET_AXIS_DATA_NUM] + value_list
        crc = self._crc16(cmd)
        cmd = [0x5A] + cmd + [crc & 0x00FF, (crc & 0xFF00) >> 8] + [0xA5]
        self._send_command(cmd)
        res = self._serial.read(1)
        if len(res) <= 0 or res[0] != 0x86:
            warn('SET_AXIS response code is not correct. May be SET_AXIS is failed.')

    def servo_off(self):
        cmd = [0x15]
        crc = self._crc16(cmd)
        cmd = [0x5A] + cmd + [crc & 0x00FF, (crc & 0xFF00) >> 8] + [0xA5]
        self._send_command(cmd)
        # ??? Alter3 Bug ???
        # response code (0x86) is not returned after SERVO_OFF command.
        # But It will come back when the next time you send the other command.
        # So send GET_AXES command to avoid trouble.
        cmd = [0x39, 0x00, self._GET_AXIS_RETURN_DATA_NUM]
        crc = self._crc16(cmd)
        cmd = [0x5A] + cmd + [crc & 0x00FF, (crc & 0xFF00) >> 8] + [0xA5]
        self._send_command(cmd)
        res = self._serial.read(1)
        if res[0] != 0x86:
            warn('SERVO_OFF response code is not correct.')

    def _send_command(self, command):
        self._serial.reset_output_buffer()
        self._serial.reset_input_buffer()
        self._serial.write(bytes(command))
        self._serial.flush()

    def _crc16(self, data, poly=0xA001):
        data = bytearray(data)
        crc = 0x0000
        for b in data:
            cur_byte = 0xFF & b
            for _ in range(0, 8):
                if (crc & 0x0001) ^ (cur_byte & 0x0001):
                    crc = (crc >> 1) ^ poly
                else:
                    crc >>= 1
                cur_byte >>= 1
        return crc & 0xFFFF


class Alter3Serial(SerialBase):
    def __init__(self, serial_port, serial_timeout=0.2):
        super(Alter3Serial, self).__init__(serial_port,
                                           constants.ALTER3_AXIS_NUM,
                                           constants.ALTER3_SET_AXIS_DATA_NUM,
                                           constants.ALTER3_GET_AXIS_RETURN_DATA_NUM,
                                           constants.ALTER3_GET_AXIS_PARSE_MAP,
                                           serial_timeout = serial_timeout)

    def set_axes(self, value_list):
        super().set_axes(value_list + [0])  # 


class Alter2Serial(SerialBase):
    """
    [all_data_mode]
    True: use ALL data channel (64 channel) including gain channel.
    set_axis and get_axis treat 64 data, but gain channel have to be set 255. These channel will be checked on the method.
    False: use only EFFECTIVE axes (36 axes).
    set_axis and get_axis treat 36 axes, and gain channel is set to 255 automatically.

    [alter3translation]
    True: convert all axis fit to alter3 axis on set_axis and get_axis.
    So it can use as if Alter3.
    """  
    def __init__(self, serial_port, serial_timeout=0.2, all_data_mode=False):
        super(Alter2Serial, self).__init__(serial_port,
                                           constants.ALTER2_AXIS_NUM,
                                           constants.ALTER2_SET_AXIS_DATA_NUM,
                                           constants.ALTER2_GET_AXIS_RETURN_DATA_NUM,
                                           constants.ALTER2_GET_AXIS_RETURN_MAP,
                                           serial_timeout = serial_timeout)
        self.all_data_mode = all_data_mode
        if self.all_data_mode:
            print('=============== all_data_mode is buggy!!!! ================')

    def get_axes(self):
        res = super().get_axes()
        if self.all_data_mode:
            res = self._convert_axis_to_all_data(res, None)
        return res
    
    def set_axes(self, value_list):
        if self.all_data_mode:
            data = self._chack_set_axes_gain_channel(value_list)
        else:
            data = self._convert_axis_to_all_data(value_list, 255)
        super().set_axes(data)

    def _convert_axis_to_all_data(self, axis_values, fill_value):
        data = [fill_value] * constants.ALTER2_SET_AXIS_DATA_NUM
        for axis_idx, data_idx in constants.ALTER2_AXIS_TO_SET_DATA_MAP:
            data[data_idx] = axis_values[axis_idx-1]
        return data

    def _chack_set_axes_gain_channel(self, data):
        for gain_idx in ALTER2_SET_DATA_GAIN_INDEX:
            if data[gain_idx] != 255:
                warn(f'SET_AXES data index {gain_idx} is gain channel. So it have to be set to 255. data changed from {data[gain_idx]} to 255.')
                data[gain_idx] = 255
        return data