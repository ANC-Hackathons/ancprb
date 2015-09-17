# Python Companion App Portion
[![Build Status](https://travis-ci.org/thompsnm/ancprb.svg?branch=master)](https://travis-ci.org/thompsnm/ancprb) [![Coverage Status](https://coveralls.io/repos/thompsnm/ancprb/badge.svg?branch=fully_test_Ship&service=github)](https://coveralls.io/github/thompsnm/ancprb?branch=fully_test_Ship)

## Install project dependencies:
```
sudo pip install -r ./requirements.txt
```

## Pair your computer with your Pebble Time
See the [applicable instructions](../pebble/README.md#pair-your-computer-with-your-pebble-time) in the Pebble README file.

## Connect your LulzBot
* Connect your LulzBot 3D printer to your computer using the provided USB cable
* Find the device file for your USB port that is connected to the LulzBot 3D printer. On OS X, this is similar to `/dev/tty.usbmodem1421`

## Running Companion App
```
$ python game_loop.py --serial <PEBBLE_TIME_DEVICE_FILE> --usb <USB_PORT_DEVICE_FILE>
```

## Running Unit Tests
```
python -m unittest discover -s ./test/ -p '*_test.py' -v
```
