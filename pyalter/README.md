# PyAlter

## Install ##

```terminal
pip install -U git+https://github.com/maru-n/pyalter.git
```

### developmental (editable) install on local ###
```terminal
git clone git@github.com:maru-n/pyalter.git
pip install -e pyalter
```


## How to use

### Local

```python
import pyalter
# Alter3 via serial port
alter = pyalter.Alter3("serial", serial_port=serial_device)
                            
# Alter3 simulator
alter = pyalter.Alter3("simulator", simulator_address=address, simulator_port=port)
                                        
# Alter2 via serial port
alter = pyalter.Alter3("alter2serial", serial_port=serial_device, alter2as3mode=False)
# alter2as3mode convert axis data to alter3 axis.

# Alter2/3 via geminoid server  
alter = pyalter.Alter3("geminoidserver", geminoid_server_address='127.0.0.1', geminoid_server_port=11000)
alter = pyalter.Alter3("alter2gs", geminoid_server_address='127.0.0.1', geminoid_server_port=11000)  

# 動かし方
pyalter.set_axes(42, 255)  # １軸毎の設定

pyalter.set_axes([1,2,3], [255, 100, 127])  # 複数軸同時
pyalter.safety_mode = False  # マワールを動かす場合はsafety_modeをFalseに (気を付けて！）

alter = pyalter.Alter3("/dev/tty.usbserial-FT2KYLHW", log="~/alter.log")  # ログをとる
```

### axis_index
- 1 上瞼開閉
- 2 眼左右
- 3	眼上下
- 4	下瞼開閉
- 5	頬引き左
- 6	頬引き右
- 7	口すぼめ
- 8	口開閉
- 9	頭左右傾げ
- 10	頭前後傾げ
- 11 首旋回
- 12 首２前後
- 13 腹部左右傾げ
- 14 腹部前後
- 15 腹部旋回
- 16 左肩甲骨上下
- 17 左肩甲骨前後
- 18 左脇開閉
- 19 左腕前後
- 20 左上腕旋回
- 21 左肘屈伸
- 22 左前腕ひねり
- 23 左手首屈伸1
- 24 左手首屈伸2
- 25 左指動作1（親指）
- 26 左指動作2（人差指）
- 27 左指動作3（中指）
- 28 左指動作4（薬指・小指連動）
- 29 右肩甲骨上下
- 30 右肩甲骨前後
- 31 右脇開閉
- 32 右腕前後
- 33 右上腕旋回
- 34 右肘屈伸
- 35 右前腕ひねり
- 36 右手首屈伸1
- 37 右手首屈伸2
- 38 右指動作1（親指）
- 39 右指動作2（人差指）
- 20 右指動作3（中指）
- 41 右指動作4（薬指・小指連動）
- 42 全体上下
- 43 全体旋回
