#########
# Alter3 and Alter2 translation
#########
ALTER3_TO_ALTER2_TRANSLATION_MAP_OLD = [
    # (alter3_axis, alter2_axis (based on set_axis indexing, 1 start indexing) )
    (1, 21, (0, 255), (0, 255), False),
    (2, 13, (0, 255), (0, 255), False),
    (3, 15, (0, 255), (0, 255), False),
    (5, 3, (0, 255), (0, 255), False),
    (6, 4, (0, 255), (0, 255), False),
    (8, 17, (0, 255), (0, 255), False),
    (11, 25, (0, 255), (0, 255), False),
    (12, 23, (0, 255), (255, 0), True),
    (13, 27, (0, 255), (0, 255), False),
    (14, 29, (0, 255), (255, 0), True), #ok
    (15, 31, (0, 255), (0, 255), False), #ok
    (16, 33, (0, 255), (0, 255), False),
    (18, 37, (120, 255), (0, 255), False), #ok
    (19, 35, (0, 255), (0, 255), False),
    (20, 39, (0, 255), (0, 255), False),
    (21, 41, (0, 255), (0, 230), False),
    (22, 43, (0, 255), (0, 255), False),
    (23, 45, (0, 255), (255, 0), True),
    (24, 47, (0, 255), (0, 255), False),
    (29, 49, (0, 255), (0, 255), False),
    (31, 53, (120, 255), (0, 255), False),
    (32, 51, (0, 255), (0, 255), False),
    (33, 55, (0, 255), (0, 255), False),
    (34, 57, (0, 255), (0, 230), False),
    (35, 59, (0, 255), (0, 255), False),
    (36, 61, (0, 255), (255, 0), True),
    (37, 63, (0, 255), (255, 0), True),
    (42, 1, (0, 255), (0, 255), False),
]

ALTER3_TO_ALTER2_TRANSLATION_MAP = []

from .constants import ALTER2_AXIS_TO_SET_DATA_MAP, ALTER2_AXIS_NUM, ALTER3_AXIS_NUM
import warnings

for a3_idx, a2_didx, a3_range, a2_range, reverse in ALTER3_TO_ALTER2_TRANSLATION_MAP_OLD:
    for x in ALTER2_AXIS_TO_SET_DATA_MAP:
        if x[1] == a2_didx - 1:
            ALTER3_TO_ALTER2_TRANSLATION_MAP.append((a3_idx, x[0], a3_range, a2_range, reverse))
            break

#print(ALTER3_TO_ALTER2_TRANSLATION_MAP)

def translate_axes_alter2_to_alter3(data, fill_value=127, use_map_function=True):
    assert len(data) == ALTER2_AXIS_NUM
    ret = [fill_value] * ALTER3_AXIS_NUM
    for a3_idx, a2_idx, (a3_min, a3_max), (a2_min, a2_max), reverse in ALTER3_TO_ALTER2_TRANSLATION_MAP:
        raw_v = data[a2_idx-1]
        if not use_map_function:
            v = raw_v if not reverse else 255-raw_v
        elif type(raw_v) is int:
            v = (a3_max - a3_min) / (a2_max - a2_min) * (raw_v - a2_min) + a3_min
            v = min(max(a3_min, a3_max), max(min(a3_min, a3_max), v))
            v = int(v)
        elif raw_v is None:
            v = None
        else:
            warnings.warn('tanslate invalid value in axis data for translation. it filled None.')
        ret[a3_idx-1] = v
    return ret

import numpy as np

def translate_axes_alter3_to_alter2(data, fill_value=127, use_map_function=True):
    assert len(data) == ALTER3_AXIS_NUM
    ret = [fill_value] * ALTER2_AXIS_NUM
    for a3_idx, a2_idx, (a3_min, a3_max), (a2_min, a2_max), reverse in ALTER3_TO_ALTER2_TRANSLATION_MAP:
        raw_v = data[a3_idx-1]
        if not use_map_function:
            v = raw_v if not reverse else 255-raw_v
        elif type(raw_v) in [int, np.int64]:
            v = (a2_max - a2_min) / (a3_max - a3_min) * (raw_v - a3_min) + a2_min
            v = min(max(a2_min, a2_max), max(min(a2_min, a2_max), v))
            v = int(v)
        elif raw_v is None:
            v = None
        else:
            warnings.warn('tanslate invalid value in axis data for translation. it filled None.')
            print(raw_v, type(raw_v))
            v = None
        ret[a2_idx-1] = v
    return ret       