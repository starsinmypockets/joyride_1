from machine import Pin, ADC
import time
import math

# pins
X_IN = ADC(27)
Y_IN = ADC(26)
X_OUT = ADC(28)
Y_OUT = ADC(29)

RECORD_BUTTON = Pin(0, Pin.IN, Pin.PULL_DOWN)
LED_OUT = Pin(4, Pin.OUT, Pin.PULL_DOWN)
CLK = Pin(5, Pin.OUT, Pin.PULL_DOWN)
STROBE = Pin(6, Pin.OUT, Pin.PULL_DOWN)

# constants
TIME_RESOLUTION = 0.1
DEBOUNCE_TIME = 0.05
LED_COORDS = [
    (-1000, -1000),
    (-1000, 0),
    (-1000, 1000),
    (0, 1000),
    (1000, 1000),
    (1000, 0),
    (1000, -1000),
    (0, -1000),
]

#globals
recording = False
sketch = []


# find nearest led on grid
def near_led(x, y):
    distance = 100000
    closest = None
    for i in range(8):
        target = LED_COORDS[i]
        dist = abs(target[0] - x) + abs(target[1] - y)
        print(x, y, target, dist)
        if dist < distance:
            closest = i
            distance = dist
    print("NEAR LED", x, y, closest, distance)
    return closest

# read values from joystick
def read_val():
    x = math.floor((X_IN.read_u16() - 32000) / 30)
    y = math.floor((Y_IN.read_u16() - 33000) / 30)
    return (x, y)


def write_x(x):
    X_OUT.write_u16(x)


def write_y(y):
    Y_OUT.write_u16(y)


# illustrate recording via LED array
def play_recording(sketch):
    STROBE.value(0)
    for i in range(len(sketch)):
        led = near_led(sketch[i][0], sketch[i][1])
        led_arr = list(map(lambda x: 1 if x == led else 0, range(9)))
        STROBE.value(0)
        for j in range(8):
            CLK.value(1)
            LED_OUT.value(led_arr[j])
            time.sleep(0.001)
            CLK.value(0)
            time.sleep(0.001)
        CLK.value(1)
        time.sleep(0.001)
        CLK.value(0)
        STROBE.value(1)


def reset():
    "RESET"
    STROBE.value(0)
    for i in range(10):
        CLK.value(1)
        time.sleep(0.01)
        LED_OUT.value(0)
        time.sleep(0.01)
        CLK.value(0)
        time.sleep(0.01)

    STROBE.value(1)

def test_shift_register():
    t = [
    [1, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 1],]

    STROBE.value(0)
    for i in range(8):
        STROBE.value(0)
        for j in range(8):
            CLK.value(1)
            LED_OUT.value(t[i][j])
            print("DATA", t[i][j])
            time.sleep(0.01)
            CLK.value(0)
            time.sleep(0.01)
        CLK.value(1)
        time.sleep(0.01)
        CLK.value(0)
        STROBE.value(1)


while True:
    # test_shift_register()
    print('REC', recording)
    
    if RECORD_BUTTON.value() == 1:
        recording = not recording
        time.sleep(DEBOUNCE_TIME)

    if not recording and len(sketch) > 1:
        play_recording(sketch)

    key = read_val()

    if recording:
        if abs(key[0]) > 100 or abs(key[1]) > 100:
            sketch.append(key)

    print("SKETCH", sketch)

    time.sleep(TIME_RESOLUTION)
    
