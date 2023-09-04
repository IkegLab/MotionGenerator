import argparse
from .alter3 import Alter3
from .constants import *
import sys
import argparse

# python -m pyalter sim:

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--serial-device', type=str, default="/dev/tty.usbserail")
    parser.add_argument('--simulator', action='store_true')
    parser.add_argument('--simulator-address', type=str, default='127.0.0.1')
    parser.add_argument('--simulator-port', type=int, default='11000')
    args = parser.parse_args()

    if args.simulator:
        address = args.simulator_address
        port = args.simulator_port
        a = Alter3("simulator", simulator_address=address, simulator_port=port, output_verbose=False)
    else:
        device = args.serial_device
        a = Alter3("serial", serial_port=device, serial_timeout=0.2, output_verbose=False)
    
    set_axes_values = [127] * ALTER3_AXIS_NUM
    while True:
        a.set_all_axes(set_axes_values)
        get_axes_values = a.get_axes()
        assert len(set_axes_values) == len(get_axes_values)
        print('-----------------------------------')
        for i, (sa, ga) in enumerate(zip(set_axes_values, get_axes_values)):
            sa_str = f'{sa:3}' if sa is not None else 'nan'
            ga_str = f'{ga:3}' if ga is not None else 'nan'
            print(f'#{i+1:02} {sa_str}/{ga_str}  ', end='')
            if (i+1) % 4 == 0 or i == len(set_axes_values)-1:
                print()

