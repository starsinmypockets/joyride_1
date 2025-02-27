import time
import math

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

sketch = [(-110, 250), (0, 300), (100, 300), (200, 300), (300, 300), (400, 300), (500, 300), (900,-900)]


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

for i in range(8):
    foo = near_led(sketch[i][0], sketch[i][1])
    print(sketch[i], foo)

assert near_led(-1000, -1000) == 0
assert near_led(900, 900) == 4
