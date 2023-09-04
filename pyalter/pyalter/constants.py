#########
# common
#########
GET_AXIS_RETURN_DATA_LEN = 14


#########
# Alter3
#########
ALTER3_AXIS_NUM = 43
ALTER3_SET_AXIS_DATA_NUM = 44  # last channel is unused
ALTER3_GET_AXIS_RETURN_DATA_NUM = 9
ALTER3_GET_AXIS_PARSE_MAP = [
    # (axis_idx, board_no, channel)
    (1,1,1), 
    (2,1,2),
    (3,1,3), 
    (8,1,4),
    (9,1,5), 
    (10,1,6),  # check! (10,4,6) on old code. (miss?)
    (11,2,3),
    (12,2,5),
    (13,3,1),
    (14,3,3),
    (15,3,5),
    (16,2,7),
    (17,4,1),
    (18,4,3),
    (19,4,5),
    (20,4,7),
    (21,5,1),
    (22,5,3),
    (23,5,5),
    (24,5,7),
    (29,2,8),
    (30,6,1),
    (31,6,3),
    (32,6,5),
    (33,6,7),
    (34,7,1),
    (35,7,3),
    (36,7,5),
    (37,7,7),
    (42,9,1),  # check! (42,9,2) on old code. (miss?)
    (43,9,3)
]
MAWARU_INDEX = 42
MAWARU_SAFE_RANGE = 10
MAWARU_SAFE_INTERVAL = 1.0  # [sec]


#########
# Alter2
#########
ALTER2_AXIS_NUM = 36
ALTER2_SET_AXIS_DATA_NUM = 64  # include gain channel
ALTER2_GET_AXIS_RETURN_DATA_NUM = 8
ALTER2_GET_AXIS_RETURN_MAP = [
    # (axis_idx, board_no, channel)
    (1,1,1),
    #(2,1,2),
    #(3,1,3),  
    #(4,1,4),
    #(5,1,5),
    #(6,1,6),
    #(7,1,7),
    #(8,1,8),
    (9,2,1),
    (10,2,3),
    (11,2,5),
    (12,2,7),
    (13,3,1),
    (14,3,3),
    (15,3,5),
    (16,3,7),
    (17,4,1),
    (18,4,3),
    (19,4,5),
    (20,4,7),
    (21,5,1),
    (22,5,3),
    (23,5,5),
    (24,5,7),
    (25,6,1),
    (26,6,3),
    (27,6,5),
    (28,6,7),
    (29,7,1),
    (30,7,3),
    (31,7,5),
    (32,7,7),
    (33,8,1),
    (34,8,3),
    (35,8,5),
    (36,8,7)
]
# Alter2 set_axes command include gain channel, but these always have to be set 255.
# So, using only effective axes is usefull.
ALTER2_SET_DATA_GAIN_INDEX = list(range(9, 68, 2))
ALTER2_AXIS_TO_SET_DATA_MAP = [
    # (axis index, data index on set_axis)
    (1,0),
    (2,1),
    (3,2),
    (4,3),
    (5,4),
    (6,5),
    (7,6),
    (8,7),
    (9,8),
    (10,10),
    (11,12),
    (12,14),
    (13,17),
    (14,18),
    (15,20),
    (16,22),
    (17,24),
    (18,26),
    (19,28),
    (20,30),
    (21,32),
    (22,34),
    (23,36),
    (24,38),
    (25,40),
    (26,42),
    (27,44),
    (28,46),
    (29,48),
    (30,50),
    (31,52),
    (32,54),
    (33,56),
    (34,58),
    (35,60),
    (36,62),
]


