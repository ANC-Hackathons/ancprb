# Python Companion App Portion

## Install project dependencies:
```
sudo pip install -r ./requirements.txt
```

## Pair your computer with your Pebble Time
* Enable BlueTooth is on your Pebble Time
* Ensure your Pebble Time is not paired with another device. You may need to disable BlueTooth on your phone.
* Enable BlueTooth on your computer
* Follow the steps to pair your computer with your Pebble Time. Actual steps will depend on you operating system
* Find the device file for your Pebble Time on your computer. On OS X, this is similar to `/dev/cu.PebbleTimeXXXX-SerialPo` or `/dev/cu.PebbleXXXX-SerialPortSe`

## Connect your LulzBot
* Connect your LulzBot 3D printer to your computer using the provided USB cable
* Find the device file for your USB port that is connected to the LulzBot 3D printer. On OS X, this is similar to `/dev/tty.usbmodem1421`

## Running Companion App
```
$ python game_loop.py --serial <PEBBLE_TIME_DEVICE_FILE> --usb <USB_PORT_DEVICE_FILE>
```
