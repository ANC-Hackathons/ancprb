# Python Companion App Portion

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
