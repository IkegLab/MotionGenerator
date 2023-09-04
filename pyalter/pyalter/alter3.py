import warnings, time
from .middleware import *
from .constants import *
from .utils import translate_axes_alter2_to_alter3, translate_axes_alter3_to_alter2


class Alter3(object):

    def __init__(self, mode,
                 serial_port=None, serial_timeout=0.2,
                 simulator_address='127.0.0.1', simulator_port=11000,
                 geminoid_server_address='127.0.0.1', geminoid_server_port=11000,
                 safemode=False, log_file=None, output_verbose=False,
                 alter2as3mode=True):
        super(Alter3, self).__init__()
        if mode == "serialmock":
            self._middleware = Alter3SerialMock()
            self.name = 'serial mock'
            self.axis_num = constants.ALTER3_AXIS_NUM
        elif mode == "simulator":
            self._middleware = Alter3Simulator(address=simulator_address, port=simulator_port)
            self.name = 'Alter3 simulator'
            self.axis_num = constants.ALTER3_AXIS_NUM
        elif mode == "serial":
            self._middleware = Alter3Serial(serial_port, serial_timeout=serial_timeout)
            self.name = 'Alter3'
            self.axis_num = constants.ALTER3_AXIS_NUM
        elif mode == "alter2serial":
            self._middleware = Alter2Serial(serial_port, serial_timeout=serial_timeout)
            self._alter2as3mode = alter2as3mode
            if alter2as3mode:
                self.name = 'Alter2 compatible with Alter3'
                self.axis_num = constants.ALTER3_AXIS_NUM
            else:
                self.name = 'Alter2'
                self.axis_num = constants.ALTER2_AXIS_NUM
        elif mode == "geminoidserver":
            self._middleware = GeminoidServer(address=geminoid_server_address, port=geminoid_server_port)
            self.name = 'Alter3 via geminoid server'
            self.axis_num = constants.ALTER3_AXIS_NUM
        elif mode == "alter2gs":
            self._middleware = Alter2GeminoidServer(address=geminoid_server_address, port=geminoid_server_port)
            self.name = 'Alter2 via geminoid server'
            self.axis_num = constants.ALTER2_AXIS_NUM
        else:
            raise Exception(f'Invalid mode "{mode}"')

        self.safemode = safemode
        if mode in ["alter2serial", "alter2gs"]:
            self.safemode = False
        self._log_file = log_file
        self._output_verbose = output_verbose

        self._log(f'start {mode} mode')

        self._last_setaxis_value = [128] * self.axis_num
        x = self.get_axes()
        if self.safemode and x[MAWARU_INDEX] is None:
            raise Exception("Initial mawa-ru value is not availabele!!")
        for i, v in enumerate(x):
            if v is not None:
                self._last_setaxis_value[i] = v

    def get_axes(self, return_alter2as3_raw=False):
        result = self._middleware.get_axes()
        self._log(f"getaxis response: {result}")
        if hasattr(self, '_alter2as3mode') and self._alter2as3mode:
            result_raw = result
            result = translate_axes_alter2_to_alter3(result, None)
            if return_alter2as3_raw:
                return result, result_raw
        return result

    def set_axes(self, axis_index, axis_value, zero_start_indexing=False):
        axis_index = axis_index if type(axis_index) is list else [axis_index]
        axis_value = axis_value if type(axis_value) is list else [axis_value]

        if (len(axis_index) is not len(axis_value)):
            warnings.warn("invalid arguments.")
            return

        valid_value = False
        for ai, av in zip(axis_index, axis_value):
            a_zero_index = ai if zero_start_indexing else ai-1
            if a_zero_index < 0 or a_zero_index >= self.axis_num:
                warnings.warn(f'axis index {ai} is out of valid range. it is ignored.')
                continue
            if a_zero_index == MAWARU_INDEX and self.safemode:
                warnings.warn(f'set command to axis {ai} (mawa-ru) is ignored on safety mode. it is ignored.')
                continue
            if av < 0 or av > 255:
                warnings.warn(f'axis value {av} is out of valid range. it is fixed in 0-255.')
                av = min(max(0, av), 255)
            valid_value = True
            self._last_setaxis_value[a_zero_index] = av
        
        self._log(f"setaxis: {axis_index} {axis_value}")
        if not valid_value:
            warnings.warn(f'no valid value on SET_AXES command. command is not executed.')
            return

        data = self._last_setaxis_value
        if hasattr(self, '_alter2as3mode') and self._alter2as3mode:
            data = translate_axes_alter3_to_alter2(data, 127)
        self._middleware.set_axes(data)

    def set_all_axes(self, axis_values):
        if len(axis_values) != self.axis_num:
            warnings.warn(f'number of axis value {len(axis_values)} is not same as alter axis.')
            return
        self.set_axes(list(range(self.axis_num)), axis_values, zero_start_indexing=True)

    def move_mawaru_safely(self, value):
        import time
        current = self.get_axes()[MAWARU_INDEX]
        if current is None:
            warnings.warn("Couldn't take current state of MAWA-RU.")
            return
        step = MAWARU_SAFE_RANGE if value > current else -MAWARU_SAFE_RANGE
        self.safemode = False
        for v in range(current, value, step):
            self.set_axes(MAWARU_INDEX, v, zero_start_indexing=True)
            time.sleep(MAWARU_SAFE_INTERVAL)
        self.set_axes(MAWARU_INDEX, value, zero_start_indexing=True)
        self.safemode = True

    def servo_off(self):
        if isinstance(self._middleware, Alter3Serial) or isinstance(self._middleware, Alter2Serial):
            self._middleware.servo_off()
        else:
            warnings.warn(f"servo_off is not needed on middleware: {self._middleware}.")

    def replay(self, logifle):
        print("not implemented yet.")

    def get_last_setaxis_value(self):
        return self._last_setaxis_value

    def get_axis(self):
        return self.get_axes()

    def set_axis(self, axis_index, axis_value, zero_start_indexing=False):
        return self.set_axes(axis_index, axis_value, zero_start_indexing=zero_start_indexing)

    def _log(self, str):
        if self._log_file is not None:
            with open(self._log_file, 'a') as f:
                f.write(f'{time.time()} {str}\n')
        if self._output_verbose:
            print(f'[Alter3] {str}')


