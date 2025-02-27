# JOYRIDE 1

A Eurorack module in the making


## Installation

```
pip3 install -r requirements.txt
pip3 install adafruit-ampy rshel
ampy --port /dev/ttyACM0 put read_keys.py main.py
```

## Running tests

TODO


## Hardware setup

TODO


## Monitor using minicom


```
pip3 install minicom
minicom -D /dev/ttyACM0 -b 115200
```
